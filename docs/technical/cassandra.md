# Apache Cassandra

## Overview

Apache Cassandra is a highly scalable, distributed NoSQL database designed for platform engineers who need to handle massive amounts of data across multiple servers with no single point of failure. It provides linear scalability, fault tolerance, and tunable consistency for modern applications.

## Key Features

- **Linear Scalability**: Scale horizontally by adding more nodes
- **Fault Tolerance**: No single point of failure with automatic data replication
- **Tunable Consistency**: Choose between consistency and availability per operation
- **High Performance**: Optimized for write-heavy workloads
- **Multi-Datacenter Support**: Built-in support for geographic distribution

## Installation

### Docker Installation
```bash
# Basic Cassandra container
docker run -d \
  --name cassandra \
  -p 9042:9042 \
  -p 7199:7199 \
  -e CASSANDRA_CLUSTER_NAME=TestCluster \
  -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
  -e CASSANDRA_DC=datacenter1 \
  cassandra:latest

# With persistent storage
docker run -d \
  --name cassandra \
  -p 9042:9042 \
  -p 7199:7199 \
  -e CASSANDRA_CLUSTER_NAME=TestCluster \
  -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
  -e CASSANDRA_DC=datacenter1 \
  -v cassandra_data:/var/lib/cassandra \
  cassandra:latest
```

