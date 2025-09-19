# Redis Pub/Sub

Redis Pub/Sub is a messaging pattern implementation provided by Redis that enables real-time message broadcasting and subscription. It's essential for building real-time applications, event-driven architectures, and inter-service communication in platform engineering.

## Overview

Redis Pub/Sub is widely used in platform engineering for:
- Real-time notifications and live updates
- Event-driven microservices communication
- WebSocket message broadcasting
- Cache invalidation coordination
- Distributed system event propagation

## Key Features

- **Lightweight Messaging**: Low-latency, high-throughput message delivery
- **Pattern-Based Subscriptions**: Subscribe using glob-style patterns
- **Fire-and-Forget**: Messages are not persisted (at-most-once delivery)
- **Real-Time**: Immediate message delivery to subscribers
- **Scalable**: Horizontal scaling with Redis Cluster
- **Simple Protocol**: Easy integration across programming languages

## Redis Pub/Sub Concepts

### Core Components
```
Publisher → Redis Server → Subscriber(s)
                      ↘ Pattern Subscriber(s)
```

### Message Flow
- **Publisher**: Sends messages to channels
- **Channel**: Named message destination
- **Subscriber**: Receives messages from specific channels
- **Pattern Subscriber**: Receives messages matching patterns

### Channel Patterns
```bash
# Exact channel subscription
SUBSCRIBE channel_name

# Pattern-based subscription (glob patterns)
PSUBSCRIBE user:*
PSUBSCRIBE events:order:*
PSUBSCRIBE notifications:*:priority:high
```

## Redis Setup for Pub/Sub

### Redis Configuration
```conf
# redis.conf - Redis configuration for Pub/Sub

# Basic networking
bind 0.0.0.0
port 6379
protected-mode yes
requirepass your_secure_password

# Memory settings
maxmemory 2gb
maxmemory-policy allkeys-lru

# Pub/Sub specific settings
client-output-buffer-limit pubsub 32mb 8mb 60

# Persistence (optional for pub/sub)
save 900 1
save 300 10
save 60 10000

# Security
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log

# Performance
tcp-keepalive 300
timeout 0
tcp-backlog 511
```

### Docker Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis-pubsub
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: redis-server /usr/local/etc/redis/redis.conf
    networks:
      - redis-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis-sentinel:
    image: redis:7-alpine
    container_name: redis-sentinel
    ports:
      - "26379:26379"
    volumes:
      - ./sentinel.conf:/usr/local/etc/redis/sentinel.conf
    command: redis-sentinel /usr/local/etc/redis/sentinel.conf
    networks:
      - redis-network
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis_data:

networks:
  redis-network:
    driver: bridge
```

## Python Redis Pub/Sub Implementation

### Basic Pub/Sub Client
```python
import redis
import json
import time
import threading
import logging
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime
import fnmatch

