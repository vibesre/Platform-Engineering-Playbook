# ClickHouse

ClickHouse is a column-oriented database management system (DBMS) for online analytical processing (OLAP). It's designed for high-performance analytics on large datasets with real-time query processing capabilities.

## Installation

### Docker Installation
```bash
# Single-node ClickHouse
docker run -d \
  --name clickhouse-server \
  --ulimit nofile=262144:262144 \
  -p 8123:8123 \
  -p 9000:9000 \
  -v clickhouse_data:/var/lib/clickhouse \
  clickhouse/clickhouse-server:latest

# ClickHouse with custom configuration
docker run -d \
  --name clickhouse-server \
  -p 8123:8123 \
  -p 9000:9000 \
  -v $(pwd)/config.xml:/etc/clickhouse-server/config.xml \
  -v $(pwd)/users.xml:/etc/clickhouse-server/users.xml \
  -v clickhouse_data:/var/lib/clickhouse \
  clickhouse/clickhouse-server:latest

# Docker Compose cluster
cat > docker-compose.yml << EOF
version: '3.8'
services:
  clickhouse-zookeeper:
    image: zookeeper:3.7
    container_name: clickhouse-zookeeper
    hostname: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=zookeeper:2888:3888;2181

  clickhouse01:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse01
    hostname: clickhouse01
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./config/clickhouse01:/etc/clickhouse-server
      - clickhouse01_data:/var/lib/clickhouse
    depends_on:
      - clickhouse-zookeeper

  clickhouse02:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse02
    hostname: clickhouse02
    ports:
      - "8124:8123"
      - "9001:9000"
    volumes:
      - ./config/clickhouse02:/etc/clickhouse-server
      - clickhouse02_data:/var/lib/clickhouse
    depends_on:
      - clickhouse-zookeeper

  clickhouse03:
    image: clickhouse/clickhouse-server:latest
    container_name: clickhouse03
    hostname: clickhouse03
    ports:
      - "8125:8123"
      - "9002:9000"
    volumes:
      - ./config/clickhouse03:/etc/clickhouse-server
      - clickhouse03_data:/var/lib/clickhouse
    depends_on:
      - clickhouse-zookeeper

volumes:
  clickhouse01_data:
  clickhouse02_data:
  clickhouse03_data:

networks:
  default:
    driver: bridge
EOF

docker-compose up -d
```

### Native Installation
```bash
# Ubuntu/Debian
sudo apt-get install -y apt-transport-https ca-certificates dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754

echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee \
    /etc/apt/sources.list.d/clickhouse.list
sudo apt-get update

sudo apt-get install -y clickhouse-server clickhouse-client

# Start service
sudo service clickhouse-server start

# CentOS/RHEL/Fedora
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo
sudo yum install -y clickhouse-server clickhouse-client

sudo systemctl start clickhouse-server
sudo systemctl enable clickhouse-server

# From binary
curl https://clickhouse.com/ | sh
sudo ./clickhouse install
sudo clickhouse start
```