### Docker Compose Cluster
```yaml
# docker-compose.yml
version: '3.8'
services:
  cassandra-1:
    image: cassandra:latest
    container_name: cassandra-1
    ports:
      - "9042:9042"
      - "7199:7199"
    environment:
      - CASSANDRA_CLUSTER_NAME=TestCluster
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_SEEDS=cassandra-1
    volumes:
      - cassandra1_data:/var/lib/cassandra
    networks:
      - cassandra-network

  cassandra-2:
    image: cassandra:latest
    container_name: cassandra-2
    ports:
      - "9043:9042"
    environment:
      - CASSANDRA_CLUSTER_NAME=TestCluster
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_SEEDS=cassandra-1
    volumes:
      - cassandra2_data:/var/lib/cassandra
    networks:
      - cassandra-network
    depends_on:
      - cassandra-1

  cassandra-3:
    image: cassandra:latest
    container_name: cassandra-3
    ports:
      - "9044:9042"
    environment:
      - CASSANDRA_CLUSTER_NAME=TestCluster
      - CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_RACK=rack1
      - CASSANDRA_SEEDS=cassandra-1
    volumes:
      - cassandra3_data:/var/lib/cassandra
    networks:
      - cassandra-network
    depends_on:
      - cassandra-2

volumes:
  cassandra1_data:
  cassandra2_data:
  cassandra3_data:

networks:
  cassandra-network:
    driver: bridge
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Service
metadata:
  name: cassandra
  namespace: database
  labels:
    app: cassandra
spec:
  clusterIP: None
  ports:
  - port: 9042
    name: cql
  - port: 7000
    name: intra-node
  - port: 7001
    name: tls-intra-node
  - port: 7199
    name: jmx
  selector:
    app: cassandra
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
  namespace: database
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      terminationGracePeriodSeconds: 300
      containers:
      - name: cassandra
        image: cassandra:latest
        ports:
        - containerPort: 7000
          name: intra-node
        - containerPort: 7001
          name: tls-intra-node
        - containerPort: 7199
          name: jmx
        - containerPort: 9042
          name: cql
        resources:
          limits:
            cpu: "2000m"
            memory: 4Gi
          requests:
            cpu: "1000m"
            memory: 2Gi
        securityContext:
          capabilities:
            add:
            - IPC_LOCK
        lifecycle:
          preStop:
            exec:
              command:
              - /bin/sh
              - -c
              - nodetool drain
        env:
        - name: MAX_HEAP_SIZE
          value: 2G
        - name: HEAP_NEWSIZE
          value: 400M
        - name: CASSANDRA_SEEDS
          value: "cassandra-0.cassandra.database.svc.cluster.local"
        - name: CASSANDRA_CLUSTER_NAME
          value: "K8Demo"
        - name: CASSANDRA_DC
          value: "DC1-K8Demo"
        - name: CASSANDRA_RACK
          value: "Rack1-K8Demo"
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        readinessProbe:
          exec:
            command:
            - /bin/bash
            - -c
            - /ready-probe.sh
          initialDelaySeconds: 15
          timeoutSeconds: 5
        volumeMounts:
        - name: cassandra-data
          mountPath: /var/lib/cassandra
        - name: cassandra-config
          mountPath: /etc/cassandra
      volumes:
      - name: cassandra-config
        configMap:
          name: cassandra-config
  volumeClaimTemplates:
  - metadata:
      name: cassandra-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cassandra-config
  namespace: database
data:
  cassandra.yaml: |
    cluster_name: 'K8Demo'
    num_tokens: 256
    hinted_handoff_enabled: true
    max_hint_window_in_ms: 10800000
    hinted_handoff_throttle_in_kb: 1024
    max_hints_delivery_threads: 2
    hints_directory: /var/lib/cassandra/hints
    hints_flush_period_in_ms: 10000
    max_hints_file_size_in_mb: 128
    batchlog_replay_throttle_in_kb: 1024
    authenticator: AllowAllAuthenticator
    authorizer: AllowAllAuthorizer
    role_manager: CassandraRoleManager
    roles_validity_in_ms: 2000
    permissions_validity_in_ms: 2000
    credentials_validity_in_ms: 2000
    partitioner: org.apache.cassandra.dht.Murmur3Partitioner
    data_file_directories:
    - /var/lib/cassandra/data
    commitlog_directory: /var/lib/cassandra/commitlog
    disk_failure_policy: stop
    commit_failure_policy: stop
    prepared_statements_cache_size_mb:
    thrift_prepared_statements_cache_size_mb:
    key_cache_size_in_mb:
    key_cache_save_period: 14400
    row_cache_size_in_mb: 0
    row_cache_save_period: 0
    counter_cache_size_in_mb:
    counter_cache_save_period: 7200
    saved_caches_directory: /var/lib/cassandra/saved_caches
    commitlog_sync: periodic
    commitlog_sync_period_in_ms: 10000
    commitlog_segment_size_in_mb: 32
    seed_provider:
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
      - seeds: "cassandra-0.cassandra.database.svc.cluster.local"
    concurrent_reads: 32
    concurrent_writes: 32
    concurrent_counter_writes: 32
    concurrent_materialized_view_writes: 32
    memtable_allocation_type: heap_buffers
    index_summary_capacity_in_mb:
    index_summary_resize_interval_in_minutes: 60
    trickle_fsync: false
    trickle_fsync_interval_in_kb: 10240
    storage_port: 7000
    ssl_storage_port: 7001
    listen_address: ${POD_IP}
    start_native_transport: true
    native_transport_port: 9042
    start_rpc: false
    rpc_port: 9160
    rpc_keepalive: true
    rpc_server_type: sync
    thrift_framed_transport_size_in_mb: 15
    incremental_backups: false
    snapshot_before_compaction: false
    auto_snapshot: true
    tombstone_warn_threshold: 1000
    tombstone_failure_threshold: 100000
    column_index_size_in_kb: 64
    batch_size_warn_threshold_in_kb: 5
    batch_size_fail_threshold_in_kb: 50
    compaction_throughput_mb_per_sec: 16
    compaction_large_partition_warning_threshold_mb: 100
    sstable_preemptive_open_interval_in_mb: 50
    read_request_timeout_in_ms: 5000
    range_request_timeout_in_ms: 10000
    write_request_timeout_in_ms: 2000
    counter_write_request_timeout_in_ms: 5000
    cas_contention_timeout_in_ms: 1000
    truncate_request_timeout_in_ms: 60000
    request_timeout_in_ms: 10000
    endpoint_snitch: GossipingPropertyFileSnitch
    dynamic_snitch_update_interval_in_ms: 100
    dynamic_snitch_reset_interval_in_ms: 600000
    dynamic_snitch_badness_threshold: 0.1
    request_scheduler: org.apache.cassandra.scheduler.NoScheduler
    server_encryption_options:
      internode_encryption: none
      keystore: conf/.keystore
      keystore_password: cassandra
      truststore: conf/.truststore
      truststore_password: cassandra
    client_encryption_options:
      enabled: false
      optional: false
      keystore: conf/.keystore
      keystore_password: cassandra
    internode_compression: dc
    inter_dc_tcp_nodelay: false
    tracetype_query_ttl: 86400
    tracetype_repair_ttl: 604800
    enable_user_defined_functions: false
    enable_scripted_user_defined_functions: false
    windows_timer_interval: 1
```

## Data Modeling

