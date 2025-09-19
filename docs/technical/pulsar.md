# Apache Pulsar

Apache Pulsar is a distributed messaging and streaming platform built for high-throughput, low-latency workloads. It provides unified messaging and streaming with multi-tenancy, geo-replication, and strong consistency guarantees.

## Installation

### Docker Setup
```bash
# Start Pulsar standalone
docker run -it \
  -p 6650:6650 \
  -p 8080:8080 \
  --name pulsar \
  apachepulsar/pulsar:3.1.0 \
  bin/pulsar standalone

# Start with custom configuration
docker run -it \
  -p 6650:6650 \
  -p 8080:8080 \
  -v $(pwd)/conf:/pulsar/conf \
  --name pulsar \
  apachepulsar/pulsar:3.1.0 \
  bin/pulsar standalone --config /pulsar/conf/standalone.conf

# Run with Docker Compose
docker-compose up -d
```

### Docker Compose
```yaml
version: '3.8'
services:
  zookeeper:
    image: zookeeper:3.8
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    volumes:
      - zookeeper-data:/data
      - zookeeper-logs:/datalog

  bookkeeper:
    image: apachepulsar/pulsar:3.1.0
    container_name: bookkeeper
    command: >
      bash -c "bin/apply-config-from-env.py conf/bookkeeper.conf &&
               bin/bookkeeper bookie"
    environment:
      BOOKIE_MEM: -Xms512m -Xmx512m -XX:MaxDirectMemorySize=1g
      zkServers: zookeeper:2181
      journalDirectory: /pulsar/data/bookkeeper/journal
      ledgerDirectories: /pulsar/data/bookkeeper/ledgers
      indexDirectories: /pulsar/data/bookkeeper/ledgers
      advertisedAddress: bookkeeper
    depends_on:
      - zookeeper
    volumes:
      - bookkeeper-data:/pulsar/data

  broker:
    image: apachepulsar/pulsar:3.1.0
    container_name: broker
    command: >
      bash -c "bin/apply-config-from-env.py conf/broker.conf &&
               bin/pulsar broker"
    environment:
      PULSAR_MEM: -Xms512m -Xmx512m -XX:MaxDirectMemorySize=1g
      zookeeperServers: zookeeper:2181
      configurationStoreServers: zookeeper:2181
      clusterName: pulsar-cluster
      managedLedgerDefaultEnsembleSize: 1
      managedLedgerDefaultWriteQuorum: 1
      managedLedgerDefaultAckQuorum: 1
      advertisedAddress: broker
      advertisedListeners: external:pulsar://localhost:6650
    depends_on:
      - zookeeper
      - bookkeeper
    ports:
      - "6650:6650"
      - "8080:8080"
    volumes:
      - broker-data:/pulsar/data

  pulsar-manager:
    image: apachepulsar/pulsar-manager:v0.3.0
    container_name: pulsar-manager
    ports:
      - "9527:9527"
      - "7750:7750"
    depends_on:
      - broker
    environment:
      SPRING_CONFIGURATION_FILE: /pulsar-manager/pulsar-manager/application.properties

volumes:
  zookeeper-data:
  zookeeper-logs:
  bookkeeper-data:
  broker-data:
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: pulsar
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zookeeper
  namespace: pulsar
spec:
  serviceName: zookeeper
  replicas: 3
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - zookeeper
            topologyKey: kubernetes.io/hostname
      containers:
      - name: zookeeper
        image: zookeeper:3.8
        ports:
        - containerPort: 2181
          name: client
        - containerPort: 2888
          name: server
        - containerPort: 3888
          name: leader-election
        env:
        - name: ZOO_MY_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.annotations['statefulset.kubernetes.io/pod-name']
        - name: ZOO_SERVERS
          value: "server.1=zookeeper-0.zookeeper:2888:3888;2181 server.2=zookeeper-1.zookeeper:2888:3888;2181 server.3=zookeeper-2.zookeeper:2888:3888;2181"
        - name: ZOO_STANDALONE_ENABLED
          value: "false"
        - name: ZOO_ADMINSERVER_ENABLED
          value: "true"
        volumeMounts:
        - name: data
          mountPath: /data
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
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
  name: zookeeper
  namespace: pulsar
spec:
  clusterIP: None
  ports:
  - port: 2181
    name: client
  - port: 2888
    name: server
  - port: 3888
    name: leader-election
  selector:
    app: zookeeper
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: bookkeeper
  namespace: pulsar
spec:
  serviceName: bookkeeper
  replicas: 3
  selector:
    matchLabels:
      app: bookkeeper
  template:
    metadata:
      labels:
        app: bookkeeper
    spec:
      initContainers:
      - name: wait-zookeeper
        image: busybox
        command: ['sh', '-c', 'until nslookup zookeeper; do echo waiting for zookeeper; sleep 2; done;']
      containers:
      - name: bookkeeper
        image: apachepulsar/pulsar:3.1.0
        command: ["sh", "-c"]
        args:
        - >
          bin/apply-config-from-env.py conf/bookkeeper.conf &&
          bin/bookkeeper bookie
        ports:
        - containerPort: 3181
          name: bookie
        env:
        - name: BOOKIE_MEM
          value: "-Xms1g -Xmx1g -XX:MaxDirectMemorySize=2g"
        - name: zkServers
          value: "zookeeper-0.zookeeper:2181,zookeeper-1.zookeeper:2181,zookeeper-2.zookeeper:2181"
        - name: journalDirectory
          value: "/pulsar/data/bookkeeper/journal"
        - name: ledgerDirectories
          value: "/pulsar/data/bookkeeper/ledgers"
        - name: indexDirectories
          value: "/pulsar/data/bookkeeper/ledgers"
        volumeMounts:
        - name: journal-disk
          mountPath: /pulsar/data/bookkeeper/journal
        - name: ledgers-disk
          mountPath: /pulsar/data/bookkeeper/ledgers
        resources:
          requests:
            memory: 1Gi
            cpu: 500m
          limits:
            memory: 2Gi
            cpu: 1000m
  volumeClaimTemplates:
  - metadata:
      name: journal-disk
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
  - metadata:
      name: ledgers-disk
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: broker
  namespace: pulsar
spec:
  replicas: 3
  selector:
    matchLabels:
      app: broker
  template:
    metadata:
      labels:
        app: broker
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - broker
              topologyKey: kubernetes.io/hostname
      containers:
      - name: broker
        image: apachepulsar/pulsar:3.1.0
        command: ["sh", "-c"]
        args:
        - >
          bin/apply-config-from-env.py conf/broker.conf &&
          bin/pulsar broker
        ports:
        - containerPort: 6650
          name: pulsar
        - containerPort: 8080
          name: http
        env:
        - name: PULSAR_MEM
          value: "-Xms1g -Xmx1g -XX:MaxDirectMemorySize=2g"
        - name: zookeeperServers
          value: "zookeeper-0.zookeeper:2181,zookeeper-1.zookeeper:2181,zookeeper-2.zookeeper:2181"
        - name: configurationStoreServers
          value: "zookeeper-0.zookeeper:2181,zookeeper-1.zookeeper:2181,zookeeper-2.zookeeper:2181"
        - name: clusterName
          value: "pulsar-cluster"
        - name: managedLedgerDefaultEnsembleSize
          value: "2"
        - name: managedLedgerDefaultWriteQuorum
          value: "2"
        - name: managedLedgerDefaultAckQuorum
          value: "2"
        resources:
          requests:
            memory: 1Gi
            cpu: 500m
          limits:
            memory: 2Gi
            cpu: 1000m
---
apiVersion: v1
kind: Service
metadata:
  name: broker
  namespace: pulsar
spec:
  ports:
  - port: 6650
    name: pulsar
  - port: 8080
    name: http
  selector:
    app: broker
```

