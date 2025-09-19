# CockroachDB

CockroachDB is a distributed SQL database that provides horizontal scaling, strong consistency, and survivability with PostgreSQL-compatible SQL interface.

## Installation

### Docker
```bash
# Single node for development
docker run -d --name cockroachdb \
  -p 26257:26257 \
  -p 8080:8080 \
  cockroachdb/cockroach:latest \
  start-single-node --insecure

# Access the web UI at http://localhost:8080
# Connect to SQL shell
docker exec -it cockroachdb cockroach sql --insecure
```

### Kubernetes Cluster
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cockroachdb-config
data:
  init.sql: |
    CREATE DATABASE platform_db;
    CREATE USER platform_user;
    GRANT ALL ON DATABASE platform_db TO platform_user;
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cockroachdb
spec:
  serviceName: cockroachdb
  replicas: 3
  selector:
    matchLabels:
      app: cockroachdb
  template:
    metadata:
      labels:
        app: cockroachdb
    spec:
      containers:
      - name: cockroachdb
        image: cockroachdb/cockroach:latest
        ports:
        - containerPort: 26257
          name: grpc
        - containerPort: 8080
          name: http
        command:
        - "/cockroach/cockroach"
        - "start"
        - "--logtostderr"
        - "--insecure"
        - "--store=path=/cockroach/cockroach-data"
        - "--listen-addr=0.0.0.0:26257"
        - "--http-addr=0.0.0.0:8080"
        - "--join=cockroachdb-0.cockroachdb:26257,cockroachdb-1.cockroachdb:26257,cockroachdb-2.cockroachdb:26257"
        env:
        - name: COCKROACH_CHANNEL
          value: kubernetes-insecure
        volumeMounts:
        - name: datadir
          mountPath: /cockroach/cockroach-data
        - name: config
          mountPath: /cockroach/init.sql
          subPath: init.sql
      volumes:
      - name: config
        configMap:
          name: cockroachdb-config
  volumeClaimTemplates:
  - metadata:
      name: datadir
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
---
apiVersion: v1
kind: Service
metadata:
  name: cockroachdb
spec:
  ports:
  - port: 26257
    targetPort: 26257
    name: grpc
  - port: 8080
    targetPort: 8080
    name: http
  selector:
    app: cockroachdb
  clusterIP: None
---
apiVersion: v1
kind: Service
metadata:
  name: cockroachdb-public
spec:
  ports:
  - port: 26257
    targetPort: 26257
    name: grpc
  - port: 8080
    targetPort: 8080
    name: http
  selector:
    app: cockroachdb
  type: LoadBalancer
```

## Database Setup

### Cluster Initialization
```sql
-- Initialize the cluster (run once)
COCKROACH init --insecure --host=localhost:26257

-- Create database and users
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE USER app_user;
CREATE USER readonly_user;

GRANT ALL ON DATABASE ecommerce TO app_user;
GRANT SELECT ON DATABASE ecommerce TO readonly_user;

-- Create tables with proper distribution
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email STRING UNIQUE NOT NULL,
    name STRING NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    region STRING NOT NULL,
    INDEX idx_users_region (region, created_at),
    INDEX idx_users_email (email)
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status STRING NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    region STRING NOT NULL,
    INDEX idx_orders_user_id (user_id, created_at),
    INDEX idx_orders_status (status, created_at),
    INDEX idx_orders_region (region, created_at)
);

-- Partition tables by region for better distribution
ALTER TABLE users PARTITION BY LIST (region) (
    PARTITION us_east VALUES IN ('us-east-1', 'us-east-2'),
    PARTITION us_west VALUES IN ('us-west-1', 'us-west-2'),
    PARTITION eu VALUES IN ('eu-west-1', 'eu-central-1'),
    PARTITION default VALUES IN (DEFAULT)
);

