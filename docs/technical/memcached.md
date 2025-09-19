# Memcached

## Overview

Memcached is a high-performance, distributed memory object caching system designed for platform engineers who need to speed up dynamic web applications by alleviating database load. It provides a simple key-value store in memory for small chunks of arbitrary data from database calls, API calls, or page rendering.

## Key Features

- **High Performance**: In-memory storage for sub-millisecond response times
- **Distributed**: Scale horizontally across multiple servers
- **Simple Protocol**: Text-based protocol that's easy to implement and debug
- **Language Agnostic**: Client libraries available for all major programming languages
- **Memory Efficient**: Optimized memory usage with LRU eviction

## Installation

### Docker Installation
```bash
# Basic Memcached container
docker run -d \
  --name memcached \
  -p 11211:11211 \
  memcached:latest

# With custom memory allocation and options
docker run -d \
  --name memcached \
  -p 11211:11211 \
  memcached:latest \
  memcached -m 512 -c 1024 -v

# Parameters explanation:
# -m 512: Allocate 512MB of memory
# -c 1024: Max simultaneous connections
# -v: Verbose mode
```

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  memcached:
    image: memcached:latest
    restart: always
    ports:
      - "11211:11211"
    command: memcached -m 512 -c 1024 -v
    networks:
      - app-network

  # Multiple Memcached instances for distribution
  memcached-1:
    image: memcached:latest
    restart: always
    ports:
      - "11211:11211"
    command: memcached -m 256 -c 512
    networks:
      - cache-network

  memcached-2:
    image: memcached:latest
    restart: always
    ports:
      - "11212:11211"
    command: memcached -m 256 -c 512
    networks:
      - cache-network

  memcached-3:
    image: memcached:latest
    restart: always
    ports:
      - "11213:11211"
    command: memcached -m 256 -c 512
    networks:
      - cache-network

  # Application server using Memcached
  app:
    build: .
    depends_on:
      - memcached-1
      - memcached-2
      - memcached-3
    environment:
      MEMCACHED_SERVERS: "memcached-1:11211,memcached-2:11211,memcached-3:11211"
    networks:
      - cache-network

networks:
  app-network:
    driver: bridge
  cache-network:
    driver: bridge
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memcached
  namespace: cache
spec:
  replicas: 3
  selector:
    matchLabels:
      app: memcached
  template:
    metadata:
      labels:
        app: memcached
    spec:
      containers:
      - name: memcached
        image: memcached:latest
        ports:
        - containerPort: 11211
          name: memcached
        command: ["memcached"]
        args:
          - "-m"
          - "512"
          - "-c"
          - "1024"
          - "-v"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          tcpSocket:
            port: 11211
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          tcpSocket:
            port: 11211
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: memcached
  namespace: cache
spec:
  selector:
    app: memcached
  ports:
  - port: 11211
    targetPort: 11211
    name: memcached
  type: ClusterIP
---
# Headless service for direct pod access
apiVersion: v1
kind: Service
metadata:
  name: memcached-headless
  namespace: cache
spec:
  selector:
    app: memcached
  ports:
  - port: 11211
    targetPort: 11211
    name: memcached
  clusterIP: None
```

### Auto-Scaling Configuration
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: memcached-hpa
  namespace: cache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: memcached
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Basic Operations

### Command Line Interface
```bash
# Connect to Memcached using telnet
telnet localhost 11211

# Basic operations
set mykey 0 3600 5
hello
STORED

get mykey
VALUE mykey 0 5
hello
END

# Set with expiration (key, flags, exptime, bytes)
set user:123 0 1800 25
{"id":123,"name":"John"}
STORED

# Add (only if key doesn't exist)
add newkey 0 3600 10
new_value
STORED

# Replace (only if key exists)
replace mykey 0 3600 8
new_data
STORED

# Delete key
delete mykey
DELETED

# Increment/Decrement counters
set counter 0 0 1
5
STORED

incr counter 1
6

decr counter 2
4

# Get statistics
stats
stats items
stats slabs
stats sizes

# Flush all data
flush_all
OK

# Quit session
quit
```

## Application Integration

### Python Integration
```python
# requirements.txt
pymemcache==4.0.0
python-memcached==1.59