### Helm Installation
```bash
# Add Pulsar Helm repository
helm repo add apache https://pulsar.apache.org/charts
helm repo update

# Install Pulsar with default values
helm install pulsar apache/pulsar \
  --namespace pulsar \
  --create-namespace

# Install with custom values
helm install pulsar apache/pulsar \
  --namespace pulsar \
  --create-namespace \
  --set broker.replicaCount=3 \
  --set bookkeeper.replicaCount=3 \
  --set zookeeper.replicaCount=3 \
  --set pulsar_manager.enabled=true
```

## Basic Operations

### CLI Operations
```bash
# Start Pulsar client
docker exec -it pulsar bash

# Create tenant
bin/pulsar-admin tenants create my-tenant \
  --admin-roles my-admin-role \
  --allowed-clusters pulsar-cluster

# Create namespace
bin/pulsar-admin namespaces create my-tenant/my-namespace

# Set namespace policies
bin/pulsar-admin namespaces set-retention my-tenant/my-namespace \
  --size 10G --time 3d

bin/pulsar-admin namespaces set-backlog-quota my-tenant/my-namespace \
  --limit 5G --policy producer_exception

# Create topic
bin/pulsar-admin topics create persistent://my-tenant/my-namespace/my-topic

# Set topic policies
bin/pulsar-admin topics set-message-ttl persistent://my-tenant/my-namespace/my-topic \
  --messageTTL 3600

# Produce messages
bin/pulsar-client produce persistent://my-tenant/my-namespace/my-topic \
  --messages "Hello Pulsar" \
  --num-messages 10

# Consume messages
bin/pulsar-client consume persistent://my-tenant/my-namespace/my-topic \
  --subscription my-subscription \
  --num-messages 10

# Get topic stats
bin/pulsar-admin topics stats persistent://my-tenant/my-namespace/my-topic

# List topics
bin/pulsar-admin topics list my-tenant/my-namespace
```

