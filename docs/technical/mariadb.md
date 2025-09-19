# MariaDB

## Overview

MariaDB is an open-source relational database management system that serves as a drop-in replacement for MySQL. It's designed for platform engineers who need a reliable, high-performance database with enhanced features, better performance, and strong enterprise capabilities while maintaining MySQL compatibility.

## Key Features

- **MySQL Compatibility**: Drop-in replacement for MySQL with enhanced features
- **High Performance**: Advanced storage engines and query optimization
- **Enterprise Features**: Columnar storage, distributed SQL, and advanced security
- **Active Development**: Rapid innovation and community-driven development
- **Multi-Master Replication**: Advanced replication and clustering options

## Installation

### Docker Installation
```bash
# Basic MariaDB container
docker run -d \
  --name mariadb \
  -e MYSQL_ROOT_PASSWORD=secretpassword \
  -e MYSQL_DATABASE=appdb \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  -p 3306:3306 \
  mariadb:latest

# With persistent storage
docker run -d \
  --name mariadb \
  -e MYSQL_ROOT_PASSWORD=secretpassword \
  -e MYSQL_DATABASE=appdb \
  -e MYSQL_USER=appuser \
  -e MYSQL_PASSWORD=apppass \
  -v mariadb_data:/var/lib/mysql \
  -p 3306:3306 \
  mariadb:latest
```

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  mariadb:
    image: mariadb:latest
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: secretpassword
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppass
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
      - ./config/my.cnf:/etc/mysql/conf.d/my.cnf
      - ./init:/docker-entrypoint-initdb.d
    command: >
      --innodb-buffer-pool-size=1G
      --innodb-log-file-size=256M
      --max-connections=200
      --query-cache-size=64M
      --query-cache-type=1

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    restart: always
    ports:
      - "8080:80"
    environment:
      PMA_HOST: mariadb
      PMA_USER: root
      PMA_PASSWORD: secretpassword
    depends_on:
      - mariadb

volumes:
  mariadb_data:
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mariadb-secret
  namespace: database
type: Opaque
stringData:
  root-password: secretpassword
  user-password: apppass
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mariadb-config
  namespace: database
data:
  my.cnf: |
    [mysqld]
    bind-address = 0.0.0.0
    default-storage-engine = innodb
    innodb-buffer-pool-size = 1G
    innodb-log-file-size = 256M
    innodb-flush-log-at-trx-commit = 1
    innodb-file-per-table = 1
    max-connections = 200
    thread-cache-size = 8
    query-cache-size = 64M
    query-cache-type = 1
    slow-query-log = 1
    slow-query-log-file = /var/lib/mysql/slow.log
    long-query-time = 2
    log-error = /var/log/mysql/error.log
    general-log = 0
    
    # Replication settings
    server-id = 1
    log-bin = mysql-bin
    binlog-format = ROW
    expire-logs-days = 7
    
    # Character set
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mariadb
  namespace: database
spec:
  serviceName: mariadb
  replicas: 1
  selector:
    matchLabels:
      app: mariadb
  template:
    metadata:
      labels:
        app: mariadb
    spec:
      containers:
      - name: mariadb
        image: mariadb:latest
        ports:
        - containerPort: 3306
          name: mysql
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mariadb-secret
              key: root-password
        - name: MYSQL_DATABASE
          value: "appdb"
        - name: MYSQL_USER
          value: "appuser"
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mariadb-secret
              key: user-password
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
        - name: mysql-config
          mountPath: /etc/mysql/conf.d
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          exec:
            command:
            - mysqladmin
            - ping
            - -h
            - localhost
            - -u
            - root
            - -p$(MYSQL_ROOT_PASSWORD)
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - mysql
            - -h
            - localhost
            - -u
            - root
            - -p$(MYSQL_ROOT_PASSWORD)
            - -e
            - "SELECT 1"
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: mysql-config
        configMap:
          name: mariadb-config
  volumeClaimTemplates:
  - metadata:
      name: mysql-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: mariadb
  namespace: database
spec:
  selector:
    app: mariadb
  ports:
  - port: 3306
    targetPort: 3306
  type: ClusterIP
```

## Configuration

### Advanced Configuration
```ini
# /etc/mysql/conf.d/my.cnf
[mysqld]
# Basic settings
bind-address = 0.0.0.0
port = 3306
default-storage-engine = innodb
default-table-type = innodb

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Performance tuning
innodb-buffer-pool-size = 2G
innodb-log-file-size = 512M
innodb-log-buffer-size = 16M
innodb-flush-log-at-trx-commit = 1
innodb-file-per-table = 1
innodb-io-capacity = 2000
innodb-read-io-threads = 8
innodb-write-io-threads = 8