ALTER TABLE orders PARTITION BY LIST (region) (
    PARTITION us_east VALUES IN ('us-east-1', 'us-east-2'),
    PARTITION us_west VALUES IN ('us-west-1', 'us-west-2'),
    PARTITION eu VALUES IN ('eu-west-1', 'eu-central-1'),
    PARTITION default VALUES IN (DEFAULT)
);
```

### Advanced Schema Design
```sql
-- Time-series data with automatic partitioning
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL,
    device_id STRING NOT NULL,
    metric_name STRING NOT NULL,
    value FLOAT NOT NULL,
    tags JSONB,
    region STRING NOT NULL,
    INDEX idx_metrics_device_time (device_id, timestamp DESC),
    INDEX idx_metrics_name_time (metric_name, timestamp DESC),
    INVERTED INDEX idx_metrics_tags (tags)
) PARTITION BY RANGE (timestamp) (
    PARTITION p2024_01 VALUES FROM ('2024-01-01') TO ('2024-02-01'),
    PARTITION p2024_02 VALUES FROM ('2024-02-01') TO ('2024-03-01'),
    PARTITION p2024_03 VALUES FROM ('2024-03-01') TO ('2024-04-01')
);

-- Materialized view for real-time analytics
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT 
    date_trunc('hour', timestamp) as hour,
    device_id,
    metric_name,
    avg(value) as avg_value,
    max(value) as max_value,
    min(value) as min_value,
    count(*) as count
FROM metrics
GROUP BY hour, device_id, metric_name;

-- Refresh materialized view automatically
CREATE SCHEDULE hourly_refresh_job
FOR 'REFRESH MATERIALIZED VIEW hourly_metrics'
RECURRING '@hourly';
```

## Python Integration

### Connection and ORM
```python
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from sqlalchemy import create_engine, Column, String, DateTime, Numeric, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from contextlib import contextmanager

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    region = Column(String, nullable=False)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    region = Column(String, nullable=False)