### Producer Examples

#### Python Producer
```python
import pulsar
import json
from datetime import datetime
import threading
import time

class PulsarProducer:
    def __init__(self, service_url='pulsar://localhost:6650'):
        self.client = pulsar.Client(service_url)
        self.producers = {}
        
    def create_producer(self, topic, producer_name=None, **kwargs):
        """Create a producer for a specific topic"""
        producer_config = {
            'topic': topic,
            'producer_name': producer_name,
            'block_if_queue_full': True,
            'batching_enabled': True,
            'batching_max_messages': 1000,
            'batching_max_publish_delay_ms': 100,
            'compression_type': pulsar.CompressionType.LZ4,
            **kwargs
        }
        
        producer = self.client.create_producer(**producer_config)
        self.producers[topic] = producer
        return producer
    
    def send_message(self, topic, message, properties=None, partition_key=None):
        """Send a single message"""
        if topic not in self.producers:
            self.create_producer(topic)
        
        producer = self.producers[topic]
        
        # Prepare message
        if isinstance(message, dict):
            message = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            message = message.encode('utf-8')
        
        # Send message
        message_id = producer.send(
            content=message,
            properties=properties or {},
            partition_key=partition_key
        )
        
        return message_id
    
    def send_async(self, topic, message, callback=None, properties=None):
        """Send message asynchronously"""
        if topic not in self.producers:
            self.create_producer(topic)
        
        producer = self.producers[topic]
        
        if isinstance(message, dict):
            message = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            message = message.encode('utf-8')
        
        def default_callback(res, msg_id):
            if res == pulsar.Result.Ok:
                print(f"Message sent successfully: {msg_id}")
            else:
                print(f"Failed to send message: {res}")
        
        producer.send_async(
            content=message,
            callback=callback or default_callback,
            properties=properties or {}
        )
    
    def send_batch(self, topic, messages, batch_size=100):
        """Send messages in batches"""
        if topic not in self.producers:
            self.create_producer(topic)
        
        producer = self.producers[topic]
        
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i + batch_size]
            
            for message in batch:
                if isinstance(message, dict):
                    content = json.dumps(message).encode('utf-8')
                else:
                    content = str(message).encode('utf-8')
                
                producer.send_async(
                    content=content,
                    callback=lambda res, msg_id: None
                )
            
            producer.flush()
    
    def close(self):
        """Close all producers and client"""
        for producer in self.producers.values():
            producer.close()
        self.client.close()

# Usage example
producer = PulsarProducer()

# Send simple message
message_id = producer.send_message(
    'persistent://public/default/events',
    {'event': 'user_login', 'user_id': 123, 'timestamp': datetime.now().isoformat()}
)

# Send with properties
producer.send_message(
    'persistent://public/default/events',
    'Hello Pulsar',
    properties={'source': 'app1', 'version': '1.0'}
)

# Send asynchronously
producer.send_async(
    'persistent://public/default/events',
    {'event': 'async_message', 'data': 'test'}
)

# Batch sending
messages = [{'id': i, 'data': f'message-{i}'} for i in range(1000)]
producer.send_batch('persistent://public/default/events', messages)

producer.close()
```

### Consumer Examples