### Kubernetes Installation
```yaml
# clickhouse-cluster.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: clickhouse
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: clickhouse-config
  namespace: clickhouse
data:
  config.xml: |
    <?xml version="1.0"?>
    <clickhouse>
        <logger>
            <level>trace</level>
            <console>true</console>
        </logger>
        <http_port>8123</http_port>
        <tcp_port>9000</tcp_port>
        <mysql_port>9004</mysql_port>
        <postgresql_port>9005</postgresql_port>
        <interserver_http_port>9009</interserver_http_port>
        
        <listen_host>0.0.0.0</listen_host>
        
        <max_connections>4096</max_connections>
        <keep_alive_timeout>3</keep_alive_timeout>
        <max_concurrent_queries>100</max_concurrent_queries>
        <uncompressed_cache_size>8589934592</uncompressed_cache_size>
        <mark_cache_size>5368709120</mark_cache_size>
        
        <path>/var/lib/clickhouse/</path>
        <tmp_path>/var/lib/clickhouse/tmp/</tmp_path>
        <user_files_path>/var/lib/clickhouse/user_files/</user_files_path>
        
        <users_config>users.xml</users_config>
        <default_profile>default</default_profile>
        <default_database>default</default_database>
        
        <timezone>UTC</timezone>
        
        <remote_servers>
            <cluster_3s_1r>
                <shard>
                    <replica>
                        <host>clickhouse-0.clickhouse</host>
                        <port>9000</port>
                    </replica>
                </shard>
                <shard>
                    <replica>
                        <host>clickhouse-1.clickhouse</host>
                        <port>9000</port>
                    </replica>
                </shard>
                <shard>
                    <replica>
                        <host>clickhouse-2.clickhouse</host>
                        <port>9000</port>
                    </replica>
                </shard>
            </cluster_3s_1r>
        </remote_servers>
        
        <zookeeper>
            <node index="1">
                <host>zookeeper</host>
                <port>2181</port>
            </node>
        </zookeeper>
        
        <macros>
            <cluster>cluster_3s_1r</cluster>
            <shard from_env="SHARD"></shard>
            <replica from_env="REPLICA"></replica>
        </macros>
        
        <distributed_ddl>
            <path>/clickhouse/task_queue/ddl</path>
        </distributed_ddl>
        
        <compression incl="clickhouse_compression">
            <case>
                <min_part_size>10000000000</min_part_size>
                <min_part_size_ratio>0.01</min_part_size_ratio>
                <method>lz4</method>
            </case>
        </compression>
    </clickhouse>
  
  users.xml: |
    <?xml version="1.0"?>
    <clickhouse>
        <profiles>
            <default>
                <max_memory_usage>10000000000</max_memory_usage>
                <use_uncompressed_cache>0</use_uncompressed_cache>
                <load_balancing>random</load_balancing>
            </default>
            <readonly>
                <readonly>1</readonly>
            </readonly>
        </profiles>
        
        <users>
            <default>
                <password></password>
                <networks incl="networks" replace="replace">
                    <ip>::/0</ip>
                </networks>
                <profile>default</profile>
                <quota>default</quota>
            </default>
        </users>
        
        <quotas>
            <default>
                <interval>
                    <duration>3600</duration>
                    <queries>0</queries>
                    <errors>0</errors>
                    <result_rows>0</result_rows>
                    <read_rows>0</read_rows>
                    <execution_time>0</execution_time>
                </interval>
            </default>
        </quotas>
    </clickhouse>
---
apiVersion: v1
kind: Service
metadata:
  name: zookeeper
  namespace: clickhouse
spec:
  ports:
  - port: 2181
    name: client
  selector:
    app: zookeeper
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zookeeper
  namespace: clickhouse
spec:
  serviceName: zookeeper
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      containers:
      - name: zookeeper
        image: zookeeper:3.7
        ports:
        - containerPort: 2181
        env:
        - name: ZOO_MY_ID
          value: "1"
        volumeMounts:
        - name: zookeeper-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: zookeeper-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: clickhouse
  namespace: clickhouse
spec:
  clusterIP: None
  ports:
  - port: 9000
    name: native
  - port: 8123
    name: http
  - port: 9009
    name: interserver
  selector:
    app: clickhouse
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: clickhouse
  namespace: clickhouse
spec:
  serviceName: clickhouse
  replicas: 3
  selector:
    matchLabels:
      app: clickhouse
  template:
    metadata:
      labels:
        app: clickhouse
    spec:
      containers:
      - name: clickhouse
        image: clickhouse/clickhouse-server:latest
        ports:
        - containerPort: 8123
          name: http
        - containerPort: 9000
          name: native
        - containerPort: 9009
          name: interserver
        env:
        - name: SHARD
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: REPLICA
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        volumeMounts:
        - name: clickhouse-config
          mountPath: /etc/clickhouse-server/config.xml
          subPath: config.xml
        - name: clickhouse-config
          mountPath: /etc/clickhouse-server/users.xml
          subPath: users.xml
        - name: clickhouse-data
          mountPath: /var/lib/clickhouse
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
      volumes:
      - name: clickhouse-config
        configMap:
          name: clickhouse-config
  volumeClaimTemplates:
  - metadata:
      name: clickhouse-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi

# Apply the configuration
kubectl apply -f clickhouse-cluster.yaml
```

## Basic Configuration

### Server Configuration
```xml
<!-- config.xml -->
<?xml version="1.0"?>
<clickhouse>
    <!-- Ports -->
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>
    <mysql_port>9004</mysql_port>
    <postgresql_port>9005</postgresql_port>
    
    <!-- Network -->
    <listen_host>0.0.0.0</listen_host>
    <max_connections>4096</max_connections>
    <keep_alive_timeout>3</keep_alive_timeout>
    
    <!-- Memory -->
    <max_concurrent_queries>100</max_concurrent_queries>
    <uncompressed_cache_size>8589934592</uncompressed_cache_size>
    <mark_cache_size>5368709120</mark_cache_size>
    <max_server_memory_usage>0</max_server_memory_usage>
    
    <!-- Storage -->
    <path>/var/lib/clickhouse/</path>
    <tmp_path>/var/lib/clickhouse/tmp/</tmp_path>
    <user_files_path>/var/lib/clickhouse/user_files/</user_files_path>
    
    <!-- Logging -->
    <logger>
        <level>information</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>1000M</size>
        <count>10</count>
    </logger>
    
    <!-- Compression -->
    <compression>
        <case>
            <min_part_size>10000000000</min_part_size>
            <min_part_size_ratio>0.01</min_part_size_ratio>
            <method>lz4</method>
        </case>
    </compression>
    
    <!-- Query settings -->
    <default_profile>default</default_profile>
    <default_database>default</default_database>
    <timezone>UTC</timezone>
    
    <!-- Distributed settings -->
    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
    </distributed_ddl>
</clickhouse>
```