class RedisPubSubManager:
    def __init__(self, host='localhost', port=6379, password=None, db=0, 
                 decode_responses=True, socket_timeout=None):
        """
        Initialize Redis Pub/Sub Manager
        
        Args:
            host: Redis server host
            port: Redis server port
            password: Redis password
            db: Redis database number
            decode_responses: Decode responses to strings
            socket_timeout: Socket timeout in seconds
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=decode_responses,
            socket_timeout=socket_timeout
        )
        
        self.pubsub = self.redis_client.pubsub()
        self.is_listening = False
        self.listener_thread = None
        self.message_handlers: Dict[str, Callable] = {}
        self.pattern_handlers: Dict[str, Callable] = {}
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def test_connection(self):
        """Test Redis connection"""
        try:
            pong = self.redis_client.ping()
            self.logger.info(f"Redis connection successful: {pong}")
            return True
        except Exception as e:
            self.logger.error(f"Redis connection failed: {e}")
            return False
    
    def publish(self, channel: str, message: Any, serialize_json=True) -> int:
        """
        Publish message to channel
        
        Args:
            channel: Channel name
            message: Message to publish
            serialize_json: Whether to serialize message as JSON
            
        Returns:
            Number of subscribers that received the message
        """
        try:
            if serialize_json and isinstance(message, (dict, list)):
                message = json.dumps(message)
            
            subscribers = self.redis_client.publish(channel, message)
            self.logger.debug(f"Published to {channel}: {message} ({subscribers} subscribers)")
            return subscribers
            
        except Exception as e:
            self.logger.error(f"Error publishing to {channel}: {e}")
            return 0
    
    def subscribe(self, channel: str, handler: Optional[Callable] = None):
        """
        Subscribe to specific channel
        
        Args:
            channel: Channel name
            handler: Message handler function
        """
        try:
            self.pubsub.subscribe(channel)
            
            if handler:
                self.message_handlers[channel] = handler
            
            self.logger.info(f"Subscribed to channel: {channel}")
            
        except Exception as e:
            self.logger.error(f"Error subscribing to {channel}: {e}")
    
    def psubscribe(self, pattern: str, handler: Optional[Callable] = None):
        """
        Subscribe to channel pattern
        
        Args:
            pattern: Channel pattern (glob-style)
            handler: Message handler function
        """
        try:
            self.pubsub.psubscribe(pattern)
            
            if handler:
                self.pattern_handlers[pattern] = handler
            
            self.logger.info(f"Subscribed to pattern: {pattern}")
            
        except Exception as e:
            self.logger.error(f"Error subscribing to pattern {pattern}: {e}")
    
    def unsubscribe(self, channel: str = None):
        """Unsubscribe from channel(s)"""
        try:
            if channel:
                self.pubsub.unsubscribe(channel)
                if channel in self.message_handlers:
                    del self.message_handlers[channel]
                self.logger.info(f"Unsubscribed from channel: {channel}")
            else:
                self.pubsub.unsubscribe()
                self.message_handlers.clear()
                self.logger.info("Unsubscribed from all channels")
                
        except Exception as e:
            self.logger.error(f"Error unsubscribing: {e}")
    
    def punsubscribe(self, pattern: str = None):
        """Unsubscribe from pattern(s)"""
        try:
            if pattern:
                self.pubsub.punsubscribe(pattern)
                if pattern in self.pattern_handlers:
                    del self.pattern_handlers[pattern]
                self.logger.info(f"Unsubscribed from pattern: {pattern}")
            else:
                self.pubsub.punsubscribe()
                self.pattern_handlers.clear()
                self.logger.info("Unsubscribed from all patterns")
                
        except Exception as e:
            self.logger.error(f"Error unsubscribing from pattern: {e}")
    
    def _handle_message(self, message):
        """Handle incoming message"""
        if message['type'] not in ['message', 'pmessage']:
            return
        
        channel = message['channel']
        data = message['data']
        
        # Try to parse JSON
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass  # Keep as string if not valid JSON
        
        # Create message context
        message_context = {
            'channel': channel,
            'data': data,
            'pattern': message.get('pattern'),
            'type': message['type'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        handled = False
        
        # Handle specific channel subscriptions
        if message['type'] == 'message' and channel in self.message_handlers:
            try:
                self.message_handlers[channel](message_context)
                handled = True
            except Exception as e:
                self.logger.error(f"Error in channel handler for {channel}: {e}")
        
        # Handle pattern subscriptions
        if message['type'] == 'pmessage':
            pattern = message['pattern']
            if pattern in self.pattern_handlers:
                try:
                    self.pattern_handlers[pattern](message_context)
                    handled = True
                except Exception as e:
                    self.logger.error(f"Error in pattern handler for {pattern}: {e}")
        
        # Default handler if no specific handler found
        if not handled:
            self.logger.info(f"Unhandled message on {channel}: {data}")
    
    def start_listening(self, sleep_time=0.01):
        """Start listening for messages in a separate thread"""
        if self.is_listening:
            self.logger.warning("Already listening for messages")
            return
        
        def listen_loop():
            """Message listening loop"""
            self.is_listening = True
            self.logger.info("Started listening for Redis Pub/Sub messages")
            
            try:
                while self.is_listening:
                    message = self.pubsub.get_message(timeout=1.0)
                    if message:
                        self._handle_message(message)
                    else:
                        time.sleep(sleep_time)
            except Exception as e:
                self.logger.error(f"Error in listening loop: {e}")
            finally:
                self.is_listening = False
                self.logger.info("Stopped listening for Redis Pub/Sub messages")
        
        self.listener_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listener_thread.start()
    
    def stop_listening(self):
        """Stop listening for messages"""
        self.is_listening = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=5)
    
    def get_active_channels(self):
        """Get list of active channels with subscriber counts"""
        try:
            pubsub_channels = self.redis_client.pubsub_channels()
            channel_info = {}
            
            for channel in pubsub_channels:
                subscribers = self.redis_client.pubsub_numsub(channel)[0][1]
                channel_info[channel] = subscribers
            
            return channel_info
        except Exception as e:
            self.logger.error(f"Error getting active channels: {e}")
            return {}
    
    def get_pattern_subscribers(self):
        """Get number of pattern subscribers"""
        try:
            return self.redis_client.pubsub_numpat()
        except Exception as e:
            self.logger.error(f"Error getting pattern subscribers: {e}")
            return 0
    
    def close(self):
        """Close Pub/Sub connection"""
        self.stop_listening()
        self.pubsub.close()

# Usage example
if __name__ == "__main__":
    # Initialize Redis Pub/Sub manager
    pubsub_manager = RedisPubSubManager(
        host='localhost',
        port=6379,
        password=None
    )
    
    # Test connection
    if not pubsub_manager.test_connection():
        exit(1)
    
    # Define message handlers
    def handle_user_events(message_context):
        """Handle user-related events"""
        channel = message_context['channel']
        data = message_context['data']
        
        print(f"User Event on {channel}: {data}")
        
        # Process based on event type
        if isinstance(data, dict):
            event_type = data.get('event_type')
            user_id = data.get('user_id')
            
            if event_type == 'user_login':
                print(f"User {user_id} logged in")
            elif event_type == 'user_logout':
                print(f"User {user_id} logged out")
    
    def handle_order_events(message_context):
        """Handle order-related events"""
        channel = message_context['channel']
        data = message_context['data']
        
        print(f"Order Event on {channel}: {data}")
        
        if isinstance(data, dict):
            event_type = data.get('event_type')
            order_id = data.get('order_id')
            
            if event_type == 'order_created':
                print(f"New order created: {order_id}")
                
                # Send notification
                notification = {
                    'type': 'order_confirmation',
                    'order_id': order_id,
                    'message': f'Order {order_id} has been created',
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                pubsub_manager.publish('notifications:order', notification)
    
    def handle_notifications(message_context):
        """Handle notification events"""
        channel = message_context['channel']
        data = message_context['data']
        
        print(f"📧 Notification: {data}")
    
    # Subscribe to specific channels
    pubsub_manager.subscribe('users:events', handle_user_events)
    pubsub_manager.subscribe('orders:events', handle_order_events)
    
    # Subscribe to patterns
    pubsub_manager.psubscribe('notifications:*', handle_notifications)
    
    # Start listening
    pubsub_manager.start_listening()
    
    # Publish some test events
    time.sleep(1)  # Wait for subscriptions to be ready
    
    # User events
    user_login_event = {
        'event_type': 'user_login',
        'user_id': 'user_123',
        'timestamp': datetime.utcnow().isoformat(),
        'ip_address': '192.168.1.100'
    }
    
    user_logout_event = {
        'event_type': 'user_logout',
        'user_id': 'user_123',
        'timestamp': datetime.utcnow().isoformat()
    }
    
    pubsub_manager.publish('users:events', user_login_event)
    time.sleep(0.5)
    pubsub_manager.publish('users:events', user_logout_event)
    
    # Order events
    order_created_event = {
        'event_type': 'order_created',
        'order_id': 'order_456',
        'customer_id': 'user_123',
        'total_amount': 99.99,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    pubsub_manager.publish('orders:events', order_created_event)
    
    # Keep running
    try:
        print("Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        pubsub_manager.close()
```

## Advanced Redis Pub/Sub Patterns

### Real-Time Chat System
```python
import uuid
from datetime import datetime
from typing import Set

class RedisChatSystem:
    def __init__(self, pubsub_manager: RedisPubSubManager):
        self.pubsub_manager = pubsub_manager
        self.user_sessions: Dict[str, Set[str]] = {}  # user_id -> set of channels
        self.active_users: Set[str] = set()
        
    def join_channel(self, user_id: str, channel: str):
        """User joins a chat channel"""
        channel_key = f"chat:{channel}"
        
        # Subscribe to channel
        self.pubsub_manager.subscribe(channel_key, self._handle_chat_message)
        
        # Track user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(channel)
        self.active_users.add(user_id)
        
        # Announce user joined
        join_message = {
            'type': 'user_joined',
            'user_id': user_id,
            'channel': channel,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.pubsub_manager.publish(channel_key, join_message)
        
        print(f"User {user_id} joined channel {channel}")
    
    def leave_channel(self, user_id: str, channel: str):
        """User leaves a chat channel"""
        channel_key = f"chat:{channel}"
        
        # Remove from user sessions
        if user_id in self.user_sessions:
            self.user_sessions[user_id].discard(channel)
            
            if not self.user_sessions[user_id]:  # No more channels
                del self.user_sessions[user_id]
                self.active_users.discard(user_id)
        
        # Announce user left
        leave_message = {
            'type': 'user_left',
            'user_id': user_id,
            'channel': channel,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.pubsub_manager.publish(channel_key, leave_message)
        
        print(f"User {user_id} left channel {channel}")
    
    def send_message(self, user_id: str, channel: str, message: str):
        """Send chat message to channel"""
        if user_id not in self.active_users:
            raise Exception(f"User {user_id} is not active")
        
        if user_id not in self.user_sessions or channel not in self.user_sessions[user_id]:
            raise Exception(f"User {user_id} is not in channel {channel}")
        
        channel_key = f"chat:{channel}"
        
        chat_message = {
            'type': 'chat_message',
            'message_id': str(uuid.uuid4()),
            'user_id': user_id,
            'channel': channel,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        subscribers = self.pubsub_manager.publish(channel_key, chat_message)
        print(f"Message sent to {subscribers} subscribers in {channel}")
        
        return chat_message['message_id']
    
    def send_private_message(self, from_user: str, to_user: str, message: str):
        """Send private message between users"""
        private_channel = f"private:{min(from_user, to_user)}:{max(from_user, to_user)}"
        
        private_message = {
            'type': 'private_message',
            'message_id': str(uuid.uuid4()),
            'from_user': from_user,
            'to_user': to_user,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.pubsub_manager.publish(private_channel, private_message)
        
        return private_message['message_id']
    
    def _handle_chat_message(self, message_context):
        """Handle incoming chat messages"""
        data = message_context['data']
        
        if isinstance(data, dict):
            message_type = data.get('type')
            
            if message_type == 'chat_message':
                user_id = data.get('user_id')
                channel = data.get('channel')
                message = data.get('message')
                timestamp = data.get('timestamp')
                
                print(f"[{timestamp}] {channel} - {user_id}: {message}")
                
            elif message_type == 'user_joined':
                user_id = data.get('user_id')
                channel = data.get('channel')
                print(f"👋 {user_id} joined {channel}")
                
            elif message_type == 'user_left':
                user_id = data.get('user_id')
                channel = data.get('channel')
                print(f"👋 {user_id} left {channel}")
    
    def get_channel_stats(self):
        """Get statistics about active channels"""
        active_channels = self.pubsub_manager.get_active_channels()
        
        stats = {
            'active_users': len(self.active_users),
            'user_sessions': len(self.user_sessions),
            'active_channels': len(active_channels),
            'total_subscribers': sum(active_channels.values()),
            'channels': active_channels
        }
        
        return stats

# Example usage
chat_system = RedisChatSystem(pubsub_manager)

# Users join channels
chat_system.join_channel('alice', 'general')
chat_system.join_channel('bob', 'general')
chat_system.join_channel('alice', 'tech')

# Send messages
chat_system.send_message('alice', 'general', 'Hello everyone!')
chat_system.send_message('bob', 'general', 'Hi Alice!')
chat_system.send_message('alice', 'tech', 'Anyone working on Redis?')

# Private message
chat_system.send_private_message('alice', 'bob', 'Want to chat privately?')

# Get stats
stats = chat_system.get_channel_stats()
print(f"Chat stats: {stats}")
```

### Event-Driven Microservices
```python
class EventDrivenService:
    def __init__(self, service_name: str, pubsub_manager: RedisPubSubManager):
        self.service_name = service_name
        self.pubsub_manager = pubsub_manager
        self.event_handlers: Dict[str, Callable] = {}
        
        # Subscribe to service-specific events
        self._setup_subscriptions()
    
    def _setup_subscriptions(self):
        """Setup event subscriptions for this service"""
        # Service-specific events
        service_channel = f"events:{self.service_name}:*"
        self.pubsub_manager.psubscribe(service_channel, self._handle_service_event)
        
        # Global events
        self.pubsub_manager.psubscribe("events:global:*", self._handle_global_event)
        
        # Health check events
        self.pubsub_manager.subscribe("health:check", self._handle_health_check)
    
    def emit_event(self, event_type: str, data: Dict[str, Any], scope='service'):
        """Emit an event"""
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'service': self.service_name,
            'data': data,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        }
        
        if scope == 'service':
            channel = f"events:{self.service_name}:{event_type}"
        elif scope == 'global':
            channel = f"events:global:{event_type}"
        else:
            channel = f"events:{scope}:{event_type}"
        
        subscribers = self.pubsub_manager.publish(channel, event)
        
        print(f"[{self.service_name}] Emitted {event_type} to {subscribers} subscribers")
        
        return event['event_id']
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register handler for specific event type"""
        self.event_handlers[event_type] = handler
    
    def _handle_service_event(self, message_context):
        """Handle service-specific events"""
        data = message_context['data']
        channel = message_context['channel']
        
        if isinstance(data, dict):
            event_type = data.get('event_type')
            source_service = data.get('service')
            
            # Don't process our own events
            if source_service == self.service_name:
                return
            
            print(f"[{self.service_name}] Received {event_type} from {source_service}")
            
            # Call registered handler
            if event_type in self.event_handlers:
                try:
                    self.event_handlers[event_type](data)
                except Exception as e:
                    print(f"Error handling {event_type}: {e}")
    
    def _handle_global_event(self, message_context):
        """Handle global events"""
        data = message_context['data']
        
        if isinstance(data, dict):
            event_type = data.get('event_type')
            print(f"[{self.service_name}] Received global event: {event_type}")
            
            # Handle global events
            if event_type == 'system_shutdown':
                self._handle_shutdown(data)
            elif event_type == 'config_update':
                self._handle_config_update(data)
    
    def _handle_health_check(self, message_context):
        """Handle health check requests"""
        health_status = {
            'service': self.service_name,
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': time.time() - self.start_time if hasattr(self, 'start_time') else 0
        }
        
        self.pubsub_manager.publish('health:response', health_status)
    
    def _handle_shutdown(self, event_data):
        """Handle system shutdown event"""
        print(f"[{self.service_name}] Received shutdown signal")
        # Perform cleanup
        self.emit_event('service_stopping', {'reason': 'system_shutdown'})
    
    def _handle_config_update(self, event_data):
        """Handle configuration update event"""
        config_data = event_data.get('data', {})
        print(f"[{self.service_name}] Configuration updated: {config_data}")
    
    def start(self):
        """Start the service"""
        self.start_time = time.time()
        self.emit_event('service_started', {'start_time': self.start_time})
        
        print(f"[{self.service_name}] Service started")
    
    def stop(self):
        """Stop the service"""
        self.emit_event('service_stopped', {'stop_time': time.time()})
        print(f"[{self.service_name}] Service stopped")

