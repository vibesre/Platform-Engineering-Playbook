# TimescaleDB

TimescaleDB is a time-series database built on PostgreSQL that provides scalable and efficient storage for time-series data with automatic partitioning.

## Installation

### Docker
```bash
docker run -d --name timescaledb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  timescale/timescaledb:latest-pg15

# Connect to the database
docker exec -it timescaledb psql -U postgres
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: timescaledb
spec:
  serviceName: timescaledb
  replicas: 1
  selector:
    matchLabels:
      app: timescaledb
  template:
    metadata:
      labels:
        app: timescaledb
    spec:
      containers:
      - name: timescaledb
        image: timescale/timescaledb:latest-pg15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          value: "password"
        - name: POSTGRES_DB
          value: "metrics"
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: timescaledb-service
spec:
  selector:
    app: timescaledb
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

## Database Setup

### Create Hypertable
```sql
-- Create the TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create metrics table
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    value DOUBLE PRECISION,
    tags JSONB
);

-- Convert to hypertable (partitioned by time)
SELECT create_hypertable('metrics', 'time');

-- Create indexes for better query performance
CREATE INDEX ON metrics (device_id, time DESC);
CREATE INDEX ON metrics (metric_name, time DESC);
CREATE INDEX ON metrics USING GIN (tags);

-- Create continuous aggregate for hourly averages
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    device_id,
    metric_name,
    avg(value) as avg_value,
    max(value) as max_value,
    min(value) as min_value,
    count(*) as count
FROM metrics
GROUP BY hour, device_id, metric_name
WITH NO DATA;

-- Enable continuous aggregate policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

## Schema Design

### Time-Series Best Practices
```sql
-- Device telemetry table
CREATE TABLE device_telemetry (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL,
    cpu_usage DOUBLE PRECISION,
    memory_usage DOUBLE PRECISION,
    disk_usage DOUBLE PRECISION,
    network_rx BIGINT,
    network_tx BIGINT,
    location POINT,
    metadata JSONB
);

SELECT create_hypertable('device_telemetry', 'time', 
    chunk_time_interval => INTERVAL '1 day');

-- Application metrics table  
CREATE TABLE app_metrics (
    time TIMESTAMPTZ NOT NULL,
    application TEXT NOT NULL,
    instance TEXT NOT NULL,
    metric_type TEXT NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    labels JSONB DEFAULT '{}'
);

SELECT create_hypertable('app_metrics', 'time',
    chunk_time_interval => INTERVAL '6 hours');

-- Add compression for older data
ALTER TABLE app_metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'application,instance',
    timescaledb.compress_orderby = 'time DESC'
);

-- Auto-compress chunks older than 7 days
SELECT add_compression_policy('app_metrics', INTERVAL '7 days');
```

## Python Integration