### User Configuration
```xml
<!-- users.xml -->
<?xml version="1.0"?>
<clickhouse>
    <profiles>
        <default>
            <max_memory_usage>10000000000</max_memory_usage>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>random</load_balancing>
            <max_execution_time>300</max_execution_time>
            <max_query_size>268435456</max_query_size>
            <interactive_delay>100000</interactive_delay>
            <connect_timeout>10</connect_timeout>
            <receive_timeout>300</receive_timeout>
            <send_timeout>300</send_timeout>
        </default>
        
        <readonly>
            <readonly>1</readonly>
            <max_memory_usage>5000000000</max_memory_usage>
        </readonly>
        
        <analytics>
            <max_memory_usage>20000000000</max_memory_usage>
            <max_execution_time>600</max_execution_time>
            <max_concurrent_queries_for_user>10</max_concurrent_queries_for_user>
        </analytics>
    </profiles>
    
    <users>
        <default>
            <password></password>
            <networks>
                <ip>::1</ip>
                <ip>127.0.0.1</ip>
                <ip>10.0.0.0/8</ip>
                <ip>172.16.0.0/12</ip>
                <ip>192.168.0.0/16</ip>
            </networks>
            <profile>default</profile>
            <quota>default</quota>
        </default>
        
        <analytics_user>
            <password_sha256_hex>65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5</password_sha256_hex>
            <networks>
                <ip>0.0.0.0/0</ip>
            </networks>
            <profile>analytics</profile>
            <quota>default</quota>
            <databases>
                <database>analytics</database>
                <database>logs</database>
            </databases>
        </analytics_user>
        
        <readonly_user>
            <password_sha256_hex>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</password_sha256_hex>
            <networks>
                <ip>0.0.0.0/0</ip>
            </networks>
            <profile>readonly</profile>
            <quota>default</quota>
        </readonly_user>
    </users>
    
    <quotas>
        <default>
            <interval>
                <duration>3600</duration>
                <queries>0</queries>
                <errors>0</errors>
                <result_rows>0</result_rows>
                <read_rows>0</read_rows>
                <execution_time>0</execution_time>
            </interval>
        </default>
        
        <analytics_quota>
            <interval>
                <duration>3600</duration>
                <queries>1000</queries>
                <errors>100</errors>
                <result_rows>1000000000</result_rows>
                <read_rows>10000000000</read_rows>
                <execution_time>18000</execution_time>
            </interval>
        </analytics_quota>
    </quotas>
</clickhouse>
```

## Data Types and Table Engines

### Basic Data Types
```sql
-- Numeric types
CREATE TABLE numeric_examples (
    id UInt64,
    count UInt32,
    price Decimal64(2),
    percentage Float32,
    precise_value Float64,
    big_number Int128
) ENGINE = MergeTree()
ORDER BY id;

-- String types
CREATE TABLE string_examples (
    id UInt64,
    name String,
    code FixedString(10),
    description LowCardinality(String),
    category Enum8('A' = 1, 'B' = 2, 'C' = 3)
) ENGINE = MergeTree()
ORDER BY id;

-- Date and time types
CREATE TABLE datetime_examples (
    id UInt64,
    event_date Date,
    event_time DateTime,
    event_time_tz DateTime('America/New_York'),
    event_time64 DateTime64(3),
    duration Interval
) ENGINE = MergeTree()
ORDER BY id;

-- Array and nested types
CREATE TABLE complex_examples (
    id UInt64,
    tags Array(String),
    coordinates Array(Float64),
    nested_data Nested(
        key String,
        value UInt32
    ),
    json_data JSON
) ENGINE = MergeTree()
ORDER BY id;
```

### Table Engines

#### MergeTree Engine Family
```sql
-- Basic MergeTree
CREATE TABLE events (
    event_id UInt64,
    user_id UInt32,
    event_type String,
    timestamp DateTime,
    properties String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, timestamp)
SETTINGS index_granularity = 8192;

-- ReplicatedMergeTree for replication
CREATE TABLE events_replicated (
    event_id UInt64,
    user_id UInt32,
    event_type String,
    timestamp DateTime,
    properties String
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events', '{replica}')
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, timestamp);

-- SummingMergeTree for aggregation
CREATE TABLE user_metrics_sum (
    user_id UInt32,
    date Date,
    page_views UInt64,
    session_duration UInt32
) ENGINE = SummingMergeTree((page_views, session_duration))
PARTITION BY toYYYYMM(date)
ORDER BY (user_id, date);

-- AggregatingMergeTree for complex aggregations
CREATE TABLE user_metrics_agg (
    user_id UInt32,
    date Date,
    page_views_sum AggregateFunction(sum, UInt64),
    unique_sessions AggregateFunction(uniq, UInt32),
    avg_duration AggregateFunction(avg, Float32)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (user_id, date);

-- CollapsingMergeTree for handling updates
CREATE TABLE user_profiles (
    user_id UInt32,
    name String,
    email String,
    updated_at DateTime,
    sign Int8
) ENGINE = CollapsingMergeTree(sign)
ORDER BY user_id;
```

#### Log Engine Family
```sql
-- Log engine for small tables
CREATE TABLE lookup_table (
    id UInt32,
    name String,
    category String
) ENGINE = Log;

-- TinyLog for very small tables
CREATE TABLE config_table (
    key String,
    value String
) ENGINE = TinyLog;

-- StripeLog for append-only data
CREATE TABLE audit_log (
    timestamp DateTime,
    action String,
    user_id UInt32,
    details String
) ENGINE = StripeLog;
```

#### Integration Engines
```sql
-- Kafka engine for streaming data
CREATE TABLE kafka_events (
    event_id UInt64,
    user_id UInt32,
    event_type String,
    timestamp DateTime,
    properties String
) ENGINE = Kafka
SETTINGS 
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'events',
    kafka_group_name = 'clickhouse_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 3;

-- MySQL engine for external data
CREATE TABLE mysql_users (
    id UInt32,
    name String,
    email String,
    created_at DateTime
) ENGINE = MySQL('mysql-server:3306', 'database', 'users', 'username', 'password');

-- URL engine for web data
CREATE TABLE web_data (
    id UInt32,
    name String,
    value Float32
) ENGINE = URL('http://api.example.com/data.csv', 'CSV');
```