#### Python Consumer
```python
import pulsar
import json
import threading
import time
from datetime import datetime

class PulsarConsumer:
    def __init__(self, service_url='pulsar://localhost:6650'):
        self.client = pulsar.Client(service_url)
        self.consumers = {}
        self.running = {}
        
    def create_consumer(self, topic, subscription_name, consumer_type=pulsar.ConsumerType.Shared, **kwargs):
        """Create a consumer for a specific topic"""
        consumer_config = {
            'topic': topic,
            'subscription_name': subscription_name,
            'consumer_type': consumer_type,
            'message_listener': None,
            'receiver_queue_size': 1000,
            'max_total_receiver_queue_size_across_partitions': 50000,
            'consumer_name': f"{subscription_name}-consumer",
            **kwargs
        }
        
        consumer = self.client.subscribe(**consumer_config)
        self.consumers[f"{topic}:{subscription_name}"] = consumer
        return consumer
    
    def consume_messages(self, topic, subscription_name, message_handler=None, num_messages=None):
        """Consume messages synchronously"""
        consumer_key = f"{topic}:{subscription_name}"
        
        if consumer_key not in self.consumers:
            self.create_consumer(topic, subscription_name)
        
        consumer = self.consumers[consumer_key]
        
        def default_handler(consumer, message):
            try:
                data = json.loads(message.data().decode('utf-8'))
                print(f"Received: {data}")
                consumer.acknowledge(message)
            except Exception as e:
                print(f"Error processing message: {e}")
                consumer.negative_acknowledge(message)
        
        handler = message_handler or default_handler
        count = 0
        
        while num_messages is None or count < num_messages:
            try:
                message = consumer.receive(timeout_millis=5000)
                handler(consumer, message)
                count += 1
            except Exception as e:
                print(f"Receive timeout or error: {e}")
                break
    
    def consume_async(self, topic, subscription_name, message_handler=None):
        """Consume messages asynchronously"""
        def default_handler(consumer, message):
            try:
                data = json.loads(message.data().decode('utf-8'))
                print(f"Async received: {data}")
                consumer.acknowledge(message)
            except Exception as e:
                print(f"Error processing message: {e}")
                consumer.negative_acknowledge(message)
        
        handler = message_handler or default_handler
        
        consumer = self.create_consumer(
            topic,
            subscription_name,
            message_listener=handler
        )
        
        return consumer
    
    def consume_with_retry(self, topic, subscription_name, max_retries=3):
        """Consume messages with retry logic"""
        consumer_key = f"{topic}:{subscription_name}"
        
        if consumer_key not in self.consumers:
            self.create_consumer(topic, subscription_name)
        
        consumer = self.consumers[consumer_key]
        
        def retry_handler(consumer, message):
            retry_count = int(message.properties().get('retry_count', '0'))
            
            try:
                # Process message
                data = json.loads(message.data().decode('utf-8'))
                print(f"Processing: {data}")
                
                # Simulate processing that might fail
                if 'error' in data:
                    raise Exception("Simulated processing error")
                
                consumer.acknowledge(message)
                
            except Exception as e:
                if retry_count < max_retries:
                    # Send to retry topic
                    retry_topic = f"{topic}-retry"
                    retry_producer = self.client.create_producer(retry_topic)
                    
                    retry_properties = dict(message.properties())
                    retry_properties['retry_count'] = str(retry_count + 1)
                    retry_properties['original_topic'] = topic
                    retry_properties['error_message'] = str(e)
                    
                    retry_producer.send(
                        content=message.data(),
                        properties=retry_properties
                    )
                    retry_producer.close()
                    
                    consumer.acknowledge(message)
                else:
                    # Send to dead letter topic
                    dlq_topic = f"{topic}-dlq"
                    dlq_producer = self.client.create_producer(dlq_topic)
                    
                    dlq_properties = dict(message.properties())
                    dlq_properties['max_retries_exceeded'] = 'true'
                    dlq_properties['final_error'] = str(e)
                    
                    dlq_producer.send(
                        content=message.data(),
                        properties=dlq_properties
                    )
                    dlq_producer.close()
                    
                    consumer.acknowledge(message)
        
        # Start consuming
        while True:
            try:
                message = consumer.receive(timeout_millis=1000)
                retry_handler(consumer, message)
            except Exception as e:
                print(f"Consumer error: {e}")
                time.sleep(1)
    
    def create_reader(self, topic, start_message_id=pulsar.MessageId.earliest):
        """Create a reader for reading from specific position"""
        reader = self.client.create_reader(
            topic=topic,
            start_message_id=start_message_id
        )
        return reader
    
    def close(self):
        """Close all consumers and client"""
        for consumer in self.consumers.values():
            consumer.close()
        self.client.close()

# Usage examples
consumer = PulsarConsumer()

# Simple consumption
consumer.consume_messages(
    'persistent://public/default/events',
    'my-subscription',
    num_messages=10
)

# Async consumption
async_consumer = consumer.consume_async(
    'persistent://public/default/events',
    'async-subscription'
)

# Custom message handler
def custom_handler(consumer, message):
    data = json.loads(message.data().decode('utf-8'))
    print(f"Custom handler received: {data}")
    
    # Conditional acknowledgment
    if data.get('process', True):
        consumer.acknowledge(message)
    else:
        consumer.negative_acknowledge(message)

consumer.consume_messages(
    'persistent://public/default/events',
    'custom-subscription',
    message_handler=custom_handler
)

consumer.close()
```

