# PostgreSQL

PostgreSQL is a powerful, open-source relational database system known for its reliability, feature robustness, and performance. It's widely used in platform engineering for applications requiring complex queries, data integrity, and scalability.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **PostgreSQL Tutorial for Beginners - Complete Course**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 4 hours](https://www.youtube.com/watch?v=qw--VYLpxG4)
- **Why it's great**: Comprehensive tutorial covering basics to advanced features

#### **PostgreSQL Administration Tutorial**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=aHbE3pTyG-Q)
- **Why it's great**: Practical administration guide with real-world scenarios

#### **Advanced PostgreSQL Features**
- **Channel**: Hussein Nasser
- **Link**: [YouTube Playlist](https://www.youtube.com/playlist?list=PLQnljOFTspQXjD0HOzN7P2tgzu7scWpl2)
- **Why it's great**: Deep dives into advanced PostgreSQL concepts and optimizations

### 📖 Essential Documentation

#### **PostgreSQL Official Documentation**
- **Link**: [postgresql.org/docs/](https://www.postgresql.org/docs/)
- **Why it's great**: Comprehensive official documentation with tutorials and examples

#### **PostgreSQL Tutorial**
- **Link**: [postgresqltutorial.com](https://www.postgresqltutorial.com/)
- **Why it's great**: Step-by-step tutorials with practical examples

#### **PostgreSQL Performance Tuning**
- **Link**: [wiki.postgresql.org/wiki/Performance_Optimization](https://wiki.postgresql.org/wiki/Performance_Optimization)
- **Why it's great**: Essential guide for optimizing PostgreSQL performance

### 📝 Must-Read Blogs & Articles

#### **PostgreSQL Blog**
- **Source**: PostgreSQL Global Development Group
- **Link**: [postgresql.org/about/news/](https://www.postgresql.org/about/news/)
- **Why it's great**: Official updates and technical insights from core team

#### **2ndQuadrant PostgreSQL Blog**
- **Source**: 2ndQuadrant
- **Link**: [2ndquadrant.com/en/blog/](https://www.2ndquadrant.com/en/blog/)
- **Why it's great**: Expert insights and advanced PostgreSQL techniques

#### **PostgreSQL vs MySQL Comparison**
- **Source**: DigitalOcean
- **Link**: [digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql](https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems)
- **Why it's great**: Comprehensive comparison of database technologies

### 🎓 Structured Courses

#### **PostgreSQL for Everybody Specialization**
- **Platform**: Coursera (University of Michigan)
- **Link**: [coursera.org/specializations/postgresql-for-everybody](https://www.coursera.org/specializations/postgresql-for-everybody)
- **Cost**: Free (audit mode)
- **Why it's great**: University-level course with practical projects

#### **Complete PostgreSQL Bootcamp**
- **Platform**: Udemy
- **Link**: [udemy.com/course/the-complete-python-postgresql-developer-course/](https://www.udemy.com/course/the-complete-python-postgresql-developer-course/)
- **Cost**: Paid
- **Why it's great**: Hands-on course with application development focus

### 🛠️ Tools & Platforms

#### **pgAdmin**
- **Link**: [pgadmin.org](https://www.pgadmin.org/)
- **Why it's great**: Most popular PostgreSQL administration and development platform

#### **Supabase**
- **Link**: [supabase.com](https://supabase.com/)
- **Why it's great**: PostgreSQL-based Backend-as-a-Service with generous free tier

#### **PostgreSQL Playground**
- **Link**: [pgexercises.com](https://pgexercises.com/)
- **Why it's great**: Interactive SQL exercises specifically for PostgreSQL

## Overview

PostgreSQL is a powerful, open-source relational database system known for its reliability, feature robustness, and performance. It's widely used in platform engineering for applications requiring complex queries, data integrity, and scalability.

## Key Features

- **ACID Compliance**: Full transaction support with data integrity
- **Extensibility**: Custom functions, data types, and operators
- **JSON Support**: Built-in JSON and JSONB data types
- **Advanced Indexing**: B-tree, Hash, GiST, SP-GiST, GIN, and BRIN
- **Replication**: Streaming, logical, and built-in replication options

## Common Use Cases

### Basic Connection and Queries
```sql
-- Connect to database
\c myapp_production

-- Create table with constraints
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Insert data
INSERT INTO users (username, email, metadata) 
VALUES ('john_doe', 'john@example.com', '{"role": "admin", "preferences": {"theme": "dark"}}');

-- Query with JSON operations
SELECT username, metadata->>'role' as role 
FROM users 
WHERE metadata @> '{"role": "admin"}';
```

### Performance Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_metadata_gin ON users USING GIN(metadata);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';

-- Update statistics
ANALYZE users;
```

### Backup and Restore
```bash
# Database backup
pg_dump -h localhost -U postgres -d myapp_production > backup.sql

# Compressed backup
pg_dump -h localhost -U postgres -d myapp_production | gzip > backup.sql.gz

# Restore database
psql -h localhost -U postgres -d myapp_production < backup.sql

# Point-in-time recovery setup
archive_mode = on
archive_command = 'cp %p /path/to/archive/%f'
wal_level = replica
```

## Configuration for Production

### postgresql.conf Tuning
```ini
# Memory settings
shared_buffers = 256MB          # 25% of RAM
effective_cache_size = 1GB      # 50-75% of RAM
work_mem = 4MB                  # Per operation memory

# Connection settings
max_connections = 100
listen_addresses = '*'

# Logging
log_statement = 'all'
log_duration = on
log_min_duration_statement = 1000  # Log slow queries
```

### Security Configuration
```sql
-- Create application user
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE myapp_production TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Enable SSL in postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
```

## Monitoring and Maintenance

### Health Check Queries
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size(current_database()));

-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Lock monitoring
SELECT * FROM pg_locks WHERE NOT granted;

-- Index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch 
FROM pg_stat_user_indexes;
```

### Automated Maintenance
```bash
#!/bin/bash
# Daily maintenance script

# Vacuum and analyze
psql -d myapp_production -c "VACUUM ANALYZE;"

# Reindex if needed
psql -d myapp_production -c "REINDEX DATABASE myapp_production;"

# Check for bloat
psql -d myapp_production -c "SELECT schemaname, tablename, n_dead_tup FROM pg_stat_user_tables WHERE n_dead_tup > 1000;"
```

## Best Practices

- Use connection pooling (PgBouncer, pgpool-II)
- Regular VACUUM and ANALYZE operations
- Monitor slow queries and optimize them
- Use prepared statements to prevent SQL injection
- Implement proper indexing strategy
- Set up monitoring and alerting
- Regular backups with point-in-time recovery

## Great Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/) - Comprehensive database documentation
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) - Step-by-step learning guide
- [pgcli](https://www.pgcli.com/) - Modern command-line interface with auto-completion
- [Postgres Guide](http://postgresguide.com/) - Practical PostgreSQL guide
- [PgHero](https://github.com/ankane/pghero) - Performance dashboard for PostgreSQL
- [PostgreSQL High Performance](https://www.postgresql.org/docs/current/performance-tips.html) - Official performance tuning guide
- [awesome-postgres](https://github.com/dhamaniasad/awesome-postgres) - Curated list of PostgreSQL resources