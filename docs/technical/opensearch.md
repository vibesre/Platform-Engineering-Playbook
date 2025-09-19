# OpenSearch

OpenSearch is a community-driven, open-source search and analytics suite derived from Elasticsearch 7.10.2 & Kibana 7.10.2. It provides a distributed, multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents.

## Installation

### Docker Installation
```bash
# Single-node cluster
docker run -d \
  --name opensearch-node1 \
  -p 9200:9200 \
  -p 9600:9600 \
  -e "discovery.type=single-node" \
  -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=MyStrongPassword123!" \
  opensearchproject/opensearch:latest

# Multi-node cluster with Docker Compose
cat > docker-compose.yml << EOF
version: '3'
services:
  opensearch-node1:
    image: opensearchproject/opensearch:latest
    container_name: opensearch-node1
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node1
      - discovery.seed_hosts=opensearch-node1,opensearch-node2
      - cluster.initial_cluster_manager_nodes=opensearch-node1,opensearch-node2
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
      - "OPENSEARCH_INITIAL_ADMIN_PASSWORD=MyStrongPassword123!"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data1:/usr/share/opensearch/data
    ports:
      - 9200:9200
      - 9600:9600
    networks:
      - opensearch-net

  opensearch-node2:
    image: opensearchproject/opensearch:latest
    container_name: opensearch-node2
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node2
      - discovery.seed_hosts=opensearch-node1,opensearch-node2
      - cluster.initial_cluster_manager_nodes=opensearch-node1,opensearch-node2
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
      - "OPENSEARCH_INITIAL_ADMIN_PASSWORD=MyStrongPassword123!"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data2:/usr/share/opensearch/data
    networks:
      - opensearch-net

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    container_name: opensearch-dashboards
    ports:
      - 5601:5601
    expose:
      - "5601"
    environment:
      OPENSEARCH_HOSTS: '["https://opensearch-node1:9200","https://opensearch-node2:9200"]'
    networks:
      - opensearch-net

volumes:
  opensearch-data1:
  opensearch-data2:

networks:
  opensearch-net:
EOF

docker-compose up -d
```

### Native Installation
```bash
# Ubuntu/Debian
curl -o- https://artifacts.opensearch.org/publickeys/opensearch.pgp | sudo apt-key add -
echo "deb https://artifacts.opensearch.org/releases/bundle/opensearch/2.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/opensearch-2.x.list
sudo apt update
sudo apt install opensearch

# CentOS/RHEL/Amazon Linux
sudo curl -SL https://artifacts.opensearch.org/releases/bundle/opensearch/2.x/opensearch-2.x.repo -o /etc/yum.repos.d/opensearch-2.x.repo
sudo yum install opensearch

# Manual installation
wget https://artifacts.opensearch.org/releases/bundle/opensearch/2.11.0/opensearch-2.11.0-linux-x64.tar.gz
tar -xzf opensearch-2.11.0-linux-x64.tar.gz
cd opensearch-2.11.0

# Set initial admin password
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=MyStrongPassword123!

# Start OpenSearch
./bin/opensearch
```