### Keyspace and Table Creation
```cql
-- Create keyspace
CREATE KEYSPACE IF NOT EXISTS ecommerce
WITH REPLICATION = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3,
  'datacenter2': 2
};

USE ecommerce;

-- User table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN
);

-- Create index on email
CREATE INDEX ON users (email);

-- Orders table (time-series pattern)
CREATE TABLE orders (
    user_id UUID,
    order_date DATE,
    order_id UUID,
    total_amount DECIMAL,
    status TEXT,
    shipping_address TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY ((user_id, order_date), order_id)
) WITH CLUSTERING ORDER BY (order_id DESC);

-- Order items table
CREATE TABLE order_items (
    order_id UUID,
    item_id UUID,
    product_id UUID,
    quantity INT,
    unit_price DECIMAL,
    total_price DECIMAL,
    PRIMARY KEY (order_id, item_id)
);

-- Products table
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    name TEXT,
    description TEXT,
    category TEXT,
    price DECIMAL,
    stock_quantity INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Product by category (denormalized for queries)
CREATE TABLE products_by_category (
    category TEXT,
    price DECIMAL,
    product_id UUID,
    name TEXT,
    stock_quantity INT,
    PRIMARY KEY (category, price, product_id)
) WITH CLUSTERING ORDER BY (price ASC);

-- User sessions (time-series with TTL)
CREATE TABLE user_sessions (
    user_id UUID,
    session_id UUID,
    started_at TIMESTAMP,
    last_activity TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    PRIMARY KEY (user_id, started_at)
) WITH CLUSTERING ORDER BY (started_at DESC)
AND default_time_to_live = 604800; -- 7 days TTL

-- Event logging table
CREATE TABLE events (
    event_date DATE,
    event_time TIMESTAMP,
    event_id UUID,
    user_id UUID,
    event_type TEXT,
    event_data TEXT,
    PRIMARY KEY ((event_date), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Counters table
CREATE TABLE page_views (
    page_url TEXT,
    view_date DATE,
    view_count COUNTER,
    PRIMARY KEY (page_url, view_date)
);
```

## Application Integration

