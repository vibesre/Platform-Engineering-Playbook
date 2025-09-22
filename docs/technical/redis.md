# Redis

Redis is an in-memory data structure store used as a database, cache, and message broker. It's essential for platform engineers building high-performance applications that need fast data access, caching, and real-time features.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Redis Crash Course Tutorial**
- **Channel**: Traversy Media
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=jgpVdJB2sKQ)
- **Why it's great**: Comprehensive overview covering all essential Redis concepts

#### **Redis Tutorial for Beginners**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=OqCK95AS-YE)
- **Why it's great**: Perfect introduction with practical examples and use cases

#### **Redis University Course**
- **Channel**: Redis
- **Link**: [university.redis.com](https://university.redis.com/)
- **Why it's great**: Official comprehensive training with hands-on labs

### 📖 Essential Documentation

#### **Redis Official Documentation**
- **Link**: [redis.io/documentation](https://redis.io/documentation)
- **Why it's great**: Comprehensive official docs with examples and best practices

#### **Redis Commands Reference**
- **Link**: [redis.io/commands](https://redis.io/commands)
- **Why it's great**: Complete command documentation with interactive examples

#### **Redis Best Practices**
- **Link**: [redis.com/redis-best-practices/](https://redis.com/redis-best-practices/)
- **Why it's great**: Production-ready guidance for performance and security

### 📝 Must-Read Blogs & Articles

#### **Redis Blog**
- **Source**: Redis Labs
- **Link**: [redis.com/blog/](https://redis.com/blog/)
- **Why it's great**: Latest updates, use cases, and technical deep dives

#### **Scaling Redis at Twitter**
- **Source**: Twitter Engineering
- **Link**: [blog.twitter.com/engineering/scaling-redis](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2014/scaling-redis-at-twitter.html)
- **Why it's great**: Real-world scaling challenges and solutions

#### **Redis Memory Optimization**
- **Source**: Redis
- **Link**: [redis.io/topics/memory-optimization](https://redis.io/topics/memory-optimization)
- **Why it's great**: Essential guide for production memory management

### 🎓 Structured Courses

#### **Redis for Developers**
- **Platform**: Redis University
- **Link**: [university.redis.com/courses/ru102js/](https://university.redis.com/courses/ru102js/)
- **Cost**: Free
- **Why it's great**: Hands-on course with real application development

#### **Redis Data Structures**
- **Platform**: Pluralsight
- **Link**: [pluralsight.com/courses/redis-data-structures](https://www.pluralsight.com/courses/redis-data-structures)
- **Cost**: Paid
- **Why it's great**: Deep dive into Redis data structures and their use cases

### 🛠️ Tools & Platforms

#### **RedisInsight**
- **Link**: [redis.com/redis-enterprise/redis-insight/](https://redis.com/redis-enterprise/redis-insight/)
- **Why it's great**: Visual Redis database management and monitoring tool

#### **Redis CLI Interactive Tutorial**
- **Link**: [try.redis.io](https://try.redis.io/)
- **Why it's great**: Hands-on browser-based Redis experience

#### **Redis Desktop Manager**
- **Link**: [resp.app](https://resp.app/)
- **Why it's great**: Cross-platform Redis GUI with advanced features

## Overview

## Key Features

- **In-Memory Storage**: Extremely fast read/write operations
- **Data Structures**: Strings, hashes, lists, sets, sorted sets, streams
- **Persistence**: RDB snapshots and AOF (Append Only File)
- **Replication**: Master-slave replication with automatic failover
- **Clustering**: Built-in clustering for horizontal scaling

## Common Use Cases

### Caching
```bash
# Basic caching operations
redis-cli set "user:1001" '{"name":"John","email":"john@example.com"}'
redis-cli get "user:1001"
redis-cli setex "session:abc123" 3600 "user_data"  # Expire in 1 hour

# Cache patterns
redis-cli set "cache:popular_posts" '[{"id":1,"title":"Post 1"},{"id":2,"title":"Post 2"}]'
redis-cli expire "cache:popular_posts" 300  # 5 minutes TTL
```

### Session Management
```python
import redis

# Python session example
r = redis.Redis(host='localhost', port=6379, db=0)

# Store session
session_data = {
    'user_id': '1001',
    'username': 'john_doe',
    'login_time': '2024-01-01T10:00:00Z'
}
r.setex('session:abc123', 3600, json.dumps(session_data))

# Retrieve session
session = r.get('session:abc123')
if session:
    user_data = json.loads(session)
```

### Message Queues
```bash
# List-based queue
redis-cli lpush "task_queue" '{"type":"email","to":"user@example.com"}'
redis-cli rpop "task_queue"

# Pub/Sub messaging
redis-cli publish "notifications" "New user registered"
redis-cli subscribe "notifications"

# Streams (advanced queues)
redis-cli xadd "events" "*" "type" "login" "user_id" "1001"
redis-cli xread "streams" "events" "0"
```

### Real-time Analytics
```bash
# Counters and metrics
redis-cli incr "page_views:2024-01-01"
redis-cli incrby "api_calls" 5
redis-cli set "current_users" 150

# Sorted sets for leaderboards
redis-cli zadd "leaderboard" 1000 "player1" 950 "player2" 1200 "player3"
redis-cli zrevrange "leaderboard" 0 9 "withscores"  # Top 10
```

## Configuration

### Basic Redis Configuration
```ini
# redis.conf
port 6379
bind 127.0.0.1
requirepass your_secure_password

# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1      # Save if at least 1 key changed in 900 seconds
save 300 10     # Save if at least 10 keys changed in 300 seconds
save 60 10000   # Save if at least 10000 keys changed in 60 seconds

# AOF persistence
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
```

### High Availability Setup
```bash
# Master configuration
port 6379
requirepass master_password

# Slave configuration
port 6380
slaveof 127.0.0.1 6379
masterauth master_password
slave-read-only yes

# Sentinel configuration
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster master_password
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
```

## Monitoring and Maintenance

### Performance Monitoring
```bash
# Real-time monitoring
redis-cli monitor

# Statistics
redis-cli info memory
redis-cli info stats
redis-cli info replication

# Slow log analysis
redis-cli slowlog get 10
redis-cli config set slowlog-log-slower-than 10000  # Log queries > 10ms
```

### Memory Management
```bash
# Check memory usage
redis-cli info memory

# Find large keys
redis-cli --bigkeys

# Memory analysis
redis-cli memory usage "user:1001"
redis-cli memory doctor
```

### Backup and Recovery
```bash
# Manual backup
redis-cli bgsave
redis-cli lastsave

# Backup files
cp /var/lib/redis/dump.rdb /backup/redis-backup-$(date +%Y%m%d).rdb

# Restore from backup
sudo service redis-server stop
sudo cp /backup/redis-backup-20240101.rdb /var/lib/redis/dump.rdb
sudo chown redis:redis /var/lib/redis/dump.rdb
sudo service redis-server start
```

## Best Practices

- Use appropriate data structures for your use case
- Set TTL on cache entries to prevent memory bloat
- Monitor memory usage and configure eviction policies
- Use Redis Sentinel or Cluster for high availability
- Secure with password authentication and network isolation
- Regular backups and disaster recovery testing
- Monitor slow queries and optimize operations

## Redis Pub/Sub

Redis Pub/Sub is a messaging pattern implementation that enables real-time message broadcasting and subscription. It's essential for building real-time applications, event-driven architectures, and inter-service communication.

### Key Pub/Sub Features

- **Lightweight Messaging**: Low-latency, high-throughput message delivery
- **Pattern-Based Subscriptions**: Subscribe using glob-style patterns
- **Fire-and-Forget**: Messages are not persisted (at-most-once delivery)
- **Real-Time**: Immediate message delivery to subscribers
- **Simple Protocol**: Easy integration across programming languages

### Basic Pub/Sub Operations

```bash
# Subscribe to specific channels
SUBSCRIBE channel1 channel2 channel3

# Subscribe to pattern-based channels
PSUBSCRIBE user:*
PSUBSCRIBE events:order:*
PSUBSCRIBE notifications:*:priority:high

# Publish messages
PUBLISH channel1 "Hello, Redis!"
PUBLISH user:123 "User login event"
PUBLISH events:order:456 "Order created"

# List active channels
PUBSUB CHANNELS
PUBSUB CHANNELS user:*

# Count subscribers
PUBSUB NUMSUB channel1 channel2
PUBSUB NUMPAT  # Pattern subscribers count
```

### Real-World Pub/Sub Examples

#### Chat Application
```python
import redis
import json
import threading

class ChatSystem:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis_client.pubsub()
        
    def join_room(self, room_id, user_id):
        """Subscribe user to a chat room"""
        channel = f"chat:room:{room_id}"
        self.pubsub.subscribe(channel)
        
        # Listen for messages in background
        thread = threading.Thread(target=self._listen_messages, args=(user_id,))
        thread.daemon = True
        thread.start()
        
    def send_message(self, room_id, user_id, message):
        """Send message to chat room"""
        channel = f"chat:room:{room_id}"
        data = {
            "user_id": user_id,
            "message": message,
            "timestamp": time.time()
        }
        self.redis_client.publish(channel, json.dumps(data))
        
    def _listen_messages(self, user_id):
        """Listen for incoming messages"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data['user_id'] != user_id:  # Don't echo own messages
                    print(f"[{data['user_id']}]: {data['message']}")
```

#### Microservices Event System
```javascript
// Event Publisher Service
const redis = require('redis');
const client = redis.createClient();

class EventPublisher {
    async publishUserEvent(userId, eventType, data) {
        const event = {
            userId,
            eventType,
            data,
            timestamp: Date.now(),
            id: generateUUID()
        };
        
        // Publish to specific user channel
        await client.publish(`user:${userId}:events`, JSON.stringify(event));
        
        // Publish to global event stream
        await client.publish('global:events', JSON.stringify(event));
        
        // Publish to event-type specific channel
        await client.publish(`events:${eventType}`, JSON.stringify(event));
    }
}

// Event Subscriber Service
class EventSubscriber {
    constructor(serviceName) {
        this.serviceName = serviceName;
        this.subscriber = redis.createClient();
    }
    
    async subscribeToUserEvents(userId) {
        await this.subscriber.subscribe(`user:${userId}:events`);
        this.subscriber.on('message', this.handleUserEvent.bind(this));
    }
    
    async subscribeToEventTypes(eventTypes) {
        const channels = eventTypes.map(type => `events:${type}`);
        await this.subscriber.subscribe(...channels);
    }
    
    handleUserEvent(channel, message) {
        const event = JSON.parse(message);
        console.log(`[${this.serviceName}] Received event:`, event);
        
        // Process event based on type
        switch(event.eventType) {
            case 'user_login':
                this.handleUserLogin(event);
                break;
            case 'order_created':
                this.handleOrderCreated(event);
                break;
            default:
                console.log('Unknown event type:', event.eventType);
        }
    }
}
```

#### Real-Time Notifications
```python
import redis
import asyncio
import websockets
import json

class NotificationService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.connected_clients = {}
        
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections"""
        user_id = await self.authenticate_user(websocket)
        if user_id:
            self.connected_clients[user_id] = websocket
            await self.subscribe_to_user_notifications(user_id)
            
    async def subscribe_to_user_notifications(self, user_id):
        """Subscribe to user-specific notifications"""
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"notifications:user:{user_id}")
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                notification = json.loads(message['data'])
                websocket = self.connected_clients.get(user_id)
                if websocket:
                    await websocket.send(json.dumps(notification))
                    
    def send_notification(self, user_id, notification_type, data):
        """Send notification to specific user"""
        notification = {
            "type": notification_type,
            "data": data,
            "timestamp": time.time()
        }
        
        # Publish to user's notification channel
        self.redis_client.publish(
            f"notifications:user:{user_id}", 
            json.dumps(notification)
        )
        
        # Also publish to notification type channel for analytics
        self.redis_client.publish(
            f"analytics:notifications:{notification_type}",
            json.dumps(notification)
        )
```

### Pub/Sub Patterns and Use Cases

#### Fan-Out Pattern
```bash
# One publisher, multiple subscribers
PUBLISH alerts:system "Server maintenance starting"

# All subscribers to alerts:system receive the message
# Subscribers: monitoring-service, notification-service, logging-service
```

#### Event Sourcing
```bash
# Publish domain events
PUBLISH events:user:created '{"userId": "123", "email": "user@example.com"}'
PUBLISH events:order:placed '{"orderId": "456", "userId": "123", "amount": 99.99}'

# Multiple services subscribe to relevant events
# User service: events:user:*
# Order service: events:order:*
# Analytics service: events:*
```

#### Cache Invalidation
```bash
# When data changes, notify all cache layers
PUBLISH cache:invalidate:user:123 "profile_updated"
PUBLISH cache:invalidate:product:456 "price_changed"

# Cache services subscribe and invalidate accordingly
PSUBSCRIBE cache:invalidate:*
```

### Production Considerations

#### Reliability and Persistence
```python
# Redis Streams for reliable messaging (alternative to Pub/Sub)
import redis

client = redis.Redis()

# Add to stream (persistent)
client.xadd('events:orders', {
    'order_id': '123',
    'status': 'created',
    'timestamp': time.time()
})

# Read from stream with consumer groups
client.xgroup_create('events:orders', 'order-processors', id='0', mkstream=True)
messages = client.xreadgroup('order-processors', 'worker-1', {'events:orders': '>'})
```

#### Monitoring Pub/Sub
```bash
# Monitor Pub/Sub activity
PUBSUB CHANNELS           # List active channels
PUBSUB NUMSUB channel1    # Number of subscribers
PUBSUB NUMPAT            # Number of pattern subscribers

# Monitor client connections
CLIENT LIST TYPE pubsub

# Monitor memory usage
INFO memory
```

### Pub/Sub vs Redis Streams

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Persistence | No | Yes |
| Message History | No | Yes |
| Consumer Groups | No | Yes |
| At-least-once delivery | No | Yes |
| Pattern matching | Yes | No |
| Performance | Higher | Good |
| Use Case | Real-time notifications | Event sourcing, reliable messaging |

## Great Resources

### Official Documentation
- [Redis Official Documentation](https://redis.io/documentation) - Comprehensive Redis guide and references
- [Redis Commands Reference](https://redis.io/commands) - Complete command documentation with examples
- [Redis Pub/Sub Documentation](https://redis.io/topics/pubsub) - Detailed Pub/Sub guide
- [Redis Streams Documentation](https://redis.io/topics/streams-intro) - Alternative to Pub/Sub for reliable messaging

### Learning Resources
- [Redis University](https://university.redis.com/) - Free courses and certifications
- [Redis CLI Interactive Tutorial](https://try.redis.io/) - Hands-on Redis experience in browser
- [Redis Best Practices](https://redis.io/topics/memory-optimization) - Memory optimization and performance tips

### Tools and Utilities
- [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - Visual Redis database management tool
- [redis-cli](https://redis.io/topics/rediscli) - Command-line interface for Redis
- [Awesome Redis](https://github.com/JamzyWang/awesome-redis) - Curated list of Redis resources and tools

---

**Next Steps**: After mastering Redis basics and Pub/Sub, explore [Kafka](/technical/kafka) for more robust messaging or [PostgreSQL](/technical/postgresql) for relational data storage.