# Connection settings
max-connections = 500
thread-cache-size = 16
table-open-cache = 4096
table-definition-cache = 2048

# Query cache
query-cache-size = 128M
query-cache-type = 1
query-cache-limit = 2M

# Logging
slow-query-log = 1
slow-query-log-file = /var/lib/mysql/slow.log
long-query-time = 2
log-error = /var/log/mysql/error.log
general-log = 0

# Binary logging for replication
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
expire-logs-days = 7
max-binlog-size = 100M

# Security
skip-symbolic-links = 1
local-infile = 0

# SSL configuration
ssl-ca = /etc/mysql/ssl/ca-cert.pem
ssl-cert = /etc/mysql/ssl/server-cert.pem
ssl-key = /etc/mysql/ssl/server-key.pem

[mysql]
default-character-set = utf8mb4

[client]
default-character-set = utf8mb4
```

### Master-Slave Replication
```sql
-- Master configuration
-- Add to my.cnf on master
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-do-db = appdb
binlog-ignore-db = mysql,information_schema,performance_schema

-- Create replication user on master
CREATE USER 'replica'@'%' IDENTIFIED BY 'replica_password';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
FLUSH PRIVILEGES;

-- Get master status
SHOW MASTER STATUS;

-- Slave configuration
-- Add to my.cnf on slave
[mysqld]
server-id = 2
relay-log = relay-log
read-only = 1

-- Configure slave
CHANGE MASTER TO
  MASTER_HOST='master-host',
  MASTER_USER='replica',
  MASTER_PASSWORD='replica_password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154;

-- Start replication
START SLAVE;

-- Check slave status
SHOW SLAVE STATUS\G
```

## Application Integration

### Python Integration
```python
# requirements.txt
mysql-connector-python==8.0.33
SQLAlchemy==2.0.23
PyMySQL==1.1.0

# database.py
import mysql.connector
from mysql.connector import pooling, Error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
import time