## Data Ingestion

### INSERT Statements
```sql
-- Simple INSERT
INSERT INTO events VALUES 
(1, 12345, 'page_view', '2023-01-15 10:30:00', '{"page": "/home"}'),
(2, 12346, 'click', '2023-01-15 10:31:00', '{"button": "signup"}');

-- INSERT with column specification
INSERT INTO events (event_id, user_id, event_type, timestamp, properties)
VALUES (3, 12347, 'purchase', '2023-01-15 10:32:00', '{"amount": 29.99}');

-- INSERT from SELECT
INSERT INTO user_metrics_sum
SELECT 
    user_id,
    toDate(timestamp) as date,
    countIf(event_type = 'page_view') as page_views,
    sum(JSONExtractUInt(properties, 'duration')) as session_duration
FROM events
WHERE timestamp >= '2023-01-15'
GROUP BY user_id, date;

-- Batch INSERT
INSERT INTO events VALUES 
(4, 12348, 'page_view', '2023-01-15 10:33:00', '{"page": "/products"}'),
(5, 12349, 'search', '2023-01-15 10:34:00', '{"query": "laptop"}'),
(6, 12350, 'add_to_cart', '2023-01-15 10:35:00', '{"product_id": 123}');
```

### Data Import from Files
```sql
-- Import from CSV
INSERT INTO events
FROM INFILE '/path/to/events.csv'
FORMAT CSV;

-- Import with custom delimiter
INSERT INTO events
FROM INFILE '/path/to/events.tsv'
FORMAT TabSeparated;

-- Import JSON data
INSERT INTO events
FROM INFILE '/path/to/events.jsonl'
FORMAT JSONEachRow;

-- Import with data transformation
INSERT INTO events
SELECT 
    toUInt64(event_id),
    toUInt32(user_id),
    event_type,
    parseDateTimeBestEffort(timestamp_str) as timestamp,
    properties
FROM file('/path/to/raw_events.csv', 'CSV', 
    'event_id String, user_id String, event_type String, timestamp_str String, properties String');
```

### Python Client Usage
```python
# requirements.txt
clickhouse-driver>=0.2.5
clickhouse-client>=0.2.4
pandas>=1.5.0
numpy>=1.24.0

# clickhouse_client.py
from clickhouse_driver import Client
from clickhouse_client import Client as HTTPClient
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class ClickHouseManager:
    def __init__(self, host='localhost', port=9000, database='default', 
                 user='default', password=''):
        self.client = Client(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            send_receive_timeout=300,
            compress_block_size=1048576
        )
        
        # HTTP client for some operations
        self.http_client = HTTPClient(
            host=host,
            port=8123,
            database=database,
            user=user,
            password=password
        )
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            result = self.client.execute(query, params or {})
            return result
        except Exception as e:
            print(f"Query execution failed: {e}")
            return None
    
    def insert_dataframe(self, table_name, df, batch_size=100000):
        """Insert pandas DataFrame into ClickHouse table"""
        try:
            # Convert DataFrame to list of tuples
            data = df.to_records(index=False).tolist()
            
            # Insert in batches
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                self.client.execute(f'INSERT INTO {table_name} VALUES', batch)
            
            print(f"Inserted {len(data)} rows into {table_name}")
        except Exception as e:
            print(f"DataFrame insertion failed: {e}")
    
    def query_to_dataframe(self, query, params=None):
        """Execute query and return results as pandas DataFrame"""
        try:
            result = self.client.execute(query, params or {}, with_column_types=True)
            
            if result:
                data, columns = result
                column_names = [col[0] for col in columns]
                df = pd.DataFrame(data, columns=column_names)
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Query to DataFrame failed: {e}")
            return pd.DataFrame()
    
    def create_table(self, table_name, schema, engine='MergeTree()', 
                     order_by=None, partition_by=None):
        """Create table with specified schema"""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema}) ENGINE = {engine}"
        
        if partition_by:
            query += f" PARTITION BY {partition_by}"
        if order_by:
            query += f" ORDER BY {order_by}"
        
        try:
            self.client.execute(query)
            print(f"Table {table_name} created successfully")
        except Exception as e:
            print(f"Table creation failed: {e}")
    
    def optimize_table(self, table_name):
        """Optimize table for better performance"""
        try:
            self.client.execute(f'OPTIMIZE TABLE {table_name} FINAL')
            print(f"Table {table_name} optimized")
        except Exception as e:
            print(f"Table optimization failed: {e}")
    
    def get_table_info(self, table_name):
        """Get table structure and statistics"""
        try:
            # Table structure
            structure = self.client.execute(f'DESCRIBE TABLE {table_name}')
            
            # Table size
            size_query = f"""
                SELECT 
                    count() as rows,
                    formatReadableSize(sum(data_uncompressed_bytes)) as uncompressed_size,
                    formatReadableSize(sum(data_compressed_bytes)) as compressed_size,
                    round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 4) as compression_ratio
                FROM system.parts 
                WHERE table = '{table_name}' AND active = 1
            """
            size_info = self.client.execute(size_query)
            
            return {
                'structure': structure,
                'size_info': size_info[0] if size_info else None
            }
        except Exception as e:
            print(f"Failed to get table info: {e}")
            return None
    
    def bulk_insert(self, table_name, data, columns=None):
        """Bulk insert data efficiently"""
        try:
            if columns:
                query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES'
            else:
                query = f'INSERT INTO {table_name} VALUES'
            
            self.client.execute(query, data)
            print(f"Bulk inserted {len(data)} rows")
        except Exception as e:
            print(f"Bulk insert failed: {e}")

# Usage examples
if __name__ == "__main__":
    # Initialize client
    ch = ClickHouseManager(host='localhost', port=9000)
    
    # Create sample table
    schema = """
        event_id UInt64,
        user_id UInt32,
        event_type LowCardinality(String),
        timestamp DateTime,
        properties String,
        revenue Nullable(Decimal64(2))
    """
    
    ch.create_table(
        'user_events', 
        schema, 
        engine='MergeTree()',
        order_by='(user_id, timestamp)',
        partition_by='toYYYYMM(timestamp)'
    )
    
    # Generate sample data
    import random
    sample_data = []
    event_types = ['page_view', 'click', 'purchase', 'signup', 'logout']
    
    for i in range(10000):
        sample_data.append((
            i + 1,  # event_id
            random.randint(1000, 9999),  # user_id
            random.choice(event_types),  # event_type
            datetime.now() - timedelta(days=random.randint(0, 30)),  # timestamp
            json.dumps({"page": f"/page{random.randint(1, 100)}"}),  # properties
            random.uniform(10, 1000) if random.random() > 0.8 else None  # revenue
        ))
    
    # Bulk insert data
    ch.bulk_insert('user_events', sample_data)
    
    # Query data
    df = ch.query_to_dataframe("""
        SELECT 
            event_type,
            count() as event_count,
            uniq(user_id) as unique_users,
            avg(revenue) as avg_revenue
        FROM user_events 
        WHERE timestamp >= today() - INTERVAL 7 DAY
        GROUP BY event_type
        ORDER BY event_count DESC
    """)
    
    print("Event Summary:")
    print(df)
    
    # Get table information
    table_info = ch.get_table_info('user_events')
    print(f"\nTable Info: {table_info}")
```

