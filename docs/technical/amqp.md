# AMQP

AMQP (Advanced Message Queuing Protocol) is an open standard application layer protocol for message-oriented middleware. It enables robust, reliable, and secure messaging between applications and systems, making it essential for enterprise integration, microservices architectures, and distributed systems in platform engineering.

## Overview

AMQP is widely used in platform engineering for:
- Enterprise application integration and message routing
- Microservices communication with reliable delivery guarantees
- Financial services and banking transaction processing
- Real-time event processing and workflow orchestration
- Cross-platform and cross-language messaging solutions

## Key Features

- **Reliable Messaging**: Guaranteed message delivery with acknowledgments
- **Flexible Routing**: Complex routing patterns with exchanges and queues
- **Security**: Built-in authentication, authorization, and encryption
- **Interoperability**: Cross-platform and cross-language communication
- **Transactions**: ACID transaction support for message processing
- **Flow Control**: Built-in flow control and message throttling

## AMQP Core Concepts

### AMQP Components
```
Publisher → Exchange → Queue → Consumer
                ↓
           Routing Rules
           (Binding Keys)
```

### Key Elements
- **Connection**: TCP connection between client and broker
- **Channel**: Virtual connection within a TCP connection
- **Exchange**: Receives messages and routes them to queues
- **Queue**: Stores messages until consumed
- **Binding**: Rules that connect exchanges to queues
- **Routing Key**: Message attribute used for routing decisions

### Exchange Types
```
Direct Exchange:    Exact routing key match
Fanout Exchange:    Broadcast to all bound queues
Topic Exchange:     Pattern-based routing with wildcards
Headers Exchange:   Route based on message headers
```

## RabbitMQ Setup and Configuration

### Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install rabbitmq-server

# macOS (Homebrew)
brew install rabbitmq

# CentOS/RHEL
sudo yum install rabbitmq-server

# Start RabbitMQ service
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# Enable management plugin
sudo rabbitmq-plugins enable rabbitmq_management

# Access management UI at http://localhost:15672
# Default credentials: guest/guest
```

### RabbitMQ Configuration
```conf
# /etc/rabbitmq/rabbitmq.conf
# RabbitMQ configuration file

# Network settings
listeners.tcp.default = 5672
management.tcp.port = 15672

# Security
default_user = admin
default_pass = secure_password
default_vhost = /
default_user_tags.administrator = true

# Memory and disk limits
vm_memory_high_watermark.relative = 0.6
disk_free_limit.relative = 2.0

# Clustering
cluster_formation.peer_discovery_backend = classic_config
cluster_formation.classic_config.nodes.1 = rabbit@node1
cluster_formation.classic_config.nodes.2 = rabbit@node2

# SSL/TLS
listeners.ssl.default = 5671
ssl_options.cacertfile = /path/to/ca_certificate.pem
ssl_options.certfile = /path/to/server_certificate.pem
ssl_options.keyfile = /path/to/server_key.pem
ssl_options.verify = verify_peer
ssl_options.fail_if_no_peer_cert = true

# Message TTL and queue limits
default_permissions.configure = .*
default_permissions.read = .*
default_permissions.write = .*
```

### User and Permission Management
```bash
# Create users
sudo rabbitmqctl add_user app_user secure_password
sudo rabbitmqctl add_user monitoring_user monitor_password

# Set user tags
sudo rabbitmqctl set_user_tags app_user none
sudo rabbitmqctl set_user_tags monitoring_user monitoring

# Create virtual hosts
sudo rabbitmqctl add_vhost production
sudo rabbitmqctl add_vhost development

# Set permissions (configure/write/read)
sudo rabbitmqctl set_permissions -p production app_user "app.*" "app.*" "app.*"
sudo rabbitmqctl set_permissions -p production monitoring_user "" "" ".*"

# List users and permissions
sudo rabbitmqctl list_users
sudo rabbitmqctl list_permissions -p production
```

## Python AMQP Implementation

### Basic AMQP Client with Pika
```python
import pika
import json
import time
import threading
import logging
from datetime import datetime
from typing import Callable, Dict, Any, Optional

