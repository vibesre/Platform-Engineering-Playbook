# TiDB

TiDB is an open-source distributed SQL database that supports horizontal scaling, strong consistency, and high availability with MySQL compatibility.

## Installation

### Docker Compose
```yaml
version: '3.8'
services:
  pd:
    image: pingcap/pd:latest
    ports:
      - "2379:2379"
      - "2380:2380"
    volumes:
      - pd_data:/data
    command:
      - --name=pd
      - --data-dir=/data/pd
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --initial-cluster=pd=http://pd:2380
      - --log-level=info

  tikv:
    image: pingcap/tikv:latest
    volumes:
      - tikv_data:/data
    command:
      - --pd-endpoints=pd:2379
      - --data-dir=/data/tikv
      - --log-level=info
    depends_on:
      - pd

  tidb:
    image: pingcap/tidb:latest
    ports:
      - "4000:4000"
      - "10080:10080"
    command:
      - --store=tikv
      - --path=pd:2379
      - --log-level=info
    depends_on:
      - tikv

  tiflash:
    image: pingcap/tiflash:latest
    volumes:
      - tiflash_data:/data
    command:
      - --pd-endpoints=pd:2379
      - --data-dir=/data/tiflash
    depends_on:
      - pd

volumes:
  pd_data:
  tikv_data:
  tiflash_data:
```

### Kubernetes with TiDB Operator
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tidb-cluster
---
apiVersion: pingcap.com/v1alpha1
kind: TidbCluster
metadata:
  name: basic
  namespace: tidb-cluster
spec:
  version: v7.5.0
  timezone: UTC
  pvReclaimPolicy: Retain
  
  pd:
    baseImage: pingcap/pd
    maxFailoverCount: 0
    replicas: 3
    requests:
      storage: "10Gi"
      cpu: "500m"
      memory: "1Gi"
    config: |
      [log]
      level = "info"
      [replication]
      max-replicas = 3
      location-labels = ["zone", "rack", "host"]

  tikv:
    baseImage: pingcap/tikv
    maxFailoverCount: 0
    replicas: 3
    requests:
      storage: "100Gi"
      cpu: "1000m"
      memory: "2Gi"
    config: |
      [storage]
      reserve-space = "2GB"
      [raftstore]
      apply-pool-size = 2
      store-pool-size = 2

  tidb:
    baseImage: pingcap/tidb
    maxFailoverCount: 0
    replicas: 2
    service:
      type: ClusterIP
      externalTrafficPolicy: Local
    config: |
      [log]
      level = "info"
      [performance]
      max-procs = 0
      max-memory = 0

  tiflash:
    baseImage: pingcap/tiflash
    maxFailoverCount: 0
    replicas: 1
    storageClaims:
    - resources:
        requests:
          storage: 100Gi
      storageClassName: local-storage
    config:
      config: |
        [logger]
        level = "info"
---
apiVersion: v1
kind: Service
metadata:
  name: tidb-service
  namespace: tidb-cluster
spec:
  selector:
    app.kubernetes.io/component: tidb
    app.kubernetes.io/instance: basic
  ports:
  - port: 4000
    targetPort: 4000
    name: mysql
  - port: 10080
    targetPort: 10080
    name: status
  type: LoadBalancer
```

## Database Setup

### Initial Configuration
```sql
-- Connect using MySQL client
mysql -h 127.0.0.1 -P 4000 -u root

-- Create database and user
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE USER 'app_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON ecommerce.* TO 'app_user'@'%';

-- Create tables optimized for TiDB
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_region_created (region, created_at),
    INDEX idx_users_email (email),
    INDEX idx_users_uuid (uuid)
) SHARD_ROW_ID_BITS = 4;

CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_orders_user_created (user_id, created_at),
    INDEX idx_orders_status_created (status, created_at),
    INDEX idx_orders_region_created (region, created_at),
    INDEX idx_orders_uuid (uuid)
) SHARD_ROW_ID_BITS = 4;