### Basic Client
```python
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import json

class TimescaleDBClient:
    def __init__(self, host='localhost', port=5432, database='postgres', 
                 user='postgres', password='password'):
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.conn = None
        
    def connect(self):
        self.conn = psycopg2.connect(**self.conn_params)
        return self.conn
        
    def disconnect(self):
        if self.conn:
            self.conn.close()
            
    def insert_metric(self, device_id, metric_name, value, tags=None, timestamp=None):
        if not timestamp:
            timestamp = datetime.utcnow()
            
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO metrics (time, device_id, metric_name, value, tags)
            VALUES (%s, %s, %s, %s, %s)
        """, (timestamp, device_id, metric_name, value, json.dumps(tags or {})))
        self.conn.commit()
        cursor.close()
        
    def insert_batch_metrics(self, metrics_data):
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO metrics (time, device_id, metric_name, value, tags)
            VALUES (%s, %s, %s, %s, %s)
        """, metrics_data)
        self.conn.commit()
        cursor.close()
        
    def query_metrics(self, device_id=None, metric_name=None, 
                     start_time=None, end_time=None, limit=1000):
        query = "SELECT * FROM metrics WHERE 1=1"
        params = []
        
        if device_id:
            query += " AND device_id = %s"
            params.append(device_id)
        if metric_name:
            query += " AND metric_name = %s"  
            params.append(metric_name)
        if start_time:
            query += " AND time >= %s"
            params.append(start_time)
        if end_time:
            query += " AND time <= %s"
            params.append(end_time)
            
        query += " ORDER BY time DESC LIMIT %s"
        params.append(limit)
        
        return pd.read_sql(query, self.conn, params=params)
        
    def get_aggregated_metrics(self, device_id, metric_name, 
                              interval='1 hour', start_time=None, end_time=None):
        query = """
            SELECT 
                time_bucket(%s, time) AS time_bucket,
                avg(value) as avg_value,
                max(value) as max_value,
                min(value) as min_value,
                count(*) as count
            FROM metrics 
            WHERE device_id = %s AND metric_name = %s
        """
        params = [interval, device_id, metric_name]
        
        if start_time:
            query += " AND time >= %s"
            params.append(start_time)
        if end_time:
            query += " AND time <= %s"
            params.append(end_time)
            
        query += " GROUP BY time_bucket ORDER BY time_bucket"
        
        return pd.read_sql(query, self.conn, params=params)

# Usage example
client = TimescaleDBClient()
client.connect()

# Insert single metric
client.insert_metric('device_001', 'cpu_usage', 75.5, 
                    tags={'environment': 'production', 'region': 'us-east-1'})

# Insert batch metrics
metrics_batch = [
    (datetime.utcnow(), 'device_001', 'memory_usage', 68.2, '{"env": "prod"}'),
    (datetime.utcnow(), 'device_002', 'cpu_usage', 82.1, '{"env": "staging"}'),
]
client.insert_batch_metrics(metrics_batch)

# Query metrics
df = client.query_metrics(
    device_id='device_001',
    metric_name='cpu_usage',
    start_time=datetime.utcnow() - timedelta(hours=24)
)
print(df.head())

client.disconnect()
```

### Monitoring Client
```python
import asyncio
import psycopg2.pool
from datetime import datetime
import logging

class TimescaleMonitoringClient:
    def __init__(self, connection_pool):
        self.pool = connection_pool
        self.logger = logging.getLogger(__name__)
        
    async def start_monitoring(self, devices, interval=60):
        while True:
            try:
                await self.collect_and_store_metrics(devices)
                await asyncio.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                
    async def collect_and_store_metrics(self, devices):
        tasks = []
        for device in devices:
            task = asyncio.create_task(self.collect_device_metrics(device))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Store all metrics in batch
        all_metrics = []
        for result in results:
            if isinstance(result, list):
                all_metrics.extend(result)
                
        if all_metrics:
            await self.store_metrics_batch(all_metrics)
            
    async def collect_device_metrics(self, device):
        # Simulate metric collection
        metrics = [
            (datetime.utcnow(), device['id'], 'cpu_usage', 
             device.get('cpu_usage', 0), '{"source": "monitoring"}'),
            (datetime.utcnow(), device['id'], 'memory_usage', 
             device.get('memory_usage', 0), '{"source": "monitoring"}'),
        ]
        return metrics
        
    async def store_metrics_batch(self, metrics):
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO metrics (time, device_id, metric_name, value, tags)
                VALUES (%s, %s, %s, %s, %s)
            """, metrics)
            conn.commit()
            cursor.close()
        finally:
            self.pool.putconn(conn)
```

## Node.js Integration

