# YugabyteDB

YugabyteDB is a distributed SQL database that provides PostgreSQL compatibility, horizontal scaling, and multi-region deployment capabilities.

## Installation

### Docker
```bash
# Single node for development
docker run -d --name yugabyte \
  -p 7000:7000 \
  -p 9000:9000 \
  -p 5433:5433 \
  yugabytedb/yugabyte:latest \
  bin/yugabyted start --daemon=false

# Access web UI at http://localhost:7000
# Connect to YSQL (PostgreSQL API)
docker exec -it yugabyte ysqlsh -h localhost
```

### Kubernetes with Helm
```yaml
# values.yaml for YugabyteDB Helm chart
Image:
  repository: yugabytedb/yugabyte
  tag: "2.20.0.0-b76"
  pullPolicy: IfNotPresent

replicas:
  master: 3
  tserver: 3

resource:
  master:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 1000m
      memory: 2Gi
  tserver:
    requests:
      cpu: 1000m
      memory: 2Gi
    limits:
      cpu: 2000m
      memory: 4Gi

storage:
  master:
    count: 1
    size: 10Gi
    storageClass: ssd
  tserver:
    count: 1
    size: 100Gi
    storageClass: ssd

gflags:
  master:
    max_clock_skew_usec: 200000
    default_memory_limit_to_ram_ratio: 0.85
  tserver:
    max_clock_skew_usec: 200000
    memory_limit_hard_bytes: 3221225472
    default_memory_limit_to_ram_ratio: 0.85

enableLoadBalancer: true

partition_fault_tolerance: zone
```

```bash
# Install YugabyteDB with Helm
helm repo add yugabytedb https://charts.yugabyte.com
helm repo update
helm install yugabyte yugabytedb/yugabyte -f values.yaml
```

### Multi-Region Kubernetes Setup
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: yugabyte
---
apiVersion: yugabyte.com/v1alpha1
kind: YBCluster
metadata:
  name: yugabyte-cluster
  namespace: yugabyte
spec:
  image:
    repository: yugabytedb/yugabyte
    tag: "2.20.0.0-b76"
    pullPolicy: IfNotPresent

  replicationFactor: 3
  enableTLS: false

  master:
    replicas: 3
    masterGFlags:
      max_clock_skew_usec: "200000"
      default_memory_limit_to_ram_ratio: "0.85"
      placement_region: us-west
      placement_zone: us-west-1a,us-west-1b,us-west-1c
    storage:
      count: 1
      size: 10Gi
      storageClass: fast-ssd
    resources:
      requests:
        cpu: 500m
        memory: 1Gi

  tserver:
    replicas: 3
    tserverGFlags:
      max_clock_skew_usec: "200000"
      memory_limit_hard_bytes: "3221225472"
      placement_region: us-west
      placement_zone: us-west-1a,us-west-1b,us-west-1c
    storage:
      count: 1
      size: 100Gi
      storageClass: fast-ssd
    resources:
      requests:
        cpu: 1000m
        memory: 2Gi

  zones:
  - name: us-west-1a
    replicaCount: 1
  - name: us-west-1b
    replicaCount: 1
  - name: us-west-1c
    replicaCount: 1
---
apiVersion: v1
kind: Service
metadata:
  name: yugabyte-ui
  namespace: yugabyte
spec:
  selector:
    app: yb-master
  ports:
  - port: 7000
    targetPort: 7000
    name: ui
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  name: yugabyte-ysql
  namespace: yugabyte
spec:
  selector:
    app: yb-tserver
  ports:
  - port: 5433
    targetPort: 5433
    name: ysql
  type: LoadBalancer
```

## Database Setup

### Initial Configuration
```sql
-- Connect using psql
psql -h localhost -p 5433 -U yugabyte -d yugabyte

-- Create database and user
CREATE DATABASE ecommerce;
\c ecommerce;

CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO app_user;

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables with optimal distribution
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for regional queries
CREATE INDEX idx_users_region_created ON users(region, created_at);
CREATE INDEX idx_users_email ON users(email);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for common query patterns
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);
CREATE INDEX idx_orders_region_created ON orders(region, created_at DESC);