## Advanced Queries and Analytics

### Complex Aggregations
```sql
-- Window functions
SELECT 
    user_id,
    event_type,
    timestamp,
    count() OVER (PARTITION BY user_id ORDER BY timestamp 
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_events,
    row_number() OVER (PARTITION BY user_id ORDER BY timestamp) as event_sequence,
    lag(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as prev_event_time,
    timestamp - lag(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as time_between_events
FROM user_events
WHERE user_id IN (SELECT user_id FROM user_events GROUP BY user_id HAVING count() > 10)
ORDER BY user_id, timestamp;

-- Advanced aggregations with ROLLUP and CUBE
SELECT 
    toYYYYMM(timestamp) as month,
    event_type,
    count() as events,
    uniq(user_id) as unique_users,
    avg(JSONExtractFloat(properties, 'duration')) as avg_duration
FROM user_events
GROUP BY ROLLUP(month, event_type)
ORDER BY month, event_type;

-- Cohort analysis
WITH user_first_seen AS (
    SELECT 
        user_id,
        min(toDate(timestamp)) as first_seen_date
    FROM user_events
    GROUP BY user_id
),
cohort_data AS (
    SELECT 
        u.user_id,
        u.first_seen_date,
        toDate(e.timestamp) as event_date,
        dateDiff('day', u.first_seen_date, toDate(e.timestamp)) as days_since_first_seen
    FROM user_first_seen u
    JOIN user_events e ON u.user_id = e.user_id
)
SELECT 
    first_seen_date,
    days_since_first_seen,
    uniq(user_id) as active_users
FROM cohort_data
WHERE first_seen_date >= '2023-01-01'
GROUP BY first_seen_date, days_since_first_seen
ORDER BY first_seen_date, days_since_first_seen;

-- Funnel analysis
SELECT 
    step,
    users,
    if(step = 1, 100, round(users * 100.0 / first_value(users) OVER (), 2)) as conversion_rate
FROM (
    SELECT 
        1 as step,
        'Page View' as step_name,
        uniq(user_id) as users
    FROM user_events 
    WHERE event_type = 'page_view' 
      AND timestamp >= today() - INTERVAL 7 DAY
    
    UNION ALL
    
    SELECT 
        2 as step,
        'Add to Cart' as step_name,
        uniq(user_id) as users
    FROM user_events 
    WHERE event_type = 'add_to_cart' 
      AND timestamp >= today() - INTERVAL 7 DAY
      AND user_id IN (
          SELECT user_id FROM user_events 
          WHERE event_type = 'page_view' 
            AND timestamp >= today() - INTERVAL 7 DAY
      )
    
    UNION ALL
    
    SELECT 
        3 as step,
        'Purchase' as step_name,
        uniq(user_id) as users
    FROM user_events 
    WHERE event_type = 'purchase' 
      AND timestamp >= today() - INTERVAL 7 DAY
      AND user_id IN (
          SELECT user_id FROM user_events 
          WHERE event_type = 'add_to_cart' 
            AND timestamp >= today() - INTERVAL 7 DAY
      )
) ORDER BY step;
```