### Kubernetes Installation
```yaml
# opensearch-cluster.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: opensearch
---
apiVersion: v1
kind: Secret
metadata:
  name: opensearch-admin-password
  namespace: opensearch
type: Opaque
data:
  password: TXlTdHJvbmdQYXNzd29yZDEyMyE=  # MyStrongPassword123!
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: opensearch-config
  namespace: opensearch
data:
  opensearch.yml: |
    cluster.name: opensearch-cluster
    network.host: 0.0.0.0
    plugins.security.ssl.transport.pemcert_filepath: esnode.pem
    plugins.security.ssl.transport.pemkey_filepath: esnode-key.pem
    plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
    plugins.security.ssl.transport.enforce_hostname_verification: false
    plugins.security.ssl.http.enabled: true
    plugins.security.ssl.http.pemcert_filepath: esnode.pem
    plugins.security.ssl.http.pemkey_filepath: esnode-key.pem
    plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem
    plugins.security.allow_unsafe_democertificates: true
    plugins.security.allow_default_init_securityindex: true
    plugins.security.authcz.admin_dn:
      - CN=kirk,OU=client,O=client,L=test,C=de
    plugins.security.audit.type: internal_opensearch
    plugins.security.enable_snapshot_restore_privilege: true
    plugins.security.check_snapshot_restore_write_privileges: true
    plugins.security.restapi.roles_enabled: ["all_access", "security_rest_api_access"]
    cluster.routing.allocation.disk.threshold_enabled: false
    node.max_local_storage_nodes: 3
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: opensearch-cluster
  namespace: opensearch
spec:
  serviceName: opensearch
  replicas: 3
  selector:
    matchLabels:
      app: opensearch
  template:
    metadata:
      labels:
        app: opensearch
    spec:
      securityContext:
        fsGroup: 1000
      initContainers:
      - name: sysctl
        image: busybox:latest
        securityContext:
          privileged: true
        command:
        - sh
        - -c
        - |
          sysctl -w vm.max_map_count=262144
          sysctl -w fs.file-max=65536
          ulimit -n 65536
          ulimit -u 4096
      containers:
      - name: opensearch
        image: opensearchproject/opensearch:latest
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
        - containerPort: 9600
          name: metrics
        env:
        - name: cluster.name
          value: opensearch-cluster
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: discovery.seed_hosts
          value: "opensearch-cluster-0.opensearch,opensearch-cluster-1.opensearch,opensearch-cluster-2.opensearch"
        - name: cluster.initial_cluster_manager_nodes
          value: "opensearch-cluster-0,opensearch-cluster-1,opensearch-cluster-2"
        - name: bootstrap.memory_lock
          value: "true"
        - name: OPENSEARCH_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: opensearch-admin-password
              key: password
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: opensearch-data
          mountPath: /usr/share/opensearch/data
        - name: opensearch-config
          mountPath: /usr/share/opensearch/config/opensearch.yml
          subPath: opensearch.yml
        securityContext:
          capabilities:
            add:
              - IPC_LOCK
              - SYS_RESOURCE
      volumes:
      - name: opensearch-config
        configMap:
          name: opensearch-config
  volumeClaimTemplates:
  - metadata:
      name: opensearch-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: opensearch
  namespace: opensearch
spec:
  clusterIP: None
  selector:
    app: opensearch
  ports:
  - port: 9200
    name: http
  - port: 9300
    name: transport
---
apiVersion: v1
kind: Service
metadata:
  name: opensearch-dashboards
  namespace: opensearch
spec:
  type: LoadBalancer
  selector:
    app: opensearch-dashboards
  ports:
  - port: 5601
    targetPort: 5601
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opensearch-dashboards
  namespace: opensearch
spec:
  replicas: 1
  selector:
    matchLabels:
      app: opensearch-dashboards
  template:
    metadata:
      labels:
        app: opensearch-dashboards
    spec:
      containers:
      - name: opensearch-dashboards
        image: opensearchproject/opensearch-dashboards:latest
        ports:
        - containerPort: 5601
        env:
        - name: OPENSEARCH_HOSTS
          value: '["https://opensearch:9200"]'
        - name: OPENSEARCH_USERNAME
          value: admin
        - name: OPENSEARCH_PASSWORD
          valueFrom:
            secretKeyRef:
              name: opensearch-admin-password
              key: password

# Apply the configuration
kubectl apply -f opensearch-cluster.yaml
```

## Basic Configuration

### Node Configuration
```yaml
# opensearch.yml
cluster.name: my-opensearch-cluster
node.name: node-1
node.roles: [cluster_manager, data, ingest, remote_cluster_client]

# Network settings
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# Discovery settings
discovery.seed_hosts: ["node1", "node2", "node3"]
cluster.initial_cluster_manager_nodes: ["node1", "node2", "node3"]

# Memory settings
bootstrap.memory_lock: true

# Security settings
plugins.security.ssl.transport.pemcert_filepath: esnode.pem
plugins.security.ssl.transport.pemkey_filepath: esnode-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: esnode.pem
plugins.security.ssl.http.pemkey_filepath: esnode-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem

# Performance settings
indices.memory.index_buffer_size: 10%
indices.memory.min_index_buffer_size: 48mb
thread_pool.write.queue_size: 1000
thread_pool.search.queue_size: 1000
```

### JVM Configuration
```bash
# jvm.options
-Xms2g
-Xmx2g

# GC settings
-XX:+UseConcMarkSweepGC
-XX:CMSInitiatingOccupancyFraction=75
-XX:+UseCMSInitiatingOccupancyOnly

# Heap dump settings
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/lib/opensearch

# GC logging
-Xlog:gc*,gc+age=trace,safepoint:gc.log:utctime,pid,tid,level
-Xlog:gc:gc.log

# JVM options for large heaps
-XX:+UseG1GC
-XX:G1HeapRegionSize=32m
-XX:+UnlockExperimentalVMOptions
-XX:+UseJVMCICompiler
```