### Schema Management
```python
import pulsar
from pulsar.schema import AvroSchema, JsonSchema, Record, String, Integer, Boolean
import json

# Define Avro schema
class UserEvent(Record):
    user_id = Integer()
    event_type = String()
    timestamp = String()
    properties = String()

# Create producer with schema
client = pulsar.Client('pulsar://localhost:6650')

# Avro schema producer
avro_producer = client.create_producer(
    topic='persistent://public/default/user-events-avro',
    schema=AvroSchema(UserEvent)
)

# JSON schema producer
json_schema = JsonSchema({
    "type": "object",
    "properties": {
        "user_id": {"type": "integer"},
        "event_type": {"type": "string"},
        "timestamp": {"type": "string"},
        "properties": {"type": "string"}
    }
})

json_producer = client.create_producer(
    topic='persistent://public/default/user-events-json',
    schema=json_schema
)

# Send typed messages
user_event = UserEvent(
    user_id=123,
    event_type='login',
    timestamp='2023-01-01T12:00:00Z',
    properties=json.dumps({'ip': '192.168.1.1'})
)

avro_producer.send(user_event)

json_producer.send({
    'user_id': 456,
    'event_type': 'logout',
    'timestamp': '2023-01-01T12:30:00Z',
    'properties': json.dumps({'session_duration': 1800})
})

# Create consumer with schema
avro_consumer = client.subscribe(
    topic='persistent://public/default/user-events-avro',
    subscription_name='avro-subscription',
    schema=AvroSchema(UserEvent)
)

json_consumer = client.subscribe(
    topic='persistent://public/default/user-events-json',
    subscription_name='json-subscription',
    schema=json_schema
)

# Consume typed messages
message = avro_consumer.receive()
user_event = message.value()
print(f"Received user event: {user_event.user_id}, {user_event.event_type}")
avro_consumer.acknowledge(message)

client.close()
```

## Advanced Features

### Functions (Serverless Computing)
```python
# function_example.py
from pulsar import Function
import json

class WordCountFunction(Function):
    def __init__(self):
        self.word_count = {}
    
    def process(self, input, context):
        # Parse input message
        data = json.loads(input)
        text = data.get('text', '')
        
        # Count words
        words = text.lower().split()
        for word in words:
            self.word_count[word] = self.word_count.get(word, 0) + 1
        
        # Return updated count for this word
        return json.dumps({
            'word_counts': self.word_count,
            'total_words': len(words)
        })

# Deploy function
def deploy_function():
    import subprocess
    
    # Package function
    subprocess.run([
        'zip', '-r', 'wordcount-function.zip', 'function_example.py'
    ])
    
    # Deploy function
    subprocess.run([
        'bin/pulsar-admin', 'functions', 'create',
        '--tenant', 'public',
        '--namespace', 'default',
        '--name', 'word-count',
        '--py', 'wordcount-function.zip',
        '--classname', 'function_example.WordCountFunction',
        '--inputs', 'persistent://public/default/text-input',
        '--output', 'persistent://public/default/word-counts',
        '--parallelism', '3'
    ])

# Function configuration
function_config = {
    "tenant": "public",
    "namespace": "default",
    "name": "word-count",
    "className": "function_example.WordCountFunction",
    "inputs": ["persistent://public/default/text-input"],
    "output": "persistent://public/default/word-counts",
    "runtime": "PYTHON",
    "parallelism": 3,
    "resources": {
        "cpu": 0.5,
        "ram": 1073741824
    },
    "autoAck": True,
    "timeoutMs": 60000
}
```