# Example services
class UserService(EventDrivenService):
    def __init__(self, pubsub_manager):
        super().__init__('user-service', pubsub_manager)
        
        # Register event handlers
        self.register_event_handler('order_created', self.handle_order_created)
        self.register_event_handler('payment_processed', self.handle_payment_processed)
    
    def create_user(self, user_data):
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user_data['user_id'] = user_id
        
        # Emit user created event
        self.emit_event('user_created', user_data, scope='global')
        
        return user_id
    
    def handle_order_created(self, event_data):
        """Handle order created event"""
        order_data = event_data.get('data', {})
        customer_id = order_data.get('customer_id')
        
        print(f"[UserService] Processing order created for customer {customer_id}")
        
        # Update user stats
        self.emit_event('user_stats_updated', {
            'customer_id': customer_id,
            'action': 'order_created'
        })
    
    def handle_payment_processed(self, event_data):
        """Handle payment processed event"""
        payment_data = event_data.get('data', {})
        customer_id = payment_data.get('customer_id')
        
        print(f"[UserService] Processing payment for customer {customer_id}")

class OrderService(EventDrivenService):
    def __init__(self, pubsub_manager):
        super().__init__('order-service', pubsub_manager)
        
        # Register event handlers
        self.register_event_handler('user_created', self.handle_user_created)
        self.register_event_handler('payment_processed', self.handle_payment_processed)
    
    def create_order(self, order_data):
        """Create a new order"""
        order_id = str(uuid.uuid4())
        order_data['order_id'] = order_id
        
        # Emit order created event
        self.emit_event('order_created', order_data, scope='global')
        
        return order_id
    
    def handle_user_created(self, event_data):
        """Handle user created event"""
        user_data = event_data.get('data', {})
        user_id = user_data.get('user_id')
        
        print(f"[OrderService] New user created: {user_id}")
        
        # Send welcome offer
        self.emit_event('welcome_offer_sent', {
            'user_id': user_id,
            'offer_type': 'first_order_discount'
        })
    
    def handle_payment_processed(self, event_data):
        """Handle payment processed event"""
        payment_data = event_data.get('data', {})
        order_id = payment_data.get('order_id')
        
        print(f"[OrderService] Payment processed for order {order_id}")
        
        # Update order status
        self.emit_event('order_status_updated', {
            'order_id': order_id,
            'status': 'paid'
        })