class CockroachDBClient:
    def __init__(self, connection_string, pool_size=10):
        self.engine = create_engine(
            connection_string,
            pool_size=pool_size,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={
                "application_name": "platform-app",
                "sslmode": "disable"  # Use "require" in production
            }
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def create_user(self, email, name, region):
        with self.get_session() as session:
            user = User(email=email, name=name, region=region)
            session.add(user)
            session.flush()
            return user.id
            
    def create_order(self, user_id, total_amount, region, status='pending'):
        with self.get_session() as session:
            order = Order(
                user_id=user_id,
                total_amount=total_amount,
                region=region,
                status=status
            )
            session.add(order)
            session.flush()
            return order.id
            
    def get_user_orders(self, user_id, limit=10):
        with self.get_session() as session:
            orders = session.query(Order)\
                .filter(Order.user_id == user_id)\
                .order_by(Order.created_at.desc())\
                .limit(limit)\
                .all()
            return [(str(o.id), o.total_amount, o.status, o.created_at) for o in orders]
            
    def execute_transaction(self, operations):
        """Execute multiple operations in a single transaction with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                with self.get_session() as session:
                    results = []
                    for operation in operations:
                        result = operation(session)
                        results.append(result)
                    return results
            except Exception as e:
                if "restart transaction" in str(e) and attempt < max_retries - 1:
                    continue  # Retry on serialization error
                raise e

# Usage example
client = CockroachDBClient("postgresql://root@localhost:26257/ecommerce")

# Create user and order in transaction
def create_user_and_order_ops(email, name, region, amount):
    def create_user_op(session):
        user = User(email=email, name=name, region=region)
        session.add(user)
        session.flush()
        return user.id
        
    def create_order_op(session):
        # This assumes user_id is available from previous operation
        # In practice, you'd need to handle this dependency
        order = Order(user_id=user_id, total_amount=amount, region=region)
        session.add(order)
        session.flush()
        return order.id
    
    return [create_user_op, create_order_op]

# Execute transaction
results = client.execute_transaction(
    create_user_and_order_ops("user@example.com", "John Doe", "us-east-1", 99.99)
)
```

### Advanced Queries and Analytics
```python
class CockroachAnalytics:
    def __init__(self, client):
        self.client = client
        
    def get_regional_metrics(self, start_date, end_date):
        """Get order metrics by region with window functions"""
        query = text("""
            SELECT 
                region,
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_order_value,
                LAG(COUNT(*)) OVER (PARTITION BY region ORDER BY DATE_TRUNC('day', created_at)) as prev_day_orders
            FROM orders 
            WHERE created_at BETWEEN :start_date AND :end_date
            GROUP BY region, DATE_TRUNC('day', created_at)
            ORDER BY region, DATE_TRUNC('day', created_at)
        """)
        
        with self.client.get_session() as session:
            result = session.execute(query, {
                'start_date': start_date,
                'end_date': end_date
            })
            return [dict(row) for row in result]
            
    def get_user_cohort_analysis(self, cohort_month):
        """Perform cohort analysis for user retention"""
        query = text("""
            WITH cohort_data AS (
                SELECT 
                    u.id as user_id,
                    DATE_TRUNC('month', u.created_at) as cohort_month,
                    DATE_TRUNC('month', o.created_at) as order_month,
                    EXTRACT(MONTH FROM AGE(o.created_at, u.created_at)) as month_number
                FROM users u
                JOIN orders o ON u.id = o.user_id
                WHERE DATE_TRUNC('month', u.created_at) = :cohort_month
            ),
            cohort_sizes AS (
                SELECT 
                    cohort_month,
                    COUNT(DISTINCT user_id) as cohort_size
                FROM cohort_data
                GROUP BY cohort_month
            )
            SELECT 
                cd.month_number,
                COUNT(DISTINCT cd.user_id) as active_users,
                cs.cohort_size,
                ROUND(COUNT(DISTINCT cd.user_id)::FLOAT / cs.cohort_size * 100, 2) as retention_rate
            FROM cohort_data cd
            JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
            GROUP BY cd.month_number, cs.cohort_size
            ORDER BY cd.month_number
        """)
        
        with self.client.get_session() as session:
            result = session.execute(query, {'cohort_month': cohort_month})
            return [dict(row) for row in result]

analytics = CockroachAnalytics(client)
```

## Node.js Integration

### Connection and Basic Operations
```javascript
const { Pool } = require('pg');
const { v4: uuidv4 } = require('uuid');

class CockroachDBClient {
    constructor(config = {}) {
        this.pool = new Pool({
            user: config.user || 'root',
            host: config.host || 'localhost',
            database: config.database || 'ecommerce',
            password: config.password || '',
            port: config.port || 26257,
            max: config.maxConnections || 20,
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 5000,
            ssl: config.ssl || false,
            application_name: config.applicationName || 'platform-app'
        });
    }

    async createUser(email, name, region) {
        const id = uuidv4();
        const query = `
            INSERT INTO users (id, email, name, region, created_at, updated_at)
            VALUES ($1, $2, $3, $4, NOW(), NOW())
            RETURNING id
        `;
        
        try {
            const result = await this.pool.query(query, [id, email, name, region]);
            return result.rows[0].id;
        } catch (error) {
            console.error('Error creating user:', error);
            throw error;
        }
    }

    async createOrder(userId, totalAmount, region, status = 'pending') {
        const id = uuidv4();
        const query = `
            INSERT INTO orders (id, user_id, total_amount, status, region, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            RETURNING id
        `;
        
        try {
            const result = await this.pool.query(query, [id, userId, totalAmount, status, region]);
            return result.rows[0].id;
        } catch (error) {
            console.error('Error creating order:', error);
            throw error;
        }
    }

    async getUserOrders(userId, limit = 10) {
        const query = `
            SELECT id, total_amount, status, created_at
            FROM orders 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2
        `;
        
        try {
            const result = await this.pool.query(query, [userId, limit]);
            return result.rows;
        } catch (error) {
            console.error('Error fetching user orders:', error);
            throw error;
        }
    }

    async executeTransaction(operations, maxRetries = 3) {
        for (let attempt = 0; attempt < maxRetries; attempt++) {
            const client = await this.pool.connect();
            
            try {
                await client.query('BEGIN');
                
                const results = [];
                for (const operation of operations) {
                    const result = await operation(client);
                    results.push(result);
                }
                
                await client.query('COMMIT');
                return results;
                
            } catch (error) {
                await client.query('ROLLBACK');
                
                // Retry on serialization errors
                if (error.message.includes('restart transaction') && attempt < maxRetries - 1) {
                    console.log(`Transaction retry ${attempt + 1}/${maxRetries}`);
                    continue;
                }
                
                throw error;
            } finally {
                client.release();
            }
        }
    }

    async getClusterStatus() {
        const query = 'SELECT node_id, address, sql_address, build, started_at FROM crdb_internal.cluster_nodes';
        
        try {
            const result = await this.pool.query(query);
            return result.rows;
        } catch (error) {
            console.error('Error fetching cluster status:', error);
            throw error;
        }
    }

    async close() {
        await this.pool.end();
    }
}

// Usage example
async function example() {
    const client = new CockroachDBClient();

    try {
        // Create user and order in transaction
        const results = await client.executeTransaction([
            async (txClient) => {
                const userResult = await txClient.query(
                    'INSERT INTO users (id, email, name, region) VALUES ($1, $2, $3, $4) RETURNING id',
                    [uuidv4(), 'user@example.com', 'John Doe', 'us-east-1']
                );
                return userResult.rows[0].id;
            },
            async (txClient) => {
                // Use the user ID from the first operation
                const orderResult = await txClient.query(
                    'INSERT INTO orders (id, user_id, total_amount, region) VALUES ($1, $2, $3, $4) RETURNING id',
                    [uuidv4(), results[0], 99.99, 'us-east-1']
                );
                return orderResult.rows[0].id;
            }
        ]);

        console.log('Created user and order:', results);

        // Check cluster status
        const clusterStatus = await client.getClusterStatus();
        console.log('Cluster nodes:', clusterStatus);

    } catch (error) {
        console.error('Example error:', error);
    } finally {
        await client.close();
    }
}

module.exports = CockroachDBClient;
```

## Performance Monitoring

### Cluster Health Checks
```sql
-- Check cluster status
SELECT node_id, address, build, started_at, updated_at 
FROM crdb_internal.cluster_nodes;

-- Check database sizes
SELECT 
    database_name,
    owner,
    primary_region,
    regions,
    survival_goal
FROM [SHOW DATABASES];

-- Check table statistics
SELECT 
    table_name,
    estimated_row_count,
    range_count,
    approximate_disk_bytes
FROM crdb_internal.table_row_statistics
WHERE database_name = 'ecommerce';

-- Monitor slow queries
SELECT 
    query,
    exec_count,
    avg_exec_time,
    max_exec_time,
    avg_rows_read,
    max_rows_read
FROM crdb_internal.statement_statistics
WHERE avg_exec_time > INTERVAL '1 second'
ORDER BY avg_exec_time DESC
LIMIT 10;
```

### Performance Optimization
```python
class CockroachMonitoring:
    def __init__(self, client):
        self.client = client
        
    def check_cluster_health(self):
        """Check overall cluster health"""
        with self.client.get_session() as session:
            # Node status
            nodes = session.execute(text("""
                SELECT node_id, address, sql_address, build, started_at, updated_at,
                       live_bytes, key_bytes, val_bytes, range_count
                FROM crdb_internal.cluster_nodes
            """)).fetchall()
            
            # Range distribution
            ranges = session.execute(text("""
                SELECT store_id, node_id, range_count, live_bytes, key_bytes, val_bytes
                FROM crdb_internal.cluster_stores
            """)).fetchall()
            
            return {
                'nodes': [dict(node) for node in nodes],
                'stores': [dict(store) for store in ranges]
            }
            
    def analyze_query_performance(self, min_exec_time='1 second'):
        """Analyze slow queries"""
        with self.client.get_session() as session:
            slow_queries = session.execute(text("""
                SELECT 
                    fingerprint_id,
                    query,
                    plan_gist,
                    exec_count,
                    avg_exec_time,
                    max_exec_time,
                    avg_rows_read,
                    max_rows_read,
                    avg_bytes_read,
                    max_bytes_read
                FROM crdb_internal.statement_statistics
                WHERE avg_exec_time > INTERVAL :min_time
                ORDER BY avg_exec_time DESC
                LIMIT 20
            """), {'min_time': min_exec_time}).fetchall()
            
            return [dict(query) for query in slow_queries]
            
    def check_replication_status(self):
        """Check replication and range distribution"""
        with self.client.get_session() as session:
            replication = session.execute(text("""
                SELECT 
                    range_id,
                    start_key,
                    end_key,
                    replicas,
                    learner_replicas,
                    split_enforced_until
                FROM crdb_internal.ranges_no_leases
                WHERE database_name = 'ecommerce'
                ORDER BY range_id
                LIMIT 50
            """)).fetchall()
            
            return [dict(r) for r in replication]

monitor = CockroachMonitoring(client)
health_status = monitor.check_cluster_health()
performance_report = monitor.analyze_query_performance()
```

## Backup and Recovery

### Automated Backup
```bash
#!/bin/bash
# CockroachDB backup script

CLUSTER_HOST="localhost:26257"
BACKUP_LOCATION="s3://your-backup-bucket/cockroachdb"
DATABASE="ecommerce"
DATE=$(date +%Y%m%d_%H%M%S)

# Full database backup
cockroach sql --insecure --host=$CLUSTER_HOST --execute="
BACKUP DATABASE $DATABASE TO '$BACKUP_LOCATION/full/$DATE' 
WITH REVISION_HISTORY;
"

# Incremental backup (daily)
cockroach sql --insecure --host=$CLUSTER_HOST --execute="
BACKUP DATABASE $DATABASE TO '$BACKUP_LOCATION/incremental/$DATE' 
AS OF SYSTEM TIME '-1m'
INCREMENTAL FROM LATEST IN '$BACKUP_LOCATION/full'
WITH REVISION_HISTORY;
"

echo "Backup completed: $DATE"
```

### Disaster Recovery
```sql
-- Restore from backup
RESTORE DATABASE ecommerce FROM 'gs://backup-bucket/full/20240101_120000'
WITH SKIP_MISSING_FOREIGN_KEYS;

-- Point-in-time restore
RESTORE DATABASE ecommerce FROM 'gs://backup-bucket/full/20240101_120000'
AS OF SYSTEM TIME '2024-01-01 14:30:00+00:00';

-- Restore specific tables
RESTORE TABLE ecommerce.users, ecommerce.orders 
FROM 'gs://backup-bucket/full/20240101_120000';
```

## Best Practices

### Schema Design
```sql
-- Use UUIDs for distributed primary keys
CREATE TABLE distributed_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- other columns
);

-- Partition large tables by region or time
ALTER TABLE events PARTITION BY LIST (region) (
    PARTITION us VALUES IN ('us-east', 'us-west'),
    PARTITION eu VALUES IN ('eu-west', 'eu-central')
);

-- Use appropriate data types
CREATE TABLE optimized_table (
    id UUID PRIMARY KEY,
    status STRING(20) NOT NULL,  -- Fixed length for enums
    amount DECIMAL(10,2),        -- Precise for money
    data JSONB,                  -- Use JSONB for semi-structured data
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Query Optimization
```sql
-- Use EXPLAIN to understand query plans
EXPLAIN (ANALYZE, DISTSQL) 
SELECT * FROM orders o 
JOIN users u ON o.user_id = u.id 
WHERE u.region = 'us-east-1' 
  AND o.created_at > NOW() - INTERVAL '7 days';

-- Create covering indexes for common queries
CREATE INDEX idx_orders_covering ON orders (user_id, created_at DESC) 
STORING (total_amount, status);

-- Use window functions for analytics
SELECT 
    user_id,
    total_amount,
    SUM(total_amount) OVER (PARTITION BY user_id ORDER BY created_at) as running_total
FROM orders;
```

## Resources

- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
- [SQL Performance Best Practices](https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview.html)
- [Multi-Region Configuration](https://www.cockroachlabs.com/docs/stable/multiregion-overview.html)
- [Production Deployment](https://www.cockroachlabs.com/docs/stable/deploy-cockroachdb-on-premises.html)
- [Backup and Restore](https://www.cockroachlabs.com/docs/stable/backup-and-restore-overview.html)
- [Monitoring and Alerting](https://www.cockroachlabs.com/docs/stable/monitoring-and-alerting.html)
- [CockroachDB University](https://university.cockroachlabs.com/)
- [Community Forum](https://forum.cockroachlabs.com/)
- [GitHub Repository](https://github.com/cockroachdb/cockroach)
- [Python Driver Documentation](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html)