### IO Connectors
```yaml
# Kafka source connector
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-source-config
data:
  kafka-source.yaml: |
    tenant: "public"
    namespace: "default"
    name: "kafka-source"
    archive: "connectors/pulsar-io-kafka-2.10.0.nar"
    parallelism: 1
    configs:
      bootstrapServers: "kafka-broker:9092"
      groupId: "pulsar-consumer-group"
      topic: "kafka-input-topic"
      keyDeserializationClass: "org.apache.kafka.common.serialization.StringDeserializer"
      valueDeserializationClass: "org.apache.kafka.common.serialization.StringDeserializer"
      autoCommitEnabled: true
    topicName: "persistent://public/default/kafka-data"

---
# Elasticsearch sink connector
apiVersion: v1
kind: ConfigMap
metadata:
  name: elasticsearch-sink-config
data:
  elasticsearch-sink.yaml: |
    tenant: "public"
    namespace: "default"
    name: "elasticsearch-sink"
    archive: "connectors/pulsar-io-elastic-search-2.10.0.nar"
    parallelism: 2
    configs:
      elasticSearchUrl: "http://elasticsearch:9200"
      indexName: "pulsar-messages"
      typeName: "_doc"
      username: "elastic"
      password: "changeme"
      bulkEnabled: true
      bulkActions: 1000
      bulkSizeInMb: 10
      bulkConcurrentRequests: 0
      bulkFlushIntervalInMs: 1000
    inputs:
      - "persistent://public/default/events"
```

### Geo-Replication
```bash
# Create clusters
bin/pulsar-admin clusters create us-west \
  --url http://pulsar-us-west:8080 \
  --broker-url pulsar://pulsar-us-west:6650

bin/pulsar-admin clusters create us-east \
  --url http://pulsar-us-east:8080 \
  --broker-url pulsar://pulsar-us-east:6650

# Create global namespace
bin/pulsar-admin namespaces create my-tenant/global-namespace \
  --clusters us-west,us-east

# Enable replication for topic
bin/pulsar-admin topics set-replication-clusters \
  persistent://my-tenant/global-namespace/replicated-topic \
  --clusters us-west,us-east

# Check replication status
bin/pulsar-admin topics stats \
  persistent://my-tenant/global-namespace/replicated-topic
```

## Monitoring and Observability

### Prometheus Metrics
```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: pulsar-metrics
  namespace: pulsar
spec:
  selector:
    matchLabels:
      app: broker
  endpoints:
  - port: http
    interval: 30s
    path: /metrics/
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: pulsar-alerts
  namespace: pulsar
spec:
  groups:
  - name: pulsar
    rules:
    - alert: PulsarBrokerDown
      expr: up{job="broker"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Pulsar broker is down"
        description: "Pulsar broker {{ $labels.instance }} has been down for more than 1 minute"
    
    - alert: PulsarHighPublishLatency
      expr: pulsar_broker_publish_latency{quantile="0.99"} > 1000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High publish latency"
        description: "99th percentile publish latency is {{ $value }}ms"
    
    - alert: PulsarHighBacklog
      expr: pulsar_subscription_back_log > 10000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High subscription backlog"
        description: "Subscription {{ $labels.subscription }} has backlog of {{ $value }} messages"
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Pulsar Monitoring Dashboard",
    "panels": [
      {
        "title": "Message Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(pulsar_broker_in_messages_total[5m])",
            "legendFormat": "Incoming Messages/sec"
          },
          {
            "expr": "rate(pulsar_broker_out_messages_total[5m])",
            "legendFormat": "Outgoing Messages/sec"
          }
        ]
      },
      {
        "title": "Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(pulsar_broker_in_bytes_total[5m])",
            "legendFormat": "Incoming Bytes/sec"
          },
          {
            "expr": "rate(pulsar_broker_out_bytes_total[5m])",
            "legendFormat": "Outgoing Bytes/sec"
          }
        ]
      },
      {
        "title": "Subscription Backlog",
        "type": "graph",
        "targets": [
          {
            "expr": "pulsar_subscription_back_log",
            "legendFormat": "{{topic}}-{{subscription}}"
          }
        ]
      },
      {
        "title": "Publish Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "pulsar_broker_publish_latency{quantile=\"0.50\"}",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "pulsar_broker_publish_latency{quantile=\"0.95\"}",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "pulsar_broker_publish_latency{quantile=\"0.99\"}",
            "legendFormat": "99th percentile"
          }
        ]
      },
      {
        "title": "Storage Size",
        "type": "graph",
        "targets": [
          {
            "expr": "pulsar_storage_size",
            "legendFormat": "{{topic}}"
          }
        ]
      }
    ]
  }
}
```