### Basic Client
```javascript
const { Pool } = require('pg');

class TimescaleDBClient {
    constructor(config = {}) {
        this.pool = new Pool({
            user: config.user || 'postgres',
            host: config.host || 'localhost',
            database: config.database || 'postgres',
            password: config.password || 'password',
            port: config.port || 5432,
            max: config.maxConnections || 20,
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 2000,
        });
    }

    async insertMetric(deviceId, metricName, value, tags = {}, timestamp = null) {
        const time = timestamp || new Date();
        const query = `
            INSERT INTO metrics (time, device_id, metric_name, value, tags)
            VALUES ($1, $2, $3, $4, $5)
        `;
        
        try {
            await this.pool.query(query, [time, deviceId, metricName, value, JSON.stringify(tags)]);
        } catch (error) {
            console.error('Error inserting metric:', error);
            throw error;
        }
    }

    async insertBatchMetrics(metrics) {
        const client = await this.pool.connect();
        
        try {
            await client.query('BEGIN');
            
            for (const metric of metrics) {
                const query = `
                    INSERT INTO metrics (time, device_id, metric_name, value, tags)
                    VALUES ($1, $2, $3, $4, $5)
                `;
                await client.query(query, [
                    metric.time || new Date(),
                    metric.deviceId,
                    metric.metricName,
                    metric.value,
                    JSON.stringify(metric.tags || {})
                ]);
            }
            
            await client.query('COMMIT');
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }

    async queryMetrics(options = {}) {
        const {
            deviceId,
            metricName,
            startTime,
            endTime,
            limit = 1000
        } = options;

        let query = 'SELECT * FROM metrics WHERE 1=1';
        const params = [];
        let paramCount = 0;

        if (deviceId) {
            params.push(deviceId);
            query += ` AND device_id = $${++paramCount}`;
        }
        if (metricName) {
            params.push(metricName);
            query += ` AND metric_name = $${++paramCount}`;
        }
        if (startTime) {
            params.push(startTime);
            query += ` AND time >= $${++paramCount}`;
        }
        if (endTime) {
            params.push(endTime);
            query += ` AND time <= $${++paramCount}`;
        }

        params.push(limit);
        query += ` ORDER BY time DESC LIMIT $${++paramCount}`;

        try {
            const result = await this.pool.query(query, params);
            return result.rows;
        } catch (error) {
            console.error('Error querying metrics:', error);
            throw error;
        }
    }

    async getAggregatedMetrics(deviceId, metricName, interval = '1 hour', startTime = null, endTime = null) {
        let query = `
            SELECT 
                time_bucket($1, time) AS time_bucket,
                avg(value) as avg_value,
                max(value) as max_value,
                min(value) as min_value,
                count(*) as count
            FROM metrics 
            WHERE device_id = $2 AND metric_name = $3
        `;
        
        const params = [interval, deviceId, metricName];
        let paramCount = 3;

        if (startTime) {
            params.push(startTime);
            query += ` AND time >= $${++paramCount}`;
        }
        if (endTime) {
            params.push(endTime);
            query += ` AND time <= $${++paramCount}`;
        }

        query += ' GROUP BY time_bucket ORDER BY time_bucket';

        try {
            const result = await this.pool.query(query, params);
            return result.rows;
        } catch (error) {
            console.error('Error getting aggregated metrics:', error);
            throw error;
        }
    }

    async close() {
        await this.pool.end();
    }
}

// Usage example
async function example() {
    const client = new TimescaleDBClient();

    try {
        // Insert single metric
        await client.insertMetric('device_001', 'cpu_usage', 75.5, {
            environment: 'production',
            region: 'us-east-1'
        });

        // Insert batch metrics
        const metrics = [
            {
                deviceId: 'device_001',
                metricName: 'memory_usage',
                value: 68.2,
                tags: { env: 'prod' }
            },
            {
                deviceId: 'device_002',
                metricName: 'cpu_usage',
                value: 82.1,
                tags: { env: 'staging' }
            }
        ];
        await client.insertBatchMetrics(metrics);

        // Query metrics
        const recentMetrics = await client.queryMetrics({
            deviceId: 'device_001',
            metricName: 'cpu_usage',
            startTime: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
        });
        console.log('Recent metrics:', recentMetrics);

        // Get aggregated metrics
        const hourlyStats = await client.getAggregatedMetrics(
            'device_001',
            'cpu_usage',
            '1 hour',
            new Date(Date.now() - 24 * 60 * 60 * 1000)
        );
        console.log('Hourly stats:', hourlyStats);

    } catch (error) {
        console.error('Example error:', error);
    } finally {
        await client.close();
    }
}

module.exports = TimescaleDBClient;
```

## Monitoring and Alerting