### Time Series Analysis
```sql
-- Time series with gaps filled
WITH RECURSIVE time_series AS (
    SELECT toDateTime('2023-01-01 00:00:00') as ts
    UNION ALL
    SELECT ts + INTERVAL 1 HOUR
    FROM time_series
    WHERE ts < toDateTime('2023-01-31 23:00:00')
)
SELECT 
    ts,
    coalesce(events, 0) as events,
    coalesce(revenue, 0) as revenue
FROM time_series
LEFT JOIN (
    SELECT 
        toStartOfHour(timestamp) as hour,
        count() as events,
        sum(revenue) as revenue
    FROM user_events
    WHERE timestamp >= '2023-01-01' AND timestamp < '2023-02-01'
    GROUP BY hour
) e ON time_series.ts = e.hour
ORDER BY ts;

-- Moving averages and trends
SELECT 
    date,
    daily_events,
    avg(daily_events) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma_7d,
    avg(daily_events) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as ma_30d,
    (daily_events - lag(daily_events, 7) OVER (ORDER BY date)) / lag(daily_events, 7) OVER (ORDER BY date) * 100 as wow_growth
FROM (
    SELECT 
        toDate(timestamp) as date,
        count() as daily_events
    FROM user_events
    GROUP BY date
) ORDER BY date;

-- Seasonality analysis
SELECT 
    hour_of_day,
    day_of_week,
    avg(hourly_events) as avg_events,
    median(hourly_events) as median_events,
    quantile(0.95)(hourly_events) as p95_events
FROM (
    SELECT 
        toHour(timestamp) as hour_of_day,
        toDayOfWeek(timestamp) as day_of_week,
        toStartOfHour(timestamp) as hour,
        count() as hourly_events
    FROM user_events
    WHERE timestamp >= today() - INTERVAL 30 DAY
    GROUP BY hour_of_day, day_of_week, hour
)
GROUP BY hour_of_day, day_of_week
ORDER BY day_of_week, hour_of_day;
```

## Performance Optimization

### Index Optimization
```sql
-- Primary key and sorting key optimization
CREATE TABLE optimized_events (
    user_id UInt32,
    timestamp DateTime,
    event_type LowCardinality(String),
    event_id UInt64,
    properties String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, timestamp, event_type)
SETTINGS index_granularity = 8192;

-- Secondary indexes
ALTER TABLE optimized_events 
ADD INDEX idx_event_type event_type TYPE set(1000) GRANULARITY 1;

ALTER TABLE optimized_events 
ADD INDEX idx_timestamp timestamp TYPE minmax GRANULARITY 1;

-- Materialized columns for JSON properties
ALTER TABLE optimized_events 
ADD COLUMN page_path String MATERIALIZED JSONExtractString(properties, 'page_path');

ALTER TABLE optimized_events 
ADD INDEX idx_page_path page_path TYPE bloom_filter(0.01) GRANULARITY 1;

-- Projection for common queries
ALTER TABLE optimized_events 
ADD PROJECTION user_daily_summary (
    SELECT 
        user_id,
        toDate(timestamp) as date,
        event_type,
        count()
    GROUP BY user_id, date, event_type
);
```

### Query Optimization Tips
```sql
-- Use PREWHERE for filtering before reading columns
SELECT 
    user_id,
    count() as events,
    uniq(JSONExtractString(properties, 'page_path')) as unique_pages
FROM user_events
PREWHERE timestamp >= today() - INTERVAL 7 DAY
WHERE event_type = 'page_view'
GROUP BY user_id;

-- Optimize JOIN operations
SELECT 
    u.user_id,
    u.signup_date,
    count(e.event_id) as total_events
FROM (
    SELECT user_id, min(toDate(timestamp)) as signup_date
    FROM user_events
    WHERE event_type = 'signup'
    GROUP BY user_id
) u
ALL LEFT JOIN user_events e ON u.user_id = e.user_id
GROUP BY u.user_id, u.signup_date;

-- Use sampling for large datasets
SELECT 
    event_type,
    count() * 10 as estimated_total  -- Sample is 0.1
FROM user_events SAMPLE 0.1
WHERE timestamp >= today() - INTERVAL 30 DAY
GROUP BY event_type;

-- Optimize aggregations with dictionaries
CREATE DICTIONARY event_type_dict (
    id UInt32,
    name String
) PRIMARY KEY id
SOURCE(CLICKHOUSE(
    HOST 'localhost'
    PORT 9000
    USER 'default'
    TABLE 'event_types'
    DB 'default'
))
LIFETIME(MIN 300 MAX 600)
LAYOUT(HASHED());

SELECT 
    dictGet('event_type_dict', 'name', event_type_id) as event_name,
    count() as events
FROM user_events_optimized
GROUP BY event_type_id;
```

## Monitoring and Observability

### System Tables Monitoring
```sql
-- Monitor query performance
SELECT 
    query_id,
    user,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage,
    query
FROM system.query_log
WHERE event_date = today()
  AND query_duration_ms > 1000
ORDER BY query_duration_ms DESC
LIMIT 10;

-- Monitor table sizes and compression
SELECT 
    table,
    sum(rows) as total_rows,
    formatReadableSize(sum(data_uncompressed_bytes)) as uncompressed_size,
    formatReadableSize(sum(data_compressed_bytes)) as compressed_size,
    round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 4) as compression_ratio
FROM system.parts
WHERE active = 1
GROUP BY table
ORDER BY sum(data_uncompressed_bytes) DESC;

-- Monitor replication status
SELECT 
    table,
    replica_name,
    is_leader,
    is_readonly,
    absolute_delay,
    queue_size,
    inserts_in_queue,
    merges_in_queue
FROM system.replicas
WHERE absolute_delay > 0;

-- Monitor mutations and background processes
SELECT 
    table,
    mutation_id,
    command,
    create_time,
    parts_to_do,
    is_done,
    latest_failed_part,
    latest_fail_time,
    latest_fail_reason
FROM system.mutations
WHERE is_done = 0;
```

