---
title: Caching & Data Stores
sidebar_position: 9
---

# Caching & Data Stores Deep Dive

Master caching strategies and data store selection for building high-performance, scalable systems. From in-memory caches to distributed data stores, learn how to optimize data access patterns.

## Caching Fundamentals

### Cache Hierarchy

```
┌─────────────────┐
│ Browser Cache   │ (Closest to user)
└────────┬────────┘
         │
┌────────▼────────┐
│   CDN Cache     │ (Geographic distribution)
└────────┬────────┘
         │
┌────────▼────────┐
│ Load Balancer   │ (Connection pooling)
│     Cache       │
└────────┬────────┘
         │
┌────────▼────────┐
│ Application     │ (In-process cache)
│     Cache       │
└────────┬────────┘
         │
┌────────▼────────┐
│ Distributed     │ (Redis/Memcached)
│     Cache       │
└────────┬────────┘
         │
┌────────▼────────┐
│   Database      │ (Query cache)
│     Cache       │
└─────────────────┘
```

### Caching Strategies

#### Cache-Aside (Lazy Loading)
```python
class CacheAside:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
    
    def get(self, key):
        # Check cache first
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Cache miss - fetch from database
        value = self.db.get(key)
        if value is not None:
            # Update cache
            self.cache.set(key, value, ttl=3600)
        
        return value
```

#### Write-Through Cache
```python
class WriteThrough:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
    
    def set(self, key, value):
        # Write to cache first
        self.cache.set(key, value)
        # Then write to database
        self.db.set(key, value)
    
    def get(self, key):
        # Always read from cache
        return self.cache.get(key)
```

#### Write-Behind (Write-Back) Cache
```python
class WriteBehind:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
        self.write_queue = Queue()
        self.start_background_writer()
    
    def set(self, key, value):
        # Write to cache immediately
        self.cache.set(key, value)
        # Queue for async database write
        self.write_queue.put((key, value))
    
    def background_writer(self):
        while True:
            batch = []
            # Batch writes for efficiency
            for _ in range(100):
                try:
                    item = self.write_queue.get(timeout=0.1)
                    batch.append(item)
                except Empty:
                    break
            
            if batch:
                self.db.batch_write(batch)
```

## Redis Deep Dive

### Redis Data Structures

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Strings - Simple key-value
r.set('user:1000:name', 'John Doe')
r.setex('session:abc123', 3600, 'user:1000')  # With TTL

# Lists - Message queues, timelines
r.lpush('queue:emails', 'email1', 'email2')
email = r.brpop('queue:emails', timeout=5)

# Sets - Unique collections, tags
r.sadd('user:1000:skills', 'python', 'redis', 'docker')
common_skills = r.sinter('user:1000:skills', 'user:2000:skills')

# Sorted Sets - Leaderboards, priorities
r.zadd('leaderboard', {'user1': 100, 'user2': 85, 'user3': 92})
top_users = r.zrevrange('leaderboard', 0, 9, withscores=True)

# Hashes - Objects
r.hset('user:1000', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'login_count': 42
})

# HyperLogLog - Cardinality estimation
r.pfadd('unique_visitors', 'user1', 'user2', 'user3')
count = r.pfcount('unique_visitors')  # Approximate count

# Bitmaps - Efficient boolean tracking
r.setbit('user:1000:login_days', 5, 1)  # Logged in on day 5
r.bitcount('user:1000:login_days')  # Total login days

# Streams - Event logs, message brokers
r.xadd('events:login', {'user_id': '1000', 'ip': '192.168.1.1'})
messages = r.xread({'events:login': '0'}, block=1000)
```

### Redis Patterns

#### Distributed Locking
```python
import time
import uuid

