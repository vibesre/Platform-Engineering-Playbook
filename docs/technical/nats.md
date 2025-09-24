# NATS

## 📚 Learning Resources

### 📖 Essential Documentation
- [NATS Documentation](https://docs.nats.io/) - Comprehensive official documentation
- [NATS Concepts](https://docs.nats.io/nats-concepts/intro) - Core messaging patterns and architecture
- [JetStream Guide](https://docs.nats.io/nats-concepts/jetstream) - Streaming and persistence features
- [Security Guide](https://docs.nats.io/running-a-nats-service/configuration/securing_nats) - Authentication and encryption

### 📝 Specialized Guides
- [NATS Patterns](https://docs.nats.io/nats-concepts/core-nats/patterns) - Common messaging patterns and best practices
- [Performance Tuning](https://docs.nats.io/running-a-nats-service/configuration/tuning-performance) - Optimization for high throughput
- [Monitoring Guide](https://docs.nats.io/running-a-nats-service/configuration/monitoring) - Observability and metrics collection
- [NATS vs Other Messaging](https://docs.nats.io/compare-nats) - Comparison with Kafka, RabbitMQ, Redis

### 🎥 Video Tutorials
- [NATS Deep Dive](https://www.youtube.com/watch?v=hjXIUPZ7ArM) - Architecture and use cases (45 min)
- [JetStream Explained](https://www.youtube.com/watch?v=jLJEQ-K2VmM) - Streaming capabilities overview (30 min)
- [NATS Security](https://www.youtube.com/watch?v=6zr7tYlTvpk) - Authentication and authorization (25 min)

### 🎓 Professional Courses
- [NATS Fundamentals](https://www.udemy.com/course/nats-messaging/) - Paid comprehensive course
- [Cloud Native Messaging](https://training.linuxfoundation.org/) - Linux Foundation training
- [Microservices Communication](https://www.pluralsight.com/courses/microservices-communication-nats) - Paid Pluralsight course

### 📚 Books
- "Cloud Native Patterns" by Cornelia Davis - [Purchase on Amazon](https://www.amazon.com/dp/1617294292)
- "Microservices Patterns" by Chris Richardson - [Purchase on Amazon](https://www.amazon.com/dp/1617294543)
- "Building Event-Driven Microservices" by Adam Bellemare - [Purchase on Amazon](https://www.amazon.com/dp/1492057894)

### 🛠️ Interactive Tools
- [NATS CLI](https://github.com/nats-io/natscli) - Command-line client for testing and management
- [NATS WebUI](https://github.com/sohlich/nats-streaming-ui) - Web interface for NATS Streaming
- [NATS Playground](https://nats.io/download/) - Local development environment

### 🚀 Ecosystem Tools
- [NATS Server](https://github.com/nats-io/nats-server) - 15k⭐ Core NATS server implementation
- [NATS Streaming](https://github.com/nats-io/nats-streaming-server) - Persistent messaging solution
- [NATS Account Server](https://github.com/nats-io/nats-account-server) - Multi-tenant account management
- [NKEYS](https://github.com/nats-io/nkeys) - Ed25519 based authentication system

### 🌐 Community & Support
- [NATS Slack](https://natsio.slack.com/) - Community discussions and support
- [NATS GitHub](https://github.com/nats-io) - Source code and issue tracking
- [NATS Twitter](https://twitter.com/nats_io) - Updates and announcements

## Understanding NATS: Cloud Native Messaging Made Simple

NATS is a simple, secure, and performant messaging system for cloud native applications, IoT messaging, and microservices architectures. It provides pub/sub, request/reply, and streaming capabilities with a focus on simplicity and performance.

### How NATS Works
NATS operates on a simple publish-subscribe model where clients connect to a NATS server and communicate through subjects. Unlike complex message brokers, NATS keeps things simple with fire-and-forget messaging, automatic pruning of stale data, and self-healing characteristics.

The system is designed around the concept of subjects - hierarchical strings that act as message routing keys. Publishers send messages to subjects, and subscribers receive messages from subjects they're interested in. NATS handles all the routing, queuing, and delivery automatically.

### The NATS Ecosystem
NATS consists of several components working together. The core NATS server provides basic messaging, while JetStream adds streaming and persistence capabilities. NATS CLI offers command-line management, and various client libraries support all major programming languages.

The ecosystem includes advanced features like NKEYS for secure authentication, leaf nodes for edge computing scenarios, and account management for multi-tenant deployments. These components work seamlessly together while maintaining NATS' simplicity.

### Why NATS Dominates Cloud Native Messaging
NATS has become the messaging backbone for cloud native applications due to its simplicity and performance. Unlike heavy message brokers that require complex setup and tuning, NATS can be deployed in seconds and performs optimally out of the box.

Its location transparency, automatic failover, and clustering capabilities make it perfect for distributed systems. The small footprint and low latency make it ideal for microservices, IoT, and edge computing scenarios where resources are constrained.

### Mental Model for Success
Think of NATS like a postal system for your applications. Instead of applications talking directly to each other (like phone calls), they send messages through NATS (like letters). The postal system (NATS) knows how to route messages based on the address (subject) without the sender needing to know where the recipient is located.

Unlike complex message brokers that are like industrial mail sorting facilities, NATS is more like an efficient local post office - simple, fast, and reliable without unnecessary complexity.

### Where to Start Your Journey
1. **Install NATS server locally** - Start with Docker or binary installation
2. **Explore with NATS CLI** - Practice pub/sub and request/reply patterns
3. **Build simple applications** - Create basic publishers and subscribers
4. **Learn about subjects** - Understand wildcards and hierarchical routing
5. **Try JetStream** - Explore persistent messaging and streaming
6. **Set up clustering** - Understand high availability patterns

### Key Concepts to Master
- **Subjects and wildcards** - Message routing and pattern matching
- **Pub/Sub patterns** - One-to-many communication patterns
- **Request/Reply** - Synchronous communication over async messaging
- **Queue groups** - Load balancing and work distribution
- **JetStream** - Persistence, replay, and stream processing
- **Clustering** - High availability and fault tolerance
- **Security models** - Authentication, authorization, and encryption
- **Monitoring** - Metrics, logging, and operational visibility

Start with basic pub/sub messaging, then progress to request/reply patterns and queue groups. Focus on understanding subject design and when to use different messaging patterns.

## Installation

### Docker Setup
```bash
# Start NATS server
docker run -d --name nats-server -p 4222:4222 -p 8222:8222 nats:2.10.5 -js -m 8222

# Start with configuration file
docker run -d --name nats-server \
  -p 4222:4222 -p 8222:8222 \
  -v $(pwd)/nats.conf:/nats.conf \
  nats:2.10.5 -c /nats.conf

# Start NATS cluster with Docker Compose
docker-compose up -d
```

### Docker Compose
```yaml
version: '3.8'
services:
  nats-1:
    image: nats:2.10.5
    ports:
      - "4222:4222"
      - "8222:8222"
    command: >
      -js
      -m 8222
      -cluster_name NATS
      -cluster nats://0.0.0.0:6222
      -routes nats://nats-2:6222,nats://nats-3:6222
    networks:
      - nats-cluster

  nats-2:
    image: nats:2.10.5
    ports:
      - "4223:4222"
      - "8223:8222"
    command: >
      -js
      -m 8222
      -cluster_name NATS
      -cluster nats://0.0.0.0:6222
      -routes nats://nats-1:6222,nats://nats-3:6222
    networks:
      - nats-cluster

  nats-3:
    image: nats:2.10.5
    ports:
      - "4224:4222"
      - "8224:8222"
    command: >
      -js
      -m 8222
      -cluster_name NATS
      -cluster nats://0.0.0.0:6222
      -routes nats://nats-1:6222,nats://nats-2:6222
    networks:
      - nats-cluster

networks:
  nats-cluster:
    driver: bridge
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nats
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nats-config
  namespace: nats
data:
  nats.conf: |
    pid_file: "/var/run/nats/nats.pid"
    http: 8222
    
    cluster {
      name: nats-cluster
      listen: 0.0.0.0:6222
      routes = [
        nats://nats-0.nats:6222
        nats://nats-1.nats:6222
        nats://nats-2.nats:6222
      ]
      cluster_advertise: $CLUSTER_ADVERTISE
      connect_retries: 30
    }
    
    jetstream {
      store_dir: "/data/jetstream"
      max_memory_store: 256MB
      max_file_store: 2GB
    }
    
    leafnodes {
      listen: 0.0.0.0:7422
    }
    
    websocket {
      listen: 0.0.0.0:8080
      no_tls: true
    }
    
    accounts {
      $SYS {
        users = [
          { user: "admin", pass: "admin" }
        ]
      }
    }
---
apiVersion: v1
kind: Service
metadata:
  name: nats
  namespace: nats
  labels:
    app: nats
spec:
  selector:
    app: nats
  clusterIP: None
  ports:
  - name: client
    port: 4222
  - name: cluster
    port: 6222
  - name: monitor
    port: 8222
  - name: metrics
    port: 7777
  - name: leafnodes
    port: 7422
  - name: websocket
    port: 8080
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nats
  namespace: nats
  labels:
    app: nats
spec:
  selector:
    matchLabels:
      app: nats
  replicas: 3
  serviceName: "nats"
  template:
    metadata:
      labels:
        app: nats
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
                  - nats
              topologyKey: kubernetes.io/hostname
      containers:
      - name: nats
        image: nats:2.10.5
        ports:
        - containerPort: 4222
          name: client
        - containerPort: 6222
          name: cluster
        - containerPort: 8222
          name: monitor
        - containerPort: 7422
          name: leafnodes
        - containerPort: 8080
          name: websocket
        command:
        - "nats-server"
        - "--config"
        - "/etc/nats-config/nats.conf"
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: CLUSTER_ADVERTISE
          value: $(POD_NAME).nats.$(POD_NAMESPACE).svc.cluster.local
        volumeMounts:
        - name: config-volume
          mountPath: /etc/nats-config
        - name: pid
          mountPath: /var/run/nats
        - name: data
          mountPath: /data
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /
            port: 8222
          initialDelaySeconds: 10
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 8222
          initialDelaySeconds: 10
          timeoutSeconds: 5
      volumes:
      - name: config-volume
        configMap:
          name: nats-config
      - name: pid
        emptyDir: {}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: nats-lb
  namespace: nats
  labels:
    app: nats
spec:
  type: LoadBalancer
  selector:
    app: nats
  ports:
  - name: client
    port: 4222
    targetPort: 4222
  - name: websocket
    port: 8080
    targetPort: 8080
```

### Binary Installation
```bash
# Download and install NATS server
curl -L https://github.com/nats-io/nats-server/releases/download/v2.10.5/nats-server-v2.10.5-linux-amd64.zip -o nats-server.zip
unzip nats-server.zip
sudo mv nats-server-v2.10.5-linux-amd64/nats-server /usr/local/bin/

# Download and install NATS CLI
curl -L https://github.com/nats-io/natscli/releases/download/v0.1.1/nats-0.1.1-linux-amd64.zip -o nats-cli.zip
unzip nats-cli.zip
sudo mv nats-0.1.1-linux-amd64/nats /usr/local/bin/

# Start NATS server
nats-server -js -m 8222

# Verify installation
nats --version
```

## Basic Operations

### CLI Operations
```bash
# Connect to NATS server
nats context add local --server nats://localhost:4222 --description "Local NATS"
nats context select local

# Server information
nats server info
nats server list

# Publish messages
nats pub subject.hello "Hello World"
nats pub user.updates '{"user": "john", "action": "login"}'

# Subscribe to messages
nats sub subject.hello
nats sub "user.*"
nats sub ">" # Subscribe to all subjects

# Request/Reply
nats reply help.please "I can help you"
nats request help.please "I need help"

# JetStream operations
nats stream add ORDERS --subjects "orders.*" --retention limits --max-age 24h
nats pub orders.new "New order data"
nats consumer add ORDERS ORDER_PROCESSOR --filter orders.new

# Account and user management
nats account info
nats server check connections
```

### Core NATS Examples

#### Python Publisher
```python
import asyncio
import nats
import json
from datetime import datetime

class NATSPublisher:
    def __init__(self, servers=["nats://localhost:4222"]):
        self.servers = servers
        self.nc = None
        
    async def connect(self):
        """Connect to NATS server"""
        self.nc = await nats.connect(
            servers=self.servers,
            error_cb=self.error_handler,
            disconnected_cb=self.disconnected_handler,
            reconnected_cb=self.reconnected_handler,
            closed_cb=self.closed_handler,
            max_reconnect_attempts=10,
            reconnect_time_wait=2
        )
        print(f"Connected to NATS at {self.nc.connected_url.netloc}")
    
    async def publish_message(self, subject, message, headers=None):
        """Publish a message to a subject"""
        if isinstance(message, dict):
            message = json.dumps(message)
        
        await self.nc.publish(subject, message.encode(), headers=headers)
        print(f"Published to {subject}: {message}")
    
    async def publish_with_reply(self, subject, message, timeout=5.0):
        """Publish message and wait for reply"""
        if isinstance(message, dict):
            message = json.dumps(message)
        
        try:
            response = await self.nc.request(subject, message.encode(), timeout=timeout)
            return response.data.decode()
        except asyncio.TimeoutError:
            print(f"Request to {subject} timed out")
            return None
    
    async def publish_batch(self, messages):
        """Publish multiple messages"""
        for subject, message in messages:
            await self.publish_message(subject, message)
        
        # Flush to ensure all messages are sent
        await self.nc.flush(timeout=1.0)
    
    async def error_handler(self, e):
        print(f"NATS error: {e}")
    
    async def disconnected_handler(self):
        print("Disconnected from NATS")
    
    async def reconnected_handler(self):
        print(f"Reconnected to NATS at {self.nc.connected_url.netloc}")
    
    async def closed_handler(self):
        print("Connection to NATS closed")
    
    async def close(self):
        """Close connection"""
        if self.nc:
            await self.nc.close()

# Usage example
async def main():
    publisher = NATSPublisher()
    await publisher.connect()
    
    # Publish simple message
    await publisher.publish_message("user.login", {
        "user_id": 123,
        "timestamp": datetime.now().isoformat(),
        "ip_address": "192.168.1.1"
    })
    
    # Publish with headers
    headers = {"Content-Type": "application/json", "Source": "user-service"}
    await publisher.publish_message("user.logout", {
        "user_id": 123,
        "session_duration": 3600
    }, headers=headers)
    
    # Request/Reply pattern
    response = await publisher.publish_with_reply("math.add", {
        "a": 5,
        "b": 3
    })
    print(f"Math service response: {response}")
    
    # Batch publishing
    messages = [
        ("events.click", {"button": "login", "user": 123}),
        ("events.view", {"page": "/dashboard", "user": 123}),
        ("events.purchase", {"item": "premium", "user": 123})
    ]
    await publisher.publish_batch(messages)
    
    await publisher.close()

# Run the example
asyncio.run(main())
```

#### Python Subscriber
```python
import asyncio
import nats
import json
import signal

class NATSSubscriber:
    def __init__(self, servers=["nats://localhost:4222"]):
        self.servers = servers
        self.nc = None
        self.subscriptions = []
        
    async def connect(self):
        """Connect to NATS server"""
        self.nc = await nats.connect(
            servers=self.servers,
            error_cb=self.error_handler,
            disconnected_cb=self.disconnected_handler,
            reconnected_cb=self.reconnected_handler,
            closed_cb=self.closed_handler
        )
        print(f"Connected to NATS at {self.nc.connected_url.netloc}")
    
    async def subscribe(self, subject, handler=None, queue_group=None):
        """Subscribe to a subject"""
        if handler is None:
            handler = self.default_message_handler
        
        subscription = await self.nc.subscribe(
            subject,
            cb=handler,
            queue=queue_group
        )
        
        self.subscriptions.append(subscription)
        print(f"Subscribed to {subject}" + (f" (queue: {queue_group})" if queue_group else ""))
        return subscription
    
    async def subscribe_with_reply(self, subject, handler):
        """Subscribe to requests and send replies"""
        async def reply_handler(msg):
            try:
                response = await handler(msg.data.decode(), msg.subject)
                if response:
                    if isinstance(response, dict):
                        response = json.dumps(response)
                    await msg.respond(response.encode())
            except Exception as e:
                error_response = json.dumps({"error": str(e)})
                await msg.respond(error_response.encode())
        
        subscription = await self.nc.subscribe(subject, cb=reply_handler)
        self.subscriptions.append(subscription)
        print(f"Subscribed to requests on {subject}")
        return subscription
    
    async def default_message_handler(self, msg):
        """Default message handler"""
        try:
            data = json.loads(msg.data.decode())
            print(f"Received on {msg.subject}: {data}")
        except json.JSONDecodeError:
            print(f"Received on {msg.subject}: {msg.data.decode()}")
    
    async def user_login_handler(self, msg):
        """Handle user login events"""
        data = json.loads(msg.data.decode())
        print(f"User {data['user_id']} logged in at {data['timestamp']}")
        
        # Process login logic here
        # e.g., update user session, log analytics, etc.
    
    async def math_service_handler(self, message, subject):
        """Handle math service requests"""
        try:
            data = json.loads(message)
            
            if subject == "math.add":
                result = data["a"] + data["b"]
                return {"result": result}
            elif subject == "math.multiply":
                result = data["a"] * data["b"]
                return {"result": result}
            else:
                return {"error": "Unknown operation"}
        except Exception as e:
            return {"error": str(e)}
    
    async def error_handler(self, e):
        print(f"NATS error: {e}")
    
    async def disconnected_handler(self):
        print("Disconnected from NATS")
    
    async def reconnected_handler(self):
        print(f"Reconnected to NATS at {self.nc.connected_url.netloc}")
    
    async def closed_handler(self):
        print("Connection to NATS closed")
    
    async def run_forever(self):
        """Keep the subscriber running"""
        try:
            # Set up signal handlers for graceful shutdown
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))
            
            # Keep running until shutdown
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
    
    async def shutdown(self):
        """Graceful shutdown"""
        print("Shutting down subscriber...")
        for subscription in self.subscriptions:
            await subscription.unsubscribe()
        
        if self.nc:
            await self.nc.close()

# Usage example
async def main():
    subscriber = NATSSubscriber()
    await subscriber.connect()
    
    # Subscribe to specific subjects
    await subscriber.subscribe("user.login", subscriber.user_login_handler)
    await subscriber.subscribe("user.logout")
    
    # Subscribe with queue groups for load balancing
    await subscriber.subscribe("events.*", queue_group="event-processors")
    
    # Subscribe to request/reply patterns
    await subscriber.subscribe_with_reply("math.*", subscriber.math_service_handler)
    
    # Wildcard subscriptions
    await subscriber.subscribe("monitoring.>")
    
    # Run forever
    await subscriber.run_forever()

# Run the subscriber
asyncio.run(main())
```

## JetStream (Streaming)

### Stream Management
```python
import asyncio
import nats
from nats.js import JetStreamContext
import json
from datetime import datetime, timedelta

class JetStreamManager:
    def __init__(self, servers=["nats://localhost:4222"]):
        self.servers = servers
        self.nc = None
        self.js = None
        
    async def connect(self):
        """Connect to NATS and create JetStream context"""
        self.nc = await nats.connect(servers=self.servers)
        self.js = self.nc.jetstream()
        print("Connected to NATS JetStream")
    
    async def create_stream(self, name, subjects, retention_policy="limits", 
                           max_age=None, max_bytes=None, max_msgs=None):
        """Create a JetStream stream"""
        config = {
            "name": name,
            "subjects": subjects,
            "retention": retention_policy,
        }
        
        if max_age:
            config["max_age"] = max_age
        if max_bytes:
            config["max_bytes"] = max_bytes
        if max_msgs:
            config["max_msgs"] = max_msgs
        
        try:
            stream = await self.js.add_stream(**config)
            print(f"Created stream: {name}")
            return stream
        except Exception as e:
            if "already exists" in str(e):
                print(f"Stream {name} already exists")
                return await self.js.stream_info(name)
            raise
    
    async def create_consumer(self, stream_name, consumer_name, 
                             filter_subject=None, deliver_policy="all",
                             ack_policy="explicit", max_deliver=5):
        """Create a JetStream consumer"""
        config = {
            "stream_name": stream_name,
            "config": {
                "durable_name": consumer_name,
                "deliver_policy": deliver_policy,
                "ack_policy": ack_policy,
                "max_deliver": max_deliver,
                "replay_policy": "instant"
            }
        }
        
        if filter_subject:
            config["config"]["filter_subject"] = filter_subject
        
        try:
            consumer = await self.js.add_consumer(**config)
            print(f"Created consumer: {consumer_name}")
            return consumer
        except Exception as e:
            if "already exists" in str(e):
                print(f"Consumer {consumer_name} already exists")
                return await self.js.consumer_info(stream_name, consumer_name)
            raise
    
    async def publish_to_stream(self, subject, message, headers=None):
        """Publish message to JetStream"""
        if isinstance(message, dict):
            message = json.dumps(message)
        
        ack = await self.js.publish(subject, message.encode(), headers=headers)
        print(f"Published to {subject}, sequence: {ack.seq}")
        return ack
    
    async def consume_messages(self, stream_name, consumer_name, batch_size=10):
        """Consume messages from stream"""
        subscription = await self.js.pull_subscribe(
            subject="",
            durable=consumer_name,
            stream=stream_name
        )
        
        while True:
            try:
                messages = await subscription.fetch(batch_size, timeout=5.0)
                
                for msg in messages:
                    try:
                        data = json.loads(msg.data.decode())
                        print(f"Processing: {data}")
                        
                        # Process message here
                        await self.process_message(data, msg.subject)
                        
                        # Acknowledge message
                        await msg.ack()
                        
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        # Negative acknowledge to retry
                        await msg.nak()
                        
            except asyncio.TimeoutError:
                print("No messages received, continuing...")
            except Exception as e:
                print(f"Error fetching messages: {e}")
                await asyncio.sleep(1)
    
    async def process_message(self, data, subject):
        """Process individual message"""
        # Implement your message processing logic here
        print(f"Processing message from {subject}: {data}")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
    
    async def stream_info(self, stream_name):
        """Get stream information"""
        info = await self.js.stream_info(stream_name)
        print(f"Stream: {info.config.name}")
        print(f"Messages: {info.state.messages}")
        print(f"Bytes: {info.state.bytes}")
        print(f"Subjects: {info.config.subjects}")
        return info
    
    async def consumer_info(self, stream_name, consumer_name):
        """Get consumer information"""
        info = await self.js.consumer_info(stream_name, consumer_name)
        print(f"Consumer: {info.name}")
        print(f"Delivered: {info.delivered.consumer_seq}")
        print(f"Pending: {info.num_pending}")
        return info
    
    async def close(self):
        """Close connection"""
        if self.nc:
            await self.nc.close()

# Usage example
async def main():
    js_manager = JetStreamManager()
    await js_manager.connect()
    
    # Create streams
    await js_manager.create_stream(
        name="ORDERS",
        subjects=["orders.*"],
        retention_policy="limits",
        max_age=24 * 3600 * 1000000000,  # 24 hours in nanoseconds
        max_msgs=1000000
    )
    
    await js_manager.create_stream(
        name="EVENTS",
        subjects=["events.*"],
        retention_policy="interest",
        max_age=7 * 24 * 3600 * 1000000000  # 7 days
    )
    
    # Create consumers
    await js_manager.create_consumer(
        stream_name="ORDERS",
        consumer_name="order-processor",
        filter_subject="orders.new",
        deliver_policy="new"
    )
    
    await js_manager.create_consumer(
        stream_name="EVENTS",
        consumer_name="analytics",
        deliver_policy="all"
    )
    
    # Publish some messages
    for i in range(10):
        await js_manager.publish_to_stream("orders.new", {
            "order_id": f"order-{i}",
            "customer_id": f"customer-{i % 3}",
            "amount": 100.00 + i,
            "timestamp": datetime.now().isoformat()
        })
    
    # Check stream info
    await js_manager.stream_info("ORDERS")
    
    # Start consuming (this would run forever)
    # await js_manager.consume_messages("ORDERS", "order-processor")
    
    await js_manager.close()

# Run the example
asyncio.run(main())
```

### Key-Value Store
```python
import asyncio
import nats
from nats.js import JetStreamContext
import json

class NATSKeyValueStore:
    def __init__(self, servers=["nats://localhost:4222"]):
        self.servers = servers
        self.nc = None
        self.js = None
        self.buckets = {}
        
    async def connect(self):
        """Connect to NATS and create JetStream context"""
        self.nc = await nats.connect(servers=self.servers)
        self.js = self.nc.jetstream()
        print("Connected to NATS Key-Value store")
    
    async def create_bucket(self, bucket_name, max_age=None, max_bytes=None):
        """Create a Key-Value bucket"""
        config = {"bucket": bucket_name}
        
        if max_age:
            config["max_age"] = max_age
        if max_bytes:
            config["max_bytes"] = max_bytes
        
        try:
            bucket = await self.js.create_key_value(**config)
            self.buckets[bucket_name] = bucket
            print(f"Created KV bucket: {bucket_name}")
            return bucket
        except Exception as e:
            if "already exists" in str(e):
                bucket = await self.js.key_value(bucket_name)
                self.buckets[bucket_name] = bucket
                print(f"Using existing KV bucket: {bucket_name}")
                return bucket
            raise
    
    async def put(self, bucket_name, key, value):
        """Put a value in the key-value store"""
        if bucket_name not in self.buckets:
            await self.create_bucket(bucket_name)
        
        bucket = self.buckets[bucket_name]
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        revision = await bucket.put(key, value.encode())
        print(f"Put {key} in {bucket_name}, revision: {revision}")
        return revision
    
    async def get(self, bucket_name, key):
        """Get a value from the key-value store"""
        if bucket_name not in self.buckets:
            bucket = await self.js.key_value(bucket_name)
            self.buckets[bucket_name] = bucket
        
        bucket = self.buckets[bucket_name]
        
        try:
            entry = await bucket.get(key)
            value = entry.value.decode()
            
            # Try to parse as JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            if "not found" in str(e):
                return None
            raise
    
    async def delete(self, bucket_name, key):
        """Delete a key from the store"""
        if bucket_name not in self.buckets:
            bucket = await self.js.key_value(bucket_name)
            self.buckets[bucket_name] = bucket
        
        bucket = self.buckets[bucket_name]
        await bucket.delete(key)
        print(f"Deleted {key} from {bucket_name}")
    
    async def list_keys(self, bucket_name):
        """List all keys in a bucket"""
        if bucket_name not in self.buckets:
            bucket = await self.js.key_value(bucket_name)
            self.buckets[bucket_name] = bucket
        
        bucket = self.buckets[bucket_name]
        keys = []
        
        async for key in bucket.keys():
            keys.append(key)
        
        return keys
    
    async def watch(self, bucket_name, key_pattern="*"):
        """Watch for changes in the key-value store"""
        if bucket_name not in self.buckets:
            bucket = await self.js.key_value(bucket_name)
            self.buckets[bucket_name] = bucket
        
        bucket = self.buckets[bucket_name]
        
        async for entry in bucket.watch(key_pattern):
            if entry.value:
                try:
                    value = json.loads(entry.value.decode())
                except json.JSONDecodeError:
                    value = entry.value.decode()
                
                print(f"Key {entry.key} changed: {value} (revision: {entry.revision})")
            else:
                print(f"Key {entry.key} deleted (revision: {entry.revision})")
    
    async def close(self):
        """Close connection"""
        if self.nc:
            await self.nc.close()

# Usage example
async def main():
    kv_store = NATSKeyValueStore()
    await kv_store.connect()
    
    # Create buckets
    await kv_store.create_bucket("user-sessions", max_age=3600)  # 1 hour TTL
    await kv_store.create_bucket("config", max_bytes=10*1024*1024)  # 10MB max
    
    # Store user session data
    session_data = {
        "user_id": 123,
        "login_time": "2023-01-01T12:00:00Z",
        "ip_address": "192.168.1.1",
        "permissions": ["read", "write"]
    }
    
    await kv_store.put("user-sessions", "session-abc123", session_data)
    
    # Store configuration
    config = {
        "database_url": "postgresql://localhost:5432/mydb",
        "redis_url": "redis://localhost:6379",
        "log_level": "INFO"
    }
    
    await kv_store.put("config", "app-config", config)
    
    # Retrieve data
    session = await kv_store.get("user-sessions", "session-abc123")
    print(f"Retrieved session: {session}")
    
    app_config = await kv_store.get("config", "app-config")
    print(f"Retrieved config: {app_config}")
    
    # List all keys
    session_keys = await kv_store.list_keys("user-sessions")
    print(f"Session keys: {session_keys}")
    
    # Update configuration
    await kv_store.put("config", "app-config", {
        **config,
        "log_level": "DEBUG"
    })
    
    # Watch for changes (this would run forever)
    # await kv_store.watch("config")
    
    await kv_store.close()

# Run the example
asyncio.run(main())
```

## Monitoring and Observability

### Prometheus Metrics
```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: nats-metrics
  namespace: nats
spec:
  selector:
    matchLabels:
      app: nats
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: nats-alerts
  namespace: nats
spec:
  groups:
  - name: nats
    rules:
    - alert: NATSServerDown
      expr: up{job="nats"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "NATS server is down"
        description: "NATS server {{ $labels.instance }} has been down for more than 1 minute"
    
    - alert: NATSHighConnectionCount
      expr: nats_core_connections > 1000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High NATS connection count"
        description: "NATS server has {{ $value }} connections"
    
    - alert: NATSHighMemoryUsage
      expr: nats_core_mem_bytes > 1073741824  # 1GB
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High NATS memory usage"
        description: "NATS server memory usage is {{ $value | humanize1024 }}B"
    
    - alert: JetStreamConsumerLag
      expr: nats_jetstream_consumer_num_pending > 1000
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High JetStream consumer lag"
        description: "Consumer {{ $labels.consumer_name }} has {{ $value }} pending messages"
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "NATS Monitoring Dashboard",
    "panels": [
      {
        "title": "Message Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(nats_core_in_msgs_total[5m])",
            "legendFormat": "Incoming Messages/sec"
          },
          {
            "expr": "rate(nats_core_out_msgs_total[5m])",
            "legendFormat": "Outgoing Messages/sec"
          }
        ]
      },
      {
        "title": "Byte Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(nats_core_in_bytes_total[5m])",
            "legendFormat": "Incoming Bytes/sec"
          },
          {
            "expr": "rate(nats_core_out_bytes_total[5m])",
            "legendFormat": "Outgoing Bytes/sec"
          }
        ]
      },
      {
        "title": "Connections",
        "type": "singlestat",
        "targets": [
          {
            "expr": "nats_core_connections",
            "legendFormat": "Active Connections"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "nats_core_mem_bytes",
            "legendFormat": "Memory Usage"
          }
        ]
      },
      {
        "title": "JetStream Streams",
        "type": "table",
        "targets": [
          {
            "expr": "nats_jetstream_stream_messages",
            "legendFormat": "{{stream_name}}"
          }
        ]
      },
      {
        "title": "Consumer Lag",
        "type": "graph",
        "targets": [
          {
            "expr": "nats_jetstream_consumer_num_pending",
            "legendFormat": "{{consumer_name}}"
          }
        ]
      }
    ]
  }
}
```

### Health Monitoring
```python
import asyncio
import aiohttp
import json
from datetime import datetime

class NATSHealthChecker:
    def __init__(self, monitoring_url="http://localhost:8222"):
        self.monitoring_url = monitoring_url
        
    async def check_server_health(self):
        """Check NATS server health"""
        async with aiohttp.ClientSession() as session:
            try:
                # General info
                async with session.get(f"{self.monitoring_url}/varz") as resp:
                    varz = await resp.json()
                
                # Connection info
                async with session.get(f"{self.monitoring_url}/connz") as resp:
                    connz = await resp.json()
                
                # JetStream info
                try:
                    async with session.get(f"{self.monitoring_url}/jsz") as resp:
                        jsz = await resp.json()
                except:
                    jsz = None
                
                health_status = {
                    "timestamp": datetime.now().isoformat(),
                    "server": {
                        "version": varz.get("version"),
                        "uptime": varz.get("uptime"),
                        "connections": varz.get("connections"),
                        "in_msgs": varz.get("in_msgs"),
                        "out_msgs": varz.get("out_msgs"),
                        "in_bytes": varz.get("in_bytes"),
                        "out_bytes": varz.get("out_bytes"),
                        "mem": varz.get("mem"),
                        "cpu": varz.get("cpu")
                    },
                    "connections": {
                        "total": connz.get("total"),
                        "offset": connz.get("offset"),
                        "limit": connz.get("limit")
                    }
                }
                
                if jsz:
                    health_status["jetstream"] = {
                        "memory": jsz.get("memory"),
                        "storage": jsz.get("storage"),
                        "accounts": len(jsz.get("accounts", [])),
                        "ha_assets": jsz.get("ha_assets")
                    }
                
                return health_status
                
            except Exception as e:
                return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def check_jetstream_streams(self):
        """Check JetStream stream health"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.monitoring_url}/jsz?streams=1") as resp:
                    data = await resp.json()
                
                streams_health = []
                for account in data.get("accounts", []):
                    for stream in account.get("streams", []):
                        stream_health = {
                            "name": stream.get("name"),
                            "subjects": stream.get("config", {}).get("subjects", []),
                            "messages": stream.get("state", {}).get("messages", 0),
                            "bytes": stream.get("state", {}).get("bytes", 0),
                            "first_seq": stream.get("state", {}).get("first_seq", 0),
                            "last_seq": stream.get("state", {}).get("last_seq", 0)
                        }
                        streams_health.append(stream_health)
                
                return streams_health
                
            except Exception as e:
                return {"error": str(e)}
    
    async def generate_health_report(self):
        """Generate comprehensive health report"""
        server_health = await self.check_server_health()
        streams_health = await self.check_jetstream_streams()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "server": server_health,
            "streams": streams_health,
            "summary": {
                "healthy": "error" not in server_health,
                "total_connections": server_health.get("server", {}).get("connections", 0),
                "total_streams": len(streams_health) if isinstance(streams_health, list) else 0
            }
        }
        
        return report

# Usage
async def main():
    health_checker = NATSHealthChecker()
    
    # Check server health
    health = await health_checker.check_server_health()
    print("Server Health:")
    print(json.dumps(health, indent=2))
    
    # Check streams
    streams = await health_checker.check_jetstream_streams()
    print("\nStreams Health:")
    print(json.dumps(streams, indent=2))
    
    # Generate full report
    report = await health_checker.generate_health_report()
    print("\nFull Health Report:")
    print(json.dumps(report, indent=2))

# Run health check
asyncio.run(main())
```

## Security and Authentication

### TLS Configuration
```yaml
# nats-tls.conf
port: 4222
https: 8222

tls {
  cert_file: "/etc/nats/certs/server.crt"
  key_file: "/etc/nats/certs/server.key"
  ca_file: "/etc/nats/certs/ca.crt"
  verify: true
  timeout: 5
}

cluster {
  name: "secure-cluster"
  listen: 0.0.0.0:6222
  
  tls {
    cert_file: "/etc/nats/certs/server.crt"
    key_file: "/etc/nats/certs/server.key"
    ca_file: "/etc/nats/certs/ca.crt"
    verify: true
  }
}
```

### Authentication Configuration
```yaml
# nats-auth.conf
authorization {
  users = [
    {
      user: "admin"
      password: "$2a$11$W2zko751KUvVy59mUTWmpOdWjpEm5qhcCZRd05GjI/sSOT.xtiHyG"
      permissions: {
        publish: ">"
        subscribe: ">"
      }
    }
    {
      user: "publisher"
      password: "$2a$11$xH8dkGrty1cBNtZjhze6/.Jk3LH6OVF5BBFN0rWG2SnE.FUEiLCLT"
      permissions: {
        publish: ["orders.*", "events.*"]
        subscribe: ["responses.*"]
      }
    }
    {
      user: "consumer"
      password: "$2a$11$UKtT4rj0nT5LuFiTLjIwGOe8J6vfUQ4/YZGpqvJWN.QhKrh8aVPpe"
      permissions: {
        publish: ["responses.*"]
        subscribe: ["orders.*", "events.*"]
      }
    }
  ]
}

accounts {
  ORDERS: {
    users: [
      { user: "order-service", password: "order-secret" }
    ]
    exports: [
      { service: "orders.*" }
    ]
  }
  
  BILLING: {
    users: [
      { user: "billing-service", password: "billing-secret" }
    ]
    imports: [
      { service: { account: "ORDERS", subject: "orders.*" }, to: "billing.orders.*" }
    ]
  }
}
```

### JWT Authentication
```python
import asyncio
import nats
import jwt
from datetime import datetime, timedelta

class JWTAuth:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key
    
    def generate_user_jwt(self, user_id, permissions=None, expires_in_hours=24):
        """Generate JWT for user authentication"""
        now = datetime.utcnow()
        
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(hours=expires_in_hours),
            "nats": {
                "permissions": permissions or {
                    "publish": ["user.>"],
                    "subscribe": ["user.>", "_INBOX.>"]
                }
            }
        }
        
        return jwt.encode(payload, self.private_key, algorithm="RS256")
    
    def generate_account_jwt(self, account_name):
        """Generate JWT for account"""
        payload = {
            "sub": account_name,
            "iat": datetime.utcnow(),
            "nats": {
                "type": "account",
                "limits": {
                    "connections": 1000,
                    "leaf_connections": 100,
                    "data": 1024*1024*1024,  # 1GB
                    "exports": 10,
                    "imports": 10
                }
            }
        }
        
        return jwt.encode(payload, self.private_key, algorithm="RS256")

# Connect with JWT
async def connect_with_jwt():
    # Generate JWT token
    auth = JWTAuth(private_key="your-private-key", public_key="your-public-key")
    user_jwt = auth.generate_user_jwt("user-123", {
        "publish": ["orders.*", "events.*"],
        "subscribe": ["notifications.*", "_INBOX.>"]
    })
    
    # Connect with JWT
    nc = await nats.connect(
        servers=["nats://localhost:4222"],
        user_jwt_cb=lambda: user_jwt.encode()
    )
    
    print("Connected with JWT authentication")
    await nc.close()

# Run JWT authentication example
asyncio.run(connect_with_jwt())
```

## Performance Tuning

### Server Configuration
```yaml
# high-performance.conf
port: 4222
monitor_port: 8222

# Connection limits
max_connections: 10000
max_control_line: 4096
max_payload: 8388608  # 8MB
max_pending: 67108864  # 64MB

# Write deadline
write_deadline: "10s"

# Ping settings
ping_interval: "2m"
ping_max: 2

# Cluster settings
cluster {
  name: "high-perf-cluster"
  listen: 0.0.0.0:6222
  no_advertise: false
  connect_retries: 10
  pool_size: 3
}

# JetStream optimization
jetstream {
  store_dir: "/data/jetstream"
  max_memory_store: 2GB
  max_file_store: 100GB
  sync_interval: "2m"
  sync_always: false
}

# System account for monitoring
system_account: $SYS

# Accounts for multi-tenancy
accounts {
  $SYS {
    users = [
      { user: "sys", pass: "sys" }
    ]
  }
}
```

### Client Optimization
```python
import asyncio
import nats
from nats.aio.client import Client

async def optimized_client_example():
    # Optimized connection settings
    nc = await nats.connect(
        servers=["nats://server1:4222", "nats://server2:4222", "nats://server3:4222"],
        
        # Connection settings
        max_reconnect_attempts=10,
        reconnect_time_wait=2,
        
        # Buffer settings
        pending_size=2*1024*1024,  # 2MB pending buffer
        
        # Flusher settings
        flush_timeout=1.0,
        
        # Performance settings
        drain_timeout=30,
        
        # Error handling
        error_cb=lambda e: print(f"Error: {e}"),
        disconnected_cb=lambda: print("Disconnected"),
        reconnected_cb=lambda: print("Reconnected"),
    )
    
    # Optimized publisher with batching
    async def batch_publisher():
        messages = []
        batch_size = 100
        
        for i in range(1000):
            messages.append(f"Message {i}")
            
            if len(messages) >= batch_size:
                # Send batch
                for msg in messages:
                    await nc.publish("test.subject", msg.encode())
                
                # Flush to ensure delivery
                await nc.flush()
                messages.clear()
        
        # Send remaining messages
        if messages:
            for msg in messages:
                await nc.publish("test.subject", msg.encode())
            await nc.flush()
    
    # Optimized consumer with queue group
    async def queue_consumer():
        async def message_handler(msg):
            # Fast message processing
            data = msg.data.decode()
            print(f"Processed: {data}")
        
        # Use queue group for load balancing
        await nc.subscribe("test.subject", cb=message_handler, queue="processors")
        
        # Keep consuming
        while True:
            await asyncio.sleep(1)
    
    # Run publisher and consumer concurrently
    await asyncio.gather(
        batch_publisher(),
        queue_consumer()
    )

# Performance testing
class PerformanceTester:
    def __init__(self, servers=["nats://localhost:4222"]):
        self.servers = servers
        
    async def test_publish_throughput(self, num_messages=10000, message_size=1024):
        """Test publishing throughput"""
        nc = await nats.connect(servers=self.servers)
        
        message = b'x' * message_size
        start_time = asyncio.get_event_loop().time()
        
        # Publish messages as fast as possible
        for i in range(num_messages):
            await nc.publish("perf.test", message)
        
        # Ensure all messages are sent
        await nc.flush()
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        throughput = num_messages / duration
        bytes_per_second = (num_messages * message_size) / duration
        
        print(f"Publish Performance:")
        print(f"  Messages/sec: {throughput:.2f}")
        print(f"  MB/sec: {bytes_per_second / 1024 / 1024:.2f}")
        print(f"  Duration: {duration:.2f}s")
        
        await nc.close()
        return throughput
    
    async def test_request_reply_latency(self, num_requests=1000):
        """Test request/reply latency"""
        nc = await nats.connect(servers=self.servers)
        
        # Set up responder
        async def responder(msg):
            await msg.respond(b"response")
        
        await nc.subscribe("perf.req", cb=responder)
        
        latencies = []
        
        for i in range(num_requests):
            start = asyncio.get_event_loop().time()
            
            try:
                response = await nc.request("perf.req", b"request", timeout=5.0)
                end = asyncio.get_event_loop().time()
                
                latency = (end - start) * 1000  # Convert to milliseconds
                latencies.append(latency)
                
            except asyncio.TimeoutError:
                print(f"Request {i} timed out")
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            print(f"Request/Reply Latency:")
            print(f"  Average: {avg_latency:.2f}ms")
            print(f"  Min: {min_latency:.2f}ms")
            print(f"  Max: {max_latency:.2f}ms")
        
        await nc.close()
        return latencies

# Run performance tests
async def run_perf_tests():
    tester = PerformanceTester()
    
    await tester.test_publish_throughput(10000, 1024)
    await tester.test_request_reply_latency(1000)

# Execute performance tests
asyncio.run(run_perf_tests())
```

---

### 📡 Stay Updated

**Release Notes**: [NATS Server](https://github.com/nats-io/nats-server/releases) • [JetStream](https://github.com/nats-io/jetstream/releases) • [NATS CLI](https://github.com/nats-io/natscli/releases)

**Project News**: [NATS Blog](https://nats.io/blog/) • [NATS Newsletter](https://nats.io/newsletter/) • [Release Videos](https://www.youtube.com/c/Synadia)

**Community**: [Slack Community](https://natsio.slack.com/) • [GitHub Discussions](https://github.com/nats-io/nats-server/discussions) • [Reddit](https://www.reddit.com/r/NATS/)