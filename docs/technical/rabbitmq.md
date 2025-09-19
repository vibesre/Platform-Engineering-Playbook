# RabbitMQ

## Overview

RabbitMQ is a robust, feature-rich message broker that implements the Advanced Message Queuing Protocol (AMQP). It's widely used for building distributed systems, microservices communication, and asynchronous processing workflows.

## Key Features

- **Reliable Messaging**: Persistent queues and message acknowledgments
- **Flexible Routing**: Exchanges, queues, and binding patterns
- **Clustering**: High availability and horizontal scaling
- **Management Interface**: Web-based administration console
- **Multiple Protocols**: AMQP, MQTT, STOMP, WebSockets

## Common Use Cases

### Basic Producer and Consumer
```python
import pika
import json

# Producer
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='task_queue', durable=True)

# Send message
message = {
    'user_id': 12345,
    'action': 'send_email',
    'data': {'email': 'user@example.com', 'template': 'welcome'}
}

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,  # Make message persistent
    )
)

print("Message sent")
connection.close()

# Consumer
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Processing: {message}")
    
    # Process the message
    process_task(message)
    
    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

### Work Queue Pattern
```python
# Work queue for distributing tasks
import pika
import time
import sys

class WorkQueue:
    def __init__(self, queue_name='work_queue'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        
        # Declare durable queue
        self.channel.queue_declare(queue=queue_name, durable=True)
    
    def publish_task(self, task_data):
        message = json.dumps(task_data)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent message
            )
        )
        print(f"Sent task: {task_data}")
    
    def start_worker(self):
        def callback(ch, method, properties, body):
            task = json.loads(body)
            print(f"Processing task: {task}")
            
            # Simulate work
            time.sleep(task.get('duration', 1))
            
            print(f"Task completed: {task}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        # Fair dispatch - don't give more than one message to a worker at a time
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback
        )
        
        print('Worker waiting for tasks. To exit press CTRL+C')
        self.channel.start_consuming()

# Usage
work_queue = WorkQueue()
work_queue.publish_task({'id': 1, 'type': 'image_resize', 'duration': 3})
work_queue.start_worker()
```

### Publish/Subscribe Pattern
```python
import pika

class PubSub:
    def __init__(self, exchange_name='events'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name
        
        # Declare fanout exchange
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='fanout'
        )
    
    def publish(self, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key='',
            body=json.dumps(message)
        )
        print(f"Published: {message}")
    
    def subscribe(self, callback):
        # Create temporary queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        
        # Bind queue to exchange
        self.channel.queue_bind(
            exchange=self.exchange_name,
            queue=queue_name
        )
        
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
        
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=wrapper,
            auto_ack=True
        )
        
        print('Subscribed to events. To exit press CTRL+C')
        self.channel.start_consuming()

# Publisher
pubsub = PubSub()
pubsub.publish({'event': 'user_registered', 'user_id': 123})

# Subscriber
def handle_event(message):
    print(f"Received event: {message}")

pubsub.subscribe(handle_event)
```

## Docker Deployment

### Basic Docker Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3.11-management
    container_name: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: password
      RABBITMQ_DEFAULT_VHOST: /
    ports:
      - "5672:5672"    # AMQP port
      - "15672:15672"  # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - app_network

  app:
    build: .
    depends_on:
      - rabbitmq
    environment:
      RABBITMQ_URL: amqp://admin:password@rabbitmq:5672/
    networks:
      - app_network

volumes:
  rabbitmq_data:

networks:
  app_network:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rabbitmq
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
    spec:
      containers:
      - name: rabbitmq
        image: rabbitmq:3.11-management
        env:
        - name: RABBITMQ_DEFAULT_USER
          value: "admin"
        - name: RABBITMQ_DEFAULT_PASS
          valueFrom:
            secretKeyRef:
              name: rabbitmq-secret
              key: password
        ports:
        - containerPort: 5672
        - containerPort: 15672
        volumeMounts:
        - name: rabbitmq-storage
          mountPath: /var/lib/rabbitmq
      volumes:
      - name: rabbitmq-storage
        persistentVolumeClaim:
          claimName: rabbitmq-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq-service
spec:
  selector:
    app: rabbitmq
  ports:
  - name: amqp
    port: 5672
    targetPort: 5672
  - name: management
    port: 15672
    targetPort: 15672
  type: LoadBalancer
```

## Advanced Configuration

### Clustering Setup
```bash
# rabbitmq.conf
cluster_formation.peer_discovery_backend = rabbit_peer_discovery_k8s
cluster_formation.k8s.host = kubernetes.default.svc.cluster.local
cluster_formation.k8s.address_type = hostname
cluster_formation.k8s.service_name = rabbitmq-headless
cluster_formation.k8s.hostname_suffix = .rabbitmq-headless.default.svc.cluster.local

# High availability
queue_master_locator = min-masters
cluster_partition_handling = autoheal

# Memory and disk limits
vm_memory_high_watermark.relative = 0.4
disk_free_limit.relative = 2.0
```

### Queue Policies
```bash
# Set HA policy for all queues
rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all"}'

# Set TTL policy
rabbitmqctl set_policy ttl-policy "temp.*" '{"message-ttl":60000}'

# Set max length policy
rabbitmqctl set_policy max-length "logs.*" '{"max-length":1000}'

# Dead letter exchange
rabbitmqctl set_policy dlx "orders.*" \
  '{"dead-letter-exchange":"orders-dlx","dead-letter-routing-key":"failed"}'
```

### Monitoring and Health Checks
```python
import requests
import pika

def check_rabbitmq_health():
    try:
        # Check management API
        response = requests.get(
            'http://localhost:15672/api/overview',
            auth=('admin', 'password')
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"RabbitMQ Version: {data['rabbitmq_version']}")
            print(f"Messages: {data['queue_totals']['messages']}")
            print(f"Connections: {data['object_totals']['connections']}")
            return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def check_connection():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        connection.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

## Message Patterns

### Request/Reply Pattern
```python
import uuid
import threading

class RPCClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        
        # Create callback queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        
        self.response = None
        self.corr_id = None
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message
        )
        
        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        
        return self.response

# RPC Server
def rpc_server():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='rpc_queue')
    
    def on_request(ch, method, props, body):
        # Process request
        result = process_request(body)
        
        # Send response
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=str(result)
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    
    channel.start_consuming()
```

## Best Practices

- Use durable queues and persistent messages for important data
- Implement proper error handling and dead letter queues
- Monitor queue lengths and consumer lag
- Use appropriate acknowledgment modes
- Configure clustering for high availability
- Implement circuit breakers for resilience
- Set resource limits and policies
- Regular backup of definitions and messages

## Great Resources

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html) - Official comprehensive documentation
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html) - Step-by-step tutorials for common patterns
- [RabbitMQ Management](https://www.rabbitmq.com/management.html) - Web-based administration guide
- [Clustering Guide](https://www.rabbitmq.com/clustering.html) - High availability setup
- [Production Checklist](https://www.rabbitmq.com/production-checklist.html) - Production deployment guidelines
- [Monitoring Guide](https://www.rabbitmq.com/monitoring.html) - Monitoring and alerting setup
- [awesome-rabbitmq](https://github.com/neutronth/awesome-rabbitmq) - Curated list of RabbitMQ resources