### Python Integration
```python
# requirements.txt
cassandra-driver==3.28.0
python-dateutil==2.8.2

# cassandra_client.py
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement, ConsistencyLevel
from cassandra import ConsistencyLevel
import uuid
from datetime import datetime, date, timedelta
import logging

class CassandraClient:
    def __init__(self, hosts, keyspace, username=None, password=None, 
                 datacenter=None, port=9042):
        self.hosts = hosts
        self.keyspace = keyspace
        self.cluster = None
        self.session = None
        self.datacenter = datacenter
        
        # Setup authentication if provided
        auth_provider = None
        if username and password:
            auth_provider = PlainTextAuthProvider(username=username, password=password)
        
        # Setup load balancing policy
        if datacenter:
            load_balancing_policy = DCAwareRoundRobinPolicy(local_dc=datacenter)
        else:
            load_balancing_policy = WhiteListRoundRobinPolicy(hosts)
        
        # Create execution profiles
        profile = ExecutionProfile(
            load_balancing_policy=load_balancing_policy,
            consistency_level=ConsistencyLevel.LOCAL_QUORUM,
            serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
            request_timeout=10
        )
        
        # Initialize cluster
        self.cluster = Cluster(
            contact_points=hosts,
            port=port,
            auth_provider=auth_provider,
            execution_profiles={EXEC_PROFILE_DEFAULT: profile}
        )
        
        self.connect()
    
    def connect(self):
        """Connect to Cassandra cluster"""
        try:
            self.session = self.cluster.connect()
            if self.keyspace:
                self.session.set_keyspace(self.keyspace)
            logging.info("Connected to Cassandra cluster")
        except Exception as e:
            logging.error(f"Failed to connect to Cassandra: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from Cassandra cluster"""
        if self.cluster:
            self.cluster.shutdown()
    
    def execute_query(self, query, parameters=None, consistency_level=None):
        """Execute a query with optional parameters"""
        try:
            statement = SimpleStatement(query)
            if consistency_level:
                statement.consistency_level = consistency_level
            
            result = self.session.execute(statement, parameters)
            return result
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise
    
    def execute_batch(self, statements, consistency_level=None):
        """Execute batch statements"""
        from cassandra.query import BatchStatement
        
        try:
            batch = BatchStatement(consistency_level=consistency_level or ConsistencyLevel.LOCAL_QUORUM)
            
            for statement, parameters in statements:
                if isinstance(statement, str):
                    statement = SimpleStatement(statement)
                batch.add(statement, parameters)
            
            self.session.execute(batch)
            return True
        except Exception as e:
            logging.error(f"Batch execution failed: {e}")
            return False

# Repository classes
class UserRepository:
    def __init__(self, cassandra_client):
        self.client = cassandra_client
        
        # Prepare statements for better performance
        self.insert_user_stmt = self.client.session.prepare("""
            INSERT INTO users (user_id, username, email, first_name, last_name, created_at, updated_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)
        
        self.get_user_stmt = self.client.session.prepare("""
            SELECT * FROM users WHERE user_id = ?
        """)
        
        self.get_user_by_email_stmt = self.client.session.prepare("""
            SELECT * FROM users WHERE email = ?
        """)
        
        self.update_user_stmt = self.client.session.prepare("""
            UPDATE users SET first_name = ?, last_name = ?, updated_at = ? WHERE user_id = ?
        """)
    
    def create_user(self, username, email, first_name, last_name):
        """Create a new user"""
        user_id = uuid.uuid4()
        now = datetime.utcnow()
        
        try:
            self.client.session.execute(self.insert_user_stmt, [
                user_id, username, email, first_name, last_name, now, now, True
            ])
            return user_id
        except Exception as e:
            logging.error(f"Failed to create user: {e}")
            raise
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            result = self.client.session.execute(self.get_user_stmt, [user_id])
            return result.one()
        except Exception as e:
            logging.error(f"Failed to get user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            result = self.client.session.execute(self.get_user_by_email_stmt, [email])
            return result.one()
        except Exception as e:
            logging.error(f"Failed to get user by email: {e}")
            return None
    
    def update_user(self, user_id, first_name=None, last_name=None):
        """Update user information"""
        try:
            current_user = self.get_user(user_id)
            if not current_user:
                return False
            
            # Use current values if not provided
            updated_first_name = first_name or current_user.first_name
            updated_last_name = last_name or current_user.last_name
            
            self.client.session.execute(self.update_user_stmt, [
                updated_first_name, updated_last_name, datetime.utcnow(), user_id
            ])
            return True
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return False

class OrderRepository:
    def __init__(self, cassandra_client):
        self.client = cassandra_client
        
        # Prepare statements
        self.insert_order_stmt = self.client.session.prepare("""
            INSERT INTO orders (user_id, order_date, order_id, total_amount, status, shipping_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """)
        
        self.get_user_orders_stmt = self.client.session.prepare("""
            SELECT * FROM orders WHERE user_id = ? AND order_date = ?
        """)
        
        self.get_user_orders_range_stmt = self.client.session.prepare("""
            SELECT * FROM orders WHERE user_id = ? AND order_date >= ? AND order_date <= ?
        """)
        
        self.update_order_status_stmt = self.client.session.prepare("""
            UPDATE orders SET status = ? WHERE user_id = ? AND order_date = ? AND order_id = ?
        """)
    
    def create_order(self, user_id, total_amount, shipping_address, order_items):
        """Create a new order with items"""
        order_id = uuid.uuid4()
        now = datetime.utcnow()
        order_date = now.date()
        
        try:
            # Batch statement for order and items
            batch_statements = []
            
            # Add order
            batch_statements.append((self.insert_order_stmt, [
                user_id, order_date, order_id, total_amount, 'pending', shipping_address, now
            ]))
            
            # Add order items
            for item in order_items:
                item_stmt = self.client.session.prepare("""
                    INSERT INTO order_items (order_id, item_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                """)
                batch_statements.append((item_stmt, [
                    order_id, uuid.uuid4(), item['product_id'], 
                    item['quantity'], item['unit_price'], 
                    item['quantity'] * item['unit_price']
                ]))
            
            success = self.client.execute_batch(batch_statements)
            return order_id if success else None
        except Exception as e:
            logging.error(f"Failed to create order: {e}")
            return None
    
    def get_user_orders(self, user_id, order_date=None, start_date=None, end_date=None):
        """Get user orders for a specific date or date range"""
        try:
            if order_date:
                result = self.client.session.execute(self.get_user_orders_stmt, [user_id, order_date])
                return list(result)
            elif start_date and end_date:
                result = self.client.session.execute(self.get_user_orders_range_stmt, 
                                                   [user_id, start_date, end_date])
                return list(result)
            else:
                # Get orders for the last 30 days
                end_date = date.today()
                start_date = end_date - timedelta(days=30)
                result = self.client.session.execute(self.get_user_orders_range_stmt, 
                                                   [user_id, start_date, end_date])
                return list(result)
        except Exception as e:
            logging.error(f"Failed to get user orders: {e}")
            return []
    
    def update_order_status(self, user_id, order_date, order_id, status):
        """Update order status"""
        try:
            self.client.session.execute(self.update_order_status_stmt, 
                                      [status, user_id, order_date, order_id])
            return True
        except Exception as e:
            logging.error(f"Failed to update order status: {e}")
            return False

class EventRepository:
    def __init__(self, cassandra_client):
        self.client = cassandra_client
        
        # Prepare statements
        self.insert_event_stmt = self.client.session.prepare("""
            INSERT INTO events (event_date, event_time, event_id, user_id, event_type, event_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        
        self.get_events_stmt = self.client.session.prepare("""
            SELECT * FROM events WHERE event_date = ? AND event_time >= ? AND event_time <= ?
        """)
    
    def log_event(self, user_id, event_type, event_data):
        """Log an event"""
        event_id = uuid.uuid4()
        now = datetime.utcnow()
        event_date = now.date()
        
        try:
            self.client.session.execute(self.insert_event_stmt, [
                event_date, now, event_id, user_id, event_type, event_data
            ])
            return event_id
        except Exception as e:
            logging.error(f"Failed to log event: {e}")
            return None
    
    def get_events(self, event_date, start_time=None, end_time=None):
        """Get events for a specific date and time range"""
        try:
            if not start_time:
                start_time = datetime.combine(event_date, datetime.min.time())
            if not end_time:
                end_time = datetime.combine(event_date, datetime.max.time())
            
            result = self.client.session.execute(self.get_events_stmt, 
                                                [event_date, start_time, end_time])
            return list(result)
        except Exception as e:
            logging.error(f"Failed to get events: {e}")
            return []

# Usage example
if __name__ == "__main__":
    # Initialize client
    client = CassandraClient(
        hosts=['127.0.0.1'],
        keyspace='ecommerce',
        datacenter='datacenter1'
    )
    
    # Initialize repositories
    user_repo = UserRepository(client)
    order_repo = OrderRepository(client)
    event_repo = EventRepository(client)
    
    try:
        # Create a user
        user_id = user_repo.create_user(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Created user: {user_id}")
        
        # Get user
        user = user_repo.get_user(user_id)
        print(f"User: {user.username} ({user.email})")
        
        # Create an order
        order_items = [
            {'product_id': uuid.uuid4(), 'quantity': 2, 'unit_price': 29.99},
            {'product_id': uuid.uuid4(), 'quantity': 1, 'unit_price': 49.99}
        ]
        
        order_id = order_repo.create_order(
            user_id=user_id,
            total_amount=109.97,
            shipping_address="123 Main St, City, State",
            order_items=order_items
        )
        print(f"Created order: {order_id}")
        
        # Get user orders
        orders = order_repo.get_user_orders(user_id)
        print(f"User has {len(orders)} orders")
        
        # Log an event
        event_id = event_repo.log_event(
            user_id=user_id,
            event_type="order_created",
            event_data=f"Order {order_id} created"
        )
        print(f"Logged event: {event_id}")
        
    finally:
        client.disconnect()
```