### Log Collection
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-pulsar-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /pulsar/logs/*.log
      pos_file /var/log/fluentd-pulsar.log.pos
      tag pulsar.*
      format json
      time_key time
      time_format %Y-%m-%dT%H:%M:%S.%NZ
    </source>
    
    <filter pulsar.**>
      @type record_transformer
      <record>
        service pulsar
        component ${tag_parts[1]}
      </record>
    </filter>
    
    <match pulsar.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name pulsar-logs
      type_name _doc
    </match>
```

## Performance Tuning

### Broker Configuration
```properties
# broker.conf

# Memory settings
PULSAR_MEM=-Xms4g -Xmx4g -XX:MaxDirectMemorySize=8g

# Network settings
maxConcurrentLookupRequest=50000
maxConcurrentTopicLoadRequest=5000

# Message settings
maxMessageSize=5242880
maxPublishRatePerTopicInMessages=10000
maxPublishRatePerTopicInBytes=1048576000

# Subscription settings
defaultRetentionTimeInMinutes=10080
defaultRetentionSizeInMB=1000

# Batch settings
maxBatchSize=1000
batchingMaxPublishDelayMicros=1000
batchingMaxMessages=1000

# Compaction
brokerServiceCompactionMonitorIntervalInSeconds=60
compactionServiceThreads=10

# Load balancing
loadBalancerEnabled=true
loadBalancerPlacementStrategy=weightedRandomSelection
loadBalancerHostUsageCheckIntervalMinutes=1
loadBalancerSheddingIntervalMinutes=30
loadBalancerSheddingGracePeriodMinutes=30

# BookKeeper settings
managedLedgerDefaultEnsembleSize=3
managedLedgerDefaultWriteQuorum=2
managedLedgerDefaultAckQuorum=2
managedLedgerCacheSizeMB=2048
managedLedgerCacheEvictionWatermark=0.9
```

### BookKeeper Configuration
```properties
# bookkeeper.conf

# Journal settings
journalSyncData=false
journalMaxSizeMB=2048
journalMaxBackups=5
journalPreAllocSizeMB=16

# Ledger storage
ledgerStorageClass=org.apache.bookkeeper.bookie.storage.ldb.DbLedgerStorage
dbStorage_writeCacheMaxSizeMb=1024
dbStorage_readAheadCacheMaxSizeMb=1024

# Performance settings
nettyMaxFrameSizeBytes=5253120
rereplicationEntryBatchSize=100
gcWaitTime=900000
gcOverreplicatedLedgerWaitTime=86400000

# Flush settings
flushInterval=60000
ledgerDirectories=/pulsar/data/bookkeeper/ledgers
indexDirectories=/pulsar/data/bookkeeper/ledgers

# Auto recovery
autoRecoveryDaemonEnabled=true
lostBookieRecoveryDelay=0
```

### Client Optimization
```python
import pulsar

# Optimized client configuration
client = pulsar.Client(
    service_url='pulsar://localhost:6650',
    operation_timeout_seconds=30,
    io_threads=4,
    message_listener_threads=4,
    concurrent_lookup_requests=50000,
    max_lookup_request=50000,
    max_lookup_redirects=20,
    max_number_of_rejected_request_per_connection=50,
    keep_alive_interval_seconds=30,
    connection_timeout_ms=10000,
    use_tls=False,
    tls_trust_certs_file_path=None,
    tls_allow_insecure_connection=False
)

# Optimized producer
producer = client.create_producer(
    topic='persistent://public/default/optimized-topic',
    producer_name='optimized-producer',
    
    # Batching settings
    batching_enabled=True,
    batching_max_messages=1000,
    batching_max_publish_delay_ms=10,
    batching_max_allowed_size_in_bytes=131072,
    
    # Performance settings
    block_if_queue_full=True,
    send_timeout_millis=30000,
    max_pending_messages=1000,
    max_pending_messages_across_partitions=50000,
    
    # Compression
    compression_type=pulsar.CompressionType.LZ4,
    
    # Partitioning
    message_routing_mode=pulsar.PartitionsRoutingMode.RoundRobinDistribution
)

# Optimized consumer
consumer = client.subscribe(
    topic='persistent://public/default/optimized-topic',
    subscription_name='optimized-subscription',
    
    # Consumer settings
    consumer_type=pulsar.ConsumerType.Shared,
    receiver_queue_size=1000,
    max_total_receiver_queue_size_across_partitions=50000,
    
    # Acknowledgment settings
    ack_timeout_millis=30000,
    negative_ack_redelivery_delay_ms=60000,
    
    # Batch receiving
    batch_receive_policy=pulsar.BatchReceivePolicy(
        max_num_messages=100,
        max_num_bytes=1024*1024,
        timeout_ms=100
    )
)
```

## Troubleshooting

### Common Issues
```bash
#!/bin/bash
# pulsar-health-check.sh

echo "=== Pulsar Health Check ==="

# Check ZooKeeper
echo "Checking ZooKeeper..."
echo ruok | nc localhost 2181

# Check BookKeeper
echo "Checking BookKeeper..."
bin/bookkeeper shell listbookies -rw
bin/bookkeeper shell listbookies -ro

# Check Broker
echo "Checking Broker..."
curl -s http://localhost:8080/admin/v2/brokers/health

# Check topic stats
echo "Checking topic stats..."
bin/pulsar-admin topics stats persistent://public/default/test-topic

# Check subscription backlog
echo "Checking subscription backlog..."
bin/pulsar-admin topics stats-internal persistent://public/default/test-topic

# Check cluster info
echo "Checking cluster info..."
bin/pulsar-admin clusters list
bin/pulsar-admin brokers list pulsar-cluster

# Check resource usage
echo "Checking resource usage..."
curl -s http://localhost:8080/metrics/ | grep -E "(pulsar_broker|pulsar_storage)"
```

### Debug Tools
```python
import pulsar
import time
import json

class PulsarDebugger:
    def __init__(self, service_url='pulsar://localhost:6650'):
        self.client = pulsar.Client(service_url)
    
    def test_connectivity(self):
        """Test basic connectivity"""
        try:
            # Try to create a producer
            producer = self.client.create_producer('persistent://public/default/test-connectivity')
            producer.send(b'test message')
            producer.close()
            print("✅ Connectivity test passed")
            return True
        except Exception as e:
            print(f"❌ Connectivity test failed: {e}")
            return False
    
    def measure_latency(self, topic, num_messages=100):
        """Measure publish/consume latency"""
        producer = self.client.create_producer(topic)
        consumer = self.client.subscribe(topic, 'latency-test')
        
        latencies = []
        
        for i in range(num_messages):
            start_time = time.time()
            
            # Send message with timestamp
            message_data = json.dumps({
                'id': i,
                'timestamp': start_time
            }).encode('utf-8')
            
            producer.send(message_data)
            
            # Receive message
            message = consumer.receive(timeout_millis=5000)
            receive_time = time.time()
            
            # Calculate latency
            latency = (receive_time - start_time) * 1000  # Convert to ms
            latencies.append(latency)
            
            consumer.acknowledge(message)
        
        producer.close()
        consumer.close()
        
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        
        print(f"Latency test results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        
        return {
            'average': avg_latency,
            'min': min_latency,
            'max': max_latency,
            'samples': latencies
        }
    
    def test_throughput(self, topic, duration_seconds=60, message_size=1024):
        """Test message throughput"""
        producer = self.client.create_producer(topic)
        
        message_data = b'x' * message_size
        start_time = time.time()
        message_count = 0
        
        while time.time() - start_time < duration_seconds:
            producer.send_async(message_data, callback=lambda res, msg_id: None)
            message_count += 1
        
        producer.flush()
        end_time = time.time()
        producer.close()
        
        duration = end_time - start_time
        throughput = message_count / duration
        bytes_per_second = (message_count * message_size) / duration
        
        print(f"Throughput test results:")
        print(f"  Messages/second: {throughput:.2f}")
        print(f"  MB/second: {bytes_per_second / 1024 / 1024:.2f}")
        print(f"  Total messages: {message_count}")
        
        return {
            'messages_per_second': throughput,
            'bytes_per_second': bytes_per_second,
            'total_messages': message_count,
            'duration': duration
        }

# Usage
debugger = PulsarDebugger()
debugger.test_connectivity()
debugger.measure_latency('persistent://public/default/latency-test')
debugger.test_throughput('persistent://public/default/throughput-test')
```

## Resources

- [Apache Pulsar Documentation](https://pulsar.apache.org/docs/)
- [GitHub Repository](https://github.com/apache/pulsar)
- [Python Client](https://pulsar.apache.org/docs/client-libraries-python/)
- [Pulsar Manager](https://github.com/apache/pulsar-manager)
- [Helm Charts](https://github.com/apache/pulsar-helm-chart)
- [Performance Tuning Guide](https://pulsar.apache.org/docs/performance-pulsar-perf/)
- [Security Guide](https://pulsar.apache.org/docs/security-overview/)
- [Functions Documentation](https://pulsar.apache.org/docs/functions-overview/)
- [IO Connectors](https://pulsar.apache.org/docs/io-overview/)
- [Community Support](https://pulsar.apache.org/community/)