# memcached_client.py
from pymemcache.client.base import Client
from pymemcache.client.hash import HashClient
from pymemcache import serde
import json
import pickle
import time
import logging
from typing import Any, Optional, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemcachedClient:
    def __init__(self, servers, serializer='json', compression=False):
        """
        Initialize Memcached client
        
        Args:
            servers: String for single server or list for multiple servers
            serializer: 'json', 'pickle', or custom serializer
            compression: Enable compression for large values
        """
        self.servers = servers
        self.serializer = serializer
        
        # Setup serializer
        if serializer == 'json':
            serde_obj = serde.JsonSerde()
        elif serializer == 'pickle':
            serde_obj = serde.PickleSerde()
        else:
            serde_obj = serde.JsonSerde()  # Default
        
        # Create client
        if isinstance(servers, list):
            # Multiple servers - use consistent hashing
            self.client = HashClient(
                servers,
                serde=serde_obj,
                connect_timeout=5,
                timeout=1,
                no_delay=True,
                ignore_exc=True
            )
        else:
            # Single server
            self.client = Client(
                servers,
                serde=serde_obj,
                connect_timeout=5,
                timeout=1,
                no_delay=True
            )
    
    def set(self, key: str, value: Any, expiry: int = 3600) -> bool:
        """Set a key-value pair with expiration"""
        try:
            result = self.client.set(key, value, expire=expiry)
            if result:
                logger.debug(f"Set key: {key}")
            return result
        except Exception as e:
            logger.error(f"Failed to set key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        try:
            value = self.client.get(key)
            if value is not None:
                logger.debug(f"Retrieved key: {key}")
            return value
        except Exception as e:
            logger.error(f"Failed to get key {key}: {e}")
            return None
    
    def get_multi(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values by keys"""
        try:
            result = self.client.get_multi(keys)
            logger.debug(f"Retrieved {len(result)} keys from {len(keys)} requested")
            return result
        except Exception as e:
            logger.error(f"Failed to get multiple keys: {e}")
            return {}
    
    def set_multi(self, mapping: Dict[str, Any], expiry: int = 3600) -> bool:
        """Set multiple key-value pairs"""
        try:
            result = self.client.set_multi(mapping, expire=expiry)
            logger.debug(f"Set {len(mapping)} keys")
            return result
        except Exception as e:
            logger.error(f"Failed to set multiple keys: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete a key"""
        try:
            result = self.client.delete(key)
            if result:
                logger.debug(f"Deleted key: {key}")
            return result
        except Exception as e:
            logger.error(f"Failed to delete key {key}: {e}")
            return False
    
    def add(self, key: str, value: Any, expiry: int = 3600) -> bool:
        """Add key only if it doesn't exist"""
        try:
            result = self.client.add(key, value, expire=expiry)
            if result:
                logger.debug(f"Added key: {key}")
            return result
        except Exception as e:
            logger.error(f"Failed to add key {key}: {e}")
            return False
    
    def replace(self, key: str, value: Any, expiry: int = 3600) -> bool:
        """Replace key only if it exists"""
        try:
            result = self.client.replace(key, value, expire=expiry)
            if result:
                logger.debug(f"Replaced key: {key}")
            return result
        except Exception as e:
            logger.error(f"Failed to replace key {key}: {e}")
            return False
    
    def increment(self, key: str, delta: int = 1) -> Optional[int]:
        """Increment a counter"""
        try:
            result = self.client.incr(key, delta)
            if result is not None:
                logger.debug(f"Incremented key {key} by {delta}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to increment key {key}: {e}")
            return None
    
    def decrement(self, key: str, delta: int = 1) -> Optional[int]:
        """Decrement a counter"""
        try:
            result = self.client.decr(key, delta)
            if result is not None:
                logger.debug(f"Decremented key {key} by {delta}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to decrement key {key}: {e}")
            return None
    
    def flush_all(self) -> bool:
        """Flush all cache data"""
        try:
            result = self.client.flush_all()
            logger.warning("Flushed all cache data")
            return result
        except Exception as e:
            logger.error(f"Failed to flush cache: {e}")
            return False
    
    def stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        try:
            stats = self.client.stats()
            return stats
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}
    
    def close(self):
        """Close client connection"""
        try:
            self.client.close()
            logger.info("Closed Memcached connection")
        except Exception as e:
            logger.error(f"Failed to close connection: {e}")

# Cache decorator
class CacheManager:
    def __init__(self, memcached_client):
        self.cache = memcached_client
    
    def cached(self, expiry=3600, key_prefix=""):
        """Decorator for caching function results"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_key(func.__name__, args, kwargs, key_prefix)
                
                # Try to get from cache
                result = self.cache.get(cache_key)
                if result is not None:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result
                
                # Execute function and cache result
                logger.debug(f"Cache miss for {func.__name__}")
                result = func(*args, **kwargs)
                self.cache.set(cache_key, result, expiry)
                
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern):
        """Invalidate cache keys matching pattern (limited functionality)"""
        # Note: Memcached doesn't support pattern-based invalidation
        # This is a placeholder for application-level cache invalidation
        logger.warning(f"Pattern invalidation not supported: {pattern}")
    
    def _generate_key(self, func_name, args, kwargs, prefix):
        """Generate cache key from function name and arguments"""
        key_parts = [prefix, func_name] if prefix else [func_name]
        
        # Add args
        for arg in args:
            key_parts.append(str(arg))
        
        # Add kwargs
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        return ":".join(key_parts)

# Repository with caching
class UserRepository:
    def __init__(self, database, cache_client):
        self.db = database
        self.cache = CacheManager(cache_client)
    
    @property
    def cache_manager(self):
        return self.cache
    
    @cache_manager.cached(expiry=1800, key_prefix="user")
    def get_user(self, user_id):
        """Get user with caching"""
        logger.info(f"Fetching user {user_id} from database")
        # Simulate database call
        user = self.db.get_user(user_id)
        return user
    
    @cache_manager.cached(expiry=600, key_prefix="user_profile")
    def get_user_profile(self, user_id):
        """Get user profile with caching"""
        logger.info(f"Fetching user profile {user_id} from database")
        profile = self.db.get_user_profile(user_id)
        return profile
    
    def update_user(self, user_id, data):
        """Update user and invalidate cache"""
        # Update in database
        result = self.db.update_user(user_id, data)
        
        # Invalidate related cache entries
        cache_keys = [
            f"user:get_user:{user_id}",
            f"user_profile:get_user_profile:{user_id}"
        ]
        
        for key in cache_keys:
            self.cache.cache.delete(key)
        
        logger.info(f"Updated user {user_id} and invalidated cache")
        return result
    
    def get_users_batch(self, user_ids):
        """Get multiple users with batch caching"""
        cache_keys = [f"user:get_user:{uid}" for uid in user_ids]
        
        # Try to get from cache
        cached_results = self.cache.cache.get_multi(cache_keys)
        
        # Determine which users need to be fetched
        missing_users = []
        results = {}
        
        for i, user_id in enumerate(user_ids):
            cache_key = cache_keys[i]
            if cache_key in cached_results:
                results[user_id] = cached_results[cache_key]
            else:
                missing_users.append(user_id)
        
        # Fetch missing users from database
        if missing_users:
            logger.info(f"Fetching {len(missing_users)} users from database")
            db_results = self.db.get_users_batch(missing_users)
            
            # Cache the results
            cache_data = {}
            for user_id, user_data in db_results.items():
                cache_key = f"user:get_user:{user_id}"
                cache_data[cache_key] = user_data
                results[user_id] = user_data
            
            self.cache.cache.set_multi(cache_data, expiry=1800)
        
        return results

# Session management with Memcached
class SessionManager:
    def __init__(self, memcached_client, default_expiry=1800):
        self.cache = memcached_client
        self.default_expiry = default_expiry
    
    def create_session(self, user_id, session_data):
        """Create a new session"""
        import uuid
        session_id = str(uuid.uuid4())
        
        session = {
            'user_id': user_id,
            'created_at': time.time(),
            'last_access': time.time(),
            **session_data
        }
        
        session_key = f"session:{session_id}"
        if self.cache.set(session_key, session, self.default_expiry):
            logger.info(f"Created session {session_id} for user {user_id}")
            return session_id
        
        return None
    
    def get_session(self, session_id):
        """Get session data"""
        session_key = f"session:{session_id}"
        session = self.cache.get(session_key)
        
        if session:
            # Update last access time
            session['last_access'] = time.time()
            self.cache.set(session_key, session, self.default_expiry)
            logger.debug(f"Retrieved session {session_id}")
        
        return session
    
    def update_session(self, session_id, data):
        """Update session data"""
        session_key = f"session:{session_id}"
        session = self.cache.get(session_key)
        
        if session:
            session.update(data)
            session['last_access'] = time.time()
            self.cache.set(session_key, session, self.default_expiry)
            logger.info(f"Updated session {session_id}")
            return True
        
        return False
    
    def destroy_session(self, session_id):
        """Destroy session"""
        session_key = f"session:{session_id}"
        if self.cache.delete(session_key):
            logger.info(f"Destroyed session {session_id}")
            return True
        
        return False
    
    def extend_session(self, session_id, expiry=None):
        """Extend session expiry"""
        if expiry is None:
            expiry = self.default_expiry
        
        session_key = f"session:{session_id}"
        session = self.cache.get(session_key)
        
        if session:
            session['last_access'] = time.time()
            self.cache.set(session_key, session, expiry)
            logger.debug(f"Extended session {session_id} expiry")
            return True
        
        return False

# Rate limiting with Memcached
class RateLimiter:
    def __init__(self, memcached_client):
        self.cache = memcached_client
    
    def is_allowed(self, identifier, limit, window):
        """
        Check if request is allowed based on rate limit
        
        Args:
            identifier: Unique identifier (user_id, IP, etc.)
            limit: Number of requests allowed
            window: Time window in seconds
        """
        key = f"rate_limit:{identifier}:{window}"
        
        # Try to increment counter
        current = self.cache.increment(key, 1)
        
        if current is None:
            # Key doesn't exist, create it
            self.cache.set(key, 1, window)
            return True
        
        return current <= limit
    
    def get_remaining(self, identifier, limit, window):
        """Get remaining requests for identifier"""
        key = f"rate_limit:{identifier}:{window}"
        current = self.cache.get(key) or 0
        return max(0, limit - current)
    
    def reset_limit(self, identifier, window):
        """Reset rate limit for identifier"""
        key = f"rate_limit:{identifier}:{window}"
        self.cache.delete(key)

# Usage example
if __name__ == "__main__":
    # Single server
    # cache = MemcachedClient("localhost:11211")
    
    # Multiple servers with consistent hashing
    cache = MemcachedClient([
        "localhost:11211",
        "localhost:11212",
        "localhost:11213"
    ])
    
    # Basic operations
    cache.set("user:123", {"id": 123, "name": "John Doe"}, 3600)
    user = cache.get("user:123")
    print(f"User: {user}")
    
    # Counters
    cache.set("page_views", 0)
    cache.increment("page_views", 1)
    views = cache.get("page_views")
    print(f"Page views: {views}")
    
    # Batch operations
    users = {
        "user:124": {"id": 124, "name": "Jane Doe"},
        "user:125": {"id": 125, "name": "Bob Smith"}
    }
    cache.set_multi(users, 1800)
    
    cached_users = cache.get_multi(["user:123", "user:124", "user:125"])
    print(f"Cached users: {len(cached_users)}")
    
    # Session management
    session_mgr = SessionManager(cache)
    session_id = session_mgr.create_session(123, {"role": "admin"})
    session = session_mgr.get_session(session_id)
    print(f"Session: {session}")
    
    # Rate limiting
    rate_limiter = RateLimiter(cache)
    allowed = rate_limiter.is_allowed("user:123", 10, 60)
    print(f"Request allowed: {allowed}")
    
    # Statistics
    stats = cache.stats()
    print(f"Cache stats: {stats}")
    
    # Close connection
    cache.close()
```

### Node.js Integration
```javascript
// package.json dependencies
{
  "dependencies": {
    "memcached": "^2.2.2",
    "express": "^4.18.0"
  }
}

// memcached-client.js
const Memcached = require('memcached');

class MemcachedClient {
  constructor(servers, options = {}) {
    const defaultOptions = {
      maxKeySize: 250,
      maxExpiration: 2592000, // 30 days
      maxValue: 1048576, // 1MB
      poolSize: 10,
      algorithm: 'md5',
      reconnect: 18000000,
      timeout: 5000,
      retries: 5,
      retry: 30000,
      remove: true,
      redundancy: false,
      keyCompression: true,
      ...options
    };

    this.memcached = new Memcached(servers, defaultOptions);
    this.servers = servers;

    // Error handling
    this.memcached.on('failure', (details) => {
      console.error('Memcached server failure:', details);
    });

    this.memcached.on('reconnecting', (details) => {
      console.log('Memcached reconnecting:', details);
    });

    this.memcached.on('reconnect', (details) => {
      console.log('Memcached reconnected:', details);
    });
  }

  async set(key, value, expiry = 3600) {
    return new Promise((resolve, reject) => {
      this.memcached.set(key, value, expiry, (err) => {
        if (err) {
          console.error(`Failed to set key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Set key: ${key}`);
          resolve(true);
        }
      });
    });
  }

  async get(key) {
    return new Promise((resolve, reject) => {
      this.memcached.get(key, (err, data) => {
        if (err) {
          console.error(`Failed to get key ${key}:`, err);
          reject(err);
        } else {
          if (data !== undefined) {
            console.debug(`Retrieved key: ${key}`);
          }
          resolve(data);
        }
      });
    });
  }

  async getMulti(keys) {
    return new Promise((resolve, reject) => {
      this.memcached.getMulti(keys, (err, data) => {
        if (err) {
          console.error('Failed to get multiple keys:', err);
          reject(err);
        } else {
          console.debug(`Retrieved ${Object.keys(data).length} keys from ${keys.length} requested`);
          resolve(data);
        }
      });
    });
  }

  async del(key) {
    return new Promise((resolve, reject) => {
      this.memcached.del(key, (err) => {
        if (err) {
          console.error(`Failed to delete key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Deleted key: ${key}`);
          resolve(true);
        }
      });
    });
  }

  async add(key, value, expiry = 3600) {
    return new Promise((resolve, reject) => {
      this.memcached.add(key, value, expiry, (err) => {
        if (err) {
          console.error(`Failed to add key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Added key: ${key}`);
          resolve(true);
        }
      });
    });
  }

  async replace(key, value, expiry = 3600) {
    return new Promise((resolve, reject) => {
      this.memcached.replace(key, value, expiry, (err) => {
        if (err) {
          console.error(`Failed to replace key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Replaced key: ${key}`);
          resolve(true);
        }
      });
    });
  }

  async incr(key, delta = 1) {
    return new Promise((resolve, reject) => {
      this.memcached.incr(key, delta, (err, result) => {
        if (err) {
          console.error(`Failed to increment key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Incremented key ${key} by ${delta}: ${result}`);
          resolve(result);
        }
      });
    });
  }

  async decr(key, delta = 1) {
    return new Promise((resolve, reject) => {
      this.memcached.decr(key, delta, (err, result) => {
        if (err) {
          console.error(`Failed to decrement key ${key}:`, err);
          reject(err);
        } else {
          console.debug(`Decremented key ${key} by ${delta}: ${result}`);
          resolve(result);
        }
      });
    });
  }

  async flush() {
    return new Promise((resolve, reject) => {
      this.memcached.flush((err) => {
        if (err) {
          console.error('Failed to flush cache:', err);
          reject(err);
        } else {
          console.warn('Flushed all cache data');
          resolve(true);
        }
      });
    });
  }

  async stats() {
    return new Promise((resolve, reject) => {
      this.memcached.stats((err, data) => {
        if (err) {
          console.error('Failed to get stats:', err);
          reject(err);
        } else {
          resolve(data);
        }
      });
    });
  }

  end() {
    this.memcached.end();
    console.log('Closed Memcached connection');
  }
}

// Cache middleware for Express
class CacheMiddleware {
  constructor(memcachedClient) {
    this.cache = memcachedClient;
  }

  // Cache GET responses
  cacheResponse(expiry = 300) {
    return async (req, res, next) => {
      // Only cache GET requests
      if (req.method !== 'GET') {
        return next();
      }

      const cacheKey = `response:${req.originalUrl}`;
      
      try {
        const cachedData = await this.cache.get(cacheKey);
        
        if (cachedData) {
          console.log(`Cache hit for ${req.originalUrl}`);
          return res.json(cachedData);
        }

        // Override res.json to cache the response
        const originalJson = res.json;
        res.json = function(data) {
          // Cache the response
          memcachedClient.set(cacheKey, data, expiry).catch(err => {
            console.error('Failed to cache response:', err);
          });
          
          // Call original json method
          return originalJson.call(this, data);
        };

        next();
      } catch (error) {
        console.error('Cache middleware error:', error);
        next();
      }
    };
  }

  // Invalidate cache by pattern (prefix)
  async invalidatePrefix(prefix) {
    // Note: Memcached doesn't support pattern deletion
    // This is a placeholder for application-level cache invalidation
    console.warn(`Pattern invalidation not supported: ${prefix}`);
  }
}

// Session store for Express
class MemcachedSessionStore {
  constructor(memcachedClient, options = {}) {
    this.cache = memcachedClient;
    this.prefix = options.prefix || 'sess:';
    this.ttl = options.ttl || 1800; // 30 minutes
  }

  async get(sessionId) {
    try {
      const session = await this.cache.get(this.prefix + sessionId);
      return session;
    } catch (error) {
      console.error('Session get error:', error);
      return null;
    }
  }

  async set(sessionId, session) {
    try {
      await this.cache.set(this.prefix + sessionId, session, this.ttl);
      return true;
    } catch (error) {
      console.error('Session set error:', error);
      return false;
    }
  }

  async destroy(sessionId) {
    try {
      await this.cache.del(this.prefix + sessionId);
      return true;
    } catch (error) {
      console.error('Session destroy error:', error);
      return false;
    }
  }

  async touch(sessionId) {
    try {
      const session = await this.get(sessionId);
      if (session) {
        await this.set(sessionId, session);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Session touch error:', error);
      return false;
    }
  }
}

// Rate limiter
class RateLimiter {
  constructor(memcachedClient) {
    this.cache = memcachedClient;
  }

  async isAllowed(identifier, limit, windowSeconds) {
    const key = `rate_limit:${identifier}:${windowSeconds}`;
    
    try {
      // Try to increment
      const current = await this.cache.incr(key, 1);
      
      if (current === false) {
        // Key doesn't exist, create it
        await this.cache.set(key, 1, windowSeconds);
        return { allowed: true, remaining: limit - 1 };
      }

      const allowed = current <= limit;
      const remaining = Math.max(0, limit - current);
      
      return { allowed, remaining, current };
    } catch (error) {
      console.error('Rate limiter error:', error);
      // Allow request on error
      return { allowed: true, remaining: limit };
    }
  }

  middleware(limit, windowSeconds, keyGenerator) {
    return async (req, res, next) => {
      const key = keyGenerator ? keyGenerator(req) : req.ip;
      
      try {
        const result = await this.isAllowed(key, limit, windowSeconds);
        
        // Add rate limit headers
        res.set({
          'X-RateLimit-Limit': limit,
          'X-RateLimit-Remaining': result.remaining,
          'X-RateLimit-Reset': new Date(Date.now() + windowSeconds * 1000).toISOString()
        });

        if (!result.allowed) {
          return res.status(429).json({
            error: 'Too Many Requests',
            message: `Rate limit exceeded. Try again in ${windowSeconds} seconds.`
          });
        }

        next();
      } catch (error) {
        console.error('Rate limiter middleware error:', error);
        next(); // Allow request on error
      }
    };
  }
}

// Express application example
const express = require('express');
const app = express();

// Initialize Memcached client
const memcachedClient = new MemcachedClient([
  'localhost:11211',
  'localhost:11212',
  'localhost:11213'
]);

// Initialize middleware
const cacheMiddleware = new CacheMiddleware(memcachedClient);
const rateLimiter = new RateLimiter(memcachedClient);
const sessionStore = new MemcachedSessionStore(memcachedClient);

app.use(express.json());

// Rate limiting middleware
app.use('/api/', rateLimiter.middleware(100, 3600, (req) => req.ip)); // 100 requests per hour per IP

// Cache middleware for specific routes
app.get('/api/users/:id', cacheMiddleware.cacheResponse(1800), async (req, res) => {
  // Simulate database call
  const user = {
    id: req.params.id,
    name: `User ${req.params.id}`,
    email: `user${req.params.id}@example.com`,
    timestamp: new Date().toISOString()
  };
  
  res.json(user);
});

// Session management routes
app.post('/api/sessions', async (req, res) => {
  const { username, password } = req.body;
  
  // Simulate authentication
  if (username === 'admin' && password === 'password') {
    const sessionId = require('crypto').randomBytes(32).toString('hex');
    const sessionData = {
      userId: 1,
      username: 'admin',
      role: 'admin',
      createdAt: new Date().toISOString()
    };
    
    await sessionStore.set(sessionId, sessionData);
    
    res.json({ sessionId, user: sessionData });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

app.get('/api/sessions/:sessionId', async (req, res) => {
  const session = await sessionStore.get(req.params.sessionId);
  
  if (session) {
    res.json(session);
  } else {
    res.status(404).json({ error: 'Session not found' });
  }
});

app.delete('/api/sessions/:sessionId', async (req, res) => {
  await sessionStore.destroy(req.params.sessionId);
  res.json({ message: 'Session destroyed' });
});

// Cache statistics endpoint
app.get('/api/cache/stats', async (req, res) => {
  try {
    const stats = await memcachedClient.stats();
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Cache management endpoints
app.post('/api/cache/flush', async (req, res) => {
  try {
    await memcachedClient.flush();
    res.json({ message: 'Cache flushed successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down gracefully...');
  memcachedClient.end();
  process.exit(0);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = { MemcachedClient, CacheMiddleware, RateLimiter, MemcachedSessionStore };
```

## Monitoring and Performance

### Monitoring Script
```bash
#!/bin/bash
# memcached-monitor.sh

MEMCACHED_HOST="localhost"
MEMCACHED_PORT="11211"

# Function to get stats
get_stats() {
    echo "stats" | nc $MEMCACHED_HOST $MEMCACHED_PORT
}

# Function to parse specific stat
get_stat() {
    local stat_name=$1
    get_stats | grep "STAT $stat_name" | awk '{print $3}'
}

echo "=== Memcached Monitoring Report ==="
echo "Server: $MEMCACHED_HOST:$MEMCACHED_PORT"
echo "Timestamp: $(date)"
echo

# Basic stats
echo "=== Basic Statistics ==="
echo "Version: $(get_stat version)"
echo "Uptime: $(get_stat uptime) seconds"
echo "Current connections: $(get_stat curr_connections)"
echo "Total connections: $(get_stat total_connections)"
echo

# Memory stats
echo "=== Memory Statistics ==="
BYTES=$(get_stat bytes)
LIMIT_MAXBYTES=$(get_stat limit_maxbytes)
MEMORY_USAGE_PERCENT=$(echo "scale=2; $BYTES * 100 / $LIMIT_MAXBYTES" | bc)

echo "Memory used: $BYTES bytes"
echo "Memory limit: $LIMIT_MAXBYTES bytes"
echo "Memory usage: ${MEMORY_USAGE_PERCENT}%"
echo

# Cache stats
echo "=== Cache Statistics ==="
GET_HITS=$(get_stat get_hits)
GET_MISSES=$(get_stat get_misses)
TOTAL_GETS=$((GET_HITS + GET_MISSES))

if [ $TOTAL_GETS -gt 0 ]; then
    HIT_RATE=$(echo "scale=2; $GET_HITS * 100 / $TOTAL_GETS" | bc)
else
    HIT_RATE=0
fi

echo "Get hits: $GET_HITS"
echo "Get misses: $GET_MISSES"
echo "Hit rate: ${HIT_RATE}%"
echo "Current items: $(get_stat curr_items)"
echo "Total items: $(get_stat total_items)"
echo

# Performance stats
echo "=== Performance Statistics ==="
echo "Command get: $(get_stat cmd_get)"
echo "Command set: $(get_stat cmd_set)"
echo "Evictions: $(get_stat evictions)"
echo "Reclaimed: $(get_stat reclaimed)"
echo

# Connection stats
echo "=== Connection Statistics ==="
echo "Current connections: $(get_stat curr_connections)"
echo "Max connections: $(get_stat max_connections)"
echo "Connection structures: $(get_stat connection_structures)"
echo "Rejected connections: $(get_stat rejected_connections)"
```

### Prometheus Monitoring
```yaml
# memcached-exporter.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memcached-exporter
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: memcached-exporter
  template:
    metadata:
      labels:
        app: memcached-exporter
    spec:
      containers:
      - name: memcached-exporter
        image: prom/memcached-exporter:latest
        ports:
        - containerPort: 9150
        args:
          - "--memcached.address=memcached.cache.svc.cluster.local:11211"
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: memcached-exporter
  namespace: monitoring
spec:
  selector:
    app: memcached-exporter
  ports:
  - port: 9150
    targetPort: 9150
```

### Key Metrics to Monitor
```promql
# Hit rate
memcached_commands_total{command="get",status="hit"} / memcached_commands_total{command="get"}

# Memory usage
memcached_current_bytes / memcached_limit_bytes

# Connection usage
memcached_current_connections / memcached_max_connections

# Operations per second
rate(memcached_commands_total[5m])

# Eviction rate
rate(memcached_items_evicted_total[5m])

# Items in cache
memcached_current_items
```

## High Availability and Scaling

### Cluster Management Script
```bash
#!/bin/bash
# memcached-cluster.sh

# Configuration
CLUSTER_NODES=(
    "memcached-1:11211"
    "memcached-2:11211"
    "memcached-3:11211"
)

# Function to check node health
check_node() {
    local node=$1
    local host=$(echo $node | cut -d: -f1)
    local port=$(echo $node | cut -d: -f2)
    
    if echo "version" | nc -w 1 $host $port > /dev/null 2>&1; then
        echo "✓ $node - healthy"
        return 0
    else
        echo "✗ $node - unhealthy"
        return 1
    fi
}

# Function to get cluster stats
cluster_stats() {
    echo "=== Cluster Health Check ==="
    
    local healthy_nodes=0
    local total_nodes=${#CLUSTER_NODES[@]}
    
    for node in "${CLUSTER_NODES[@]}"; do
        if check_node $node; then
            ((healthy_nodes++))
        fi
    done
    
    echo
    echo "Healthy nodes: $healthy_nodes / $total_nodes"
    
    if [ $healthy_nodes -eq $total_nodes ]; then
        echo "Cluster status: HEALTHY"
    elif [ $healthy_nodes -gt 0 ]; then
        echo "Cluster status: DEGRADED"
    else
        echo "Cluster status: DOWN"
    fi
}

# Function to flush all nodes
flush_cluster() {
    echo "Flushing all cluster nodes..."
    
    for node in "${CLUSTER_NODES[@]}"; do
        local host=$(echo $node | cut -d: -f1)
        local port=$(echo $node | cut -d: -f2)
        
        if echo "flush_all" | nc -w 1 $host $port > /dev/null 2>&1; then
            echo "✓ Flushed $node"
        else
            echo "✗ Failed to flush $node"
        fi
    done
}

# Main menu
case "$1" in
    "health")
        cluster_stats
        ;;
    "flush")
        flush_cluster
        ;;
    *)
        echo "Usage: $0 {health|flush}"
        exit 1
        ;;
esac
```

## Best Practices

- Use consistent hashing for distributing keys across multiple servers
- Implement proper error handling and fallback mechanisms
- Monitor memory usage and hit rates regularly
- Use appropriate expiration times for different data types
- Implement cache warming strategies for critical data
- Use compression for large values to save memory
- Design cache keys to avoid conflicts and enable easy invalidation
- Regular monitoring of server health and performance metrics
- Implement proper security measures (firewall, network isolation)

## Great Resources

- [Memcached Documentation](https://memcached.org/) - Official documentation and guides
- [Memcached Wiki](https://github.com/memcached/memcached/wiki) - Community documentation
- [Memcached Protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt) - Protocol specification
- [Memcached Best Practices](https://cloud.google.com/memorystore/docs/memcached/best-practices) - Google Cloud best practices
- [Memcached GitHub](https://github.com/memcached/memcached) - Source code and issues
- [libmemcached](https://libmemcached.org/) - C/C++ client library
- [Memcached Monitoring](https://github.com/prometheus/memcached_exporter) - Prometheus exporter
- [Scaling Memcached](https://www.youtube.com/watch?v=TGl81wr8lz8) - Scaling strategies and patterns