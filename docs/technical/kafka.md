# Apache Kafka

## Overview

Apache Kafka is a distributed streaming platform designed for building real-time data pipelines and streaming applications. It's widely used for high-throughput, fault-tolerant messaging and event streaming in modern architectures.

## Key Features

- **High Throughput**: Handle millions of messages per second
- **Distributed**: Horizontally scalable across multiple servers
- **Durable**: Persistent storage with configurable retention
- **Fault Tolerant**: Replication and partition tolerance
- **Real-time**: Low-latency message processing

## Common Use Cases

### Producer Example
```python
from kafka import KafkaProducer
import json
import time

# Create producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send messages
for i in range(100):
    message = {
        'user_id': f'user_{i}',
        'action': 'page_view',
        'timestamp': time.time()
    }
    
    producer.send('user-events', message)
    print(f"Sent message {i}")

producer.flush()
producer.close()
```

### Consumer Example
```python
from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='analytics-group',
    auto_offset_reset='earliest'
)

# Process messages
for message in consumer:
    event = message.value
    print(f"Processing event: {event['action']} for user {event['user_id']}")
    
    # Process the event (store in database, trigger actions, etc.)
    process_user_event(event)
```

### Topic Management
```bash
# Create topic
kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic user-events \
  --partitions 3 \
  --replication-factor 2

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Describe topic
kafka-topics.sh --describe \
  --bootstrap-server localhost:9092 \
  --topic user-events

# Delete topic
kafka-topics.sh --delete \
  --bootstrap-server localhost:9092 \
  --topic user-events
```

## Configuration

### Server Configuration (server.properties)
```properties
# Broker settings
broker.id=1
listeners=PLAINTEXT://localhost:9092
log.dirs=/var/kafka-logs

# Zookeeper connection
zookeeper.connect=localhost:2181

# Log retention
log.retention.hours=168
log.retention.bytes=1073741824
log.segment.bytes=1073741824

# Replication settings
default.replication.factor=3
min.insync.replicas=2

# Network settings
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
```

### Producer Configuration
```python
producer_config = {
    'bootstrap_servers': ['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],
    'acks': 'all',  # Wait for all replicas
    'retries': 3,
    'batch_size': 16384,
    'linger_ms': 5,
    'buffer_memory': 33554432,
    'compression_type': 'snappy'
}

producer = KafkaProducer(**producer_config)
```

### Consumer Configuration
```python
consumer_config = {
    'bootstrap_servers': ['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],
    'group_id': 'my-consumer-group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': False,
    'max_poll_records': 500,
    'session_timeout_ms': 30000
}

consumer = KafkaConsumer('my-topic', **consumer_config)
```

## Monitoring and Operations

### Performance Monitoring
```bash
# Consumer group status
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group my-consumer-group

# Topic statistics
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic user-events

# Broker performance
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

### Log Analysis
```bash
# View topic logs
kafka-dump-log.sh --files /var/kafka-logs/user-events-0/00000000000000000000.log

# Consumer lag monitoring
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group analytics-group
```

## Deployment

### Docker Compose Setup
```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_LOG_RETENTION_HOURS: 168
      KAFKA_LOG_RETENTION_BYTES: 1073741824
```

### Kubernetes Deployment
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
spec:
  kafka:
    version: 3.5.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
```

## Security

### SASL/SCRAM Authentication
```properties
# server.properties
sasl.enabled.mechanisms=SCRAM-SHA-256
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256
security.inter.broker.protocol=SASL_PLAINTEXT
listeners=SASL_PLAINTEXT://localhost:9092
```

```bash
# Create SCRAM user
kafka-configs.sh --bootstrap-server localhost:9092 \
  --alter --add-config 'SCRAM-SHA-256=[password=secret]' \
  --entity-type users --entity-name alice
```

## Best Practices

- Design topics with appropriate partition counts
- Use consumer groups for scalable message processing
- Implement proper error handling and dead letter queues
- Monitor consumer lag and throughput metrics
- Use appropriate serialization formats (Avro, Protobuf)
- Implement idempotent producers for exactly-once semantics
- Regular backup and disaster recovery planning

## Great Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) - Official comprehensive documentation
- [Confluent Platform](https://docs.confluent.io/) - Enterprise Kafka platform and tools
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/) - Stream processing with Kafka
- [Strimzi Kafka Operator](https://strimzi.io/) - Kubernetes-native Kafka deployment
- [Kafka Manager](https://github.com/yahoo/CMAK) - Web-based management tool
- [Kafka Connect](https://kafka.apache.org/documentation/#connect) - Data integration framework
- [awesome-kafka](https://github.com/infoslack/awesome-kafka) - Curated list of Kafka resources