# MySQL

MySQL is one of the world's most popular open-source relational databases, widely used for web applications and platform engineering. It's known for its reliability, ease of use, and strong performance for read-heavy workloads.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **MySQL Tutorial for Beginners - Full Course**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 4 hours](https://www.youtube.com/watch?v=7S_tz1z_5bA)
- **Why it's great**: Comprehensive tutorial covering basics to advanced MySQL concepts

#### **MySQL Database Tutorial**
- **Channel**: Programming with Mosh
- **Link**: [YouTube - 3 hours](https://www.youtube.com/watch?v=7S_tz1z_5bA)
- **Why it's great**: Professional instruction with practical examples and best practices

#### **MySQL Administration Tutorial**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=9ylj9NR0Lcg)
- **Why it's great**: Focus on MySQL administration and production deployment

### 📖 Essential Documentation

#### **MySQL Official Documentation**
- **Link**: [dev.mysql.com/doc/](https://dev.mysql.com/doc/)
- **Why it's great**: Comprehensive official documentation with tutorials and reference

#### **MySQL Tutorial**
- **Link**: [mysqltutorial.org](https://www.mysqltutorial.org/)
- **Why it's great**: Step-by-step tutorials with practical examples and exercises

#### **MySQL Performance Best Practices**
- **Link**: [dev.mysql.com/doc/refman/8.0/en/optimization.html](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- **Why it's great**: Official guide to MySQL performance optimization

### 📝 Must-Read Blogs & Articles

#### **MySQL Blog**
- **Source**: Oracle MySQL Team
- **Link**: [blogs.oracle.com/mysql/](https://blogs.oracle.com/mysql/)
- **Why it's great**: Official updates and technical insights from MySQL team

#### **Percona Database Performance Blog**
- **Source**: Percona
- **Link**: [percona.com/blog/](https://www.percona.com/blog/)
- **Why it's great**: Expert insights on MySQL performance and optimization

#### **MySQL vs PostgreSQL Comparison**
- **Source**: DigitalOcean
- **Link**: [digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql](https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems)
- **Why it's great**: Comprehensive comparison of database technologies

### 🎓 Structured Courses

#### **MySQL for Data Analytics and Business Intelligence**
- **Platform**: Udemy
- **Link**: [udemy.com/course/sql-mysql-for-data-analytics-and-business-intelligence/](https://www.udemy.com/course/sql-mysql-for-data-analytics-and-business-intelligence/)
- **Cost**: Paid
- **Why it's great**: Practical course with real-world business scenarios

#### **MySQL Database Administration**
- **Platform**: Linux Academy
- **Link**: [acloudguru.com/course/mysql-database-administration](https://acloudguru.com/course/mysql-database-administration)
- **Cost**: Paid
- **Why it's great**: Professional DBA training with production focus

### 🛠️ Tools & Platforms

#### **MySQL Workbench**
- **Link**: [mysql.com/products/workbench/](https://www.mysql.com/products/workbench/)
- **Why it's great**: Official visual tool for MySQL database design and administration

#### **phpMyAdmin**
- **Link**: [phpmyadmin.net](https://www.phpmyadmin.net/)
- **Why it's great**: Popular web-based MySQL administration tool

#### **PlanetScale**
- **Link**: [planetscale.com](https://planetscale.com/)
- **Why it's great**: Serverless MySQL platform with branching and generous free tier

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