-- Create analytics table with TiFlash replica
CREATE TABLE order_analytics (
    date_key DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    total_orders INT NOT NULL DEFAULT 0,
    total_revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    avg_order_value DECIMAL(10,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (date_key, region)
);

-- Add TiFlash replica for OLAP queries
ALTER TABLE order_analytics SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
ALTER TABLE users SET TIFLASH REPLICA 1;
```

### Advanced Schema with Partitioning
```sql
-- Partitioned table for time-series data
CREATE TABLE metrics (
    id BIGINT AUTO_INCREMENT,
    timestamp TIMESTAMP NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE NOT NULL,
    tags JSON,
    region VARCHAR(50) NOT NULL,
    PRIMARY KEY (id, timestamp),
    INDEX idx_metrics_device_time (device_id, timestamp),
    INDEX idx_metrics_name_time (metric_name, timestamp)
) SHARD_ROW_ID_BITS = 4
PARTITION BY RANGE (UNIX_TIMESTAMP(timestamp)) (
    PARTITION p202401 VALUES LESS THAN (UNIX_TIMESTAMP('2024-02-01')),
    PARTITION p202402 VALUES LESS THAN (UNIX_TIMESTAMP('2024-03-01')),
    PARTITION p202403 VALUES LESS THAN (UNIX_TIMESTAMP('2024-04-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Hash partitioned table for high-write workloads
CREATE TABLE events (
    id BIGINT AUTO_INCREMENT,
    event_id VARCHAR(36) NOT NULL,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, user_id),
    UNIQUE KEY uk_event_id (event_id),
    INDEX idx_events_type_created (event_type, created_at)
) SHARD_ROW_ID_BITS = 4
PARTITION BY HASH(user_id) PARTITIONS 16;

-- Set TiFlash replicas for analytical queries
ALTER TABLE metrics SET TIFLASH REPLICA 1;
ALTER TABLE events SET TIFLASH REPLICA 1;
```

## Python Integration

### Database Client with Connection Pool
```python
import pymysql
from pymysql.pooling import ConnectionPool
from contextlib import contextmanager
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class TiDBClient:
    def __init__(self, host='localhost', port=4000, user='root', 
                 password='', database='ecommerce', pool_size=10):
        self.pool_config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'autocommit': True,
            'pool_size': pool_size,
            'pool_name': 'tidb_pool'
        }
        self.pool = ConnectionPool(**self.pool_config)
        
    @contextmanager
    def get_connection(self):
        conn = self.pool.get_connection()
        try:
            yield conn
        finally:
            conn.close()
            
    def create_user(self, email: str, name: str, region: str) -> str:
        """Create a new user and return UUID"""
        user_uuid = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (uuid, email, name, region, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
            """, (user_uuid, email, name, region))
            conn.commit()
            
        return user_uuid
        
    def create_order(self, user_uuid: str, total_amount: float, 
                    region: str, status: str = 'pending') -> str:
        """Create a new order and return order UUID"""
        order_uuid = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user ID
            cursor.execute("SELECT id FROM users WHERE uuid = %s", (user_uuid,))
            user_result = cursor.fetchone()
            if not user_result:
                raise ValueError(f"User with UUID {user_uuid} not found")
                
            user_id = user_result[0]
            
            cursor.execute("""
                INSERT INTO orders (uuid, user_id, total_amount, status, region, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """, (order_uuid, user_id, total_amount, status, region))
            conn.commit()
            
        return order_uuid
        
    def get_user_orders(self, user_uuid: str, limit: int = 10) -> List[Dict]:
        """Get orders for a specific user"""
        with self.get_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT o.uuid, o.total_amount, o.status, o.region, o.created_at
                FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE u.uuid = %s
                ORDER BY o.created_at DESC
                LIMIT %s
            """, (user_uuid, limit))
            
            return cursor.fetchall()
            
    def bulk_insert_metrics(self, metrics_data: List[Dict]) -> None:
        """Bulk insert metrics data for high throughput"""
        if not metrics_data:
            return
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Prepare batch insert
            insert_query = """
                INSERT INTO metrics (timestamp, device_id, metric_name, value, tags, region)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Convert data to tuples
            values = []
            for metric in metrics_data:
                values.append((
                    metric.get('timestamp', datetime.now()),
                    metric['device_id'],
                    metric['metric_name'],
                    metric['value'],
                    json.dumps(metric.get('tags', {})),
                    metric.get('region', 'default')
                ))
            
            cursor.executemany(insert_query, values)
            conn.commit()
            
    def execute_analytical_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute analytical queries that use TiFlash replicas"""
        with self.get_connection() as conn:
            # Use hint to force TiFlash usage for OLAP queries
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SET @@tidb_isolation_read_engines = 'tiflash'")
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.execute("SET @@tidb_isolation_read_engines = 'tikv,tiflash'")
            return result

# Usage example
client = TiDBClient(host='localhost', port=4000, user='root', database='ecommerce')

# Create user and orders
user_uuid = client.create_user('user@example.com', 'John Doe', 'us-west-1')
order_uuid = client.create_order(user_uuid, 99.99, 'us-west-1')

# Bulk insert metrics
metrics = [
    {
        'timestamp': datetime.now(),
        'device_id': f'device_{i}',
        'metric_name': 'cpu_usage',
        'value': 50 + (i % 50),
        'tags': {'env': 'production', 'host': f'host_{i}'},
        'region': 'us-west-1'
    }
    for i in range(1000)
]
client.bulk_insert_metrics(metrics)
```

### Advanced Analytics and Reporting
```python
class TiDBAnalytics:
    def __init__(self, client: TiDBClient):
        self.client = client
        
    def generate_daily_report(self, date: str, region: Optional[str] = None) -> Dict[str, Any]:
        """Generate daily business analytics report"""
        base_query = """
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[orders, users]) */
                COUNT(*) as total_orders,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers,
                MAX(total_amount) as max_order_value,
                MIN(total_amount) as min_order_value
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE DATE(o.created_at) = %s
        """
        
        params = [date]
        if region:
            base_query += " AND o.region = %s"
            params.append(region)
            
        result = self.client.execute_analytical_query(base_query, tuple(params))
        return result[0] if result else {}
        
    def get_regional_performance(self, start_date: str, end_date: str) -> List[Dict]:
        """Analyze performance by region"""
        query = """
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[orders]) */
                region,
                COUNT(*) as order_count,
                SUM(total_amount) as revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers,
                COUNT(*) / COUNT(DISTINCT DATE(created_at)) as avg_daily_orders
            FROM orders
            WHERE DATE(created_at) BETWEEN %s AND %s
            GROUP BY region
            ORDER BY revenue DESC
        """
        
        return self.client.execute_analytical_query(query, (start_date, end_date))
        
    def get_user_cohort_analysis(self, registration_month: str) -> List[Dict]:
        """Perform cohort analysis for user retention"""
        query = """
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[users, orders]) */
                TIMESTAMPDIFF(MONTH, u.created_at, o.created_at) as months_since_registration,
                COUNT(DISTINCT u.id) as active_users,
                COUNT(o.id) as total_orders,
                SUM(o.total_amount) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE DATE_FORMAT(u.created_at, '%Y-%m') = %s
            GROUP BY months_since_registration
            ORDER BY months_since_registration
        """
        
        return self.client.execute_analytical_query(query, (registration_month,))
        
    def get_real_time_metrics(self, device_id: str, hours: int = 24) -> List[Dict]:
        """Get real-time metrics for a device"""
        query = """
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[metrics]) */
                metric_name,
                AVG(value) as avg_value,
                MAX(value) as max_value,
                MIN(value) as min_value,
                COUNT(*) as data_points,
                STDDEV(value) as std_deviation
            FROM metrics
            WHERE device_id = %s 
              AND timestamp >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            GROUP BY metric_name
            ORDER BY metric_name
        """
        
        return self.client.execute_analytical_query(query, (device_id, hours))

analytics = TiDBAnalytics(client)
daily_report = analytics.generate_daily_report('2024-01-15')
regional_performance = analytics.get_regional_performance('2024-01-01', '2024-01-31')
```

## Node.js Integration

### Connection and Basic Operations
```javascript
const mysql = require('mysql2/promise');
const { v4: uuidv4 } = require('uuid');

class TiDBClient {
    constructor(config = {}) {
        this.poolConfig = {
            host: config.host || 'localhost',
            port: config.port || 4000,
            user: config.user || 'root',
            password: config.password || '',
            database: config.database || 'ecommerce',
            charset: 'utf8mb4',
            connectionLimit: config.connectionLimit || 10,
            acquireTimeout: 60000,
            timeout: 60000,
            multipleStatements: false
        };
        
        this.pool = mysql.createPool(this.poolConfig);
    }

    async createUser(email, name, region) {
        const userUuid = uuidv4();
        const connection = await this.pool.getConnection();
        
        try {
            await connection.execute(
                'INSERT INTO users (uuid, email, name, region, created_at, updated_at) VALUES (?, ?, ?, ?, NOW(), NOW())',
                [userUuid, email, name, region]
            );
            return userUuid;
        } finally {
            connection.release();
        }
    }

    async createOrder(userUuid, totalAmount, region, status = 'pending') {
        const orderUuid = uuidv4();
        const connection = await this.pool.getConnection();
        
        try {
            await connection.beginTransaction();
            
            // Get user ID
            const [userRows] = await connection.execute(
                'SELECT id FROM users WHERE uuid = ?',
                [userUuid]
            );
            
            if (userRows.length === 0) {
                throw new Error(`User with UUID ${userUuid} not found`);
            }
            
            const userId = userRows[0].id;
            
            // Create order
            await connection.execute(
                'INSERT INTO orders (uuid, user_id, total_amount, status, region, created_at, updated_at) VALUES (?, ?, ?, ?, ?, NOW(), NOW())',
                [orderUuid, userId, totalAmount, status, region]
            );
            
            await connection.commit();
            return orderUuid;
            
        } catch (error) {
            await connection.rollback();
            throw error;
        } finally {
            connection.release();
        }
    }

    async getUserOrders(userUuid, limit = 10) {
        const connection = await this.pool.getConnection();
        
        try {
            const [rows] = await connection.execute(`
                SELECT o.uuid, o.total_amount, o.status, o.region, o.created_at
                FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE u.uuid = ?
                ORDER BY o.created_at DESC
                LIMIT ?
            `, [userUuid, limit]);
            
            return rows;
        } finally {
            connection.release();
        }
    }

    async bulkInsertMetrics(metricsData) {
        if (!metricsData || metricsData.length === 0) {
            return;
        }

        const connection = await this.pool.getConnection();
        
        try {
            const values = metricsData.map(metric => [
                metric.timestamp || new Date(),
                metric.device_id,
                metric.metric_name,
                metric.value,
                JSON.stringify(metric.tags || {}),
                metric.region || 'default'
            ]);

            await connection.query(
                'INSERT INTO metrics (timestamp, device_id, metric_name, value, tags, region) VALUES ?',
                [values]
            );
        } finally {
            connection.release();
        }
    }

    async executeAnalyticalQuery(query, params = []) {
        const connection = await this.pool.getConnection();
        
        try {
            // Force TiFlash usage for analytical queries
            await connection.execute("SET @@tidb_isolation_read_engines = 'tiflash'");
            const [rows] = await connection.execute(query, params);
            await connection.execute("SET @@tidb_isolation_read_engines = 'tikv,tiflash'");
            return rows;
        } finally {
            connection.release();
        }
    }

    async getClusterInfo() {
        const connection = await this.pool.getConnection();
        
        try {
            const [stores] = await connection.execute(`
                SELECT STORE_ID, ADDRESS, STATE, LABEL 
                FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS
            `);
            
            const [regions] = await connection.execute(`
                SELECT REGION_ID, START_KEY, END_KEY, LEADER_STORE_ID, PEERS
                FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS
                LIMIT 10
            `);
            
            return { stores, regions };
        } finally {
            connection.release();
        }
    }

    async close() {
        await this.pool.end();
    }
}

// Analytics helper class
class TiDBAnalytics {
    constructor(client) {
        this.client = client;
    }

    async getDailyReport(date, region = null) {
        let query = `
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[orders, users]) */
                COUNT(*) as total_orders,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers,
                MAX(total_amount) as max_order_value,
                MIN(total_amount) as min_order_value
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE DATE(o.created_at) = ?
        `;
        
        const params = [date];
        if (region) {
            query += ' AND o.region = ?';
            params.push(region);
        }
        
        const results = await this.client.executeAnalyticalQuery(query, params);
        return results[0] || {};
    }

    async getRegionalPerformance(startDate, endDate) {
        const query = `
            SELECT /*+ READ_FROM_STORAGE(TIFLASH[orders]) */
                region,
                COUNT(*) as order_count,
                SUM(total_amount) as revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers
            FROM orders
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY region
            ORDER BY revenue DESC
        `;
        
        return await this.client.executeAnalyticalQuery(query, [startDate, endDate]);
    }
}

// Usage example
async function example() {
    const client = new TiDBClient({
        host: 'localhost',
        port: 4000,
        user: 'root',
        database: 'ecommerce'
    });

    try {
        // Create user and order
        const userUuid = await client.createUser('user@example.com', 'John Doe', 'us-west-1');
        const orderUuid = await client.createOrder(userUuid, 99.99, 'us-west-1');
        
        console.log('Created user:', userUuid);
        console.log('Created order:', orderUuid);

        // Bulk insert metrics
        const metrics = Array.from({ length: 1000 }, (_, i) => ({
            timestamp: new Date(),
            device_id: `device_${i % 100}`,
            metric_name: 'cpu_usage',
            value: Math.random() * 100,
            tags: { env: 'production', datacenter: 'us-west-1' },
            region: 'us-west-1'
        }));
        
        await client.bulkInsertMetrics(metrics);
        console.log('Inserted metrics:', metrics.length);

        // Analytics
        const analytics = new TiDBAnalytics(client);
        const dailyReport = await analytics.getDailyReport('2024-01-15');
        console.log('Daily report:', dailyReport);

        // Cluster info
        const clusterInfo = await client.getClusterInfo();
        console.log('Cluster stores:', clusterInfo.stores.length);

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await client.close();
    }
}

module.exports = { TiDBClient, TiDBAnalytics };
```

## Performance Monitoring

### Cluster Health Monitoring
```sql
-- Check TiKV store status
SELECT STORE_ID, ADDRESS, STATE, CAPACITY, AVAILABLE, LEADER_COUNT, REGION_COUNT
FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS;

-- Check TiFlash replica status
SELECT TABLE_SCHEMA, TABLE_NAME, REPLICA_COUNT, LOCATION_LABELS, AVAILABLE, PROGRESS
FROM INFORMATION_SCHEMA.TIFLASH_REPLICA;

-- Monitor slow queries
SELECT QUERY_TIME, QUERY, DB, INDEX_NAMES, STATS, PLAN_DIGEST
FROM INFORMATION_SCHEMA.SLOW_QUERY
WHERE TIME >= NOW() - INTERVAL 1 HOUR
ORDER BY QUERY_TIME DESC
LIMIT 10;

-- Check region distribution
SELECT STORE_ID, COUNT(*) as REGION_COUNT, 
       SUM(APPROXIMATE_SIZE) as TOTAL_SIZE_MB,
       AVG(APPROXIMATE_SIZE) as AVG_REGION_SIZE_MB
FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS
GROUP BY STORE_ID
ORDER BY REGION_COUNT DESC;
```

### Performance Optimization
```python
def monitor_tidb_performance(client):
    """Monitor TiDB cluster performance"""
    
    # Check slow queries
    slow_queries = client.execute_analytical_query("""
        SELECT 
            QUERY_TIME,
            QUERY,
            DB,
            PARSE_TIME,
            COMPILE_TIME,
            PROCESS_TIME,
            INDEX_NAMES,
            STATS
        FROM INFORMATION_SCHEMA.SLOW_QUERY
        WHERE TIME >= NOW() - INTERVAL 1 HOUR
          AND QUERY_TIME > 1
        ORDER BY QUERY_TIME DESC
        LIMIT 20
    """)
    
    # Check TiKV store status
    store_status = client.execute_analytical_query("""
        SELECT 
            STORE_ID,
            ADDRESS,
            STATE,
            CAPACITY,
            AVAILABLE,
            LEADER_COUNT,
            REGION_COUNT,
            (CAPACITY - AVAILABLE) / CAPACITY * 100 as USAGE_PERCENT
        FROM INFORMATION_SCHEMA.TIKV_STORE_STATUS
        ORDER BY USAGE_PERCENT DESC
    """)
    
    # Check hotspot regions
    hot_regions = client.execute_analytical_query("""
        SELECT 
            REGION_ID,
            STORE_ID,
            DB_NAME,
            TABLE_NAME,
            HOT_DEGREE,
            HOT_TYPE,
            READ_BYTES,
            READ_KEYS,
            WRITE_BYTES,
            WRITE_KEYS
        FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS
        WHERE HOT_DEGREE > 0
        ORDER BY HOT_DEGREE DESC
        LIMIT 10
    """)
    
    return {
        'slow_queries': slow_queries,
        'store_status': store_status,
        'hot_regions': hot_regions
    }
```

## Backup and Disaster Recovery

### BR (Backup & Restore) Setup
```bash
#!/bin/bash
# TiDB backup script using BR

# Configuration
TIDB_HOST="127.0.0.1:2379"  # PD endpoint
BACKUP_STORAGE="s3://tidb-backups"
DATABASE="ecommerce"
DATE=$(date +%Y%m%d_%H%M%S)

# Full backup
tiup br backup full \
  --pd $TIDB_HOST \
  --storage "$BACKUP_STORAGE/full/$DATE" \
  --log-level info

# Database-specific backup
tiup br backup db \
  --pd $TIDB_HOST \
  --db $DATABASE \
  --storage "$BACKUP_STORAGE/db/$DATABASE/$DATE" \
  --log-level info

# Table-specific backup
tiup br backup table \
  --pd $TIDB_HOST \
  --db $DATABASE \
  --table orders \
  --storage "$BACKUP_STORAGE/table/$DATABASE.orders/$DATE" \
  --log-level info

echo "Backup completed: $DATE"
```

### Point-in-Time Recovery
```bash
# Restore full cluster
tiup br restore full \
  --pd "127.0.0.1:2379" \
  --storage "s3://tidb-backups/full/20240115_120000"

# Restore specific database
tiup br restore db \
  --pd "127.0.0.1:2379" \
  --db ecommerce \
  --storage "s3://tidb-backups/db/ecommerce/20240115_120000"

# Restore to specific timestamp
tiup br restore full \
  --pd "127.0.0.1:2379" \
  --storage "s3://tidb-backups/full/20240115_120000" \
  --restored-ts "404198278510403585"  # TSO from SHOW MASTER STATUS
```

## Best Practices

### Schema Design Optimization
```sql
-- Use AUTO_RANDOM for high-write tables
CREATE TABLE high_write_table (
    id BIGINT AUTO_RANDOM PRIMARY KEY,
    data VARCHAR(1000)
) SHARD_ROW_ID_BITS = 4;

-- Avoid hotspots with proper shard key selection
CREATE TABLE time_series_data (
    id BIGINT AUTO_INCREMENT,
    shard_key VARCHAR(32) GENERATED ALWAYS AS (SHA1(device_id)) STORED,
    device_id VARCHAR(100),
    timestamp TIMESTAMP,
    value DOUBLE,
    PRIMARY KEY (shard_key, id),
    INDEX idx_device_time (device_id, timestamp)
) SHARD_ROW_ID_BITS = 4;

-- Use appropriate data types
CREATE TABLE optimized_table (
    id BIGINT AUTO_RANDOM PRIMARY KEY,
    status TINYINT NOT NULL,           -- Use TINYINT for small enums
    amount DECIMAL(10,2) NOT NULL,     -- DECIMAL for currency
    data JSON,                         -- JSON for flexible data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    region VARCHAR(50) NOT NULL,
    INDEX idx_status_region (status, region),
    INDEX idx_created_region (created_at, region)
) SHARD_ROW_ID_BITS = 4;
```

### Query Optimization
```sql
-- Use EXPLAIN to analyze query plans
EXPLAIN FORMAT='ROW' SELECT * FROM orders o 
JOIN users u ON o.user_id = u.id 
WHERE u.region = 'us-west-1' 
  AND o.created_at > '2024-01-01';

-- Use hints for OLAP queries
SELECT /*+ READ_FROM_STORAGE(TIFLASH[orders]) */
    region, COUNT(*), SUM(total_amount)
FROM orders 
WHERE created_at >= '2024-01-01'
GROUP BY region;

-- Avoid unnecessary ORDER BY on large datasets
SELECT * FROM orders 
WHERE region = 'us-west-1' 
  AND status = 'pending'
LIMIT 100;  -- Without ORDER BY for better performance
```

## Resources

- [TiDB Documentation](https://docs.pingcap.com/tidb/stable)
- [TiDB Best Practices](https://docs.pingcap.com/tidb/stable/tidb-best-practices)
- [Performance Tuning Guide](https://docs.pingcap.com/tidb/stable/performance-tuning-overview)
- [TiDB Operator Documentation](https://docs.pingcap.com/tidb-in-kubernetes/stable)
- [Backup and Restore Guide](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)
- [TiFlash Documentation](https://docs.pingcap.com/tidb/stable/tiflash-overview)
- [TiDB University](https://university.pingcap.com/)
- [Community Forum](https://asktug.com/)
- [GitHub Repository](https://github.com/pingcap/tidb)
- [MySQL Compatibility](https://docs.pingcap.com/tidb/stable/mysql-compatibility)