### Java Integration
```java
// pom.xml dependencies
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-core</artifactId>
    <version>4.15.0</version>
</dependency>
<dependency>
    <groupId>com.datastax.oss</groupId>
    <artifactId>java-driver-query-builder</artifactId>
    <version>4.15.0</version>
</dependency>

// CassandraClient.java
package com.example.cassandra;

import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.config.DriverConfigLoader;
import com.datastax.oss.driver.api.core.cql.*;
import com.datastax.oss.driver.api.querybuilder.QueryBuilder;
import com.datastax.oss.driver.api.querybuilder.insert.Insert;
import com.datastax.oss.driver.api.querybuilder.select.Select;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.InetSocketAddress;
import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public class CassandraClient {
    private static final Logger logger = LoggerFactory.getLogger(CassandraClient.class);
    
    private CqlSession session;
    private String keyspace;
    
    public CassandraClient(List<String> contactPoints, String keyspace, String datacenter) {
        this.keyspace = keyspace;
        
        try {
            // Create session builder
            CqlSession.Builder builder = CqlSession.builder();
            
            // Add contact points
            for (String contactPoint : contactPoints) {
                builder.addContactPoint(new InetSocketAddress(contactPoint, 9042));
            }
            
            // Set local datacenter
            builder.withLocalDatacenter(datacenter);
            
            // Set keyspace
            if (keyspace != null && !keyspace.isEmpty()) {
                builder.withKeyspace(keyspace);
            }
            
            this.session = builder.build();
            logger.info("Connected to Cassandra cluster");
            
        } catch (Exception e) {
            logger.error("Failed to connect to Cassandra", e);
            throw new RuntimeException("Failed to connect to Cassandra", e);
        }
    }
    
    public ResultSet execute(String query, Object... parameters) {
        try {
            PreparedStatement prepared = session.prepare(query);
            return session.execute(prepared.bind(parameters));
        } catch (Exception e) {
            logger.error("Query execution failed: " + query, e);
            throw e;
        }
    }
    
    public ResultSet execute(Statement<?> statement) {
        try {
            return session.execute(statement);
        } catch (Exception e) {
            logger.error("Statement execution failed", e);
            throw e;
        }
    }
    
    public BatchStatement createBatch() {
        return BatchStatement.newInstance(DefaultBatchType.LOGGED);
    }
    
    public void close() {
        if (session != null) {
            session.close();
        }
    }
}

// User.java
package com.example.cassandra.model;

import java.time.Instant;
import java.util.UUID;

public class User {
    private UUID userId;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private Instant createdAt;
    private Instant updatedAt;
    private boolean isActive;
    
    // Constructors
    public User() {}
    
    public User(UUID userId, String username, String email, String firstName, String lastName) {
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();
        this.isActive = true;
    }
    
    // Getters and setters
    public UUID getUserId() { return userId; }
    public void setUserId(UUID userId) { this.userId = userId; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    
    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
    
    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }
}

// UserRepository.java
package com.example.cassandra.repository;

import com.datastax.oss.driver.api.core.cql.PreparedStatement;
import com.datastax.oss.driver.api.core.cql.ResultSet;
import com.datastax.oss.driver.api.core.cql.Row;
import com.example.cassandra.CassandraClient;
import com.example.cassandra.model.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

public class UserRepository {
    private static final Logger logger = LoggerFactory.getLogger(UserRepository.class);
    
    private final CassandraClient client;
    private final PreparedStatement insertUserStmt;
    private final PreparedStatement getUserStmt;
    private final PreparedStatement getUserByEmailStmt;
    private final PreparedStatement updateUserStmt;
    
    public UserRepository(CassandraClient client) {
        this.client = client;
        
        // Prepare statements
        this.insertUserStmt = client.session.prepare(
            "INSERT INTO users (user_id, username, email, first_name, last_name, created_at, updated_at, is_active) " +
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        );
        
        this.getUserStmt = client.session.prepare(
            "SELECT * FROM users WHERE user_id = ?"
        );
        
        this.getUserByEmailStmt = client.session.prepare(
            "SELECT * FROM users WHERE email = ?"
        );
        
        this.updateUserStmt = client.session.prepare(
            "UPDATE users SET first_name = ?, last_name = ?, updated_at = ? WHERE user_id = ?"
        );
    }
    
    public UUID createUser(String username, String email, String firstName, String lastName) {
        UUID userId = UUID.randomUUID();
        Instant now = Instant.now();
        
        try {
            client.session.execute(insertUserStmt.bind(
                userId, username, email, firstName, lastName, now, now, true
            ));
            
            logger.info("Created user: {}", userId);
            return userId;
        } catch (Exception e) {
            logger.error("Failed to create user", e);
            throw new RuntimeException("Failed to create user", e);
        }
    }
    
    public Optional<User> getUser(UUID userId) {
        try {
            ResultSet result = client.session.execute(getUserStmt.bind(userId));
            Row row = result.one();
            
            if (row != null) {
                User user = new User();
                user.setUserId(row.getUuid("user_id"));
                user.setUsername(row.getString("username"));
                user.setEmail(row.getString("email"));
                user.setFirstName(row.getString("first_name"));
                user.setLastName(row.getString("last_name"));
                user.setCreatedAt(row.getInstant("created_at"));
                user.setUpdatedAt(row.getInstant("updated_at"));
                user.setActive(row.getBoolean("is_active"));
                
                return Optional.of(user);
            }
            
            return Optional.empty();
        } catch (Exception e) {
            logger.error("Failed to get user: {}", userId, e);
            return Optional.empty();
        }
    }
    
    public Optional<User> getUserByEmail(String email) {
        try {
            ResultSet result = client.session.execute(getUserByEmailStmt.bind(email));
            Row row = result.one();
            
            if (row != null) {
                return getUser(row.getUuid("user_id"));
            }
            
            return Optional.empty();
        } catch (Exception e) {
            logger.error("Failed to get user by email: {}", email, e);
            return Optional.empty();
        }
    }
    
    public boolean updateUser(UUID userId, String firstName, String lastName) {
        try {
            Optional<User> existingUser = getUser(userId);
            if (!existingUser.isPresent()) {
                return false;
            }
            
            User user = existingUser.get();
            String updatedFirstName = firstName != null ? firstName : user.getFirstName();
            String updatedLastName = lastName != null ? lastName : user.getLastName();
            
            client.session.execute(updateUserStmt.bind(
                updatedFirstName, updatedLastName, Instant.now(), userId
            ));
            
            logger.info("Updated user: {}", userId);
            return true;
        } catch (Exception e) {
            logger.error("Failed to update user: {}", userId, e);
            return false;
        }
    }
}

// Main application
package com.example.cassandra;

import com.example.cassandra.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.Optional;
import java.util.UUID;

public class Application {
    private static final Logger logger = LoggerFactory.getLogger(Application.class);
    
    public static void main(String[] args) {
        CassandraClient client = null;
        
        try {
            // Initialize Cassandra client
            client = new CassandraClient(
                Arrays.asList("127.0.0.1"),
                "ecommerce",
                "datacenter1"
            );
            
            // Initialize repository
            UserRepository userRepository = new UserRepository(client);
            
            // Create user
            UUID userId = userRepository.createUser(
                "johndoe",
                "john@example.com",
                "John",
                "Doe"
            );
            logger.info("Created user: {}", userId);
            
            // Get user
            Optional<User> user = userRepository.getUser(userId);
            if (user.isPresent()) {
                logger.info("Retrieved user: {} ({})", 
                    user.get().getUsername(), user.get().getEmail());
            }
            
            // Update user
            boolean updated = userRepository.updateUser(userId, "John", "Smith");
            logger.info("User updated: {}", updated);
            
            // Get updated user
            Optional<User> updatedUser = userRepository.getUser(userId);
            if (updatedUser.isPresent()) {
                logger.info("Updated user: {} {}", 
                    updatedUser.get().getFirstName(), updatedUser.get().getLastName());
            }
            
        } catch (Exception e) {
            logger.error("Application error", e);
        } finally {
            if (client != null) {
                client.close();
            }
        }
    }
}
```