## Data Management

### Index Management
```bash
# Create index with mapping
curl -X PUT "localhost:9200/products" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "my_analyzer"
      },
      "description": {
        "type": "text",
        "analyzer": "my_analyzer"
      },
      "price": {
        "type": "double"
      },
      "category": {
        "type": "keyword"
      },
      "tags": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      },
      "location": {
        "type": "geo_point"
      },
      "metadata": {
        "type": "object",
        "enabled": false
      }
    }
  }
}'

# Index documents
curl -X POST "localhost:9200/products/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "Laptop",
  "description": "High-performance laptop for gaming",
  "price": 1299.99,
  "category": "electronics",
  "tags": ["laptop", "gaming", "electronics"],
  "created_at": "2023-01-15 10:30:00",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "metadata": {
    "internal_id": "PROD-12345",
    "supplier": "TechCorp"
  }
}'

# Bulk indexing
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' -d'
{"index": {"_index": "products", "_id": "2"}}
{"name": "Smartphone", "price": 699.99, "category": "electronics"}
{"index": {"_index": "products", "_id": "3"}}
{"name": "Headphones", "price": 149.99, "category": "electronics"}
{"update": {"_index": "products", "_id": "1"}}
{"doc": {"price": 1199.99}}
'
```

### Search Operations
```bash
# Simple search
curl -X GET "localhost:9200/products/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}'

# Complex search with filters and aggregations
curl -X GET "localhost:9200/products/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "description": "gaming"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "price": {
              "gte": 500,
              "lte": 2000
            }
          }
        },
        {
          "terms": {
            "category": ["electronics", "computers"]
          }
        }
      ]
    }
  },
  "sort": [
    {
      "price": {
        "order": "desc"
      }
    }
  ],
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          {"to": 500},
          {"from": 500, "to": 1000},
          {"from": 1000}
        ]
      }
    },
    "categories": {
      "terms": {
        "field": "category",
        "size": 10
      }
    }
  },
  "highlight": {
    "fields": {
      "description": {}
    }
  },
  "from": 0,
  "size": 20
}'

# Geo search
curl -X GET "localhost:9200/products/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "filter": {
        "geo_distance": {
          "distance": "10km",
          "location": {
            "lat": 40.7128,
            "lon": -74.0060
          }
        }
      }
    }
  }
}'
```

## Python Client Usage

