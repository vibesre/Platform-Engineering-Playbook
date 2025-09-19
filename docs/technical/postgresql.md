# PostgreSQL

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