## Performance Optimization

### Tuning Parameters
```yaml
# cassandra.yaml optimizations
# JVM settings
MAX_HEAP_SIZE: "8G"
HEAP_NEWSIZE: "2G"

# Cassandra settings
concurrent_reads: 32
concurrent_writes: 32
concurrent_counter_writes: 32
concurrent_materialized_view_writes: 32

# Memtable settings
memtable_allocation_type: heap_buffers
memtable_heap_space_in_mb: 2048
memtable_offheap_space_in_mb: 2048

# Commit log settings
commitlog_sync: periodic
commitlog_sync_period_in_ms: 10000
commitlog_segment_size_in_mb: 32

# Compaction settings
compaction_throughput_mb_per_sec: 64
compaction_large_partition_warning_threshold_mb: 100

# Read/Write timeout settings
read_request_timeout_in_ms: 5000
range_request_timeout_in_ms: 10000
write_request_timeout_in_ms: 2000
counter_write_request_timeout_in_ms: 5000

# Cache settings
key_cache_size_in_mb: 200
row_cache_size_in_mb: 0
counter_cache_size_in_mb: 50
```

### Performance Monitoring Queries
```cql
-- Check cluster status
DESCRIBE CLUSTER;

-- Check keyspace and table info
DESCRIBE KEYSPACE ecommerce;
DESCRIBE TABLE users;

-- Check table statistics
SELECT * FROM system.size_estimates WHERE keyspace_name = 'ecommerce';

-- Check compaction stats
SELECT * FROM system.compaction_history LIMIT 10;

-- Check token ranges
SELECT * FROM system.local;
SELECT * FROM system.peers;
```