### Basic Client Setup
```python
# requirements.txt
opensearch-py>=2.3.0
requests>=2.28.0
urllib3>=1.26.0

# opensearch_client.py
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk, scan
import json
import ssl
from datetime import datetime, timedelta
import logging

class OpenSearchClient:
    def __init__(self, hosts, username='admin', password='admin', use_ssl=True, verify_certs=False):
        self.client = OpenSearch(
            hosts=hosts,
            http_auth=(username, password),
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            timeout=30,
            max_retries=10,
            retry_on_timeout=True
        )
    
    def health_check(self):
        """Check cluster health"""
        try:
            health = self.client.cluster.health()
            return health
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return None
    
    def create_index(self, index_name, mapping=None, settings=None):
        """Create an index with optional mapping and settings"""
        body = {}
        if settings:
            body['settings'] = settings
        if mapping:
            body['mappings'] = mapping
        
        try:
            response = self.client.indices.create(index=index_name, body=body)
            logging.info(f"Index '{index_name}' created successfully")
            return response
        except Exception as e:
            logging.error(f"Failed to create index '{index_name}': {e}")
            return None
    
    def index_document(self, index_name, doc_id, document):
        """Index a single document"""
        try:
            response = self.client.index(
                index=index_name,
                id=doc_id,
                body=document,
                refresh=True
            )
            return response
        except Exception as e:
            logging.error(f"Failed to index document: {e}")
            return None
    
    def bulk_index(self, index_name, documents):
        """Bulk index multiple documents"""
        actions = []
        for doc_id, document in documents.items():
            action = {
                "_index": index_name,
                "_id": doc_id,
                "_source": document
            }
            actions.append(action)
        
        try:
            response = bulk(self.client, actions)
            logging.info(f"Bulk indexed {len(actions)} documents")
            return response
        except Exception as e:
            logging.error(f"Bulk indexing failed: {e}")
            return None
    
    def search(self, index_name, query, size=10, from_=0, sort=None, aggs=None):
        """Perform search query"""
        body = {
            "query": query,
            "size": size,
            "from": from_
        }
        
        if sort:
            body["sort"] = sort
        if aggs:
            body["aggs"] = aggs
        
        try:
            response = self.client.search(index=index_name, body=body)
            return response
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return None
    
    def scroll_search(self, index_name, query, scroll_size=1000, scroll_timeout='5m'):
        """Perform scrolling search for large result sets"""
        try:
            for doc in scan(
                self.client,
                query={"query": query},
                index=index_name,
                size=scroll_size,
                scroll=scroll_timeout
            ):
                yield doc
        except Exception as e:
            logging.error(f"Scroll search failed: {e}")
    
    def update_document(self, index_name, doc_id, update_doc):
        """Update a document"""
        try:
            response = self.client.update(
                index=index_name,
                id=doc_id,
                body={"doc": update_doc},
                refresh=True
            )
            return response
        except Exception as e:
            logging.error(f"Failed to update document: {e}")
            return None
    
    def delete_document(self, index_name, doc_id):
        """Delete a document"""
        try:
            response = self.client.delete(
                index=index_name,
                id=doc_id,
                refresh=True
            )
            return response
        except Exception as e:
            logging.error(f"Failed to delete document: {e}")
            return None
    
    def create_index_template(self, template_name, index_patterns, template_body):
        """Create an index template"""
        try:
            response = self.client.indices.put_template(
                name=template_name,
                body={
                    "index_patterns": index_patterns,
                    **template_body
                }
            )
            logging.info(f"Template '{template_name}' created successfully")
            return response
        except Exception as e:
            logging.error(f"Failed to create template: {e}")
            return None

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client
    client = OpenSearchClient(
        hosts=[{'host': 'localhost', 'port': 9200}],
        username='admin',
        password='MyStrongPassword123!'
    )
    
    # Check cluster health
    health = client.health_check()
    if health:
        print(f"Cluster status: {health['status']}")
    
    # Create index with mapping
    mapping = {
        "properties": {
            "title": {"type": "text", "analyzer": "standard"},
            "content": {"type": "text", "analyzer": "standard"},
            "timestamp": {"type": "date"},
            "category": {"type": "keyword"},
            "tags": {"type": "keyword"},
            "author": {
                "properties": {
                    "name": {"type": "text"},
                    "email": {"type": "keyword"}
                }
            }
        }
    }
    
    settings = {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "content_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "stemmer"]
                }
            },
            "filter": {
                "stemmer": {
                    "type": "stemmer",
                    "language": "english"
                }
            }
        }
    }
    
    client.create_index("blog_posts", mapping, settings)
    
    # Index sample documents
    documents = {
        "1": {
            "title": "OpenSearch Tutorial",
            "content": "Learn how to use OpenSearch for full-text search",
            "timestamp": "2023-01-15T10:30:00",
            "category": "tutorial",
            "tags": ["search", "opensearch", "elasticsearch"],
            "author": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        },
        "2": {
            "title": "Advanced Search Techniques",
            "content": "Master complex queries and aggregations",
            "timestamp": "2023-01-16T14:20:00",
            "category": "advanced",
            "tags": ["search", "queries", "aggregations"],
            "author": {
                "name": "Jane Smith",
                "email": "jane@example.com"
            }
        }
    }
    
    client.bulk_index("blog_posts", documents)
    
    # Perform search
    query = {
        "bool": {
            "must": [
                {"match": {"content": "search"}}
            ],
            "filter": [
                {"terms": {"tags": ["opensearch", "elasticsearch"]}}
            ]
        }
    }
    
    aggs = {
        "categories": {
            "terms": {"field": "category"}
        },
        "authors": {
            "terms": {"field": "author.name.keyword"}
        }
    }
    
    results = client.search("blog_posts", query, aggs=aggs)
    if results:
        print(f"Found {results['hits']['total']['value']} documents")
        for hit in results['hits']['hits']:
            print(f"- {hit['_source']['title']} (Score: {hit['_score']})")
```

## Advanced Features