### Performance Monitoring Script
```python
# monitoring.py
import time
from datetime import datetime
import pandas as pd

class ClickHouseMonitor:
    def __init__(self, clickhouse_client):
        self.client = clickhouse_client
    
    def get_system_metrics(self):
        """Get comprehensive system metrics"""
        metrics = {}
        
        # Query performance metrics
        query_metrics = self.client.query_to_dataframe("""
            SELECT 
                count() as total_queries,
                avg(query_duration_ms) as avg_duration_ms,
                quantile(0.95)(query_duration_ms) as p95_duration_ms,
                sum(read_rows) as total_read_rows,
                sum(read_bytes) as total_read_bytes,
                avg(memory_usage) as avg_memory_usage
            FROM system.query_log
            WHERE event_date = today()
              AND event_time >= now() - INTERVAL 1 HOUR
              AND query_kind = 'Select'
        """)
        metrics['queries'] = query_metrics.iloc[0].to_dict() if not query_metrics.empty else {}
        
        # Table metrics
        table_metrics = self.client.query_to_dataframe("""
            SELECT 
                table,
                sum(rows) as total_rows,
                sum(data_uncompressed_bytes) as uncompressed_bytes,
                sum(data_compressed_bytes) as compressed_bytes,
                count() as parts_count
            FROM system.parts
            WHERE active = 1
            GROUP BY table
            ORDER BY uncompressed_bytes DESC
            LIMIT 10
        """)
        metrics['tables'] = table_metrics.to_dict('records')
        
        # Memory usage
        memory_metrics = self.client.query_to_dataframe("""
            SELECT 
                metric,
                value
            FROM system.asynchronous_metrics
            WHERE metric LIKE '%Memory%'
               OR metric LIKE '%Cache%'
        """)
        metrics['memory'] = memory_metrics.to_dict('records')
        
        # Merge and mutation status
        merge_metrics = self.client.query_to_dataframe("""
            SELECT 
                count() as active_merges,
                sum(progress) / count() as avg_merge_progress
            FROM system.merges
        """)
        metrics['merges'] = merge_metrics.iloc[0].to_dict() if not merge_metrics.empty else {}
        
        return metrics
    
    def check_slow_queries(self, duration_threshold=5000):
        """Identify slow queries"""
        slow_queries = self.client.query_to_dataframe(f"""
            SELECT 
                query_id,
                user,
                query_duration_ms,
                read_rows,
                formatReadableSize(read_bytes) as read_bytes_formatted,
                formatReadableSize(memory_usage) as memory_usage_formatted,
                substr(query, 1, 100) as query_preview
            FROM system.query_log
            WHERE event_date = today()
              AND query_duration_ms > {duration_threshold}
              AND query_kind = 'Select'
            ORDER BY query_duration_ms DESC
            LIMIT 20
        """)
        return slow_queries
    
    def check_replication_lag(self):
        """Check replication lag across replicas"""
        replication_status = self.client.query_to_dataframe("""
            SELECT 
                table,
                replica_name,
                absolute_delay,
                queue_size,
                inserts_in_queue,
                merges_in_queue,
                is_readonly
            FROM system.replicas
            WHERE absolute_delay > 60  -- More than 1 minute lag
               OR queue_size > 100
        """)
        return replication_status
    
    def generate_health_report(self):
        """Generate comprehensive health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.get_system_metrics(),
            'slow_queries': self.check_slow_queries().to_dict('records'),
            'replication_issues': self.check_replication_lag().to_dict('records')
        }
        
        # Calculate health score
        health_score = 100
        metrics = report['metrics']
        
        # Penalize for slow queries
        if metrics.get('queries', {}).get('p95_duration_ms', 0) > 5000:
            health_score -= 20
        
        # Penalize for replication lag
        if report['replication_issues']:
            health_score -= 30
        
        # Penalize for high memory usage
        memory_usage = sum(m['value'] for m in metrics.get('memory', []) 
                          if 'MemoryResident' in m['metric'])
        if memory_usage > 80 * 1024 * 1024 * 1024:  # 80GB
            health_score -= 15
        
        report['health_score'] = max(0, health_score)
        return report
    
    def monitor_continuously(self, interval=300):
        """Monitor continuously with specified interval"""
        print(f"Starting ClickHouse monitoring (interval: {interval}s)")
        
        while True:
            try:
                report = self.generate_health_report()
                timestamp = report['timestamp']
                health_score = report['health_score']
                
                print(f"\n[{timestamp}] Health Score: {health_score}/100")
                
                # Print key metrics
                queries = report['metrics'].get('queries', {})
                if queries:
                    print(f"  Queries (last hour): {queries.get('total_queries', 0)}")
                    print(f"  Avg query duration: {queries.get('avg_duration_ms', 0):.2f}ms")
                    print(f"  P95 query duration: {queries.get('p95_duration_ms', 0):.2f}ms")
                
                # Alert on issues
                if report['slow_queries']:
                    print(f"  ⚠️  {len(report['slow_queries'])} slow queries detected")
                
                if report['replication_issues']:
                    print(f"  ⚠️  {len(report['replication_issues'])} replication issues")
                
                if health_score < 70:
                    print(f"  🚨 Health score below threshold!")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped")
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(interval)

# Usage
if __name__ == "__main__":
    from clickhouse_client import ClickHouseManager
    
    ch = ClickHouseManager()
    monitor = ClickHouseMonitor(ch)
    
    # Generate single report
    report = monitor.generate_health_report()
    print(f"Health Score: {report['health_score']}/100")
    
    # Start continuous monitoring
    # monitor.monitor_continuously(interval=300)
```