## Monitoring and Operations

### Prometheus Monitoring
```yaml
# cassandra-exporter.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cassandra-exporter
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cassandra-exporter
  template:
    metadata:
      labels:
        app: cassandra-exporter
    spec:
      containers:
      - name: cassandra-exporter
        image: criteord/cassandra_exporter:latest
        ports:
        - containerPort: 8080
        env:
        - name: CASSANDRA_HOST
          value: "cassandra.database.svc.cluster.local"
        - name: CASSANDRA_PORT
          value: "7199"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: cassandra-exporter
  namespace: monitoring
spec:
  selector:
    app: cassandra-exporter
  ports:
  - port: 8080
    targetPort: 8080
```

### Key Metrics to Monitor
```promql
# Cluster health
cassandra_cluster_status

# Read/Write latency
cassandra_clientrequest_latency{quantile="0.95"}

# Read/Write throughput
rate(cassandra_clientrequest_total[5m])

# Compaction pending tasks
cassandra_compaction_pendingtasks

# Heap memory usage
cassandra_jvm_memory_used{area="heap"}

# GC metrics
rate(cassandra_jvm_gc_total[5m])

# Connection metrics
cassandra_clientrequest_connections

# Storage metrics
cassandra_storage_totaldiskspaceused
```

## Backup and Recovery