-- Create a covering index for analytical queries
CREATE INDEX idx_orders_analytics ON orders(region, status, created_at) 
INCLUDE (total_amount, user_id);
```

### Advanced Schema with Row-Level Geography
```sql
-- Create geo-partitioned table for global applications
CREATE TABLE global_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency CHAR(3) NOT NULL,
    region VARCHAR(50) NOT NULL,
    country_code CHAR(2) NOT NULL,
    transaction_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY LIST (region);

-- Create regional partitions
CREATE TABLE global_transactions_us PARTITION OF global_transactions
FOR VALUES IN ('us-east-1', 'us-west-1', 'us-central-1');

CREATE TABLE global_transactions_eu PARTITION OF global_transactions  
FOR VALUES IN ('eu-west-1', 'eu-central-1', 'eu-north-1');

CREATE TABLE global_transactions_asia PARTITION OF global_transactions
FOR VALUES IN ('ap-south-1', 'ap-southeast-1', 'ap-northeast-1');

-- Create time-series table with automatic partitioning
CREATE TABLE metrics (
    id UUID DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    tags JSONB,
    region VARCHAR(50) NOT NULL,
    PRIMARY KEY (region, timestamp, id)
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE metrics_2024_01 PARTITION OF metrics
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE metrics_2024_02 PARTITION OF metrics
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add tablet splitting for high-write tables
ALTER TABLE metrics SPLIT AT VALUES (('us-east-1', '2024-01-15'), ('us-west-1', '2024-01-15'));

-- Create materialized view for real-time analytics
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT 
    date_trunc('hour', timestamp) as hour,
    region,
    device_id,
    metric_name,
    avg(value) as avg_value,
    max(value) as max_value,
    min(value) as min_value,
    count(*) as data_points
FROM metrics
GROUP BY hour, region, device_id, metric_name;

-- Create unique index on materialized view
CREATE UNIQUE INDEX idx_hourly_metrics_unique 
ON hourly_metrics(hour, region, device_id, metric_name);
```

## Python Integration

### Connection and ORM Setup
```python
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, Column, String, DateTime, Numeric, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timedelta
from contextlib import contextmanager
import json

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    region = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='pending')
    region = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class YugabyteDBClient:
    def __init__(self, connection_string, pool_size=10):
        # For SQLAlchemy ORM
        self.engine = create_engine(
            connection_string,
            pool_size=pool_size,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={
                "application_name": "platform-app",
                "connect_timeout": 10,
                "options": "-c default_transaction_isolation=repeatable_read"
            }
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # For raw connections
        self.connection_pool = ThreadedConnectionPool(
            minconn=5,
            maxconn=pool_size,
            dsn=connection_string
        )
        
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
            
    @contextmanager
    def get_connection(self):
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
            
    def create_user(self, email, name, region):
        with self.get_session() as session:
            user = User(email=email, name=name, region=region)
            session.add(user)
            session.flush()
            return str(user.id)
            
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
            return str(order.id)
            
    def get_user_orders(self, user_id, limit=10):
        with self.get_session() as session:
            orders = session.query(Order)\
                .filter(Order.user_id == user_id)\
                .order_by(Order.created_at.desc())\
                .limit(limit)\
                .all()
            return [(str(o.id), float(o.total_amount), o.status, o.created_at) for o in orders]
            
    def bulk_insert_metrics(self, metrics_data):
        """High-performance bulk insert using COPY"""
        if not metrics_data:
            return
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Prepare data for COPY
            csv_data = []
            for metric in metrics_data:
                csv_data.append([
                    metric.get('timestamp', datetime.now()),
                    metric['device_id'],
                    metric['metric_name'],
                    metric['value'],
                    json.dumps(metric.get('tags', {})),
                    metric.get('region', 'default')
                ])
            
            # Use COPY for high-performance insert
            cursor.execute("BEGIN")
            try:
                cursor.copy_from(
                    io.StringIO('\n'.join(['\t'.join(map(str, row)) for row in csv_data])),
                    'metrics',
                    columns=('timestamp', 'device_id', 'metric_name', 'value', 'tags', 'region')
                )
                cursor.execute("COMMIT")
            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e
                
    def execute_read_replica_query(self, query, params=None):
        """Execute read queries with follower read preference"""
        with self.get_connection() as conn:
            # Set follower reads for better read performance
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SET yb_read_from_followers = true")
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.execute("SET yb_read_from_followers = false")
            return result

# Usage example
client = YugabyteDBClient("postgresql://yugabyte:@localhost:5433/ecommerce")

# Create user and order
user_id = client.create_user('user@example.com', 'John Doe', 'us-west-1')
order_id = client.create_order(user_id, 99.99, 'us-west-1')

# Bulk insert metrics for time-series data
import io
metrics = [
    {
        'timestamp': datetime.now(),
        'device_id': f'device_{i}',
        'metric_name': 'cpu_usage',
        'value': 50 + (i % 50),
        'tags': {'env': 'production', 'host': f'host_{i}'},
        'region': 'us-west-1'
    }
    for i in range(10000)
]
client.bulk_insert_metrics(metrics)
```

### Advanced Analytics and Cross-Region Queries
```python
class YugabyteAnalytics:
    def __init__(self, client):
        self.client = client
        
    def get_global_regional_metrics(self, start_date, end_date):
        """Get metrics across all regions with smart query routing"""
        query = """
            SELECT 
                region,
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_order,
                COUNT(DISTINCT user_id) as unique_customers
            FROM orders 
            WHERE created_at BETWEEN %s AND %s
            GROUP BY region
            ORDER BY total_revenue DESC
        """
        
        return self.client.execute_read_replica_query(query, (start_date, end_date))
        
    def get_real_time_dashboard_data(self, region=None):
        """Get real-time dashboard data with follower reads"""
        base_query = """
            WITH recent_orders AS (
                SELECT region, status, total_amount, created_at
                FROM orders
                WHERE created_at >= NOW() - INTERVAL '1 hour'
            ),
            hourly_stats AS (
                SELECT 
                    date_trunc('hour', created_at) as hour,
                    region,
                    COUNT(*) as orders_count,
                    SUM(total_amount) as hourly_revenue
                FROM recent_orders
                GROUP BY hour, region
            )
            SELECT 
                r.region,
                COUNT(*) as total_recent_orders,
                SUM(r.total_amount) as recent_revenue,
                AVG(r.total_amount) as avg_order_value,
                SUM(CASE WHEN r.status = 'pending' THEN 1 ELSE 0 END) as pending_orders,
                hs.hourly_revenue as last_hour_revenue
            FROM recent_orders r
            LEFT JOIN hourly_stats hs ON r.region = hs.region 
                AND hs.hour = date_trunc('hour', NOW())
            WHERE 1=1
        """
        
        params = []
        if region:
            base_query += " AND r.region = %s"
            params.append(region)
            
        base_query += " GROUP BY r.region, hs.hourly_revenue ORDER BY recent_revenue DESC"
        
        return self.client.execute_read_replica_query(base_query, params)
        
    def analyze_cross_region_performance(self, metric_name, hours=24):
        """Analyze metrics performance across regions"""
        query = """
            SELECT 
                region,
                device_id,
                AVG(value) as avg_value,
                MAX(value) as max_value,
                MIN(value) as min_value,
                STDDEV(value) as std_deviation,
                COUNT(*) as data_points,
                PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY value) as p95_value
            FROM metrics
            WHERE metric_name = %s 
              AND timestamp >= NOW() - INTERVAL '%s hours'
            GROUP BY region, device_id
            ORDER BY region, avg_value DESC
        """
        
        return self.client.execute_read_replica_query(query, (metric_name, hours))
        
    def get_user_behavior_cohort(self, cohort_month):
        """Advanced cohort analysis with window functions"""
        query = """
            WITH user_cohorts AS (
                SELECT 
                    u.id as user_id,
                    u.region,
                    date_trunc('month', u.created_at) as cohort_month,
                    date_trunc('month', o.created_at) as order_month,
                    o.total_amount,
                    ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY o.created_at) as order_sequence
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id
                WHERE date_trunc('month', u.created_at) = %s
            ),
            cohort_metrics AS (
                SELECT 
                    region,
                    cohort_month,
                    order_month,
                    COUNT(DISTINCT user_id) as active_users,
                    COUNT(user_id) as total_orders,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value,
                    COUNT(CASE WHEN order_sequence = 1 THEN 1 END) as first_orders
                FROM user_cohorts
                WHERE order_month IS NOT NULL
                GROUP BY region, cohort_month, order_month
            )
            SELECT 
                region,
                cohort_month,
                order_month,
                EXTRACT(MONTH FROM AGE(order_month, cohort_month)) as months_since_signup,
                active_users,
                total_orders,
                total_revenue,
                avg_order_value,
                first_orders,
                LAG(active_users) OVER (PARTITION BY region ORDER BY order_month) as prev_month_users
            FROM cohort_metrics
            ORDER BY region, order_month
        """
        
        return self.client.execute_read_replica_query(query, (cohort_month,))

analytics = YugabyteAnalytics(client)
regional_metrics = analytics.get_global_regional_metrics('2024-01-01', '2024-01-31')
dashboard_data = analytics.get_real_time_dashboard_data()
```

## Node.js Integration

### High-Performance Client
```javascript
const { Pool } = require('pg');
const { v4: uuidv4 } = require('uuid');
const copyFrom = require('pg-copy-streams').from;

class YugabyteDBClient {
    constructor(config = {}) {
        this.poolConfig = {
            user: config.user || 'yugabyte',
            host: config.host || 'localhost',
            database: config.database || 'ecommerce',
            password: config.password || '',
            port: config.port || 5433,
            max: config.maxConnections || 20,
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 10000,
            application_name: config.applicationName || 'platform-app',
            statement_timeout: 30000,
            query_timeout: 30000
        };
        
        this.pool = new Pool(this.poolConfig);
        
        // Separate pool for read replicas
        this.readPool = new Pool({
            ...this.poolConfig,
            max: config.readMaxConnections || 10,
            application_name: 'platform-app-read'
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
            SELECT id, total_amount, status, region, created_at
            FROM orders 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2
        `;
        
        try {
            // Use read replica for better performance
            const client = await this.readPool.connect();
            await client.query('SET yb_read_from_followers = true');
            const result = await client.query(query, [userId, limit]);
            await client.query('SET yb_read_from_followers = false');
            client.release();
            return result.rows;
        } catch (error) {
            console.error('Error fetching user orders:', error);
            throw error;
        }
    }

    async bulkInsertMetrics(metricsData) {
        if (!metricsData || metricsData.length === 0) {
            return;
        }

        const client = await this.pool.connect();
        
        try {
            await client.query('BEGIN');
            
            // Use COPY for high-performance bulk insert
            const copyQuery = `
                COPY metrics (timestamp, device_id, metric_name, value, tags, region)
                FROM STDIN WITH (FORMAT csv, DELIMITER E'\t')
            `;
            
            const stream = client.query(copyFrom(copyQuery));
            
            for (const metric of metricsData) {
                const row = [
                    metric.timestamp || new Date().toISOString(),
                    metric.device_id,
                    metric.metric_name,
                    metric.value,
                    JSON.stringify(metric.tags || {}),
                    metric.region || 'default'
                ].join('\t') + '\n';
                
                stream.write(row);
            }
            
            stream.end();
            
            await new Promise((resolve, reject) => {
                stream.on('finish', resolve);
                stream.on('error', reject);
            });
            
            await client.query('COMMIT');
            
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }

    async executeAnalyticalQuery(query, params = [], useFollowerRead = true) {
        const client = await this.readPool.connect();
        
        try {
            if (useFollowerRead) {
                await client.query('SET yb_read_from_followers = true');
            }
            
            const result = await client.query(query, params);
            
            if (useFollowerRead) {
                await client.query('SET yb_read_from_followers = false');
            }
            
            return result.rows;
        } finally {
            client.release();
        }
    }

    async getClusterStatus() {
        const query = `
            SELECT 
                host, 
                port, 
                num_sst_files, 
                num_tablets, 
                total_ram_usage,
                read_ops_per_sec,
                write_ops_per_sec
            FROM yb_servers() 
            WHERE server_type = 'tserver'
        `;
        
        try {
            const result = await this.pool.query(query);
            return result.rows;
        } catch (error) {
            console.error('Error fetching cluster status:', error);
            throw error;
        }
    }

    async optimizeTabletsForTable(tableName) {
        """Split tablets for better distribution"""
        const query = `
            SELECT yb_hash_code_for_split($1) as split_point
        `;
        
        try {
            const result = await this.pool.query(query, [tableName]);
            return result.rows;
        } catch (error) {
            console.error('Error optimizing tablets:', error);
            throw error;
        }
    }

    async close() {
        await this.pool.end();
        await this.readPool.end();
    }
}

// Analytics class for complex queries
class YugabyteAnalytics {
    constructor(client) {
        this.client = client;
    }

    async getRegionalPerformance(startDate, endDate) {
        const query = `
            SELECT 
                region,
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) as median_order
            FROM orders
            WHERE created_at BETWEEN $1 AND $2
            GROUP BY region
            ORDER BY total_revenue DESC
        `;
        
        return await this.client.executeAnalyticalQuery(query, [startDate, endDate]);
    }

    async getRealTimeMetrics(deviceId, hours = 24) {
        const query = `
            SELECT 
                metric_name,
                region,
                AVG(value) as avg_value,
                MAX(value) as max_value,
                MIN(value) as min_value,
                STDDEV(value) as std_deviation,
                COUNT(*) as data_points,
                PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY value) as p95_value
            FROM metrics
            WHERE device_id = $1 
              AND timestamp >= NOW() - INTERVAL '$2 hours'
            GROUP BY metric_name, region
            ORDER BY metric_name, region
        `;
        
        return await this.client.executeAnalyticalQuery(query, [deviceId, hours]);
    }

    async getHourlyTrends(region, days = 7) {
        const query = `
            SELECT 
                date_trunc('hour', created_at) as hour,
                COUNT(*) as order_count,
                SUM(total_amount) as hourly_revenue,
                AVG(total_amount) as avg_order_value,
                COUNT(DISTINCT user_id) as unique_customers
            FROM orders
            WHERE region = $1 
              AND created_at >= NOW() - INTERVAL '$2 days'
            GROUP BY hour
            ORDER BY hour
        `;
        
        return await this.client.executeAnalyticalQuery(query, [region, days]);
    }
}

// Usage example
async function example() {
    const client = new YugabyteDBClient({
        host: 'localhost',
        port: 5433,
        user: 'yugabyte',
        database: 'ecommerce',
        maxConnections: 20
    });

    try {
        // Create user and order
        const userId = await client.createUser('user@example.com', 'John Doe', 'us-west-1');
        const orderId = await client.createOrder(userId, 99.99, 'us-west-1');
        
        console.log('Created user:', userId);
        console.log('Created order:', orderId);

        // Bulk insert metrics
        const metrics = Array.from({ length: 10000 }, (_, i) => ({
            timestamp: new Date(),
            device_id: `device_${i % 1000}`,
            metric_name: 'cpu_usage',
            value: Math.random() * 100,
            tags: { env: 'production', datacenter: 'us-west-1' },
            region: 'us-west-1'
        }));
        
        console.time('Bulk insert');
        await client.bulkInsertMetrics(metrics);
        console.timeEnd('Bulk insert');

        // Analytics
        const analytics = new YugabyteAnalytics(client);
        const regionalPerf = await analytics.getRegionalPerformance('2024-01-01', '2024-01-31');
        console.log('Regional performance:', regionalPerf);

        // Cluster status
        const clusterStatus = await client.getClusterStatus();
        console.log('Cluster nodes:', clusterStatus.length);

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await client.close();
    }
}

module.exports = { YugabyteDBClient, YugabyteAnalytics };
```

## Performance Monitoring

### Cluster Health and Metrics
```sql
-- Check tablet servers status
SELECT host, port, num_sst_files, num_tablets, total_ram_usage, 
       read_ops_per_sec, write_ops_per_sec
FROM yb_servers() 
WHERE server_type = 'tserver';

-- Check master servers status  
SELECT host, port, is_leader, uptime_seconds
FROM yb_servers() 
WHERE server_type = 'master';

-- Monitor tablet distribution
SELECT 
    table_name,
    COUNT(*) as tablet_count,
    MIN(start_key) as min_start_key,
    MAX(end_key) as max_end_key
FROM yb_tablet_servers()
GROUP BY table_name
ORDER BY tablet_count DESC;

-- Check slow queries
SELECT 
    datname,
    usename,
    query,
    mean_exec_time,
    calls,
    total_exec_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements pss
JOIN pg_database pd ON pss.dbid = pd.oid
WHERE mean_exec_time > 1000  -- queries slower than 1 second
ORDER BY mean_exec_time DESC
LIMIT 20;
```

### Performance Optimization
```python
def monitor_yugabyte_performance(client):
    """Comprehensive YugabyteDB performance monitoring"""
    
    # Check tablet server performance
    tserver_stats = client.execute_read_replica_query("""
        SELECT 
            host,
            port,
            num_sst_files,
            num_tablets,
            total_ram_usage / (1024*1024*1024) as ram_usage_gb,
            read_ops_per_sec,
            write_ops_per_sec,
            total_sst_file_size / (1024*1024*1024) as sst_size_gb
        FROM yb_servers() 
        WHERE server_type = 'tserver'
        ORDER BY read_ops_per_sec + write_ops_per_sec DESC
    """)
    
    # Check table statistics
    table_stats = client.execute_read_replica_query("""
        SELECT 
            schemaname,
            tablename,
            n_tup_ins as inserts,
            n_tup_upd as updates,
            n_tup_del as deletes,
            n_tup_hot_upd as hot_updates,
            n_live_tup as live_tuples,
            n_dead_tup as dead_tuples,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze
        FROM pg_stat_user_tables
        ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC
    """)
    
    # Check index usage
    index_stats = client.execute_read_replica_query("""
        SELECT 
            schemaname,
            tablename,
            indexrelname,
            idx_tup_read,
            idx_tup_fetch,
            idx_scan,
            CASE 
                WHEN idx_scan = 0 THEN 'Unused'
                WHEN idx_tup_read = 0 THEN 'Never Read'
                ELSE 'Active'
            END as index_status
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC
    """)
    
    # Check replication lag (for multi-region setups)
    replication_stats = client.execute_read_replica_query("""
        SELECT 
            application_name,
            client_addr,
            state,
            sent_lsn,
            write_lsn,
            flush_lsn,
            replay_lsn,
            write_lag,
            flush_lag,
            replay_lag
        FROM pg_stat_replication
        ORDER BY replay_lag DESC NULLS LAST
    """)
    
    return {
        'tserver_performance': tserver_stats,
        'table_statistics': table_stats,
        'index_usage': index_stats,
        'replication_status': replication_stats
    }

def optimize_table_performance(client, table_name):
    """Optimize specific table performance"""
    
    # Analyze table statistics
    client.pool.query(f"ANALYZE {table_name}")
    
    # Check tablet distribution
    tablet_info = client.execute_read_replica_query("""
        SELECT 
            tablet_id,
            table_name,
            start_key,
            end_key,
            leader_replica,
            followers
        FROM yb_table_tablets()
        WHERE table_name = %s
        ORDER BY start_key
    """, [table_name])
    
    # Suggest optimizations based on tablet distribution
    if len(tablet_info) < 4:  # Too few tablets
        print(f"Consider splitting {table_name} for better parallelism")
        
    return tablet_info
```

## Backup and Disaster Recovery

### Distributed Backup Strategy
```bash
#!/bin/bash
# YugabyteDB backup script

# Configuration
YUGABYTE_MASTER="localhost:7100"
BACKUP_LOCATION="s3://yugabyte-backups"
KEYSPACE="ecommerce"
DATE=$(date +%Y%m%d_%H%M%S)

# Full keyspace backup
yb-admin -master_addresses $YUGABYTE_MASTER \
  create_snapshot ysql.$KEYSPACE

# Get snapshot ID
SNAPSHOT_ID=$(yb-admin -master_addresses $YUGABYTE_MASTER \
  list_snapshots | grep ysql.$KEYSPACE | awk '{print $1}' | tail -1)

# Export snapshot to external storage
yb-admin -master_addresses $YUGABYTE_MASTER \
  export_snapshot $SNAPSHOT_ID $BACKUP_LOCATION/full/$DATE

# Table-level backup
yb-admin -master_addresses $YUGABYTE_MASTER \
  create_snapshot ysql.$KEYSPACE orders

# Get table snapshot ID
TABLE_SNAPSHOT_ID=$(yb-admin -master_addresses $YUGABYTE_MASTER \
  list_snapshots | grep "ysql.$KEYSPACE orders" | awk '{print $1}' | tail -1)

# Export table snapshot
yb-admin -master_addresses $YUGABYTE_MASTER \
  export_snapshot $TABLE_SNAPSHOT_ID $BACKUP_LOCATION/table/orders/$DATE

echo "Backup completed: $DATE"
echo "Full snapshot ID: $SNAPSHOT_ID"
echo "Table snapshot ID: $TABLE_SNAPSHOT_ID"
```

### Point-in-Time Recovery
```bash
# List available snapshots
yb-admin -master_addresses localhost:7100 list_snapshots

# Restore from snapshot
yb-admin -master_addresses localhost:7100 \
  import_snapshot s3://yugabyte-backups/full/20240115_120000 \
  $SNAPSHOT_ID

# Restore to new keyspace
yb-admin -master_addresses localhost:7100 \
  import_snapshot s3://yugabyte-backups/full/20240115_120000 \
  $SNAPSHOT_ID ecommerce_restore

# Restore specific table
yb-admin -master_addresses localhost:7100 \
  import_snapshot s3://yugabyte-backups/table/orders/20240115_120000 \
  $TABLE_SNAPSHOT_ID
```

## Best Practices

### Schema Design for Distribution
```sql
-- Use hash sharding for even distribution
CREATE TABLE distributed_table (
    id UUID PRIMARY KEY,
    data TEXT
) SPLIT INTO 16 TABLETS;

-- Use range sharding for time-series data
CREATE TABLE time_series_data (
    timestamp TIMESTAMPTZ,
    device_id TEXT,
    value DOUBLE PRECISION,
    PRIMARY KEY (timestamp, device_id)
) SPLIT AT VALUES (('2024-01-01'), ('2024-02-01'), ('2024-03-01'));

-- Co-locate related tables for joins
CREATE TABLEGROUP ecommerce_group;

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE,
    region TEXT
) TABLEGROUP ecommerce_group;

CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    total_amount DECIMAL(10,2)
) TABLEGROUP ecommerce_group;
```

### Query Optimization
```sql
-- Use prepared statements for better performance
PREPARE get_user_orders(UUID, INT) AS
SELECT id, total_amount, status, created_at
FROM orders 
WHERE user_id = $1 
ORDER BY created_at DESC 
LIMIT $2;

EXECUTE get_user_orders('123e4567-e89b-12d3-a456-426614174000', 10);

-- Use covering indexes for read-heavy workloads
CREATE INDEX idx_orders_covering 
ON orders (user_id, created_at DESC) 
INCLUDE (total_amount, status);

-- Batch operations for better throughput
INSERT INTO metrics (timestamp, device_id, metric_name, value, region)
SELECT 
    generate_series(NOW() - INTERVAL '1 hour', NOW(), INTERVAL '1 minute'),
    'device_' || (random() * 1000)::int,
    'cpu_usage',
    random() * 100,
    'us-west-1';
```

## Resources

- [YugabyteDB Documentation](https://docs.yugabyte.com/)
- [SQL Performance Tuning](https://docs.yugabyte.com/preview/explore/query-1-performance/)
- [Multi-Region Deployments](https://docs.yugabyte.com/preview/deploy/multi-dc/)
- [Backup and Restore Guide](https://docs.yugabyte.com/preview/manage/backup-restore/)
- [Monitoring and Alerting](https://docs.yugabyte.com/preview/reference/configuration/yb-tserver/)
- [PostgreSQL Compatibility](https://docs.yugabyte.com/preview/api/ysql/datatypes/)
- [Best Practices Guide](https://docs.yugabyte.com/preview/develop/best-practices-ysql/)
- [Community Forum](https://community.yugabyte.com/)
- [GitHub Repository](https://github.com/yugabyte/yugabyte-db)
- [Performance Benchmarks](https://docs.yugabyte.com/preview/benchmark/)