### Index Lifecycle Management (ISM)
```python
# ism_policy.py
import json

def create_ism_policy(client, policy_name):
    """Create Index State Management policy"""
    policy = {
        "policy": {
            "description": "Log rotation policy",
            "default_state": "hot",
            "states": [
                {
                    "name": "hot",
                    "actions": [
                        {
                            "rollover": {
                                "min_index_age": "1d",
                                "min_doc_count": 1000000
                            }
                        }
                    ],
                    "transitions": [
                        {
                            "state_name": "warm",
                            "conditions": {
                                "min_index_age": "7d"
                            }
                        }
                    ]
                },
                {
                    "name": "warm",
                    "actions": [
                        {
                            "replica_count": {
                                "number_of_replicas": 0
                            }
                        },
                        {
                            "force_merge": {
                                "max_num_segments": 1
                            }
                        }
                    ],
                    "transitions": [
                        {
                            "state_name": "cold",
                            "conditions": {
                                "min_index_age": "30d"
                            }
                        }
                    ]
                },
                {
                    "name": "cold",
                    "actions": [],
                    "transitions": [
                        {
                            "state_name": "delete",
                            "conditions": {
                                "min_index_age": "90d"
                            }
                        }
                    ]
                },
                {
                    "name": "delete",
                    "actions": [
                        {
                            "delete": {}
                        }
                    ]
                }
            ],
            "ism_template": {
                "index_patterns": ["logs-*"],
                "priority": 100
            }
        }
    }
    
    try:
        response = client.transport.perform_request(
            'PUT',
            f'/_plugins/_ism/policies/{policy_name}',
            body=policy
        )
        print(f"ISM policy '{policy_name}' created successfully")
        return response
    except Exception as e:
        print(f"Failed to create ISM policy: {e}")
        return None

def apply_ism_policy(client, index_name, policy_name):
    """Apply ISM policy to an index"""
    try:
        response = client.transport.perform_request(
            'POST',
            f'/_plugins/_ism/add/{index_name}',
            body={"policy_id": policy_name}
        )
        print(f"ISM policy '{policy_name}' applied to index '{index_name}'")
        return response
    except Exception as e:
        print(f"Failed to apply ISM policy: {e}")
        return None
```

### Alerting Configuration
```python
# alerting.py
def create_monitor(client, monitor_name):
    """Create alerting monitor"""
    monitor = {
        "type": "monitor",
        "name": monitor_name,
        "enabled": True,
        "schedule": {
            "period": {
                "interval": 1,
                "unit": "MINUTES"
            }
        },
        "inputs": [
            {
                "search": {
                    "indices": ["logs-*"],
                    "query": {
                        "size": 0,
                        "query": {
                            "bool": {
                                "filter": [
                                    {
                                        "range": {
                                            "@timestamp": {
                                                "gte": "now-5m"
                                            }
                                        }
                                    },
                                    {
                                        "term": {
                                            "level": "ERROR"
                                        }
                                    }
                                ]
                            }
                        },
                        "aggs": {
                            "error_count": {
                                "value_count": {
                                    "field": "message"
                                }
                            }
                        }
                    }
                }
            }
        ],
        "triggers": [
            {
                "name": "High error rate",
                "severity": "1",
                "condition": {
                    "script": {
                        "source": "ctx.results[0].aggregations.error_count.value > 10",
                        "lang": "painless"
                    }
                },
                "actions": [
                    {
                        "name": "send_email",
                        "destination_id": "email_destination_id",
                        "message_template": {
                            "source": "High error rate detected: {{ctx.results.0.aggregations.error_count.value}} errors in the last 5 minutes",
                            "lang": "mustache"
                        },
                        "throttle_enabled": True,
                        "throttle": {
                            "value": 10,
                            "unit": "MINUTES"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = client.transport.perform_request(
            'POST',
            '/_plugins/_alerting/monitors',
            body=monitor
        )
        print(f"Monitor '{monitor_name}' created successfully")
        return response
    except Exception as e:
        print(f"Failed to create monitor: {e}")
        return None
```

## Performance Optimization