### Backup Script
```bash
#!/bin/bash
# cassandra-backup.sh

# Configuration
CASSANDRA_HOST="localhost"
KEYSPACE="ecommerce"
BACKUP_DIR="/backups/cassandra"
S3_BUCKET="my-cassandra-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p ${BACKUP_DIR}/${DATE}

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a ${BACKUP_DIR}/backup.log
}

# Function to create snapshot
create_snapshot() {
    local snapshot_name="backup_${DATE}"
    
    log "Creating snapshot: ${snapshot_name}"
    
    # Create snapshot
    nodetool -h ${CASSANDRA_HOST} snapshot -t ${snapshot_name} ${KEYSPACE}
    
    if [ $? -eq 0 ]; then
        log "Snapshot created successfully"
        return 0
    else
        log "ERROR: Failed to create snapshot"
        return 1
    fi
}

# Function to copy snapshot data
copy_snapshot_data() {
    local snapshot_name="backup_${DATE}"
    local data_dir="/var/lib/cassandra/data"
    
    log "Copying snapshot data"
    
    # Find and copy snapshot directories
    find ${data_dir}/${KEYSPACE} -name "*${snapshot_name}*" -type d | while read snapshot_dir; do
        table_name=$(basename $(dirname ${snapshot_dir}))
        target_dir="${BACKUP_DIR}/${DATE}/${table_name}"
        
        mkdir -p ${target_dir}
        cp -r ${snapshot_dir}/* ${target_dir}/
        
        log "Copied snapshot for table: ${table_name}"
    done
    
    # Copy schema
    cqlsh -h ${CASSANDRA_HOST} -e "DESCRIBE KEYSPACE ${KEYSPACE};" > ${BACKUP_DIR}/${DATE}/schema.cql
    
    log "Schema exported"
}

# Function to create archive
create_archive() {
    log "Creating archive"
    
    cd ${BACKUP_DIR}
    tar -czf ${DATE}.tar.gz ${DATE}/
    
    if [ $? -eq 0 ]; then
        log "Archive created: ${DATE}.tar.gz"
        
        # Remove uncompressed directory
        rm -rf ${DATE}/
        
        return 0
    else
        log "ERROR: Failed to create archive"
        return 1
    fi
}

# Function to upload to S3
upload_to_s3() {
    local archive_file="${BACKUP_DIR}/${DATE}.tar.gz"
    
    if command -v aws &> /dev/null; then
        log "Uploading to S3: ${S3_BUCKET}"
        
        aws s3 cp ${archive_file} s3://${S3_BUCKET}/cassandra/${DATE}.tar.gz
        
        if [ $? -eq 0 ]; then
            log "S3 upload completed successfully"
            
            # Remove local archive after successful upload
            rm -f ${archive_file}
        else
            log "ERROR: S3 upload failed"
        fi
    else
        log "AWS CLI not found, skipping S3 upload"
    fi
}

# Function to cleanup old snapshots
cleanup_snapshots() {
    log "Cleaning up old snapshots"
    
    # List and remove old snapshots (keep last 3)
    nodetool -h ${CASSANDRA_HOST} listsnapshots | grep backup_ | sort -r | tail -n +4 | while read line; do
        snapshot_name=$(echo ${line} | awk '{print $1}')
        log "Removing old snapshot: ${snapshot_name}"
        nodetool -h ${CASSANDRA_HOST} clearsnapshot -t ${snapshot_name}
    done
}

# Function to cleanup old backups
cleanup_old_backups() {
    local retention_days=7
    
    log "Cleaning up backups older than ${retention_days} days"
    
    find ${BACKUP_DIR} -name "*.tar.gz" -mtime +${retention_days} -delete
    find ${BACKUP_DIR} -name "*.log" -mtime +${retention_days} -delete
}

# Main backup process
main() {
    log "Starting Cassandra backup process"
    
    # Create snapshot
    if create_snapshot; then
        # Copy snapshot data
        copy_snapshot_data
        
        # Create archive
        if create_archive; then
            # Upload to S3
            upload_to_s3
        fi
        
        # Cleanup old snapshots
        cleanup_snapshots
    fi
    
    # Cleanup old backups
    cleanup_old_backups
    
    log "Backup process completed"
}

# Run main function
main
```

## Best Practices

- Design tables based on query patterns, not normalized data structures
- Use appropriate partition keys to distribute data evenly
- Avoid large partitions (>100MB) and wide rows
- Use time-based partitioning for time-series data
- Implement proper data modeling with denormalization
- Monitor compaction and adjust strategies as needed
- Use appropriate consistency levels for your use case
- Regular maintenance tasks (repair, cleanup, compaction)
- Implement proper backup and disaster recovery procedures

## Great Resources

- [Cassandra Documentation](https://cassandra.apache.org/doc/latest/) - Official comprehensive documentation
- [DataStax Academy](https://academy.datastax.com/) - Free courses and training
- [Cassandra Data Modeling](https://cassandra.apache.org/doc/latest/data_modeling/) - Data modeling best practices
- [CQL Reference](https://cassandra.apache.org/doc/latest/cql/) - Complete CQL documentation
- [Cassandra GitHub](https://github.com/apache/cassandra) - Source code and community
- [Planet Cassandra](https://planetcassandra.org/) - Community resources and articles
- [Cassandra Performance](https://docs.datastax.com/en/dse-planning/docs/) - Performance tuning guide
- [Cassandra Operations](https://cassandra.apache.org/doc/latest/operating/) - Operations and maintenance guide