class MariaDBConnection:
    def __init__(self, config):
        self.config = config
        self.pool = None
        self.engine = None
        self.setup_connection_pool()
        self.setup_sqlalchemy()
    
    def setup_connection_pool(self):
        """Setup connection pool"""
        pool_config = {
            'pool_name': 'mariadb_pool',
            'pool_size': 20,
            'pool_reset_session': True,
            'host': self.config['host'],
            'port': self.config['port'],
            'database': self.config['database'],
            'user': self.config['user'],
            'password': self.config['password'],
            'charset': 'utf8mb4',
            'autocommit': False,
            'time_zone': '+00:00'
        }
        
        try:
            self.pool = pooling.MySQLConnectionPool(**pool_config)
            logging.info("MariaDB connection pool created successfully")
        except Error as e:
            logging.error(f"Error creating connection pool: {e}")
            raise
    
    def setup_sqlalchemy(self):
        """Setup SQLAlchemy engine"""
        connection_string = (
            f"mysql+pymysql://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            f"?charset=utf8mb4"
        )
        
        self.engine = create_engine(
            connection_string,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool"""
        connection = None
        try:
            connection = self.pool.get_connection()
            yield connection
            connection.commit()
        except Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    @contextmanager
    def get_session(self):
        """Get SQLAlchemy session"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Session error: {e}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute query with connection pooling"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                
                if fetch and cursor.with_rows:
                    return cursor.fetchall()
                else:
                    return cursor.rowcount
            finally:
                cursor.close()
    
    def execute_transaction(self, queries):
        """Execute multiple queries in transaction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                for query, params in queries:
                    cursor.execute(query, params or ())
                
                conn.commit()
                return True
            except Error as e:
                conn.rollback()
                logging.error(f"Transaction failed: {e}")
                return False
            finally:
                cursor.close()

# Database models and operations
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")

# Repository pattern
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, username, email, password_hash):
        """Create new user"""
        with self.db.get_session() as session:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash
            )
            session.add(user)
            session.flush()
            return user.id
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        with self.db.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username):
        """Get user by username"""
        with self.db.get_session() as session:
            return session.query(User).filter(User.username == username).first()
    
    def update_user(self, user_id, **kwargs):
        """Update user"""
        with self.db.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.updated_at = datetime.utcnow()
                return True
            return False
    
    def delete_user(self, user_id):
        """Delete user"""
        with self.db.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                return True
            return False
    
    def get_active_users(self, limit=100, offset=0):
        """Get active users with pagination"""
        with self.db.get_session() as session:
            return session.query(User)\
                .filter(User.is_active == True)\
                .offset(offset)\
                .limit(limit)\
                .all()

# Usage example
if __name__ == "__main__":
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'appdb',
        'user': 'appuser',
        'password': 'apppass'
    }
    
    # Initialize database connection
    db = MariaDBConnection(db_config)
    
    # Create tables
    Base.metadata.create_all(db.engine)
    
    # Initialize repository
    user_repo = UserRepository(db)
    
    # Create user
    user_id = user_repo.create_user(
        username="johndoe",
        email="john@example.com",
        password_hash="hashed_password"
    )
    
    # Get user
    user = user_repo.get_user_by_id(user_id)
    print(f"Created user: {user.username} ({user.email})")
    
    # Update user
    user_repo.update_user(user_id, email="john.doe@example.com")
    
    # Get updated user
    updated_user = user_repo.get_user_by_id(user_id)
    print(f"Updated user email: {updated_user.email}")
```

### Node.js Integration
```javascript
// package.json dependencies
{
  "dependencies": {
    "mysql2": "^3.6.0",
    "sequelize": "^6.32.0",
    "express": "^4.18.0"
  }
}

// database.js
const mysql = require('mysql2/promise');
const { Sequelize, DataTypes } = require('sequelize');

class MariaDBConnection {
  constructor(config) {
    this.config = config;
    this.pool = null;
    this.sequelize = null;
    this.setupConnectionPool();
    this.setupSequelize();
  }
  
  setupConnectionPool() {
    this.pool = mysql.createPool({
      host: this.config.host,
      port: this.config.port,
      user: this.config.user,
      password: this.config.password,
      database: this.config.database,
      charset: 'utf8mb4',
      connectionLimit: 20,
      queueLimit: 0,
      acquireTimeout: 60000,
      timeout: 60000,
      reconnect: true,
      timezone: '+00:00'
    });
  }
  
  setupSequelize() {
    this.sequelize = new Sequelize(
      this.config.database,
      this.config.user,
      this.config.password,
      {
        host: this.config.host,
        port: this.config.port,
        dialect: 'mysql',
        pool: {
          max: 20,
          min: 0,
          acquire: 30000,
          idle: 10000
        },
        timezone: '+00:00',
        logging: false
      }
    );
  }
  
  async executeQuery(query, params = []) {
    const connection = await this.pool.getConnection();
    try {
      const [rows] = await connection.execute(query, params);
      return rows;
    } finally {
      connection.release();
    }
  }
  
  async executeTransaction(queries) {
    const connection = await this.pool.getConnection();
    try {
      await connection.beginTransaction();
      
      for (const { query, params } of queries) {
        await connection.execute(query, params || []);
      }
      
      await connection.commit();
      return true;
    } catch (error) {
      await connection.rollback();
      throw error;
    } finally {
      connection.release();
    }
  }
  
  async testConnection() {
    try {
      await this.sequelize.authenticate();
      console.log('MariaDB connection established successfully');
      return true;
    } catch (error) {
      console.error('Unable to connect to MariaDB:', error);
      return false;
    }
  }
}

// models/User.js
const { DataTypes } = require('sequelize');

const User = (sequelize) => {
  return sequelize.define('User', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    username: {
      type: DataTypes.STRING(50),
      allowNull: false,
      unique: true
    },
    email: {
      type: DataTypes.STRING(100),
      allowNull: false,
      unique: true,
      validate: {
        isEmail: true
      }
    },
    passwordHash: {
      type: DataTypes.STRING(255),
      allowNull: false,
      field: 'password_hash'
    },
    isActive: {
      type: DataTypes.BOOLEAN,
      defaultValue: true,
      field: 'is_active'
    }
  }, {
    tableName: 'users',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    underscored: true
  });
};

// models/Post.js
const Post = (sequelize) => {
  return sequelize.define('Post', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    title: {
      type: DataTypes.STRING(200),
      allowNull: false
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false
    },
    authorId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      field: 'author_id',
      references: {
        model: 'users',
        key: 'id'
      }
    },
    isPublished: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
      field: 'is_published'
    }
  }, {
    tableName: 'posts',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    underscored: true
  });
};

// repositories/UserRepository.js
class UserRepository {
  constructor(User, Post) {
    this.User = User;
    this.Post = Post;
  }
  
  async createUser(userData) {
    try {
      const user = await this.User.create(userData);
      return user;
    } catch (error) {
      throw new Error(`Failed to create user: ${error.message}`);
    }
  }
  
  async getUserById(id) {
    try {
      const user = await this.User.findByPk(id, {
        include: [{
          model: this.Post,
          as: 'posts'
        }]
      });
      return user;
    } catch (error) {
      throw new Error(`Failed to get user: ${error.message}`);
    }
  }
  
  async getUserByUsername(username) {
    try {
      const user = await this.User.findOne({
        where: { username }
      });
      return user;
    } catch (error) {
      throw new Error(`Failed to get user: ${error.message}`);
    }
  }
  
  async updateUser(id, updateData) {
    try {
      const [updatedRowsCount] = await this.User.update(updateData, {
        where: { id }
      });
      return updatedRowsCount > 0;
    } catch (error) {
      throw new Error(`Failed to update user: ${error.message}`);
    }
  }
  
  async deleteUser(id) {
    try {
      const deletedRowsCount = await this.User.destroy({
        where: { id }
      });
      return deletedRowsCount > 0;
    } catch (error) {
      throw new Error(`Failed to delete user: ${error.message}`);
    }
  }
  
  async getActiveUsers(limit = 100, offset = 0) {
    try {
      const users = await this.User.findAndCountAll({
        where: { isActive: true },
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });
      return users;
    } catch (error) {
      throw new Error(`Failed to get users: ${error.message}`);
    }
  }
}

// app.js
const express = require('express');
const app = express();

// Database configuration
const dbConfig = {
  host: 'localhost',
  port: 3306,
  user: 'appuser',
  password: 'apppass',
  database: 'appdb'
};

// Initialize database
const db = new MariaDBConnection(dbConfig);

// Initialize models
const UserModel = User(db.sequelize);
const PostModel = Post(db.sequelize);

// Define associations
UserModel.hasMany(PostModel, { foreignKey: 'authorId', as: 'posts' });
PostModel.belongsTo(UserModel, { foreignKey: 'authorId', as: 'author' });

// Initialize repository
const userRepository = new UserRepository(UserModel, PostModel);

app.use(express.json());

// Routes
app.post('/users', async (req, res) => {
  try {
    const { username, email, passwordHash } = req.body;
    const user = await userRepository.createUser({
      username,
      email,
      passwordHash
    });
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/users/:id', async (req, res) => {
  try {
    const user = await userRepository.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.put('/users/:id', async (req, res) => {
  try {
    const updated = await userRepository.updateUser(req.params.id, req.body);
    if (!updated) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json({ message: 'User updated successfully' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.delete('/users/:id', async (req, res) => {
  try {
    const deleted = await userRepository.deleteUser(req.params.id);
    if (!deleted) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/users', async (req, res) => {
  try {
    const { limit = 100, offset = 0 } = req.query;
    const users = await userRepository.getActiveUsers(
      parseInt(limit),
      parseInt(offset)
    );
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;

async function startServer() {
  try {
    // Test database connection
    await db.testConnection();
    
    // Sync database models
    await db.sequelize.sync({ force: false });
    console.log('Database synchronized');
    
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
```

## High Availability and Clustering

### Galera Cluster Setup
```yaml
# docker-compose-galera.yml
version: '3.8'
services:
  mariadb-galera-1:
    image: mariadb:latest
    command: >
      --wsrep-new-cluster
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://
      --wsrep-node-address=mariadb-galera-1
      --wsrep-node-name=node1
      --wsrep-sst-method=rsync
      --binlog-format=row
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
    environment:
      MYSQL_ROOT_PASSWORD: clusterpassword
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppass
    networks:
      - galera-network
    volumes:
      - galera1_data:/var/lib/mysql

  mariadb-galera-2:
    image: mariadb:latest
    command: >
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://mariadb-galera-1
      --wsrep-node-address=mariadb-galera-2
      --wsrep-node-name=node2
      --wsrep-sst-method=rsync
      --binlog-format=row
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
    environment:
      MYSQL_ROOT_PASSWORD: clusterpassword
    networks:
      - galera-network
    volumes:
      - galera2_data:/var/lib/mysql
    depends_on:
      - mariadb-galera-1

  mariadb-galera-3:
    image: mariadb:latest
    command: >
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://mariadb-galera-1,mariadb-galera-2
      --wsrep-node-address=mariadb-galera-3
      --wsrep-node-name=node3
      --wsrep-sst-method=rsync
      --binlog-format=row
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
    environment:
      MYSQL_ROOT_PASSWORD: clusterpassword
    networks:
      - galera-network
    volumes:
      - galera3_data:/var/lib/mysql
    depends_on:
      - mariadb-galera-1
      - mariadb-galera-2

  haproxy:
    image: haproxy:latest
    ports:
      - "3306:3306"
      - "8404:8404"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    networks:
      - galera-network
    depends_on:
      - mariadb-galera-1
      - mariadb-galera-2
      - mariadb-galera-3

networks:
  galera-network:
    driver: bridge

volumes:
  galera1_data:
  galera2_data:
  galera3_data:
```

### HAProxy Configuration for Load Balancing
```config
# haproxy.cfg
global
    daemon
    log stdout local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy

defaults
    mode tcp
    log global
    option tcplog
    option dontlognull
    retries 3
    timeout queue 1m
    timeout connect 10s
    timeout client 1m
    timeout server 1m
    timeout check 10s

# Stats page
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE

# MariaDB read-write (writes go to primary)
listen mariadb-write
    bind *:3306
    mode tcp
    option mysql-check user haproxy
    balance roundrobin
    server node1 mariadb-galera-1:3306 check weight 100
    server node2 mariadb-galera-2:3306 check weight 100 backup
    server node3 mariadb-galera-3:3306 check weight 100 backup

# MariaDB read-only (reads distributed across all nodes)
listen mariadb-read
    bind *:3307
    mode tcp
    option mysql-check user haproxy
    balance roundrobin
    server node1 mariadb-galera-1:3306 check weight 100
    server node2 mariadb-galera-2:3306 check weight 100
    server node3 mariadb-galera-3:3306 check weight 100
```

## Monitoring and Performance

### Prometheus Monitoring
```yaml
# mysql-exporter.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-exporter
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql-exporter
  template:
    metadata:
      labels:
        app: mysql-exporter
    spec:
      containers:
      - name: mysql-exporter
        image: prom/mysqld-exporter:latest
        ports:
        - containerPort: 9104
        env:
        - name: DATA_SOURCE_NAME
          value: "exporter:password@(mariadb:3306)/"
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
  name: mysql-exporter
  namespace: monitoring
spec:
  selector:
    app: mysql-exporter
  ports:
  - port: 9104
    targetPort: 9104
```

### Key Performance Metrics
```sql
-- Performance monitoring queries
-- Check current connections
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- Query performance
SHOW STATUS LIKE 'Slow_queries';
SHOW STATUS LIKE 'Questions';
SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE TIME > 30;

-- InnoDB metrics
SHOW ENGINE INNODB STATUS;
SHOW STATUS LIKE 'Innodb_buffer_pool%';
SHOW STATUS LIKE 'Innodb_log%';

-- Replication status
SHOW SLAVE STATUS\G
SHOW MASTER STATUS;

-- Table optimization
ANALYZE TABLE users;
OPTIMIZE TABLE users;
CHECK TABLE users;

-- Index usage analysis
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    INDEX_NAME,
    CARDINALITY,
    SUB_PART,
    PACKED,
    NULLABLE,
    INDEX_TYPE
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = 'appdb'
ORDER BY TABLE_NAME, SEQ_IN_INDEX;
```

### Grafana Dashboard Queries
```promql
# Connection metrics
mysql_global_status_threads_connected

# Query rate
rate(mysql_global_status_questions[5m])

# Slow queries
rate(mysql_global_status_slow_queries[5m])

# InnoDB buffer pool efficiency
mysql_global_status_innodb_buffer_pool_read_requests / 
(mysql_global_status_innodb_buffer_pool_read_requests + mysql_global_status_innodb_buffer_pool_reads)

# Replication lag
mysql_slave_lag_seconds

# Table locks
rate(mysql_global_status_table_locks_waited[5m])

# Query cache hit rate
mysql_global_status_qcache_hits / 
(mysql_global_status_qcache_hits + mysql_global_status_qcache_inserts)
```

## Backup and Recovery

### Automated Backup Script
```bash
#!/bin/bash
# mariadb-backup.sh

# Configuration
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="backup_user"
DB_PASS="backup_password"
BACKUP_DIR="/backups/mariadb"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a ${BACKUP_DIR}/backup.log
}

# Function to create database backup
backup_database() {
    local database=$1
    local backup_file="${BACKUP_DIR}/${database}_${DATE}.sql.gz"
    
    log "Starting backup of database: ${database}"
    
    # Create backup with compression
    mysqldump \
        --host=${DB_HOST} \
        --port=${DB_PORT} \
        --user=${DB_USER} \
        --password=${DB_PASS} \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --add-drop-database \
        --databases ${database} | gzip > ${backup_file}
    
    if [ $? -eq 0 ]; then
        log "Backup completed successfully: ${backup_file}"
        
        # Verify backup
        if [ -s ${backup_file} ]; then
            log "Backup file verified: $(du -h ${backup_file} | cut -f1)"
        else
            log "ERROR: Backup file is empty!"
            return 1
        fi
    else
        log "ERROR: Backup failed for database: ${database}"
        return 1
    fi
}

# Function to cleanup old backups
cleanup_old_backups() {
    log "Cleaning up backups older than ${RETENTION_DAYS} days"
    find ${BACKUP_DIR} -name "*.sql.gz" -mtime +${RETENTION_DAYS} -delete
    find ${BACKUP_DIR} -name "*.log" -mtime +${RETENTION_DAYS} -delete
}

# Function to upload to S3 (optional)
upload_to_s3() {
    local backup_file=$1
    local s3_bucket="my-backup-bucket"
    
    if command -v aws &> /dev/null; then
        log "Uploading backup to S3: ${s3_bucket}"
        aws s3 cp ${backup_file} s3://${s3_bucket}/mariadb/$(basename ${backup_file})
        
        if [ $? -eq 0 ]; then
            log "S3 upload completed successfully"
        else
            log "ERROR: S3 upload failed"
        fi
    fi
}

# Main backup process
main() {
    log "Starting MariaDB backup process"
    
    # Get list of databases to backup
    DATABASES=$(mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS} -e "SHOW DATABASES;" | grep -Ev "^(Database|information_schema|performance_schema|mysql|sys)$")
    
    # Backup each database
    for database in ${DATABASES}; do
        backup_database ${database}
        
        # Upload to S3 if configured
        backup_file="${BACKUP_DIR}/${database}_${DATE}.sql.gz"
        if [ -f ${backup_file} ]; then
            upload_to_s3 ${backup_file}
        fi
    done
    
    # Cleanup old backups
    cleanup_old_backups
    
    log "Backup process completed"
}

# Run main function
main
```

### Point-in-Time Recovery
```bash
#!/bin/bash
# point-in-time-recovery.sh

# Configuration
BACKUP_FILE="/backups/mariadb/appdb_20240101_120000.sql.gz"
BINLOG_DIR="/var/lib/mysql"
RECOVERY_TIME="2024-01-01 15:30:00"
DB_NAME="appdb"

# Restore from backup
echo "Restoring database from backup..."
zcat ${BACKUP_FILE} | mysql -u root -p

# Apply binary logs for point-in-time recovery
echo "Applying binary logs up to ${RECOVERY_TIME}..."
mysqlbinlog \
    --stop-datetime="${RECOVERY_TIME}" \
    ${BINLOG_DIR}/mysql-bin.* | mysql -u root -p ${DB_NAME}

echo "Point-in-time recovery completed"
```

## Best Practices

- Use InnoDB storage engine for ACID compliance and better performance
- Implement proper indexing strategies for query optimization
- Configure appropriate buffer pool size (75% of available RAM)
- Enable slow query logging for performance monitoring
- Use connection pooling in applications
- Implement regular backup and recovery testing
- Monitor replication lag in master-slave setups
- Use SSL/TLS for secure connections
- Regular maintenance tasks (ANALYZE, OPTIMIZE tables)

## Great Resources

- [MariaDB Documentation](https://mariadb.org/documentation/) - Official comprehensive documentation
- [MariaDB Knowledge Base](https://mariadb.com/kb/en/) - Detailed guides and tutorials
- [MariaDB Performance Blog](https://mariadb.org/performance/) - Performance optimization tips
- [Galera Cluster Documentation](https://galeracluster.com/library/documentation/) - Multi-master clustering
- [MariaDB GitHub](https://github.com/MariaDB/server) - Source code and community
- [MariaDB vs MySQL](https://mariadb.com/kb/en/mariadb-vs-mysql-features/) - Feature comparison
- [MariaDB ColumnStore](https://mariadb.com/products/columnstore/) - Columnar storage engine
- [MariaDB MaxScale](https://mariadb.com/products/maxscale/) - Database proxy and load balancer