### Query Optimization
```python
# query_optimization.py
class QueryOptimizer:
    def __init__(self, client):
        self.client = client
    
    def analyze_slow_queries(self, index_name, time_threshold='100ms'):
        """Analyze slow queries"""
        try:
            # Enable slow log
            settings = {
                "index.search.slowlog.threshold.query.warn": time_threshold,
                "index.search.slowlog.threshold.query.info": "50ms",
                "index.search.slowlog.threshold.query.debug": "20ms",
                "index.search.slowlog.threshold.query.trace": "10ms"
            }
            
            self.client.indices.put_settings(
                index=index_name,
                body={"settings": settings}
            )
            
            print(f"Slow query logging enabled for index '{index_name}'")
        except Exception as e:
            print(f"Failed to enable slow query logging: {e}")
    
    def profile_search(self, index_name, query):
        """Profile search performance"""
        try:
            body = {
                "profile": True,
                "query": query
            }
            
            response = self.client.search(index=index_name, body=body)
            
            # Extract profiling information
            profile_data = response.get('profile', {})
            shards = profile_data.get('shards', [])
            
            for shard in shards:
                searches = shard.get('searches', [])
                for search in searches:
                    query_data = search.get('query', [])
                    for q in query_data:
                        print(f"Query type: {q['type']}")
                        print(f"Time: {q['time_in_nanos']} ns")
                        print(f"Breakdown: {q['breakdown']}")
            
            return profile_data
        except Exception as e:
            print(f"Failed to profile search: {e}")
            return None
    
    def optimize_index(self, index_name):
        """Optimize index for search performance"""
        try:
            # Force merge to reduce segments
            self.client.indices.forcemerge(
                index=index_name,
                max_num_segments=1
            )
            
            # Update index settings
            settings = {
                "index": {
                    "refresh_interval": "30s",
                    "number_of_replicas": 0,
                    "translog.flush_threshold_size": "1gb",
                    "merge.policy.max_merged_segment": "5gb"
                }
            }
            
            self.client.indices.put_settings(
                index=index_name,
                body={"settings": settings}
            )
            
            print(f"Index '{index_name}' optimized")
        except Exception as e:
            print(f"Failed to optimize index: {e}")
```

### Cluster Monitoring
```python
# monitoring.py
import time
from datetime import datetime

class ClusterMonitor:
    def __init__(self, client):
        self.client = client
    
    def get_cluster_stats(self):
        """Get comprehensive cluster statistics"""
        try:
            stats = {
                'health': self.client.cluster.health(),
                'stats': self.client.cluster.stats(),
                'nodes': self.client.nodes.stats(),
                'indices': self.client.indices.stats()
            }
            return stats
        except Exception as e:
            print(f"Failed to get cluster stats: {e}")
            return None
    
    def monitor_performance(self, interval=60):
        """Monitor cluster performance metrics"""
        print(f"Starting cluster monitoring (interval: {interval}s)")
        
        while True:
            try:
                timestamp = datetime.now().isoformat()
                stats = self.get_cluster_stats()
                
                if stats:
                    health = stats['health']
                    cluster_stats = stats['stats']
                    
                    print(f"\n[{timestamp}] Cluster Health:")
                    print(f"  Status: {health['status']}")
                    print(f"  Nodes: {health['number_of_nodes']}")
                    print(f"  Active Shards: {health['active_shards']}")
                    print(f"  Relocating Shards: {health['relocating_shards']}")
                    print(f"  Unassigned Shards: {health['unassigned_shards']}")
                    
                    indices_stats = cluster_stats['indices']
                    print(f"\n[{timestamp}] Indices Stats:")
                    print(f"  Total Indices: {indices_stats['count']}")
                    print(f"  Total Documents: {indices_stats['docs']['count']}")
                    print(f"  Store Size: {indices_stats['store']['size_in_bytes'] / (1024**3):.2f} GB")
                    
                    nodes_stats = stats['nodes']
                    print(f"\n[{timestamp}] Nodes Performance:")
                    for node_id, node_stats in nodes_stats['nodes'].items():
                        node_name = node_stats['name']
                        jvm = node_stats['jvm']
                        os = node_stats['os']
                        
                        print(f"  Node: {node_name}")
                        print(f"    Heap Used: {jvm['mem']['heap_used_percent']}%")
                        print(f"    CPU Usage: {os['cpu']['percent']}%")
                        print(f"    Load Average: {os.get('cpu', {}).get('load_average', {}).get('1m', 'N/A')}")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped")
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(interval)
    
    def check_shard_allocation(self):
        """Check shard allocation and balance"""
        try:
            allocation = self.client.cat.allocation(format='json')
            shards = self.client.cat.shards(format='json')
            
            print("Shard Allocation Summary:")
            for alloc in allocation:
                print(f"  Node: {alloc['node']}")
                print(f"    Shards: {alloc['shards']}")
                print(f"    Disk Used: {alloc['disk.percent']}%")
                print(f"    Disk Available: {alloc['disk.avail']}")
            
            # Check for unassigned shards
            unassigned = [s for s in shards if s['state'] == 'UNASSIGNED']
            if unassigned:
                print(f"\nUnassigned Shards ({len(unassigned)}):")
                for shard in unassigned[:10]:  # Show first 10
                    print(f"  {shard['index']} - Shard {shard['shard']} ({shard['prirep']})")
            
        except Exception as e:
            print(f"Failed to check shard allocation: {e}")
```

