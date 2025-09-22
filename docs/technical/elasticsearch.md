# Elasticsearch

Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene. It provides near real-time search and analytics capabilities for all types of data, making it ideal for log analysis, full-text search, security intelligence, business analytics, and operational intelligence use cases.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Elasticsearch Tutorial for Beginners**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=gS_nHTWZEJ8)
- **Why it's great**: Perfect introduction covering core concepts and practical examples

#### **Complete Guide to Elasticsearch**
- **Channel**: KodeKloud
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=4q0bCb8MhYY)
- **Why it's great**: Comprehensive tutorial from basics to advanced features

#### **Elasticsearch and Kibana Tutorial**
- **Channel**: edureka!
- **Link**: [YouTube - 4 hours](https://www.youtube.com/watch?v=gQ1c1uILyKI)
- **Why it's great**: Complete ELK stack tutorial with hands-on demonstrations

### 📖 Essential Documentation

#### **Elasticsearch Official Documentation**
- **Link**: [elastic.co/guide/en/elasticsearch/reference/current/](https://www.elastic.co/guide/en/elasticsearch/reference/current/)
- **Why it's great**: Comprehensive official reference with examples and best practices

#### **Elasticsearch: The Definitive Guide**
- **Authors**: Clinton Gormley, Zachary Tong
- **Link**: [elastic.co/guide/en/elasticsearch/guide/current/](https://www.elastic.co/guide/en/elasticsearch/guide/current/)
- **Why it's great**: Free online book covering core concepts and practical usage

#### **Elastic Stack Documentation**
- **Link**: [elastic.co/guide/](https://www.elastic.co/guide/)
- **Why it's great**: Complete documentation for the entire Elastic ecosystem

### 📝 Must-Read Blogs & Articles

#### **Elastic Blog**
- **Source**: Elastic
- **Link**: [elastic.co/blog/](https://www.elastic.co/blog/)
- **Why it's great**: Official updates, use cases, and technical deep dives

#### **Elasticsearch Performance Tips**
- **Source**: Elastic
- **Link**: [elastic.co/blog/elasticsearch-performance-tuning-tips](https://www.elastic.co/blog/elasticsearch-performance-tuning-tips)
- **Why it's great**: Essential performance optimization strategies

#### **Search Relevance with Elasticsearch**
- **Source**: Sematext
- **Link**: [sematext.com/blog/elasticsearch-search-relevance/](https://sematext.com/blog/elasticsearch-search-relevance/)
- **Why it's great**: Practical guide to improving search quality

### 🎓 Structured Courses

#### **Elastic Certified Engineer**
- **Provider**: Elastic
- **Link**: [training.elastic.co/exam/elastic-certified-engineer](https://training.elastic.co/exam/elastic-certified-engineer)
- **Cost**: Paid certification
- **Why it's great**: Official certification with comprehensive training materials

#### **Complete Elasticsearch Masterclass with Logstash and Kibana**
- **Platform**: Udemy
- **Link**: [udemy.com/course/complete-elasticsearch-masterclass-with-kibana-and-logstash/](https://www.udemy.com/course/complete-elasticsearch-masterclass-with-kibana-and-logstash/)
- **Cost**: Paid
- **Why it's great**: Hands-on projects covering the entire ELK stack

### 🛠️ Tools & Platforms

#### **Elasticsearch Service (Cloud)**
- **Link**: [cloud.elastic.co](https://cloud.elastic.co/)
- **Why it's great**: Hosted Elasticsearch with free tier for learning

#### **Kibana Dev Tools**
- **Link**: [elastic.co/guide/en/kibana/current/console-kibana.html](https://www.elastic.co/guide/en/kibana/current/console-kibana.html)
- **Why it's great**: Interactive console for testing queries and APIs

#### **Elasticsearch Head Plugin**
- **Link**: [github.com/mobz/elasticsearch-head](https://github.com/mobz/elasticsearch-head)
- **Why it's great**: Web-based interface for cluster management and data browsing

## Overview

Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene. It provides near real-time search and analytics capabilities for all types of data, making it ideal for log analysis, full-text search, security intelligence, business analytics, and operational intelligence use cases.

## Architecture

### Core Components

#### 1. Cluster
- Collection of one or more nodes (servers)
- Shares data and provides federated indexing and search capabilities
- Identified by a unique cluster name

#### 2. Node
- Single server that stores data and participates in cluster's indexing and search
- Types of nodes:
  - **Master Node**: Manages cluster-wide operations
  - **Data Node**: Stores data and executes data-related operations
  - **Ingest Node**: Pre-processes documents before indexing
  - **Coordinating Node**: Routes requests, handles search reduce phase
  - **Machine Learning Node**: Runs machine learning jobs

#### 3. Index
- Collection of documents with similar characteristics
- Identified by a unique name
- Maps to one or more primary shards and zero or more replica shards

#### 4. Shard
- Subdivision of an index
- **Primary Shard**: Original horizontal partition of an index
- **Replica Shard**: Copy of a primary shard for high availability

#### 5. Document
- Basic unit of information that can be indexed
- Expressed in JSON format
- Belongs to a type within an index

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Elasticsearch Cluster                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Master Node │  │ Master Node │  │ Master Node │     │
│  │  (Eligible) │  │  (Active)   │  │  (Eligible) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Data Node  │  │  Data Node  │  │  Data Node  │     │
│  │   Shard 1   │  │   Shard 2   │  │   Shard 3   │     │
│  │  Replica 2  │  │  Replica 3  │  │  Replica 1  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐                       │
│  │ Ingest Node │  │ Coord Node  │                       │
│  └─────────────┘  └─────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

## Configuration Examples

### Basic Configuration (elasticsearch.yml)

```yaml
# ======================== Elasticsearch Configuration =========================
#
# ---------------------------------- Cluster -----------------------------------
cluster.name: production-logs
cluster.initial_master_nodes: ["es-master-01", "es-master-02", "es-master-03"]

# ------------------------------------ Node ------------------------------------
node.name: es-node-01
node.roles: ["master", "data", "ingest"]
node.attr.rack: rack1
node.attr.zone: us-east-1a

# ----------------------------------- Paths ------------------------------------
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
path.repo: ["/mnt/backups", "/mnt/snapshots"]

# ----------------------------------- Memory -----------------------------------
bootstrap.memory_lock: true

# ---------------------------------- Network -----------------------------------
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# --------------------------------- Discovery ----------------------------------
discovery.seed_hosts: ["es-master-01", "es-master-02", "es-master-03"]
discovery.type: multi-node

# ---------------------------------- Security ----------------------------------
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12

# ---------------------------------- Various -----------------------------------
action.destructive_requires_name: true
indices.query.bool.max_clause_count: 4096
```

### JVM Configuration (jvm.options)

```bash
# Heap size (adjust based on available memory)
-Xms16g
-Xmx16g

# G1GC Configuration
-XX:+UseG1GC
-XX:G1ReservePercent=25
-XX:InitiatingHeapOccupancyPercent=30

# GC logging
-Xlog:gc*,gc+age=trace,safepoint:file=/var/log/elasticsearch/gc.log:utctime,pid,tags:filecount=32,filesize=64m

# Error handling
-XX:+ExitOnOutOfMemoryError
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/lib/elasticsearch/heap-dump.hprof

# JVM performance
-XX:+AlwaysPreTouch
-XX:-OmitStackTraceInFastThrow
-Djava.awt.headless=true
```

### Index Template Example

```json
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "priority": 200,
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "refresh_interval": "30s",
      "codec": "best_compression",
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs-current"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "level": {
          "type": "keyword"
        },
        "host": {
          "type": "keyword"
        },
        "application": {
          "type": "keyword"
        },
        "trace_id": {
          "type": "keyword"
        }
      }
    }
  }
}
```

### Index Lifecycle Management Policy

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50GB",
            "max_age": "7d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          },
          "allocate": {
            "require": {
              "node.attr.box_type": "warm"
            }
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          },
          "allocate": {
            "require": {
              "node.attr.box_type": "cold"
            }
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

## Performance Tuning

### 1. Hardware Optimization

```yaml
# Recommended Hardware Specifications
Master Nodes:
  CPU: 4-8 cores
  RAM: 8-16 GB
  Disk: 100 GB SSD
  
Data Nodes:
  CPU: 16-32 cores
  RAM: 64-128 GB (50% for heap, 50% for OS cache)
  Disk: 4-8 TB NVMe SSD
  
Ingest Nodes:
  CPU: 8-16 cores
  RAM: 32-64 GB
  Disk: 500 GB SSD
```

### 2. Heap Size Configuration

```bash
# Calculate heap size (50% of RAM, max 32GB)
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
HEAP_SIZE=$((TOTAL_RAM / 2))
if [ $HEAP_SIZE -gt 32 ]; then
    HEAP_SIZE=32
fi

# Set in jvm.options
echo "-Xms${HEAP_SIZE}g" >> /etc/elasticsearch/jvm.options
echo "-Xmx${HEAP_SIZE}g" >> /etc/elasticsearch/jvm.options
```

### 3. Indexing Performance

```json
// Bulk indexing settings
PUT /logs-*/_settings
{
  "index": {
    "refresh_interval": "-1",
    "number_of_replicas": 0,
    "translog.durability": "async",
    "translog.flush_threshold_size": "1GB"
  }
}

// After bulk indexing
PUT /logs-*/_settings
{
  "index": {
    "refresh_interval": "30s",
    "number_of_replicas": 1,
    "translog.durability": "request"
  }
}
```

### 4. Query Performance

```json
// Use filters instead of queries when possible
GET /logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "status": "error" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  }
}

// Use source filtering
GET /logs-*/_search
{
  "_source": ["@timestamp", "message", "level"],
  "query": { ... }
}

// Optimize aggregations
GET /logs-*/_search
{
  "size": 0,
  "aggs": {
    "errors_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "1h",
        "min_doc_count": 1
      },
      "aggs": {
        "error_count": {
          "filter": { "term": { "level": "error" } }
        }
      }
    }
  }
}
```

### 5. Shard Optimization

```bash
# Calculate optimal shard size (20-50GB per shard)
# Example: 1TB daily data = 20-50 shards

# Set shard allocation awareness
PUT /_cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone,rack",
    "cluster.routing.allocation.awareness.force.zone.values": "us-east-1a,us-east-1b,us-east-1c"
  }
}
```

## Integration Patterns

### 1. Logstash Integration

```ruby
# Logstash output configuration
output {
  elasticsearch {
    hosts => ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
    index => "logs-%{[@metadata][target_index]}-%{+YYYY.MM.dd}"
    template_name => "logs-template"
    template => "/etc/logstash/templates/logs-template.json"
    
    # Security
    ssl => true
    ssl_certificate_verification => true
    cacert => "/etc/logstash/certs/ca.crt"
    user => "logstash_writer"
    password => "${LOGSTASH_PASSWORD}"
    
    # Performance
    pipeline => "logs-pipeline"
    bulk_path => "/_bulk"
    pool_max => 200
    pool_max_per_route => 100
    resurrect_delay => 5
    retry_on_conflict => 5
    
    # ILM
    ilm_enabled => true
    ilm_rollover_alias => "logs-current"
    ilm_pattern => "{now/d}-000001"
    ilm_policy => "logs-policy"
  }
}
```

### 2. Beats Integration

```yaml
# Filebeat configuration
output.elasticsearch:
  hosts: ["https://es-01:9200", "https://es-02:9200", "https://es-03:9200"]
  protocol: "https"
  username: "filebeat_writer"
  password: "${FILEBEAT_PASSWORD}"
  
  # SSL Configuration
  ssl.certificate_authorities: ["/etc/filebeat/certs/ca.crt"]
  ssl.certificate: "/etc/filebeat/certs/filebeat.crt"
  ssl.key: "/etc/filebeat/certs/filebeat.key"
  
  # Performance settings
  worker: 4
  bulk_max_size: 2048
  compression_level: 5
  
  # Index settings
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
  
  # Pipeline
  pipeline: "filebeat-pipeline"
  
  # ILM
  setup.ilm.enabled: true
  setup.ilm.rollover_alias: "filebeat-current"
  setup.ilm.pattern: "{now/d}-000001"
  setup.ilm.policy: "filebeat-policy"
```

### 3. Application Integration (Python)

```python
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import logging
from typing import List, Dict, Any

class ElasticsearchLogger:
    def __init__(self, hosts: List[str], index_prefix: str = "app-logs"):
        self.es = Elasticsearch(
            hosts=hosts,
            use_ssl=True,
            verify_certs=True,
            ca_certs="/path/to/ca.crt",
            client_cert="/path/to/client.crt",
            client_key="/path/to/client.key",
            # Connection pooling
            maxsize=100,
            # Retry configuration
            max_retries=3,
            retry_on_timeout=True,
            retry_on_status=[502, 503, 504]
        )
        self.index_prefix = index_prefix
        self.buffer = []
        self.buffer_size = 1000
        
    def log(self, level: str, message: str, **kwargs):
        """Log a message to Elasticsearch"""
        document = {
            "@timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "host": kwargs.get("host", "unknown"),
            "application": kwargs.get("application", "app"),
            "trace_id": kwargs.get("trace_id"),
            **kwargs
        }
        
        self.buffer.append({
            "_index": f"{self.index_prefix}-{datetime.utcnow().strftime('%Y.%m.%d')}",
            "_source": document
        })
        
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        """Flush buffer to Elasticsearch"""
        if not self.buffer:
            return
            
        try:
            helpers.bulk(
                self.es,
                self.buffer,
                chunk_size=500,
                max_retries=3,
                initial_backoff=2
            )
            self.buffer.clear()
        except Exception as e:
            logging.error(f"Failed to bulk index: {e}")
            # Implement fallback logic
```

### 4. Kafka Integration

```json
// Kafka Connect Elasticsearch Sink
{
  "name": "elasticsearch-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "connection.url": "https://es-01:9200,https://es-02:9200,https://es-03:9200",
    "connection.username": "kafka_connect",
    "connection.password": "${file:/opt/kafka/connect-secrets/elasticsearch-password:password}",
    
    "topics": "logs-topic,metrics-topic,events-topic",
    "type.name": "_doc",
    "key.ignore": "true",
    "schema.ignore": "true",
    
    "transforms": "TimestampRouter",
    "transforms.TimestampRouter.type": "org.apache.kafka.connect.transforms.TimestampRouter",
    "transforms.TimestampRouter.topic.format": "logs-${topic}-${timestamp}",
    "transforms.TimestampRouter.timestamp.format": "yyyy.MM.dd",
    
    "batch.size": 2000,
    "max.in.flight.requests": 5,
    "max.buffered.records": 20000,
    "linger.ms": 1000,
    
    "behavior.on.null.values": "delete",
    "behavior.on.malformed.documents": "warn",
    
    "elastic.security.protocol": "SSL",
    "elastic.https.ssl.truststore.location": "/opt/kafka/connect-certs/truststore.jks",
    "elastic.https.ssl.truststore.password": "${file:/opt/kafka/connect-secrets/truststore-password:password}",
    "elastic.https.ssl.keystore.location": "/opt/kafka/connect-certs/keystore.jks",
    "elastic.https.ssl.keystore.password": "${file:/opt/kafka/connect-secrets/keystore-password:password}"
  }
}
```

## Production Deployment Strategies

### 1. Kubernetes Deployment

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: production-cluster
  namespace: elastic-system
spec:
  version: 8.11.0
  
  nodeSets:
  # Master nodes
  - name: masters
    count: 3
    config:
      node.roles: ["master"]
      node.store.allow_mmap: false
    podTemplate:
      spec:
        nodeSelector:
          node-type: elasticsearch-master
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 8Gi
              cpu: 2
            limits:
              memory: 8Gi
              cpu: 4
          env:
          - name: ES_JAVA_OPTS
            value: "-Xms4g -Xmx4g"
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
        storageClassName: fast-ssd
  
  # Data nodes
  - name: data-hot
    count: 6
    config:
      node.roles: ["data_hot", "ingest"]
      node.attr.box_type: hot
    podTemplate:
      spec:
        nodeSelector:
          node-type: elasticsearch-data-hot
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 64Gi
              cpu: 16
            limits:
              memory: 64Gi
              cpu: 32
          env:
          - name: ES_JAVA_OPTS
            value: "-Xms32g -Xmx32g"
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 2Ti
        storageClassName: nvme-ssd
  
  # Coordinating nodes
  - name: coordinating
    count: 3
    config:
      node.roles: []
    podTemplate:
      spec:
        nodeSelector:
          node-type: elasticsearch-coord
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 16Gi
              cpu: 4
            limits:
              memory: 16Gi
              cpu: 8
          env:
          - name: ES_JAVA_OPTS
            value: "-Xms8g -Xmx8g"
            
  http:
    tls:
      selfSignedCertificate:
        subjectAltNames:
        - dns: elasticsearch.example.com
        - dns: "*.elasticsearch.example.com"
    service:
      spec:
        type: LoadBalancer
        loadBalancerIP: 10.0.0.100
```

### 2. Monitoring and Alerting

```yaml
# Prometheus rules
groups:
- name: elasticsearch
  interval: 30s
  rules:
  - alert: ElasticsearchClusterRed
    expr: elasticsearch_cluster_health_status{color="red"} == 1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Elasticsearch cluster is red"
      description: "Elasticsearch cluster {{ $labels.cluster }} is red for more than 5 minutes"
  
  - alert: ElasticsearchNodeDiskSpace
    expr: (1 - (elasticsearch_filesystem_data_available_bytes / elasticsearch_filesystem_data_size_bytes)) * 100 > 85
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Elasticsearch node disk space is running low"
      description: "Node {{ $labels.node }} disk usage is above 85%"
  
  - alert: ElasticsearchHeapUsage
    expr: (elasticsearch_jvm_memory_used_bytes{area="heap"} / elasticsearch_jvm_memory_max_bytes{area="heap"}) * 100 > 90
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Elasticsearch heap usage is high"
      description: "Node {{ $labels.node }} heap usage is above 90%"
  
  - alert: ElasticsearchPendingTasks
    expr: elasticsearch_cluster_health_number_of_pending_tasks > 100
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Elasticsearch has many pending tasks"
      description: "Cluster {{ $labels.cluster }} has {{ $value }} pending tasks"
```

### 3. Backup and Recovery

```bash
#!/bin/bash
# Snapshot repository setup
curl -X PUT "https://localhost:9200/_snapshot/s3_backup" \
  -H "Content-Type: application/json" \
  -u elastic:"${ELASTIC_PASSWORD}" \
  --cacert /etc/elasticsearch/certs/ca.crt \
  -d '{
    "type": "s3",
    "settings": {
      "bucket": "elasticsearch-backups",
      "region": "us-east-1",
      "base_path": "production-cluster",
      "compress": true,
      "chunk_size": "100m",
      "max_restore_bytes_per_sec": "100mb",
      "max_snapshot_bytes_per_sec": "40mb"
    }
  }'

# Create snapshot policy
curl -X PUT "https://localhost:9200/_slm/policy/daily-snapshots" \
  -H "Content-Type: application/json" \
  -u elastic:"${ELASTIC_PASSWORD}" \
  --cacert /etc/elasticsearch/certs/ca.crt \
  -d '{
    "schedule": "0 0 2 * * ?",
    "name": "<snapshot-{now/d{yyyy.MM.dd}}>",
    "repository": "s3_backup",
    "config": {
      "indices": ["logs-*", "metrics-*"],
      "include_global_state": false,
      "partial": true
    },
    "retention": {
      "expire_after": "30d",
      "min_count": 5,
      "max_count": 50
    }
  }'
```

### 4. Security Configuration

```yaml
# Security settings
xpack:
  security:
    enabled: true
    
    # Transport layer security
    transport:
      ssl:
        enabled: true
        verification_mode: certificate
        client_authentication: required
        keystore:
          path: elastic-certificates.p12
        truststore:
          path: elastic-certificates.p12
    
    # HTTP layer security
    http:
      ssl:
        enabled: true
        keystore:
          path: elastic-http.p12
        truststore:
          path: elastic-http.p12
    
    # Authentication
    authc:
      realms:
        native:
          native1:
            order: 0
        ldap:
          ldap1:
            order: 1
            url: "ldaps://ldap.example.com:636"
            bind_dn: "cn=elasticsearch,ou=services,dc=example,dc=com"
            user_search:
              base_dn: "ou=users,dc=example,dc=com"
              filter: "(uid={0})"
            group_search:
              base_dn: "ou=groups,dc=example,dc=com"
            ssl:
              certificate_authorities: ["/etc/elasticsearch/certs/ldap-ca.crt"]
        saml:
          saml1:
            order: 2
            idp:
              metadata:
                path: "/etc/elasticsearch/saml/idp-metadata.xml"
              entity_id: "https://idp.example.com"
            sp:
              entity_id: "https://elasticsearch.example.com"
              acs: "https://elasticsearch.example.com:9200/_security/saml/acs"
    
    # Authorization
    authz:
      anonymous:
        roles: anonymous_read_only
        authz_exception: true
```

### 5. Multi-Region Deployment

```yaml
# Cross-cluster replication setup
PUT /_ccr/follow/logs-us-west
{
  "remote_cluster": "us-west-cluster",
  "leader_index_patterns": ["logs-*"],
  "follow_index_pattern": "{{leader_index}}-replica",
  "settings": {
    "index.number_of_replicas": 0
  },
  "max_read_request_operation_count": 5120,
  "max_outstanding_read_requests": 12,
  "max_read_request_size": "32mb",
  "max_write_request_operation_count": 5120,
  "max_write_request_size": "9223372036854775807b",
  "max_outstanding_write_requests": 9,
  "max_write_buffer_count": 2147483647,
  "max_write_buffer_size": "512mb",
  "max_retry_delay": "500ms",
  "read_poll_timeout": "1m"
}

# Remote cluster configuration
PUT /_cluster/settings
{
  "persistent": {
    "cluster.remote": {
      "us-west-cluster": {
        "seeds": ["es-west-01:9300", "es-west-02:9300", "es-west-03:9300"],
        "transport.ping_schedule": "30s"
      },
      "eu-central-cluster": {
        "seeds": ["es-eu-01:9300", "es-eu-02:9300", "es-eu-03:9300"],
        "transport.ping_schedule": "30s"
      }
    }
  }
}
```

## Best Practices

### 1. Cluster Sizing
- Start with 3 master-eligible nodes for high availability
- Use dedicated master nodes for clusters > 10 nodes
- Allocate 50% of RAM to heap (max 32GB)
- Keep shard sizes between 20-50GB
- Aim for < 20 shards per GB of heap

### 2. Index Management
- Use Index Lifecycle Management (ILM) for automatic rollover
- Implement time-based indices for logs
- Use index templates for consistent mappings
- Enable compression for older indices
- Delete or archive old data regularly

### 3. Security
- Always enable TLS/SSL for transport and HTTP
- Use role-based access control (RBAC)
- Implement API key authentication for applications
- Enable audit logging for compliance
- Regular security updates and patches

### 4. Monitoring
- Monitor cluster health and node statistics
- Set up alerts for disk space, heap usage, and cluster state
- Track indexing and search performance
- Monitor garbage collection metrics
- Use Elastic Stack monitoring or Prometheus

### 5. Disaster Recovery
- Regular automated snapshots
- Test restore procedures
- Multi-region deployment for critical data
- Document recovery procedures
- Maintain runbooks for common issues

## Comprehensive Resources

### 📚 Official Documentation & References
- [Elasticsearch Official Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/)
- [Elasticsearch REST API Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- [Elasticsearch Java API Client](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/)
- [Elasticsearch Configuration Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html)

### 🎓 Learning Resources
- [Elastic Certified Engineer Program](https://www.elastic.co/training/certification)
- [Elasticsearch Training Courses](https://www.elastic.co/training/)
- [Getting Started with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
- [Elasticsearch Tutorials on Elastic.co](https://www.elastic.co/blog/category/elasticsearch)

### 🛠️ Essential Tools
- [Kibana](https://www.elastic.co/kibana/) - Data visualization and exploration
- [Elasticsearch Head](https://github.com/mobz/elasticsearch-head) - Web front end for browsing and interacting
- [Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/current/) - Index management tool
- [Rally](https://github.com/elastic/rally) - Performance benchmarking tool
- [Elasticdump](https://github.com/elasticsearch-dump/elasticsearch-dump) - Import/export tool

### 🏗️ Projects & Examples
- [Elasticsearch Examples Repository](https://github.com/elastic/elasticsearch/tree/main/docs/reference)
- [Log Analysis with ELK Stack](https://github.com/deviantony/docker-elk)
- [Elasticsearch Docker Examples](https://github.com/elastic/elasticsearch/tree/main/docs/reference/setup/install/docker)
- [Search Analytics Dashboard](https://github.com/elastic/app-search-reference-ui-react)

### 👥 Community & Support
- [Elastic Community Forum](https://discuss.elastic.co/)
- [Stack Overflow - elasticsearch](https://stackoverflow.com/questions/tagged/elasticsearch)
- [Elasticsearch Reddit](https://www.reddit.com/r/elasticsearch/)
- [Elastic Slack Community](https://ela.st/slack)
- [GitHub - Elasticsearch Issues](https://github.com/elastic/elasticsearch/issues)

### 📊 Monitoring & Observability
- [Elastic Stack Monitoring](https://www.elastic.co/guide/en/elasticsearch/reference/current/monitor-elasticsearch-cluster.html)
- [Metricbeat for Elasticsearch](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-elasticsearch.html)
- [Elasticsearch Prometheus Exporter](https://github.com/justwatchcom/elasticsearch_exporter)
- [Grafana Elasticsearch Dashboards](https://grafana.com/grafana/dashboards/?search=elasticsearch)

### 🔐 Security Resources
- [Elasticsearch Security Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html)
- [X-Pack Security Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-getting-started.html)
- [Authentication and Authorization](https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-up-authentication.html)
- [TLS/SSL Configuration](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html)

### 📈 Advanced Topics
- [Machine Learning in Elasticsearch](https://www.elastic.co/guide/en/machine-learning/current/)
- [Cross-Cluster Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html)
- [Index Lifecycle Management](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)
- [Elasticsearch Performance Tuning](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html)

### 🎥 Video Content
- [Elastic YouTube Channel](https://www.youtube.com/c/elasticsearch)
- [ElasticON Conference Videos](https://www.elastic.co/elasticon/)
- [Elasticsearch Tutorial Series](https://www.youtube.com/playlist?list=PLhLSfisesZIvgGh_VoFFsHhIQf7L4aHS5)
- [ELK Stack Crash Course](https://www.youtube.com/watch?v=ksTxFm40L48)

### 📖 Books & Publications
- "Elasticsearch: The Definitive Guide" by Zachary Tong and Lee Chin
- "Learning Elastic Stack 7.0" by Pranav Shukla
- "Mastering Elasticsearch" by Bharvi Dixit
- "Elasticsearch in Action" by Radu Gheorghe
- [Elastic Blog](https://www.elastic.co/blog/) - Latest updates and best practices