class AMQPManager:
    def __init__(self, connection_params=None, exchange_config=None):
        """
        Initialize AMQP Manager
        
        connection_params: pika.ConnectionParameters or connection URL
        exchange_config: Dictionary with exchange configurations
        """
        if connection_params is None:
            connection_params = pika.ConnectionParameters(
                host='localhost',
                port=5672,
                virtual_host='/',
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        
        self.connection_params = connection_params
        self.connection = None
        self.channel = None
        self.is_connected = False
        
        # Exchange configurations
        self.exchange_config = exchange_config or {
            'direct_exchange': {'type': 'direct', 'durable': True},
            'topic_exchange': {'type': 'topic', 'durable': True},
            'fanout_exchange': {'type': 'fanout', 'durable': True}
        }
        
        # Message handlers
        self.message_handlers: Dict[str, Callable] = {}
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Establish connection to RabbitMQ broker"""
        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.is_connected = True
            
            # Declare exchanges
            self._declare_exchanges()
            
            self.logger.info("Connected to RabbitMQ broker")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to RabbitMQ: {e}")
            return False
    
    def disconnect(self):
        """Close connection to RabbitMQ broker"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            self.is_connected = False
            self.logger.info("Disconnected from RabbitMQ broker")
        except Exception as e:
            self.logger.error(f"Error disconnecting: {e}")
    
    def _declare_exchanges(self):
        """Declare configured exchanges"""
        for exchange_name, config in self.exchange_config.items():
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=config['type'],
                durable=config.get('durable', True),
                auto_delete=config.get('auto_delete', False)
            )
            self.logger.info(f"Declared exchange: {exchange_name} ({config['type']})")
    
    def declare_queue(self, queue_name, durable=True, exclusive=False, 
                     auto_delete=False, arguments=None):
        """Declare a queue"""
        if not self.is_connected:
            raise Exception("Not connected to RabbitMQ")
        
        try:
            result = self.channel.queue_declare(
                queue=queue_name,
                durable=durable,
                exclusive=exclusive,
                auto_delete=auto_delete,
                arguments=arguments or {}
            )
            
            self.logger.info(f"Declared queue: {queue_name}")
            return result.method.queue
            
        except Exception as e:
            self.logger.error(f"Failed to declare queue {queue_name}: {e}")
            raise
    
    def bind_queue(self, queue_name, exchange_name, routing_key=""):
        """Bind queue to exchange with routing key"""
        if not self.is_connected:
            raise Exception("Not connected to RabbitMQ")
        
        try:
            self.channel.queue_bind(
                exchange=exchange_name,
                queue=queue_name,
                routing_key=routing_key
            )
            
            self.logger.info(f"Bound queue {queue_name} to exchange {exchange_name} with key '{routing_key}'")
            
        except Exception as e:
            self.logger.error(f"Failed to bind queue: {e}")
            raise
    
    def publish_message(self, exchange_name, routing_key, message_body, 
                       properties=None, mandatory=False, immediate=False):
        """Publish message to exchange"""
        if not self.is_connected:
            raise Exception("Not connected to RabbitMQ")
        
        try:
            # Convert message to JSON if it's a dict
            if isinstance(message_body, dict):
                message_body = json.dumps(message_body)
            
            # Set default properties
            if properties is None:
                properties = pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    timestamp=int(time.time()),
                    content_type='application/json'
                )
            
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=properties,
                mandatory=mandatory,
                immediate=immediate
            )
            
            self.logger.info(f"Published message to {exchange_name} with key '{routing_key}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to publish message: {e}")
            return False
    
    def consume_messages(self, queue_name, callback_func, auto_ack=False, 
                        exclusive=False, consumer_tag="", arguments=None):
        """Start consuming messages from queue"""
        if not self.is_connected:
            raise Exception("Not connected to RabbitMQ")
        
        def wrapper_callback(ch, method, properties, body):
            """Wrapper callback to handle message processing"""
            try:
                # Parse JSON body if possible
                try:
                    message_data = json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    message_data = body.decode('utf-8')
                
                # Create message context
                message_context = {
                    'body': message_data,
                    'properties': properties,
                    'delivery_tag': method.delivery_tag,
                    'routing_key': method.routing_key,
                    'exchange': method.exchange,
                    'redelivered': method.redelivered
                }
                
                # Call user callback
                result = callback_func(message_context)
                
                # Handle acknowledgment
                if not auto_ack:
                    if result is not False:  # Acknowledge unless explicitly returning False
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    else:
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
                if not auto_ack:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        try:
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=wrapper_callback,
                auto_ack=auto_ack,
                exclusive=exclusive,
                consumer_tag=consumer_tag,
                arguments=arguments or {}
            )
            
            self.logger.info(f"Started consuming from queue: {queue_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to start consuming: {e}")
            raise
    
    def start_consuming(self):
        """Start consuming messages (blocking)"""
        if not self.is_connected:
            raise Exception("Not connected to RabbitMQ")
        
        try:
            self.logger.info("Starting message consumption...")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Stopping consumption...")
            self.channel.stop_consuming()
        except Exception as e:
            self.logger.error(f"Error during consumption: {e}")
            raise
    
    def setup_dead_letter_queue(self, queue_name, dlq_name, exchange_name, 
                               routing_key, ttl_ms=None):
        """Setup dead letter queue for failed messages"""
        try:
            # Declare dead letter exchange and queue
            dlq_exchange = f"{exchange_name}.dlq"
            
            self.channel.exchange_declare(
                exchange=dlq_exchange,
                exchange_type='direct',
                durable=True
            )
            
            self.declare_queue(dlq_name, durable=True)
            self.bind_queue(dlq_name, dlq_exchange, routing_key)
            
            # Setup main queue with DLQ arguments
            queue_args = {
                'x-dead-letter-exchange': dlq_exchange,
                'x-dead-letter-routing-key': routing_key
            }
            
            if ttl_ms:
                queue_args['x-message-ttl'] = ttl_ms
            
            self.declare_queue(queue_name, arguments=queue_args)
            
            self.logger.info(f"Setup dead letter queue: {dlq_name} for {queue_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup dead letter queue: {e}")
            raise