## Security Configuration

### Authentication and Authorization
```yaml
# internal_users.yml
admin:
  hash: "$2y$12$VcCDgh2NDk07JGN0rjGbM.Ad41qVR/YFJcgHp0UGns5JDymv..TOG"
  reserved: true
  backend_roles:
  - "admin"
  description: "Demo admin user"

kibanaserver:
  hash: "$2y$12$4AcgAt3xwOWadA5s5blL6ev39OXDNhmOesEoo33eZtrq2N0YrU3H."
  reserved: true
  description: "Demo kibanaserver user"

logstash:
  hash: "$2y$12$u1ShR4l4uBS3PLsYb8KkJOxMZjR3pABl.LXMb2nZSlmimhXqZJrx6"
  reserved: false
  backend_roles:
  - "logstash"
  description: "Demo logstash user"

readall:
  hash: "$2y$12$ae4ycwzwvLtZxwZ1pfblcuN0FAlFDKpPsKkd9s.4h6CKafPb/yNTG"
  reserved: false
  backend_roles:
  - "readall"
  description: "Demo readall user"
```

```yaml
# roles.yml
admin_role:
  reserved: true
  cluster_permissions:
  - "cluster:admin/*"
  - "cluster:monitor/*"
  index_permissions:
  - index_patterns:
    - "*"
    allowed_actions:
    - "indices:*"

logstash_role:
  reserved: false
  cluster_permissions:
  - "cluster:monitor/main"
  - "cluster:admin/ingest/pipeline/*"
  index_permissions:
  - index_patterns:
    - "logs-*"
    - "logstash-*"
    allowed_actions:
    - "indices:admin/create"
    - "indices:admin/mapping/put"
    - "indices:data/write/*"

readall_role:
  reserved: false
  cluster_permissions:
  - "cluster:monitor/*"
  index_permissions:
  - index_patterns:
    - "*"
    allowed_actions:
    - "indices:data/read/*"
    - "indices:admin/get"
    - "indices:admin/exists"
    - "indices:admin/mappings/get"

kibana_user:
  reserved: true
  cluster_permissions:
  - "cluster:monitor/*"
  index_permissions:
  - index_patterns:
    - ".kibana*"
    allowed_actions:
    - "indices:*"
```

### SSL/TLS Configuration
```bash
# Generate certificates
#!/bin/bash
# generate-certs.sh

# Generate root CA
openssl genrsa -out root-ca-key.pem 2048
openssl req -new -x509 -sha256 -key root-ca-key.pem -out root-ca.pem -days 365 \
  -subj "/C=US/ST=CA/L=San Francisco/O=Example/CN=root-ca"

# Generate node certificate
openssl genrsa -out esnode-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in esnode-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out esnode-key.pem

# Create certificate signing request
openssl req -new -key esnode-key.pem -out esnode.csr \
  -subj "/C=US/ST=CA/L=San Francisco/O=Example/CN=opensearch-node"

# Sign the certificate
openssl x509 -req -in esnode.csr -CA root-ca.pem -CAkey root-ca-key.pem \
  -CAcreateserial -sha256 -out esnode.pem -days 365

# Generate admin certificate
openssl genrsa -out admin-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem

openssl req -new -key admin-key.pem -out admin.csr \
  -subj "/C=US/ST=CA/L=San Francisco/O=Example/CN=admin"

openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem \
  -CAcreateserial -sha256 -out admin.pem -days 365

# Cleanup
rm esnode-key-temp.pem admin-key-temp.pem esnode.csr admin.csr
```

## Backup and Recovery

