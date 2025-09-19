# MySQL

## Overview

MySQL is one of the world's most popular open-source relational databases, widely used for web applications and platform engineering. It's known for its reliability, ease of use, and strong performance for read-heavy workloads.

## Key Features

- **ACID Compliance**: Full transaction support with strong consistency
- **High Performance**: Optimized for fast reads and web applications
- **Replication**: Master-slave and master-master replication
- **Storage Engines**: InnoDB, MyISAM, and others for different use cases
- **Scalability**: Horizontal scaling through sharding and clustering

## Common Use Cases

### Basic Operations
```sql
-- Database and table creation
CREATE DATABASE myapp_production;
USE myapp_production;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Performance Optimization
```sql
-- Query optimization
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Table analysis
ANALYZE TABLE users;
OPTIMIZE TABLE users;

-- Slow query analysis
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SELECT * FROM mysql.slow_log;
```

### Backup and Recovery
```bash
# Full database backup
mysqldump -u root -p --single-transaction --flush-logs --master-data=2 myapp_production > backup.sql

# Compressed backup
mysqldump -u root -p myapp_production | gzip > backup.sql.gz

# Restore database
mysql -u root -p myapp_production < backup.sql

# Binary log backup (for point-in-time recovery)
mysqlbinlog --start-position=4 mysql-bin.000001 > recovery.sql
```

## Configuration

### Production my.cnf
```ini
[mysqld]
# Basic settings
bind-address = 0.0.0.0
port = 3306
datadir = /var/lib/mysql

# Memory settings
innodb_buffer_pool_size = 1G
key_buffer_size = 256M
max_connections = 200

# Performance tuning
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 1
query_cache_size = 128M

# Replication
server-id = 1
log-bin = mysql-bin
binlog_format = ROW
```

### Security Configuration
```sql
-- Create application user
CREATE USER 'app_user'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp_production.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- SSL configuration
ALTER USER 'app_user'@'%' REQUIRE SSL;
```

## Monitoring

### Performance Metrics
```sql
-- Connection statistics
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Threads_connected';

-- Query performance
SHOW STATUS LIKE 'Slow_queries';
SHOW STATUS LIKE 'Questions';

-- InnoDB statistics
SHOW ENGINE INNODB STATUS;
SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS;
```

## Best Practices

- Use InnoDB storage engine for ACID compliance
- Implement proper indexing strategy
- Regular backups with binary logging
- Monitor slow queries and optimize them
- Use connection pooling
- Set up replication for high availability
- Security: strong passwords, SSL, limited privileges

## Great Resources

- [MySQL Official Documentation](https://dev.mysql.com/doc/) - Comprehensive MySQL reference and guides
- [MySQL Performance Blog](https://www.percona.com/blog/) - Advanced performance tuning tips
- [MySQL Tutorial](https://www.mysqltutorial.org/) - Step-by-step learning guide
- [MySQL Workbench](https://www.mysql.com/products/workbench/) - Visual database design and administration
- [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit) - Advanced MySQL administration tools
- [MySQL High Availability](https://dev.mysql.com/doc/mysql-ha-scalability/en/) - Official high availability guide
- [awesome-mysql](https://github.com/shlomi-noach/awesome-mysql) - Curated list of MySQL resources