## Backup and Recovery

### Backup Strategies
```sql
-- Create backup using FREEZE
ALTER TABLE user_events FREEZE;

-- Backup to S3
BACKUP TABLE user_events TO S3('s3://my-bucket/clickhouse-backups/user_events/', 'access_key', 'secret_key');

-- Backup multiple tables
BACKUP DATABASE default TO S3('s3://my-bucket/clickhouse-backups/full/', 'access_key', 'secret_key');

-- Incremental backup
BACKUP TABLE user_events TO S3('s3://my-bucket/clickhouse-backups/incremental/', 'access_key', 'secret_key')
SETTINGS backup_type='incremental', backup_base='s3://my-bucket/clickhouse-backups/base/';
```

### Automated Backup Script
```python
# backup_manager.py
import subprocess
import boto3
import os
from datetime import datetime, timedelta
import logging

class ClickHouseBackupManager:
    def __init__(self, s3_bucket, aws_access_key, aws_secret_key, backup_path):
        self.s3_bucket = s3_bucket
        self.backup_path = backup_path
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
    def create_backup(self, database_name, table_name=None):
        """Create backup of database or specific table"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if table_name:
            backup_name = f"{database_name}_{table_name}_{timestamp}"
            backup_query = f"BACKUP TABLE {database_name}.{table_name} TO S3('{self.s3_bucket}/{self.backup_path}/{backup_name}/')"
        else:
            backup_name = f"{database_name}_full_{timestamp}"
            backup_query = f"BACKUP DATABASE {database_name} TO S3('{self.s3_bucket}/{self.backup_path}/{backup_name}/')"
        
        try:
            # Execute backup command
            cmd = f'clickhouse-client --query="{backup_query}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info(f"Backup created successfully: {backup_name}")
                return backup_name
            else:
                logging.error(f"Backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logging.error(f"Backup creation failed: {e}")
            return None
    
    def restore_backup(self, backup_name, target_database=None, target_table=None):
        """Restore from backup"""
        try:
            if target_table:
                restore_query = f"RESTORE TABLE {target_database}.{target_table} FROM S3('{self.s3_bucket}/{self.backup_path}/{backup_name}/')"
            else:
                restore_query = f"RESTORE DATABASE {target_database or 'default'} FROM S3('{self.s3_bucket}/{self.backup_path}/{backup_name}/')"
            
            cmd = f'clickhouse-client --query="{restore_query}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info(f"Restore completed successfully from: {backup_name}")
                return True
            else:
                logging.error(f"Restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            logging.error(f"Restore failed: {e}")
            return False
    
    def list_backups(self):
        """List available backups"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=self.backup_path,
                Delimiter='/'
            )
            
            backups = []
            for prefix in response.get('CommonPrefixes', []):
                backup_name = prefix['Prefix'].split('/')[-2]
                backups.append(backup_name)
            
            return sorted(backups, reverse=True)
            
        except Exception as e:
            logging.error(f"Failed to list backups: {e}")
            return []
    
    def cleanup_old_backups(self, retention_days=30):
        """Remove backups older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            backups = self.list_backups()
            
            for backup_name in backups:
                # Extract timestamp from backup name
                try:
                    timestamp_str = backup_name.split('_')[-2] + '_' + backup_name.split('_')[-1]
                    backup_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    
                    if backup_date < cutoff_date:
                        # Delete backup
                        self.s3_client.delete_object(
                            Bucket=self.s3_bucket,
                            Key=f"{self.backup_path}/{backup_name}/"
                        )
                        logging.info(f"Deleted old backup: {backup_name}")
                        
                except ValueError:
                    # Skip if timestamp parsing fails
                    continue
                    
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")
    
    def automated_backup(self, databases, retention_days=30):
        """Perform automated backup with cleanup"""
        for database in databases:
            backup_name = self.create_backup(database)
            if backup_name:
                logging.info(f"Successfully backed up database: {database}")
            else:
                logging.error(f"Failed to backup database: {database}")
        
        # Cleanup old backups
        self.cleanup_old_backups(retention_days)
```

## Resources

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse Python Driver](https://github.com/mymarilyn/clickhouse-driver)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [ClickHouse Performance Guide](https://clickhouse.com/docs/en/operations/performance/)
- [ClickHouse Cluster Setup](https://clickhouse.com/docs/en/architecture/cluster-deployment/)
- [ClickHouse Monitoring](https://clickhouse.com/docs/en/operations/monitoring/)
- [ClickHouse Backup and Restore](https://clickhouse.com/docs/en/operations/backup/)
- [ClickHouse Community](https://clickhouse.com/company/community)
- [ClickHouse GitHub Repository](https://github.com/ClickHouse/ClickHouse)
- [ClickHouse Blog](https://clickhouse.com/blog/)