# Example usage
user_service = UserService(pubsub_manager)
order_service = OrderService(pubsub_manager)

# Start services
user_service.start()
order_service.start()

# Simulate business operations
user_id = user_service.create_user({
    'email': 'john@example.com',
    'name': 'John Doe'
})

order_id = order_service.create_order({
    'customer_id': user_id,
    'items': [{'product_id': 'prod_1', 'quantity': 2}],
    'total_amount': 99.99
})
```

## WebSocket Integration

### Real-Time WebSocket with Redis Pub/Sub
```python
import asyncio
import websockets
import json
from typing import Set, Dict

class WebSocketRedisGateway:
    def __init__(self, pubsub_manager: RedisPubSubManager):
        self.pubsub_manager = pubsub_manager
        self.websocket_connections: Set[websockets.WebSocketServerProtocol] = set()
        self.user_connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        
        # Setup Redis subscriptions
        self._setup_redis_subscriptions()
    
    def _setup_redis_subscriptions(self):
        """Setup Redis subscriptions for WebSocket broadcasting"""
        # Subscribe to WebSocket-specific channels
        self.pubsub_manager.psubscribe('websocket:*', self._handle_websocket_message)
        self.pubsub_manager.psubscribe('broadcast:*', self._handle_broadcast_message)
    
    def _handle_websocket_message(self, message_context):
        """Handle Redis messages for WebSocket clients"""
        data = message_context['data']
        channel = message_context['channel']
        
        if isinstance(data, dict):
            # Extract target user or broadcast to all
            target_user = data.get('target_user')
            message_data = data.get('message', data)
            
            if target_user:
                asyncio.create_task(self._send_to_user(target_user, message_data))
            else:
                asyncio.create_task(self._broadcast_to_all(message_data))
    
    def _handle_broadcast_message(self, message_context):
        """Handle broadcast messages"""
        data = message_context['data']
        asyncio.create_task(self._broadcast_to_all(data))
    
    async def _send_to_user(self, user_id: str, message: Dict):
        """Send message to specific user's WebSocket connections"""
        if user_id in self.user_connections:
            disconnected = set()
            
            for websocket in self.user_connections[user_id]:
                try:
                    await websocket.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(websocket)
            
            # Clean up disconnected connections
            for websocket in disconnected:
                self.user_connections[user_id].discard(websocket)
                self.websocket_connections.discard(websocket)
    
    async def _broadcast_to_all(self, message: Dict):
        """Broadcast message to all WebSocket connections"""
        if not self.websocket_connections:
            return
        
        disconnected = set()
        message_json = json.dumps(message)
        
        for websocket in self.websocket_connections:
            try:
                await websocket.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(websocket)
        
        # Clean up disconnected connections
        for websocket in disconnected:
            self.websocket_connections.discard(websocket)
            
            # Remove from user connections
            for user_id, connections in self.user_connections.items():
                connections.discard(websocket)
    
    async def register_connection(self, websocket: websockets.WebSocketServerProtocol, user_id: str = None):
        """Register new WebSocket connection"""
        self.websocket_connections.add(websocket)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(websocket)
        
        print(f"WebSocket connected. Total connections: {len(self.websocket_connections)}")
    
    async def unregister_connection(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister WebSocket connection"""
        self.websocket_connections.discard(websocket)
        
        # Remove from user connections
        for user_id, connections in self.user_connections.items():
            connections.discard(websocket)
        
        print(f"WebSocket disconnected. Total connections: {len(self.websocket_connections)}")
    
    def send_user_message(self, user_id: str, message: Dict):
        """Send message to specific user via Redis"""
        redis_message = {
            'target_user': user_id,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.pubsub_manager.publish('websocket:user_message', redis_message)
    
    def broadcast_message(self, message: Dict):
        """Broadcast message to all WebSocket clients via Redis"""
        self.pubsub_manager.publish('broadcast:all', message)

# WebSocket server
async def websocket_handler(websocket, path, gateway: WebSocketRedisGateway):
    """Handle WebSocket connections"""
    user_id = None
    
    try:
        # Register connection
        await gateway.register_connection(websocket)
        
        async for message in websocket:
            try:
                data = json.loads(message)
                message_type = data.get('type')
                
                if message_type == 'auth':
                    # Authenticate user
                    user_id = data.get('user_id')
                    await gateway.register_connection(websocket, user_id)
                    
                    # Send authentication confirmation
                    auth_response = {
                        'type': 'auth_success',
                        'user_id': user_id,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    await websocket.send(json.dumps(auth_response))
                
                elif message_type == 'chat_message':
                    # Handle chat message
                    if user_id:
                        chat_data = {
                            'type': 'chat_message',
                            'user_id': user_id,
                            'message': data.get('message'),
                            'channel': data.get('channel', 'general'),
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        
                        # Publish to Redis for distribution
                        gateway.pubsub_manager.publish('broadcast:chat', chat_data)
                
            except json.JSONDecodeError:
                error_response = {
                    'type': 'error',
                    'message': 'Invalid JSON',
                    'timestamp': datetime.utcnow().isoformat()
                }
                await websocket.send(json.dumps(error_response))
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await gateway.unregister_connection(websocket)

# Start WebSocket server
gateway = WebSocketRedisGateway(pubsub_manager)

async def start_websocket_server():
    """Start WebSocket server"""
    print("Starting WebSocket server on localhost:8765")
    
    async with websockets.serve(
        lambda ws, path: websocket_handler(ws, path, gateway),
        "localhost",
        8765
    ):
        await asyncio.Future()  # Run forever

# Example WebSocket client usage
"""
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = function() {
    // Authenticate
    ws.send(JSON.stringify({
        type: 'auth',
        user_id: 'user_123'
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};

// Send chat message
function sendMessage(text) {
    ws.send(JSON.stringify({
        type: 'chat_message',
        message: text,
        channel: 'general'
    }));
}
"""
```

## Monitoring and Performance

### Redis Pub/Sub Monitoring
```python
import psutil
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta

class RedisPubSubMonitor:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.message_stats = defaultdict(lambda: {
            'count': 0,
            'last_seen': None,
            'rates': deque(maxlen=60)  # 60 seconds of rate data
        })
        self.start_time = time.time()
        
    def get_redis_info(self):
        """Get Redis server information"""
        try:
            info = self.redis_client.info()
            
            return {
                'version': info.get('redis_version'),
                'mode': info.get('redis_mode'),
                'connected_clients': info.get('connected_clients'),
                'used_memory': info.get('used_memory'),
                'used_memory_human': info.get('used_memory_human'),
                'total_connections_received': info.get('total_connections_received'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits'),
                'keyspace_misses': info.get('keyspace_misses'),
                'uptime_in_seconds': info.get('uptime_in_seconds')
            }
        except Exception as e:
            print(f"Error getting Redis info: {e}")
            return {}
    
    def get_pubsub_stats(self):
        """Get Pub/Sub specific statistics"""
        try:
            # Get active channels
            channels = self.redis_client.pubsub_channels()
            channel_stats = {}
            
            for channel in channels:
                subscribers = self.redis_client.pubsub_numsub(channel.decode() if isinstance(channel, bytes) else channel)
                if subscribers:
                    channel_stats[subscribers[0][0]] = subscribers[0][1]
            
            # Get pattern subscribers
            pattern_subscribers = self.redis_client.pubsub_numpat()
            
            return {
                'active_channels': len(channels),
                'channel_details': channel_stats,
                'pattern_subscribers': pattern_subscribers,
                'total_subscribers': sum(channel_stats.values())
            }
        except Exception as e:
            print(f"Error getting Pub/Sub stats: {e}")
            return {}
    
    def record_message(self, channel):
        """Record message for statistics"""
        current_time = time.time()
        
        stats = self.message_stats[channel]
        stats['count'] += 1
        stats['last_seen'] = current_time
        
        # Calculate rate (messages per second)
        if len(stats['rates']) > 0:
            time_diff = current_time - (stats['last_rate_time'] if 'last_rate_time' in stats else current_time - 1)
            rate = 1 / time_diff if time_diff > 0 else 0
        else:
            rate = 1
        
        stats['rates'].append(rate)
        stats['last_rate_time'] = current_time
    
    def get_message_stats(self):
        """Get message statistics"""
        current_time = time.time()
        
        stats = {}
        for channel, data in self.message_stats.items():
            avg_rate = sum(data['rates']) / len(data['rates']) if data['rates'] else 0
            
            stats[channel] = {
                'total_messages': data['count'],
                'last_seen': data['last_seen'],
                'avg_rate_per_second': round(avg_rate, 2),
                'time_since_last_message': round(current_time - data['last_seen'], 2) if data['last_seen'] else None
            }
        
        return stats
    
    def print_dashboard(self):
        """Print monitoring dashboard"""
        redis_info = self.get_redis_info()
        pubsub_stats = self.get_pubsub_stats()
        message_stats = self.get_message_stats()
        
        print("\n" + "="*60)
        print("REDIS PUB/SUB MONITORING DASHBOARD")
        print("="*60)
        print(f"Timestamp: {datetime.utcnow().isoformat()}")
        
        # Redis server info
        print(f"\nRedis Server Info:")
        print(f"  Version: {redis_info.get('version', 'Unknown')}")
        print(f"  Mode: {redis_info.get('mode', 'Unknown')}")
        print(f"  Uptime: {redis_info.get('uptime_in_seconds', 0)} seconds")
        print(f"  Connected Clients: {redis_info.get('connected_clients', 0)}")
        print(f"  Used Memory: {redis_info.get('used_memory_human', 'Unknown')}")
        print(f"  Total Commands: {redis_info.get('total_commands_processed', 0)}")
        
        # Pub/Sub stats
        print(f"\nPub/Sub Statistics:")
        print(f"  Active Channels: {pubsub_stats.get('active_channels', 0)}")
        print(f"  Total Subscribers: {pubsub_stats.get('total_subscribers', 0)}")
        print(f"  Pattern Subscribers: {pubsub_stats.get('pattern_subscribers', 0)}")
        
        # Channel details
        channel_details = pubsub_stats.get('channel_details', {})
        if channel_details:
            print(f"\nChannel Details:")
            for channel, subscribers in sorted(channel_details.items(), key=lambda x: x[1], reverse=True):
                print(f"  {channel:<30} {subscribers:>10} subscribers")
        
        # Message statistics
        if message_stats:
            print(f"\nMessage Statistics:")
            for channel, stats in sorted(message_stats.items(), key=lambda x: x[1]['total_messages'], reverse=True):
                last_seen = stats['time_since_last_message']
                last_seen_str = f"{last_seen:.1f}s ago" if last_seen is not None else "Never"
                
                print(f"  {channel:<30} {stats['total_messages']:>8} msgs, "
                      f"{stats['avg_rate_per_second']:>6.2f} msg/s, last: {last_seen_str}")
    
    def check_health(self, thresholds=None):
        """Check Redis Pub/Sub health"""
        if thresholds is None:
            thresholds = {
                'max_memory_usage_percent': 80,
                'max_clients': 1000,
                'max_inactive_time': 300  # 5 minutes
            }
        
        alerts = []
        
        try:
            redis_info = self.get_redis_info()
            
            # Check memory usage
            used_memory = redis_info.get('used_memory', 0)
            if used_memory > 0:
                # Get total system memory
                total_memory = psutil.virtual_memory().total
                memory_percent = (used_memory / total_memory) * 100
                
                if memory_percent > thresholds['max_memory_usage_percent']:
                    alerts.append({
                        'type': 'high_memory_usage',
                        'value': memory_percent,
                        'threshold': thresholds['max_memory_usage_percent']
                    })
            
            # Check client connections
            connected_clients = redis_info.get('connected_clients', 0)
            if connected_clients > thresholds['max_clients']:
                alerts.append({
                    'type': 'high_client_count',
                    'value': connected_clients,
                    'threshold': thresholds['max_clients']
                })
            
            # Check for inactive channels
            message_stats = self.get_message_stats()
            current_time = time.time()
            
            for channel, stats in message_stats.items():
                if stats['time_since_last_message'] and stats['time_since_last_message'] > thresholds['max_inactive_time']:
                    alerts.append({
                        'type': 'inactive_channel',
                        'channel': channel,
                        'inactive_time': stats['time_since_last_message'],
                        'threshold': thresholds['max_inactive_time']
                    })
            
            return alerts
            
        except Exception as e:
            return [{'type': 'monitoring_error', 'message': str(e)}]

# Usage example
monitor = RedisPubSubMonitor(pubsub_manager.redis_client)

# Monitor message activity
def monitored_handler(message_context):
    channel = message_context['channel']
    monitor.record_message(channel)
    print(f"Message on {channel}: {message_context['data']}")

# Subscribe with monitoring
pubsub_manager.subscribe('test:channel', monitored_handler)

# Periodically print dashboard
def monitoring_loop():
    while True:
        time.sleep(30)  # Update every 30 seconds
        monitor.print_dashboard()
        
        # Check health
        alerts = monitor.check_health()
        if alerts:
            print("\n🚨 HEALTH ALERTS:")
            for alert in alerts:
                print(f"  {alert}")

import threading
monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
monitor_thread.start()
```

## Best Practices

### Message Design and Patterns
```python
# Good: Structured message with metadata
good_message = {
    'event_id': str(uuid.uuid4()),
    'event_type': 'user.login',
    'timestamp': datetime.utcnow().isoformat(),
    'version': '1.0',
    'source': 'auth_service',
    'data': {
        'user_id': 'user_123',
        'ip_address': '192.168.1.100',
        'user_agent': 'Mozilla/5.0...'
    },
    'metadata': {
        'correlation_id': 'trace_abc123',
        'session_id': 'session_456'
    }
}

# Good: Hierarchical channel naming
GOOD_CHANNELS = [
    'events:user:login',
    'events:order:created',
    'notifications:email:sent',
    'alerts:system:high_cpu',
    'metrics:api:response_time'
]

# Bad: Flat channel naming
BAD_CHANNELS = [
    'user_login',
    'order_created',
    'email_sent'
]

# Message validation
def validate_event_message(message):
    """Validate event message structure"""
    required_fields = ['event_id', 'event_type', 'timestamp', 'data']
    
    if not isinstance(message, dict):
        return False, "Message must be a dictionary"
    
    for field in required_fields:
        if field not in message:
            return False, f"Missing required field: {field}"
    
    # Validate timestamp
    try:
        datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        return False, "Invalid timestamp format"
    
    return True, "Valid message"

# Channel pattern best practices
class ChannelPatterns:
    """Best practices for Redis Pub/Sub channel patterns"""
    
    @staticmethod
    def user_events(user_id):
        return f"events:user:{user_id}:*"
    
    @staticmethod
    def service_events(service_name):
        return f"events:service:{service_name}:*"
    
    @staticmethod
    def alert_events(severity):
        return f"alerts:*:{severity}"
    
    @staticmethod
    def metric_events(metric_type):
        return f"metrics:{metric_type}:*"

# Good: Idempotent message processing
def idempotent_message_handler(message_context):
    """Process messages idempotently"""
    data = message_context['data']
    
    if isinstance(data, dict) and 'event_id' in data:
        event_id = data['event_id']
        
        # Check if already processed
        if redis_client.exists(f"processed:{event_id}"):
            print(f"Event {event_id} already processed, skipping")
            return
        
        try:
            # Process the event
            process_event(data)
            
            # Mark as processed (with expiration)
            redis_client.setex(f"processed:{event_id}", 3600, "1")  # 1 hour expiry
            
        except Exception as e:
            print(f"Error processing event {event_id}: {e}")
            # Don't mark as processed on error
```

### Performance and Reliability
```python
# Connection pooling for high throughput
import redis.connection

class HighThroughputPubSub:
    def __init__(self, redis_url, pool_size=10):
        self.pool = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=pool_size,
            socket_timeout=5,
            socket_connect_timeout=5,
            socket_keepalive=True,
            socket_keepalive_options={}
        )
        self.redis_client = redis.Redis(connection_pool=self.pool)
        
    def publish_batch(self, messages):
        """Publish multiple messages efficiently"""
        pipe = self.redis_client.pipeline()
        
        for channel, message in messages:
            pipe.publish(channel, message)
        
        results = pipe.execute()
        return sum(results)  # Total subscribers reached

# Message compression for large payloads
import gzip
import base64

def compress_message(message):
    """Compress message for transmission"""
    if isinstance(message, dict):
        message = json.dumps(message)
    
    compressed = gzip.compress(message.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def decompress_message(compressed_message):
    """Decompress received message"""
    try:
        compressed_bytes = base64.b64decode(compressed_message.encode('utf-8'))
        decompressed = gzip.decompress(compressed_bytes)
        return json.loads(decompressed.decode('utf-8'))
    except Exception as e:
        # Fallback to treating as regular string
        return compressed_message

# Circuit breaker for Redis failures
class RedisCircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Redis circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e

# Graceful degradation
def publish_with_fallback(pubsub_manager, channel, message, fallback_storage=None):
    """Publish with fallback to alternative storage"""
    try:
        return pubsub_manager.publish(channel, message)
    except Exception as e:
        print(f"Redis publish failed: {e}")
        
        if fallback_storage:
            # Store in alternative system (database, file, etc.)
            fallback_storage.store_message(channel, message)
            return 0  # No subscribers via Redis
        else:
            raise
```

## Resources

- [Redis Pub/Sub Documentation](https://redis.io/docs/manual/pubsub/) - Official Redis Pub/Sub documentation
- [Redis Python Client (redis-py)](https://redis-py.readthedocs.io/) - Python Redis client library
- [Redis Patterns](https://redis.io/docs/manual/patterns/) - Common Redis usage patterns
- [Redis Sentinel](https://redis.io/docs/manual/sentinel/) - High availability for Redis
- [Redis Cluster](https://redis.io/docs/manual/scaling/) - Scaling Redis horizontally
- [Redis Best Practices](https://redis.io/docs/manual/clients-guide/) - Client-side best practices
- [Redis Pub/Sub vs Streams](https://redis.io/docs/data-types/streams-tutorial/) - Choosing between Pub/Sub and Streams
- [WebSocket with Redis](https://redis.io/docs/manual/pubsub/#pattern-matching) - Real-time web applications
- [Redis Performance Tuning](https://redis.io/docs/manual/performance/) - Optimization guidelines
- [Redis Security](https://redis.io/docs/manual/security/) - Security best practices