### Health Checks
```sql
-- Check database size and chunk information
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE tablename LIKE '%metrics%';

-- Check chunk statistics
SELECT 
    chunk_name,
    chunk_schema,
    range_start,
    range_end,
    pg_size_pretty(chunk_size) as size
FROM timescaledb_information.chunks
WHERE hypertable_name = 'metrics'
ORDER BY range_start DESC
LIMIT 10;

-- Check continuous aggregate status
SELECT 
    view_name,
    completed_threshold,
    invalidation_threshold,
    job_status
FROM timescaledb_information.continuous_aggregates;
```

### Performance Monitoring
```python
def monitor_timescaledb_performance(client):
    """Monitor TimescaleDB performance metrics"""
    
    # Check query performance
    slow_queries = client.query_metrics("""
        SELECT 
            query,
            calls,
            total_time,
            mean_time,
            rows
        FROM pg_stat_statements 
        WHERE mean_time > 1000
        ORDER BY mean_time DESC
        LIMIT 10
    """)
    
    # Check chunk compression ratios
    compression_stats = client.query_metrics("""
        SELECT 
            chunk_name,
            before_compression_table_bytes,
            after_compression_table_bytes,
            ROUND(
                (before_compression_table_bytes::float / after_compression_table_bytes::float), 2
            ) as compression_ratio
        FROM chunk_compression_stats('metrics')
        ORDER BY compression_ratio DESC
    """)
    
    return {
        'slow_queries': slow_queries,
        'compression_stats': compression_stats
    }
```

## Backup and Recovery

### Backup Strategy
```bash
#!/bin/bash
# TimescaleDB backup script

DB_NAME="metrics"
BACKUP_DIR="/backups/timescaledb"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Full database backup
pg_dump -h localhost -U postgres -d $DB_NAME \
  --format=custom \
  --file="$BACKUP_DIR/full_backup_$DATE.backup"

# Continuous aggregate backup
pg_dump -h localhost -U postgres -d $DB_NAME \
  --table=metrics_hourly \
  --format=custom \
  --file="$BACKUP_DIR/aggregates_backup_$DATE.backup"

# Compress older backups
find $BACKUP_DIR -name "*.backup" -mtime +7 -exec gzip {} \;

# Clean up old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Point-in-Time Recovery
```bash
# Stop TimescaleDB
docker stop timescaledb

# Restore from backup
docker run --rm \
  -v $BACKUP_DIR:/backups \
  -v timescaledb_data:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg15 \
  pg_restore -d postgres /backups/full_backup_20240101_120000.backup

# Start TimescaleDB
docker start timescaledb
```

## Best Practices

### Data Retention
```sql
-- Set up automatic data retention
SELECT add_retention_policy('metrics', INTERVAL '90 days');

-- Manual data cleanup
DELETE FROM metrics 
WHERE time < NOW() - INTERVAL '1 year';

-- Vacuum to reclaim space
VACUUM ANALYZE metrics;
```

### Query Optimization
```sql
-- Create appropriate indexes
CREATE INDEX CONCURRENTLY ON metrics (device_id, time DESC) 
WHERE metric_name = 'cpu_usage';

-- Use time_bucket for aggregations
SELECT 
    time_bucket('5 minutes', time) AS bucket,
    device_id,
    avg(value) as avg_cpu
FROM metrics 
WHERE metric_name = 'cpu_usage' 
  AND time > NOW() - INTERVAL '1 hour'
GROUP BY bucket, device_id
ORDER BY bucket DESC;

-- Use EXPLAIN ANALYZE to optimize queries
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM metrics 
WHERE device_id = 'device_001' 
  AND time > NOW() - INTERVAL '1 day';
```

## Resources

- [TimescaleDB Documentation](https://docs.timescale.com/)
- [Time-Series Data Best Practices](https://docs.timescale.com/timescaledb/latest/how-to-guides/schema-management/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [TimescaleDB Tutorials](https://docs.timescale.com/tutorials/latest/)
- [Continuous Aggregates Guide](https://docs.timescale.com/timescaledb/latest/how-to-guides/continuous-aggregates/)
- [Compression Guide](https://docs.timescale.com/timescaledb/latest/how-to-guides/compression/)
- [TimescaleDB GitHub](https://github.com/timescale/timescaledb)
- [Community Forum](https://community.timescale.com/)
- [Python psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Node.js pg Library](https://node-postgres.com/)