# Usage example
if __name__ == "__main__":
    # Connection parameters
    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('guest', 'guest'),
        heartbeat=600,
        blocked_connection_timeout=300
    )
    
    # Exchange configuration
    exchange_config = {
        'order_exchange': {'type': 'topic', 'durable': True},
        'notification_exchange': {'type': 'fanout', 'durable': True},
        'dlq_exchange': {'type': 'direct', 'durable': True}
    }
    
    # Initialize AMQP manager
    amqp_manager = AMQPManager(connection_params, exchange_config)
    
    if amqp_manager.connect():
        # Declare queues
        order_queue = amqp_manager.declare_queue('order_processing_queue')
        notification_queue = amqp_manager.declare_queue('notification_queue')
        
        # Setup dead letter queue
        amqp_manager.setup_dead_letter_queue(
            'order_processing_queue',
            'order_processing_dlq',
            'order_exchange',
            'order.failed'
        )
        
        # Bind queues to exchanges
        amqp_manager.bind_queue(order_queue, 'order_exchange', 'order.created')
        amqp_manager.bind_queue(order_queue, 'order_exchange', 'order.updated')
        amqp_manager.bind_queue(notification_queue, 'notification_exchange', '')
        
        # Define message handlers
        def process_order(message_context):
            """Process order messages"""
            message = message_context['body']
            routing_key = message_context['routing_key']
            
            print(f"Processing order message: {routing_key}")
            print(f"Order data: {message}")
            
            try:
                # Simulate order processing
                order_id = message.get('order_id')
                if not order_id:
                    raise ValueError("Missing order_id")
                
                print(f"Processing order {order_id}")
                
                # Simulate processing time
                time.sleep(1)
                
                # Publish confirmation
                confirmation = {
                    'order_id': order_id,
                    'status': 'processed',
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                amqp_manager.publish_message(
                    'notification_exchange',
                    '',
                    confirmation
                )
                
                return True
                
            except Exception as e:
                print(f"Error processing order: {e}")
                return False  # Will nack and potentially send to DLQ
        
        def process_notification(message_context):
            """Process notification messages"""
            message = message_context['body']
            print(f"Sending notification: {message}")
            return True
        
        # Start consuming messages
        amqp_manager.consume_messages('order_processing_queue', process_order)
        amqp_manager.consume_messages('notification_queue', process_notification)
        
        # Publish some test messages
        order_message = {
            'order_id': '12345',
            'customer_id': 'cust_789',
            'items': [
                {'product_id': 'prod_1', 'quantity': 2},
                {'product_id': 'prod_2', 'quantity': 1}
            ],
            'total_amount': 89.99,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        amqp_manager.publish_message(
            'order_exchange',
            'order.created',
            order_message
        )
        
        # Start consuming (blocking)
        try:
            amqp_manager.start_consuming()
        finally:
            amqp_manager.disconnect()
    else:
        print("Failed to connect to RabbitMQ")
```

## Advanced AMQP Patterns

### Request-Response Pattern
```python
import uuid
import threading
from queue import Queue, Empty

class AMQPRequestResponse:
    def __init__(self, amqp_manager):
        self.amqp_manager = amqp_manager
        self.pending_requests = {}
        self.response_queue = None
        self.correlation_id_lock = threading.Lock()
        
        # Setup response handling
        self._setup_response_queue()
    
    def _setup_response_queue(self):
        """Setup exclusive queue for responses"""
        # Declare exclusive queue for responses
        result = self.amqp_manager.channel.queue_declare(
            queue='',
            exclusive=True,
            auto_delete=True
        )
        self.response_queue = result.method.queue
        
        # Start consuming responses
        self.amqp_manager.consume_messages(
            self.response_queue,
            self._handle_response,
            auto_ack=True
        )
        
        # Start consumer thread
        self.consumer_thread = threading.Thread(
            target=self._consume_responses,
            daemon=True
        )
        self.consumer_thread.start()
    
    def _consume_responses(self):
        """Consume responses in separate thread"""
        while True:
            try:
                self.amqp_manager.connection.process_data_events(time_limit=1)
            except Exception as e:
                print(f"Error consuming responses: {e}")
                break
    
    def _handle_response(self, message_context):
        """Handle incoming response messages"""
        properties = message_context['properties']
        correlation_id = properties.correlation_id
        
        if correlation_id in self.pending_requests:
            response_queue = self.pending_requests[correlation_id]
            response_queue.put(message_context['body'])
            del self.pending_requests[correlation_id]
        
        return True
    
    def send_request(self, exchange, routing_key, request_data, timeout=30):
        """Send request and wait for response"""
        correlation_id = str(uuid.uuid4())
        response_queue = Queue()
        
        with self.correlation_id_lock:
            self.pending_requests[correlation_id] = response_queue
        
        # Prepare request properties
        properties = pika.BasicProperties(
            reply_to=self.response_queue,
            correlation_id=correlation_id,
            delivery_mode=2
        )
        
        # Send request
        success = self.amqp_manager.publish_message(
            exchange,
            routing_key,
            request_data,
            properties
        )
        
        if not success:
            with self.correlation_id_lock:
                del self.pending_requests[correlation_id]
            raise Exception("Failed to send request")
        
        # Wait for response
        try:
            response = response_queue.get(timeout=timeout)
            return response
        except Empty:
            with self.correlation_id_lock:
                if correlation_id in self.pending_requests:
                    del self.pending_requests[correlation_id]
            raise TimeoutError(f"Request timed out after {timeout} seconds")

class AMQPRequestHandler:
    def __init__(self, amqp_manager):
        self.amqp_manager = amqp_manager
        self.request_handlers = {}
    
    def register_handler(self, routing_key, handler_func):
        """Register request handler for routing key"""
        self.request_handlers[routing_key] = handler_func
    
    def handle_request(self, message_context):
        """Handle incoming request and send response"""
        properties = message_context['properties']
        routing_key = message_context['routing_key']
        request_data = message_context['body']
        
        # Get handler for routing key
        handler = self.request_handlers.get(routing_key)
        if not handler:
            print(f"No handler registered for routing key: {routing_key}")
            return True
        
        try:
            # Process request
            response_data = handler(request_data)
            
            # Send response if reply_to is specified
            if properties.reply_to:
                response_properties = pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
                
                self.amqp_manager.publish_message(
                    '',  # Default exchange
                    properties.reply_to,
                    response_data,
                    response_properties
                )
            
            return True
            
        except Exception as e:
            print(f"Error handling request: {e}")
            
            # Send error response
            if properties.reply_to:
                error_response = {
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                error_properties = pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
                
                self.amqp_manager.publish_message(
                    '',
                    properties.reply_to,
                    error_response,
                    error_properties
                )
            
            return True

# Example usage
def user_service_handler(request_data):
    """Handle user service requests"""
    user_id = request_data.get('user_id')
    if not user_id:
        raise ValueError("Missing user_id")
    
    # Simulate user lookup
    user_data = {
        'user_id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com',
        'status': 'active'
    }
    
    return user_data

# Setup request-response
req_resp = AMQPRequestResponse(amqp_manager)
req_handler = AMQPRequestHandler(amqp_manager)

# Register handler
req_handler.register_handler('user.get', user_service_handler)

# Setup request queue
amqp_manager.declare_queue('user_requests')
amqp_manager.bind_queue('user_requests', 'direct_exchange', 'user.get')
amqp_manager.consume_messages('user_requests', req_handler.handle_request)

# Send request
request_data = {'user_id': '123'}
response = req_resp.send_request('direct_exchange', 'user.get', request_data)
print(f"Response: {response}")
```

### Publish-Subscribe with Topic Routing
```python
class TopicPublisher:
    def __init__(self, amqp_manager, exchange_name='topic_exchange'):
        self.amqp_manager = amqp_manager
        self.exchange_name = exchange_name
    
    def publish_event(self, event_type, entity_type, entity_id, event_data):
        """Publish event with hierarchical routing key"""
        routing_key = f"{event_type}.{entity_type}.{entity_id}"
        
        message = {
            'event_type': event_type,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'data': event_data,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        }
        
        return self.amqp_manager.publish_message(
            self.exchange_name,
            routing_key,
            message
        )
    
    def publish_order_event(self, event_type, order_id, order_data):
        """Publish order-specific events"""
        return self.publish_event(event_type, 'order', order_id, order_data)
    
    def publish_user_event(self, event_type, user_id, user_data):
        """Publish user-specific events"""
        return self.publish_event(event_type, 'user', user_id, user_data)

class TopicSubscriber:
    def __init__(self, amqp_manager, exchange_name='topic_exchange'):
        self.amqp_manager = amqp_manager
        self.exchange_name = exchange_name
        self.subscriptions = {}
    
    def subscribe(self, routing_pattern, queue_name, handler_func):
        """Subscribe to events matching routing pattern"""
        # Declare queue
        self.amqp_manager.declare_queue(queue_name, durable=True)
        
        # Bind queue with routing pattern
        self.amqp_manager.bind_queue(queue_name, self.exchange_name, routing_pattern)
        
        # Store subscription
        self.subscriptions[queue_name] = {
            'pattern': routing_pattern,
            'handler': handler_func
        }
        
        # Start consuming
        self.amqp_manager.consume_messages(queue_name, handler_func)
    
    def subscribe_to_all_orders(self, queue_name, handler_func):
        """Subscribe to all order events"""
        self.subscribe('*.order.*', queue_name, handler_func)
    
    def subscribe_to_order_created(self, queue_name, handler_func):
        """Subscribe to order creation events"""
        self.subscribe('created.order.*', queue_name, handler_func)
    
    def subscribe_to_specific_user(self, user_id, queue_name, handler_func):
        """Subscribe to events for specific user"""
        self.subscribe(f'*.user.{user_id}', queue_name, handler_func)

# Example usage
publisher = TopicPublisher(amqp_manager)
subscriber = TopicSubscriber(amqp_manager)

# Define event handlers
def handle_order_events(message_context):
    """Handle all order events"""
    event = message_context['body']
    print(f"Order Event: {event['event_type']} for order {event['entity_id']}")
    return True

def handle_order_created(message_context):
    """Handle order creation events"""
    event = message_context['body']
    print(f"New order created: {event['entity_id']}")
    
    # Send welcome email
    order_data = event['data']
    customer_email = order_data.get('customer_email')
    if customer_email:
        print(f"Sending order confirmation to {customer_email}")
    
    return True

def handle_user_events(message_context):
    """Handle user events for specific user"""
    event = message_context['body']
    print(f"User Event: {event['event_type']} for user {event['entity_id']}")
    return True

# Setup subscriptions
subscriber.subscribe_to_all_orders('all_orders_queue', handle_order_events)
subscriber.subscribe_to_order_created('order_created_queue', handle_order_created)
subscriber.subscribe_to_specific_user('123', 'user_123_events', handle_user_events)

# Publish events
order_data = {
    'customer_id': '456',
    'customer_email': 'customer@example.com',
    'total_amount': 99.99,
    'items': [{'product_id': 'prod_1', 'quantity': 2}]
}

publisher.publish_order_event('created', '789', order_data)
publisher.publish_order_event('updated', '789', {'status': 'processing'})
publisher.publish_user_event('login', '123', {'ip_address': '192.168.1.100'})
```

## Docker and Docker Compose Setup

### RabbitMQ with Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3.12-management
    container_name: rabbitmq-broker
    hostname: rabbitmq
    ports:
      - "5672:5672"     # AMQP port
      - "15672:15672"   # Management UI
      - "5671:5671"     # AMQP over TLS
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: secure_password
      RABBITMQ_DEFAULT_VHOST: /
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      - ./rabbitmq/config:/etc/rabbitmq
      - ./rabbitmq/logs:/var/log/rabbitmq
    networks:
      - amqp-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  amqp-publisher:
    build: 
      context: .
      dockerfile: Dockerfile.publisher
    container_name: amqp-publisher
    depends_on:
      rabbitmq:
        condition: service_healthy
    environment:
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: admin
      RABBITMQ_PASSWORD: secure_password
    volumes:
      - ./app:/app
    networks:
      - amqp-network
    restart: unless-stopped

  amqp-consumer:
    build: 
      context: .
      dockerfile: Dockerfile.consumer
    container_name: amqp-consumer
    depends_on:
      rabbitmq:
        condition: service_healthy
    environment:
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: admin
      RABBITMQ_PASSWORD: secure_password
    volumes:
      - ./app:/app
    networks:
      - amqp-network
    restart: unless-stopped
    deploy:
      replicas: 3

  amqp-monitor:
    image: python:3.9-slim
    container_name: amqp-monitor
    depends_on:
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./monitoring:/app
    working_dir: /app
    command: ["python", "amqp_monitor.py"]
    environment:
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: admin
      RABBITMQ_PASSWORD: secure_password
    networks:
      - amqp-network
    restart: unless-stopped

networks:
  amqp-network:
    driver: bridge

volumes:
  rabbitmq_data:
```

### RabbitMQ Configuration Files
```conf
# rabbitmq/config/rabbitmq.conf
# Management plugin configuration
management.tcp.port = 15672
management.tcp.ip = 0.0.0.0

# AMQP configuration
listeners.tcp.default = 5672
listeners.ssl.default = 5671

# Clustering
cluster_formation.peer_discovery_backend = classic_config

# Memory and disk limits
vm_memory_high_watermark.relative = 0.6
disk_free_limit.relative = 2.0

# Security
auth_backends.1 = internal
auth_backends.2 = cache

# SSL/TLS
ssl_options.verify = verify_peer
ssl_options.fail_if_no_peer_cert = false

# Logging
log.console = true
log.console.level = info
log.file = /var/log/rabbitmq/rabbitmq.log
log.file.level = info

# Default limits
default_permissions.configure = .*
default_permissions.read = .*
default_permissions.write = .*
```

```conf
# rabbitmq/config/advanced.config
[
  {rabbit, [
    {tcp_listeners, [5672]},
    {ssl_listeners, [5671]},
    {default_user, <<"admin">>},
    {default_pass, <<"secure_password">>},
    {hipe_compile, false},
    {collect_statistics_interval, 5000}
  ]},
  {rabbitmq_management, [
    {listener, [
      {port, 15672},
      {ip, "0.0.0.0"}
    ]}
  ]}
].
```

## Monitoring and Management

### AMQP Connection Monitoring
```python
import requests
import time
from datetime import datetime

class RabbitMQMonitor:
    def __init__(self, management_url, username, password):
        self.management_url = management_url.rstrip('/')
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
    
    def get_overview(self):
        """Get cluster overview statistics"""
        response = self.session.get(f"{self.management_url}/api/overview")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get overview: {response.status_code}")
    
    def get_queues(self, vhost="/"):
        """Get queue statistics"""
        response = self.session.get(f"{self.management_url}/api/queues/{vhost}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get queues: {response.status_code}")
    
    def get_exchanges(self, vhost="/"):
        """Get exchange statistics"""
        response = self.session.get(f"{self.management_url}/api/exchanges/{vhost}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get exchanges: {response.status_code}")
    
    def get_connections(self):
        """Get connection statistics"""
        response = self.session.get(f"{self.management_url}/api/connections")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get connections: {response.status_code}")
    
    def get_channels(self):
        """Get channel statistics"""
        response = self.session.get(f"{self.management_url}/api/channels")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get channels: {response.status_code}")
    
    def print_dashboard(self):
        """Print monitoring dashboard"""
        try:
            overview = self.get_overview()
            queues = self.get_queues()
            connections = self.get_connections()
            
            print("\n" + "="*60)
            print("RABBITMQ MONITORING DASHBOARD")
            print("="*60)
            print(f"Timestamp: {datetime.utcnow().isoformat()}")
            print(f"RabbitMQ Version: {overview.get('rabbitmq_version', 'Unknown')}")
            print(f"Erlang Version: {overview.get('erlang_version', 'Unknown')}")
            
            # Message statistics
            message_stats = overview.get('message_stats', {})
            print(f"\nMessage Statistics:")
            print(f"  Total Published: {message_stats.get('publish', 0)}")
            print(f"  Total Delivered: {message_stats.get('deliver_get', 0)}")
            print(f"  Total Acknowledged: {message_stats.get('ack', 0)}")
            
            # Queue statistics
            print(f"\nQueue Statistics:")
            print(f"  Total Queues: {len(queues)}")
            total_messages = sum(q.get('messages', 0) for q in queues)
            total_ready = sum(q.get('messages_ready', 0) for q in queues)
            total_unacked = sum(q.get('messages_unacknowledged', 0) for q in queues)
            
            print(f"  Total Messages: {total_messages}")
            print(f"  Ready Messages: {total_ready}")
            print(f"  Unacknowledged: {total_unacked}")
            
            # Top queues by message count
            print(f"\nTop Queues by Message Count:")
            sorted_queues = sorted(queues, key=lambda q: q.get('messages', 0), reverse=True)
            for queue in sorted_queues[:5]:
                name = queue['name']
                messages = queue.get('messages', 0)
                ready = queue.get('messages_ready', 0)
                unacked = queue.get('messages_unacknowledged', 0)
                print(f"  {name:<30} Total: {messages:>6} Ready: {ready:>6} Unacked: {unacked:>6}")
            
            # Connection statistics
            print(f"\nConnection Statistics:")
            print(f"  Total Connections: {len(connections)}")
            active_connections = [c for c in connections if c.get('state') == 'running']
            print(f"  Active Connections: {len(active_connections)}")
            
            # Connection details
            for conn in active_connections[:5]:
                name = conn.get('name', 'Unknown')
                user = conn.get('user', 'Unknown')
                vhost = conn.get('vhost', '/')
                print(f"  {name:<30} User: {user:<15} VHost: {vhost}")
            
        except Exception as e:
            print(f"Error generating dashboard: {e}")
    
    def check_queue_health(self, queue_thresholds=None):
        """Check queue health against thresholds"""
        if queue_thresholds is None:
            queue_thresholds = {
                'max_messages': 1000,
                'max_unacked': 100,
                'max_consumer_utilisation': 0.8
            }
        
        alerts = []
        
        try:
            queues = self.get_queues()
            
            for queue in queues:
                queue_name = queue['name']
                messages = queue.get('messages', 0)
                unacked = queue.get('messages_unacknowledged', 0)
                consumer_util = queue.get('consumer_utilisation', 0)
                
                # Check thresholds
                if messages > queue_thresholds['max_messages']:
                    alerts.append({
                        'type': 'high_message_count',
                        'queue': queue_name,
                        'value': messages,
                        'threshold': queue_thresholds['max_messages']
                    })
                
                if unacked > queue_thresholds['max_unacked']:
                    alerts.append({
                        'type': 'high_unacked_count',
                        'queue': queue_name,
                        'value': unacked,
                        'threshold': queue_thresholds['max_unacked']
                    })
                
                if consumer_util > queue_thresholds['max_consumer_utilisation']:
                    alerts.append({
                        'type': 'high_consumer_utilisation',
                        'queue': queue_name,
                        'value': consumer_util,
                        'threshold': queue_thresholds['max_consumer_utilisation']
                    })
            
            return alerts
            
        except Exception as e:
            return [{'type': 'monitoring_error', 'message': str(e)}]

# Usage example
monitor = RabbitMQMonitor(
    management_url="http://localhost:15672",
    username="admin",
    password="secure_password"
)

# Print dashboard
monitor.print_dashboard()

# Check health
alerts = monitor.check_queue_health()
if alerts:
    print("\n🚨 ALERTS:")
    for alert in alerts:
        print(f"  {alert['type']}: {alert}")
```

## Best Practices

### Message Design and Serialization
```python
import json
import gzip
import pickle
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class AMQPMessage:
    """Standardized AMQP message format"""
    message_id: str
    message_type: str
    timestamp: str
    version: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class MessageSerializer:
    """Message serialization with compression and validation"""
    
    @staticmethod
    def serialize_json(message_data, compress=False):
        """Serialize message to JSON with optional compression"""
        json_data = json.dumps(message_data, ensure_ascii=False, separators=(',', ':'))
        
        if compress:
            return gzip.compress(json_data.encode('utf-8'))
        else:
            return json_data.encode('utf-8')
    
    @staticmethod
    def deserialize_json(message_bytes, compressed=False):
        """Deserialize JSON message with optional decompression"""
        if compressed:
            message_bytes = gzip.decompress(message_bytes)
        
        return json.loads(message_bytes.decode('utf-8'))
    
    @staticmethod
    def create_standard_message(message_type, data, message_id=None, metadata=None):
        """Create standardized message"""
        import uuid
        
        return AMQPMessage(
            message_id=message_id or str(uuid.uuid4()),
            message_type=message_type,
            timestamp=datetime.utcnow().isoformat(),
            version="1.0",
            data=data,
            metadata=metadata or {}
        )

# Message validation
def validate_message_schema(message_data, required_fields):
    """Validate message against schema"""
    errors = []
    
    for field in required_fields:
        if field not in message_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate timestamp format
    if 'timestamp' in message_data:
        try:
            datetime.fromisoformat(message_data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            errors.append("Invalid timestamp format")
    
    return errors

# Good message examples
order_message = MessageSerializer.create_standard_message(
    message_type="order.created",
    data={
        "order_id": "ORD-12345",
        "customer_id": "CUST-789",
        "items": [
            {"product_id": "PROD-1", "quantity": 2, "price": 29.99},
            {"product_id": "PROD-2", "quantity": 1, "price": 19.99}
        ],
        "total_amount": 79.97,
        "currency": "USD",
        "shipping_address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105"
        }
    },
    metadata={
        "source_system": "ecommerce_api",
        "correlation_id": "trace-abc123",
        "user_agent": "Mobile App v2.1"
    }
)

# Serialize message
serialized = MessageSerializer.serialize_json(order_message.to_dict(), compress=True)
```

### Connection Management and Resilience
```python
import time
import random
from contextlib import contextmanager

class ResilientAMQPConnection:
    def __init__(self, connection_params_list, max_retries=5, retry_delay=1):
        self.connection_params_list = connection_params_list
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.current_connection = None
        self.current_channel = None
        
    def connect_with_failover(self):
        """Connect with automatic failover"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            for params in self.connection_params_list:
                try:
                    connection = pika.BlockingConnection(params)
                    channel = connection.channel()
                    
                    self.current_connection = connection
                    self.current_channel = channel
                    
                    print(f"Connected to {params.host}:{params.port}")
                    return connection, channel
                    
                except Exception as e:
                    last_exception = e
                    print(f"Failed to connect to {params.host}:{params.port}: {e}")
                    continue
            
            if attempt < self.max_retries - 1:
                delay = self.retry_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
        
        raise Exception(f"Failed to connect after {self.max_retries} attempts. Last error: {last_exception}")
    
    @contextmanager
    def get_channel(self):
        """Context manager for channel operations"""
        if not self.current_connection or self.current_connection.is_closed:
            self.connect_with_failover()
        
        try:
            yield self.current_channel
        except pika.exceptions.ConnectionClosed:
            print("Connection closed, attempting to reconnect...")
            self.connect_with_failover()
            yield self.current_channel
        except Exception as e:
            print(f"Channel error: {e}")
            raise
    
    def publish_with_retry(self, exchange, routing_key, message, properties=None):
        """Publish with automatic retry"""
        for attempt in range(self.max_retries):
            try:
                with self.get_channel() as channel:
                    channel.basic_publish(
                        exchange=exchange,
                        routing_key=routing_key,
                        body=message,
                        properties=properties or pika.BasicProperties(delivery_mode=2)
                    )
                return True
                
            except Exception as e:
                print(f"Publish attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise
        
        return False
    
    def close(self):
        """Close connection"""
        if self.current_connection and not self.current_connection.is_closed:
            self.current_connection.close()

# Usage with multiple brokers
connection_params = [
    pika.ConnectionParameters(host='primary-rabbitmq.example.com', port=5672),
    pika.ConnectionParameters(host='backup-rabbitmq.example.com', port=5672),
    pika.ConnectionParameters(host='localhost', port=5672)
]

resilient_conn = ResilientAMQPConnection(connection_params)
resilient_conn.publish_with_retry('orders', 'order.created', json.dumps(order_message.to_dict()))
```

### Performance Optimization
```python
class HighPerformanceAMQP:
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.connection = None
        self.channel = None
        self.message_buffer = []
        self.buffer_size = 100
        
    def setup_optimized_connection(self):
        """Setup connection with optimized parameters"""
        # Optimize connection parameters
        optimized_params = pika.ConnectionParameters(
            **self.connection_params,
            heartbeat=600,  # Longer heartbeat
            blocked_connection_timeout=300,
            socket_timeout=5,
            channel_max=100,  # More channels
            frame_max=131072  # Larger frame size
        )
        
        self.connection = pika.BlockingConnection(optimized_params)
        self.channel = self.connection.channel()
        
        # Enable publisher confirms for reliability
        self.channel.confirm_delivery()
        
        # Set QoS for consumers
        self.channel.basic_qos(prefetch_count=50)
    
    def batch_publish(self, exchange, messages, routing_key_func=None):
        """Publish messages in batches for better performance"""
        if not routing_key_func:
            routing_key_func = lambda msg: ''
        
        # Batch messages
        for i in range(0, len(messages), self.buffer_size):
            batch = messages[i:i + self.buffer_size]
            
            for message in batch:
                routing_key = routing_key_func(message)
                
                self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            
            # Process pending confirms
            try:
                self.channel.confirm_delivery()
                print(f"Batch of {len(batch)} messages published successfully")
            except pika.exceptions.UnroutableError as e:
                print(f"Some messages were unroutable: {e}")
    
    def consume_with_threading(self, queue_name, handler_func, thread_count=4):
        """Consume messages using multiple threads"""
        import threading
        import queue
        
        message_queue = queue.Queue(maxsize=1000)
        
        def message_consumer():
            """Consumer thread function"""
            while True:
                try:
                    message_data = message_queue.get(timeout=1)
                    if message_data is None:  # Shutdown signal
                        break
                    
                    handler_func(message_data)
                    message_queue.task_done()
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error processing message: {e}")
        
        def amqp_receiver(ch, method, properties, body):
            """AMQP message receiver"""
            message_data = {
                'body': body,
                'method': method,
                'properties': properties,
                'channel': ch
            }
            
            try:
                message_queue.put(message_data, timeout=1)
            except queue.Full:
                print("Message queue full, rejecting message")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        # Start consumer threads
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=message_consumer, daemon=True)
            thread.start()
            threads.append(thread)
        
        # Start AMQP consumption
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=amqp_receiver,
            auto_ack=False
        )
        
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopping consumption...")
            
            # Signal threads to stop
            for _ in range(thread_count):
                message_queue.put(None)
            
            # Wait for threads to finish
            for thread in threads:
                thread.join()
            
            self.channel.stop_consuming()

# Usage
high_perf = HighPerformanceAMQP({
    'host': 'localhost',
    'port': 5672,
    'virtual_host': '/',
    'credentials': pika.PlainCredentials('guest', 'guest')
})

high_perf.setup_optimized_connection()

# Batch publish
messages = [{'id': i, 'data': f'message_{i}'} for i in range(1000)]
high_perf.batch_publish('test_exchange', messages, lambda msg: f"msg.{msg['id'] % 10}")
```

## Resources

- [AMQP 0.9.1 Specification](https://www.amqp.org/specification/0-9-1/amqp-org-download) - Official AMQP specification
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html) - Complete RabbitMQ documentation
- [Pika Documentation](https://pika.readthedocs.io/) - Python AMQP client library
- [RabbitMQ Management HTTP API](https://www.rabbitmq.com/management.html) - Management and monitoring API
- [AMQP Best Practices](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html) - Production best practices
- [RabbitMQ Clustering](https://www.rabbitmq.com/clustering.html) - High availability setup
- [Message Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/) - Enterprise integration patterns
- [Apache Qpid](https://qpid.apache.org/) - Alternative AMQP broker implementation
- [Spring AMQP](https://docs.spring.io/spring-amqp/docs/current/reference/html/) - Java/Spring AMQP integration
- [Node.js AMQP](https://www.npmjs.com/package/amqplib) - JavaScript AMQP client library