### Snapshot Repository Setup
```python
# backup_restore.py
import boto3
from datetime import datetime, timedelta

class BackupManager:
    def __init__(self, client):
        self.client = client
    
    def create_s3_repository(self, repo_name, bucket_name, base_path='snapshots'):
        """Create S3 snapshot repository"""
        repository_config = {
            "type": "s3",
            "settings": {
                "bucket": bucket_name,
                "base_path": base_path,
                "region": "us-east-1",
                "compress": True,
                "chunk_size": "100mb",
                "max_restore_bytes_per_sec": "100mb",
                "max_snapshot_bytes_per_sec": "100mb"
            }
        }
        
        try:
            response = self.client.snapshot.create_repository(
                repository=repo_name,
                body=repository_config
            )
            print(f"Repository '{repo_name}' created successfully")
            return response
        except Exception as e:
            print(f"Failed to create repository: {e}")
            return None
    
    def create_snapshot(self, repo_name, snapshot_name, indices=None):
        """Create snapshot of specified indices"""
        snapshot_config = {
            "ignore_unavailable": False,
            "include_global_state": True,
            "partial": False
        }
        
        if indices:
            snapshot_config["indices"] = indices
        
        try:
            response = self.client.snapshot.create(
                repository=repo_name,
                snapshot=snapshot_name,
                body=snapshot_config,
                wait_for_completion=False
            )
            print(f"Snapshot '{snapshot_name}' creation started")
            return response
        except Exception as e:
            print(f"Failed to create snapshot: {e}")
            return None
    
    def restore_snapshot(self, repo_name, snapshot_name, indices=None, rename_pattern=None, rename_replacement=None):
        """Restore snapshot"""
        restore_config = {
            "ignore_unavailable": False,
            "include_global_state": False,
            "partial": False
        }
        
        if indices:
            restore_config["indices"] = indices
        
        if rename_pattern and rename_replacement:
            restore_config["rename_pattern"] = rename_pattern
            restore_config["rename_replacement"] = rename_replacement
        
        try:
            response = self.client.snapshot.restore(
                repository=repo_name,
                snapshot=snapshot_name,
                body=restore_config,
                wait_for_completion=False
            )
            print(f"Snapshot '{snapshot_name}' restore started")
            return response
        except Exception as e:
            print(f"Failed to restore snapshot: {e}")
            return None
    
    def list_snapshots(self, repo_name):
        """List all snapshots in repository"""
        try:
            response = self.client.snapshot.get(
                repository=repo_name,
                snapshot="_all"
            )
            return response['snapshots']
        except Exception as e:
            print(f"Failed to list snapshots: {e}")
            return []
    
    def delete_old_snapshots(self, repo_name, retention_days=30):
        """Delete snapshots older than retention period"""
        try:
            snapshots = self.list_snapshots(repo_name)
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            for snapshot in snapshots:
                snapshot_date = datetime.fromisoformat(
                    snapshot['start_time'].replace('Z', '+00:00')
                ).replace(tzinfo=None)
                
                if snapshot_date < cutoff_date:
                    self.client.snapshot.delete(
                        repository=repo_name,
                        snapshot=snapshot['snapshot']
                    )
                    print(f"Deleted old snapshot: {snapshot['snapshot']}")
        
        except Exception as e:
            print(f"Failed to delete old snapshots: {e}")
    
    def automated_backup(self, repo_name, indices_pattern, retention_days=30):
        """Perform automated backup with cleanup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"auto_backup_{timestamp}"
        
        # Create snapshot
        self.create_snapshot(repo_name, snapshot_name, indices_pattern)
        
        # Clean up old snapshots
        self.delete_old_snapshots(repo_name, retention_days)
        
        print(f"Automated backup completed: {snapshot_name}")
```

## Resources

- [OpenSearch Documentation](https://opensearch.org/docs/)
- [OpenSearch Python Client](https://opensearch.org/docs/latest/clients/python/)
- [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/)
- [OpenSearch Security](https://opensearch.org/docs/latest/security/)
- [OpenSearch Performance Tuning](https://opensearch.org/docs/latest/tuning-your-cluster/)
- [OpenSearch Index Management](https://opensearch.org/docs/latest/im-plugin/)
- [OpenSearch Alerting](https://opensearch.org/docs/latest/monitoring-plugins/alerting/)
- [OpenSearch Community Forum](https://forum.opensearch.org/)
- [OpenSearch GitHub Repository](https://github.com/opensearch-project/OpenSearch)
- [OpenSearch Blog](https://opensearch.org/blog/)