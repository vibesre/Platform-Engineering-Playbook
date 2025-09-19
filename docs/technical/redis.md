# Redis

## Overview

Redis is an in-memory data structure store used as a database, cache, and message broker. It's essential for platform engineers building high-performance applications that need fast data access, caching, and real-time features.

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

## Great Resources

- [Redis Official Documentation](https://redis.io/documentation) - Comprehensive Redis guide and references
- [Redis Commands Reference](https://redis.io/commands) - Complete command documentation with examples
- [Redis University](https://university.redis.com/) - Free courses and certifications
- [Redis CLI Interactive Tutorial](https://try.redis.io/) - Hands-on Redis experience in browser
- [Redis Best Practices](https://redis.io/topics/memory-optimization) - Memory optimization and performance tips
- [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - Visual Redis database management tool
- [Awesome Redis](https://github.com/JamzyWang/awesome-redis) - Curated list of Redis resources and tools