class RedisLock:
    def __init__(self, redis_client, key, timeout=10):
        self.redis = redis_client
        self.key = key
        self.timeout = timeout
        self.identifier = str(uuid.uuid4())
    
    def acquire(self):
        end = time.time() + self.timeout
        while time.time() < end:
            if self.redis.set(self.key, self.identifier, 
                            nx=True, ex=self.timeout):
                return True
            time.sleep(0.001)
        return False
    
    def release(self):
        lua_script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """
        self.redis.eval(lua_script, 1, self.key, self.identifier)
```

#### Rate Limiting
```python
class RateLimiter:
    def __init__(self, redis_client, max_requests=100, window=3600):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window
    
    def is_allowed(self, key):
        now = time.time()
        pipeline = self.redis.pipeline()
        pipeline.zremrangebyscore(key, 0, now - self.window)
        pipeline.zadd(key, {str(now): now})
        pipeline.zcount(key, '-inf', '+inf')
        pipeline.expire(key, self.window + 1)
        results = pipeline.execute()
        
        return results[2] <= self.max_requests
```

### Redis Cluster & Scaling

```python
from rediscluster import RedisCluster

# Cluster configuration
startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"}
]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Sharding happens automatically based on key hash slots
rc.set("key1", "value1")  # Goes to node based on CRC16(key) % 16384
```

**Production Configuration:**
```conf
# redis.conf for production
maxmemory 8gb
maxmemory-policy allkeys-lru
save 900 1 300 10 60 10000
appendonly yes
appendfsync everysec
tcp-backlog 511
timeout 0
tcp-keepalive 300

# Cluster specific
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-require-full-coverage yes
```

**Resources:**
- 📚 [Redis in Action](https://www.manning.com/books/redis-in-action)
- 📖 [Redis Documentation](https://redis.io/documentation)
- 🎥 [Redis University](https://university.redis.com/)
- 📖 [Redis Design Patterns](https://redislabs.com/redis-best-practices/introduction/)

## Memcached

### When to Use Memcached vs Redis

| Feature | Memcached | Redis |
|---------|-----------|-------|
| Data Types | String only | Multiple |
| Persistence | No | Yes |
| Replication | No | Yes |
| Memory Efficiency | Better | Good |
| Multi-threading | Yes | No* |
| Simplicity | Very simple | More complex |

*Redis 6+ has I/O threading

### Memcached Best Practices

```python
import pymemcache.client.base

# Connection pooling
from pymemcache.client.hash import HashClient

servers = [
    ('cache1.example.com', 11211),
    ('cache2.example.com', 11211),
    ('cache3.example.com', 11211)
]

client = HashClient(servers, use_pooling=True,
                   pool_size=10, pool_idle_timeout=30)

# Efficient serialization
import pickle
def serializer(key, value):
    if isinstance(value, str):
        return value, 1
    return pickle.dumps(value), 2

def deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return pickle.loads(value)
    raise Exception("Unknown flags")

client = pymemcache.client.base.Client(
    ('localhost', 11211),
    serializer=serializer,
    deserializer=deserializer
)
```

**Resources:**
- 📖 [Memcached Wiki](https://github.com/memcached/memcached/wiki)
- 🎥 [Scaling Memcached at Facebook](https://www.youtube.com/watch?v=4qiXlsQhPqY)

## Specialized Data Stores

### Time Series Databases

#### InfluxDB
```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url="http://localhost:8086", 
                       token="my-token", org="my-org")

write_api = client.write_api(write_options=SYNCHRONOUS)

# Write metrics
point = Point("cpu_usage") \
    .tag("host", "server01") \
    .field("usage_percent", 73.5) \
    .time(datetime.utcnow())

write_api.write(bucket="metrics", record=point)

# Query data
query = '''
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> aggregateWindow(every: 5m, fn: mean)
'''
result = client.query_api().query(query)
```

#### Prometheus (Pull-based)
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
request_count = Counter('http_requests_total', 
                       'Total HTTP requests', 
                       ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds',
                           'HTTP request latency')
active_connections = Gauge('active_connections',
                          'Number of active connections')

# Use in application
@request_duration.time()
def handle_request(method, endpoint):
    request_count.labels(method=method, endpoint=endpoint).inc()
    # Process request
```

**Resources:**
- 📖 [InfluxDB Documentation](https://docs.influxdata.com/)
- 📖 [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- 🎥 [Time Series Database Lectures](https://www.youtube.com/watch?v=fH7Xnpy8YhI)

### Graph Databases

#### Neo4j
```cypher
// Create nodes and relationships
CREATE (u1:User {name: 'Alice', id: 1})
CREATE (u2:User {name: 'Bob', id: 2})
CREATE (p1:Post {title: 'Graph Databases', id: 101})
CREATE (u1)-[:FOLLOWS]->(u2)
CREATE (u1)-[:LIKED]->(p1)
CREATE (u2)-[:AUTHORED]->(p1)

// Friend recommendations
MATCH (user:User {id: 1})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(fof)
WHERE NOT (user)-[:FOLLOWS]->(fof) AND user <> fof
RETURN fof.name, COUNT(*) as mutual_friends
ORDER BY mutual_friends DESC
LIMIT 10
```

**Resources:**
- 📚 [Graph Databases](https://www.oreilly.com/library/view/graph-databases-2nd/9781491930885/)
- 📖 [Neo4j Documentation](https://neo4j.com/docs/)
- 🎥 [Graph Database Use Cases](https://www.youtube.com/watch?v=3A6wZtP7pPs)

### Vector Databases (AI/ML)

#### Pinecone/Weaviate/Qdrant
```python
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")
index = pinecone.Index("embeddings")

# Upsert vectors
vectors = [
    ("vec1", [0.1, 0.2, 0.3, 0.4], {"text": "hello world"}),
    ("vec2", [0.2, 0.3, 0.4, 0.5], {"text": "machine learning"})
]
index.upsert(vectors=vectors)

# Similarity search
query_vector = [0.15, 0.25, 0.35, 0.45]
results = index.query(
    vector=query_vector,
    top_k=5,
    include_metadata=True
)
```

**Resources:**
- 📖 [Vector Database Comparison](https://github.com/erikbern/ann-benchmarks)
- 🎥 [Building RAG with Vector DBs](https://www.youtube.com/watch?v=bKjq6nYKz4Y)
- 📖 [Pinecone Learning Center](https://www.pinecone.io/learn/)

## Cache Invalidation Strategies

### TTL-Based Invalidation
```python
class TTLCache:
    def set(self, key, value, ttl=3600):
        self.redis.setex(key, ttl, value)
        # Also track in a sorted set for cleanup
        self.redis.zadd('ttl_tracker', {key: time.time() + ttl})
```

### Event-Based Invalidation
```python
class EventBasedCache:
    def __init__(self, cache, event_bus):
        self.cache = cache
        self.event_bus = event_bus
        self.event_bus.subscribe('data_changed', self.invalidate)
    
    def invalidate(self, event):
        # Invalidate related cache entries
        if event.type == 'user_updated':
            keys = [
                f'user:{event.user_id}',
                f'user:{event.user_id}:posts',
                f'user:{event.user_id}:friends'
            ]
            for key in keys:
                self.cache.delete(key)
```

### Cache Stampede Prevention
```python
class StampedeProtection:
    def get_or_compute(self, key, compute_fn, ttl=3600):
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Try to acquire lock
        lock_key = f'lock:{key}'
        if self.cache.set(lock_key, '1', nx=True, ex=30):
            try:
                # We have the lock, compute value
                value = compute_fn()
                self.cache.setex(key, ttl, value)
                return value
            finally:
                self.cache.delete(lock_key)
        else:
            # Someone else is computing, wait and retry
            time.sleep(0.1)
            return self.get_or_compute(key, compute_fn, ttl)
```

## Production Best Practices

### Monitoring and Metrics

```python
# Key metrics to monitor
cache_metrics = {
    'hit_rate': 'cache_hits / (cache_hits + cache_misses)',
    'eviction_rate': 'evictions per second',
    'memory_usage': 'current memory / max memory',
    'connection_count': 'active client connections',
    'command_rate': 'commands processed per second',
    'key_count': 'total number of keys',
    'expired_keys': 'keys expired per minute'
}

# Prometheus metrics for cache monitoring
from prometheus_client import Counter, Histogram, Gauge

cache_hits = Counter('cache_hits_total', 'Total cache hits')
cache_misses = Counter('cache_misses_total', 'Total cache misses')
cache_latency = Histogram('cache_operation_duration_seconds', 
                         'Cache operation latency')
cache_size = Gauge('cache_size_bytes', 'Current cache size')
```

### High Availability Patterns

```yaml
# Redis Sentinel configuration
sentinel:
  - host: sentinel1.example.com
    port: 26379
  - host: sentinel2.example.com
    port: 26379
  - host: sentinel3.example.com
    port: 26379

master_name: mymaster
quorum: 2
down_after_milliseconds: 5000
failover_timeout: 60000
```

### Performance Optimization

```python
# Pipeline operations for bulk operations
pipeline = redis_client.pipeline()
for i in range(10000):
    pipeline.set(f'key:{i}', f'value:{i}')
    if i % 1000 == 0:
        pipeline.execute()
        pipeline = redis_client.pipeline()
pipeline.execute()

# Connection pooling
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    socket_keepalive=True,
    socket_keepalive_options={
        1: 1,  # TCP_KEEPIDLE
        2: 5,  # TCP_KEEPINTVL
        3: 5,  # TCP_KEEPCNT
    }
)
```

## Interview Preparation

### Common Questions
1. Explain cache eviction policies (LRU, LFU, FIFO)
2. How to handle cache consistency in distributed systems?
3. Design a distributed cache with geographic replication
4. Implement a rate limiter using Redis
5. When to use different caching strategies?

### System Design Scenarios
1. Design a global CDN cache system
2. Build a session store for millions of users
3. Design a distributed cache for a social media feed
4. Create a caching layer for a recommendation system

## Essential Resources

### Books
- 📚 [Redis Essentials](https://www.packtpub.com/product/redis-essentials/9781784392451)
- 📚 [High Performance Browser Networking](https://hpbn.co/) - CDN and caching
- 📚 [Designing Data-Intensive Applications](https://dataintensive.net/) - Chapter 5

### Documentation
- 📖 [Redis Commands Reference](https://redis.io/commands)
- 📖 [Memcached Protocol](https://github.com/memcached/memcached/blob/master/doc/protocol.txt)
- 📖 [AWS ElastiCache Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/BestPractices.html)

### Tools
- 🔧 [Redis Commander](https://github.com/joeferner/redis-commander) - Web UI
- 🔧 [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - Official GUI
- 🔧 [twemproxy](https://github.com/twitter/twemproxy) - Redis/Memcached proxy
- 🔧 [KeyDB](https://keydb.dev/) - Multithreaded Redis fork

Remember: Effective caching is critical for system performance. Understanding when and how to cache, along with proper invalidation strategies, separates good engineers from great ones.