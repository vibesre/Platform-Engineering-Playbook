# MQTT

MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe messaging protocol designed for constrained devices and low-bandwidth, high-latency networks. It's essential for IoT applications, real-time messaging, and distributed systems in platform engineering.

## Overview

MQTT is widely used in platform engineering for:
- IoT device communication and telemetry
- Real-time messaging between distributed services
- Mobile application push notifications
- Sensor data collection and monitoring
- Edge computing and gateway communications

## Key Features

- **Lightweight Protocol**: Minimal overhead for resource-constrained devices
- **Publish/Subscribe Model**: Decoupled communication pattern
- **Quality of Service (QoS)**: Three levels of message delivery guarantee
- **Retained Messages**: Last known value persistence
- **Last Will and Testament**: Automatic notification on client disconnection
- **Persistent Sessions**: Session state preservation across connections

## MQTT Protocol Basics

### Quality of Service Levels
```
QoS 0 - At most once delivery (Fire and forget)
QoS 1 - At least once delivery (Acknowledged delivery)
QoS 2 - Exactly once delivery (Assured delivery)
```

### Topic Structure
```
# Hierarchical topic structure using forward slashes
home/livingroom/temperature
sensors/building1/floor2/room101/humidity
vehicles/truck001/gps/latitude
devices/gateway01/status

# Wildcards
sensors/+/temperature        # Single-level wildcard (+)
sensors/#                    # Multi-level wildcard (#)
```

### Message Format
```
Topic: String identifier for the message channel
Payload: Binary data (typically JSON, but can be any format)
QoS: Quality of service level (0, 1, or 2)
Retain: Flag to store the last message on the topic
```

## MQTT Broker Setup

### Mosquitto Broker Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mosquitto mosquitto-clients

# macOS (Homebrew)
brew install mosquitto

# CentOS/RHEL
sudo yum install mosquitto mosquitto-clients

# Start Mosquitto service
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Test with command line clients
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
mosquitto_sub -h localhost -t test/topic
```

### Mosquitto Configuration
```conf
# /etc/mosquitto/mosquitto.conf
# Basic configuration
port 1883
protocol mqtt

# WebSocket support
listener 9001
protocol websockets

# Security configuration
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl.conf

# Persistence
persistence true
persistence_location /var/lib/mosquitto/
autosave_interval 300

# Logging
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
log_timestamp true

# Connection limits
max_connections 1000
max_inflight_messages 20
max_queued_messages 100

# Keep alive
keepalive_interval 60

# Message size limits
message_size_limit 268435456  # 256MB
```

### TLS/SSL Configuration
```conf
# TLS configuration
listener 8883
protocol mqtt
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
require_certificate true
use_identity_as_username true

# TLS over WebSockets
listener 9002
protocol websockets
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

## Python MQTT Implementation

### Basic MQTT Client
```python
import paho.mqtt.client as mqtt
import json
import time
import threading
from datetime import datetime
import logging

class MQTTManager:
    def __init__(self, broker_host, broker_port=1883, client_id=None, 
                 username=None, password=None, use_tls=False):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id or f"mqtt_client_{int(time.time())}"
        self.username = username
        self.password = password
        self.use_tls = use_tls
        
        # Initialize client
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Set up authentication
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Set up TLS
        if use_tls:
            self.client.tls_set()
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        
        # Message handlers
        self.message_handlers = {}
        self.connected = False
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            self.connected = True
            self.logger.info(f"Connected to MQTT broker {self.broker_host}:{self.broker_port}")
            # Resubscribe to topics on reconnect
            self._resubscribe()
        else:
            self.logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects from broker"""
        self.connected = False
        if rc != 0:
            self.logger.warning("Unexpected disconnection from MQTT broker")
        else:
            self.logger.info("Disconnected from MQTT broker")
    
    def _on_message(self, client, userdata, msg):
        """Callback for when message is received"""
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        self.logger.info(f"Received message on topic '{topic}': {payload}")
        
        # Call specific handler if registered
        if topic in self.message_handlers:
            try:
                self.message_handlers[topic](topic, payload, msg.qos, msg.retain)
            except Exception as e:
                self.logger.error(f"Error in message handler for topic '{topic}': {e}")
        
        # Call wildcard handlers
        for pattern, handler in self.message_handlers.items():
            if self._topic_matches_pattern(topic, pattern):
                try:
                    handler(topic, payload, msg.qos, msg.retain)
                except Exception as e:
                    self.logger.error(f"Error in wildcard handler for pattern '{pattern}': {e}")
    
    def _on_publish(self, client, userdata, mid):
        """Callback for when message is published"""
        self.logger.debug(f"Message published with message ID: {mid}")
    
    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback for when subscription is confirmed"""
        self.logger.info(f"Subscription confirmed with QoS: {granted_qos}")
    
    def _topic_matches_pattern(self, topic, pattern):
        """Check if topic matches wildcard pattern"""
        if '+' not in pattern and '#' not in pattern:
            return topic == pattern
        
        topic_parts = topic.split('/')
        pattern_parts = pattern.split('/')
        
        # Handle multi-level wildcard (#)
        if '#' in pattern:
            hash_index = pattern_parts.index('#')
            if hash_index == len(pattern_parts) - 1:
                return topic_parts[:hash_index] == pattern_parts[:hash_index]
        
        # Handle single-level wildcard (+)
        if len(topic_parts) != len(pattern_parts):
            return False
        
        for i, (topic_part, pattern_part) in enumerate(zip(topic_parts, pattern_parts)):
            if pattern_part != '+' and pattern_part != topic_part:
                return False
        
        return True
    
    def _resubscribe(self):
        """Resubscribe to all topics after reconnection"""
        for topic in self.message_handlers.keys():
            if '+' not in topic and '#' not in topic:
                self.client.subscribe(topic)
    
    def connect(self, keepalive=60):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, keepalive)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
            
            if not self.connected:
                raise Exception("Failed to connect within timeout")
            
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish(self, topic, payload, qos=0, retain=False):
        """Publish message to topic"""
        if not self.connected:
            self.logger.error("Not connected to MQTT broker")
            return False
        
        try:
            # Convert payload to string if it's a dict
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            result = self.client.publish(topic, payload, qos, retain)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.debug(f"Published to topic '{topic}': {payload}")
                return True
            else:
                self.logger.error(f"Failed to publish to topic '{topic}': {result.rc}")
                return False
        except Exception as e:
            self.logger.error(f"Error publishing message: {e}")
            return False
    
    def subscribe(self, topic, qos=0, callback=None):
        """Subscribe to topic with optional callback"""
        if not self.connected:
            self.logger.error("Not connected to MQTT broker")
            return False
        
        try:
            # Register callback if provided
            if callback:
                self.message_handlers[topic] = callback
            
            result = self.client.subscribe(topic, qos)
            
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                self.logger.info(f"Subscribed to topic '{topic}' with QoS {qos}")
                return True
            else:
                self.logger.error(f"Failed to subscribe to topic '{topic}': {result[0]}")
                return False
        except Exception as e:
            self.logger.error(f"Error subscribing to topic: {e}")
            return False
    
    def unsubscribe(self, topic):
        """Unsubscribe from topic"""
        if not self.connected:
            self.logger.error("Not connected to MQTT broker")
            return False
        
        try:
            result = self.client.unsubscribe(topic)
            
            # Remove callback handler
            if topic in self.message_handlers:
                del self.message_handlers[topic]
            
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                self.logger.info(f"Unsubscribed from topic '{topic}'")
                return True
            else:
                self.logger.error(f"Failed to unsubscribe from topic '{topic}': {result[0]}")
                return False
        except Exception as e:
            self.logger.error(f"Error unsubscribing from topic: {e}")
            return False
    
    def set_will(self, topic, payload, qos=0, retain=False):
        """Set Last Will and Testament message"""
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            self.client.will_set(topic, payload, qos, retain)
            self.logger.info(f"Set LWT for topic '{topic}': {payload}")
        except Exception as e:
            self.logger.error(f"Error setting LWT: {e}")

# Usage example
if __name__ == "__main__":
    # Initialize MQTT manager
    mqtt_manager = MQTTManager(
        broker_host="localhost",
        broker_port=1883,
        client_id="platform_client",
        username="mqtt_user",
        password="mqtt_password"
    )
    
    # Define message handlers
    def temperature_handler(topic, payload, qos, retain):
        """Handler for temperature sensor data"""
        try:
            data = json.loads(payload)
            print(f"Temperature reading: {data['temperature']}°C from {data['sensor_id']}")
            
            # Process temperature data
            if data['temperature'] > 30:
                alert_payload = {
                    "alert_type": "high_temperature",
                    "sensor_id": data['sensor_id'],
                    "temperature": data['temperature'],
                    "timestamp": datetime.utcnow().isoformat()
                }
                mqtt_manager.publish("alerts/temperature", alert_payload)
        except json.JSONDecodeError:
            print(f"Invalid JSON in temperature message: {payload}")
    
    def status_handler(topic, payload, qos, retain):
        """Handler for device status messages"""
        print(f"Device status update on {topic}: {payload}")
    
    # Set Last Will and Testament
    lwt_message = {
        "client_id": "platform_client",
        "status": "offline",
        "timestamp": datetime.utcnow().isoformat()
    }
    mqtt_manager.set_will("clients/platform_client/status", lwt_message)
    
    # Connect to broker
    if mqtt_manager.connect():
        # Subscribe to topics with handlers
        mqtt_manager.subscribe("sensors/+/temperature", callback=temperature_handler)
        mqtt_manager.subscribe("devices/+/status", callback=status_handler)
        
        # Publish some test data
        sensor_data = {
            "sensor_id": "temp_01",
            "temperature": 25.5,
            "humidity": 60.2,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        mqtt_manager.publish("sensors/temp_01/temperature", sensor_data, qos=1)
        
        # Publish device status
        device_status = {
            "device_id": "gateway_01",
            "status": "online",
            "uptime": 3600,
            "memory_usage": 45.2
        }
        
        mqtt_manager.publish("devices/gateway_01/status", device_status, retain=True)
        
        # Keep the client running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Disconnecting...")
            mqtt_manager.disconnect()
    else:
        print("Failed to connect to MQTT broker")
```

## IoT Device Simulation

### Sensor Data Publisher
```python
import random
import time
from datetime import datetime, timedelta
import json

class IoTSensorSimulator:
    def __init__(self, mqtt_manager, device_id, sensor_types):
        self.mqtt_manager = mqtt_manager
        self.device_id = device_id
        self.sensor_types = sensor_types
        self.running = False
        self.location = {"latitude": 37.7749, "longitude": -122.4194}  # San Francisco
    
    def generate_sensor_data(self, sensor_type):
        """Generate realistic sensor data"""
        timestamp = datetime.utcnow().isoformat()
        
        if sensor_type == "temperature":
            # Simulate temperature with daily cycle
            hour = datetime.utcnow().hour
            base_temp = 20 + 10 * math.sin((hour - 6) * math.pi / 12)
            temperature = base_temp + random.uniform(-2, 2)
            
            return {
                "device_id": self.device_id,
                "sensor_type": "temperature",
                "value": round(temperature, 2),
                "unit": "celsius",
                "timestamp": timestamp,
                "location": self.location
            }
        
        elif sensor_type == "humidity":
            humidity = random.uniform(30, 80)
            return {
                "device_id": self.device_id,
                "sensor_type": "humidity",
                "value": round(humidity, 2),
                "unit": "percent",
                "timestamp": timestamp,
                "location": self.location
            }
        
        elif sensor_type == "pressure":
            pressure = random.uniform(1010, 1030)
            return {
                "device_id": self.device_id,
                "sensor_type": "pressure",
                "value": round(pressure, 2),
                "unit": "hPa",
                "timestamp": timestamp,
                "location": self.location
            }
        
        elif sensor_type == "motion":
            motion_detected = random.choice([True, False])
            return {
                "device_id": self.device_id,
                "sensor_type": "motion",
                "value": motion_detected,
                "timestamp": timestamp,
                "location": self.location
            }
        
        elif sensor_type == "air_quality":
            pm25 = random.uniform(5, 50)
            pm10 = pm25 + random.uniform(5, 20)
            
            return {
                "device_id": self.device_id,
                "sensor_type": "air_quality",
                "pm25": round(pm25, 2),
                "pm10": round(pm10, 2),
                "unit": "μg/m³",
                "timestamp": timestamp,
                "location": self.location
            }
    
    def publish_sensor_data(self):
        """Publish sensor data for all sensor types"""
        for sensor_type in self.sensor_types:
            data = self.generate_sensor_data(sensor_type)
            topic = f"sensors/{self.device_id}/{sensor_type}"
            
            success = self.mqtt_manager.publish(topic, data, qos=1)
            if success:
                print(f"Published {sensor_type} data: {data['value']}")
    
    def publish_device_status(self):
        """Publish device health status"""
        status_data = {
            "device_id": self.device_id,
            "status": "online",
            "battery_level": random.uniform(20, 100),
            "signal_strength": random.uniform(-80, -40),
            "uptime": random.randint(3600, 86400),
            "firmware_version": "1.2.3",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        topic = f"devices/{self.device_id}/status"
        self.mqtt_manager.publish(topic, status_data, qos=1, retain=True)
        print(f"Published device status: {status_data['status']}")
    
    def start_simulation(self, interval=30, status_interval=300):
        """Start continuous sensor data simulation"""
        self.running = True
        last_status_time = time.time()
        
        while self.running:
            try:
                # Publish sensor data
                self.publish_sensor_data()
                
                # Publish status periodically
                current_time = time.time()
                if current_time - last_status_time >= status_interval:
                    self.publish_device_status()
                    last_status_time = current_time
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.stop_simulation()
            except Exception as e:
                print(f"Error in simulation: {e}")
                time.sleep(5)
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        
        # Publish offline status
        offline_status = {
            "device_id": self.device_id,
            "status": "offline",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        topic = f"devices/{self.device_id}/status"
        self.mqtt_manager.publish(topic, offline_status, qos=1, retain=True)
        print(f"Device {self.device_id} simulation stopped")

# Example usage
import math

if __name__ == "__main__":
    # Initialize MQTT manager
    mqtt_manager = MQTTManager(
        broker_host="localhost",
        client_id="iot_simulator"
    )
    
    # Connect to broker
    if mqtt_manager.connect():
        # Create IoT device simulator
        device_simulator = IoTSensorSimulator(
            mqtt_manager=mqtt_manager,
            device_id="weather_station_001",
            sensor_types=["temperature", "humidity", "pressure", "air_quality"]
        )
        
        # Start simulation
        print("Starting IoT sensor simulation...")
        device_simulator.start_simulation(interval=10, status_interval=60)
    else:
        print("Failed to connect to MQTT broker")
```

## MQTT with Docker and Docker Compose

### Mosquitto Docker Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: mosquitto-broker
    ports:
      - "1883:1883"     # MQTT port
      - "9001:9001"     # WebSocket port
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    environment:
      - MOSQUITTO_USERNAME=mqtt_user
      - MOSQUITTO_PASSWORD=mqtt_password
    restart: unless-stopped
    networks:
      - mqtt-network

  mqtt-client:
    build: 
      context: .
      dockerfile: Dockerfile.mqtt-client
    container_name: mqtt-client
    depends_on:
      - mosquitto
    environment:
      - MQTT_BROKER=mosquitto
      - MQTT_PORT=1883
      - MQTT_USERNAME=mqtt_user
      - MQTT_PASSWORD=mqtt_password
    volumes:
      - ./app:/app
    networks:
      - mqtt-network
    restart: unless-stopped

  mqtt-monitor:
    image: python:3.9-slim
    container_name: mqtt-monitor
    depends_on:
      - mosquitto
    volumes:
      - ./monitoring:/app
    working_dir: /app
    command: ["python", "mqtt_monitor.py"]
    environment:
      - MQTT_BROKER=mosquitto
      - MQTT_PORT=1883
    networks:
      - mqtt-network
    restart: unless-stopped

networks:
  mqtt-network:
    driver: bridge

volumes:
  mosquitto-data:
  mosquitto-logs:
```

### Mosquitto Docker Configuration
```conf
# mosquitto/config/mosquitto.conf
# Mosquitto configuration for Docker

# Basic settings
user mosquitto
persistence true
persistence_location /mosquitto/data/

# Logging
log_dest file /mosquitto/log/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
log_timestamp true

# Default listener
listener 1883
protocol mqtt
allow_anonymous false

# WebSocket listener
listener 9001
protocol websockets
allow_anonymous false

# Authentication
password_file /mosquitto/config/passwd
acl_file /mosquitto/config/acl

# Connection settings
max_connections 1000
max_inflight_messages 20
max_queued_messages 100
keepalive_interval 60

# Security
require_certificate false
use_identity_as_username false
```

### MQTT Client Dockerfile
```dockerfile
# Dockerfile.mqtt-client
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD ["python", "mqtt_client.py"]
```

## Advanced MQTT Patterns

### MQTT Message Routing and Processing
```python
import re
from collections import defaultdict
from typing import Callable, Dict, List
import asyncio

class MQTTMessageRouter:
    def __init__(self, mqtt_manager):
        self.mqtt_manager = mqtt_manager
        self.routes: Dict[str, List[Callable]] = defaultdict(list)
        self.middleware: List[Callable] = []
        
    def add_middleware(self, middleware_func):
        """Add middleware function that processes all messages"""
        self.middleware.append(middleware_func)
    
    def route(self, topic_pattern: str):
        """Decorator to register route handlers"""
        def decorator(handler_func):
            self.routes[topic_pattern].append(handler_func)
            return handler_func
        return decorator
    
    def add_route(self, topic_pattern: str, handler_func):
        """Programmatically add route handler"""
        self.routes[topic_pattern].append(handler_func)
    
    def _convert_mqtt_pattern_to_regex(self, mqtt_pattern: str) -> str:
        """Convert MQTT wildcard pattern to regex"""
        # Escape special regex characters except + and #
        pattern = re.escape(mqtt_pattern)
        
        # Replace MQTT wildcards with regex equivalents
        pattern = pattern.replace(r'\+', r'[^/]+')  # Single level wildcard
        pattern = pattern.replace(r'\#', r'.*')     # Multi level wildcard
        
        return f'^{pattern}$'
    
    def process_message(self, topic: str, payload: str, qos: int, retain: bool):
        """Process incoming message through middleware and routes"""
        message_data = {
            'topic': topic,
            'payload': payload,
            'qos': qos,
            'retain': retain,
            'timestamp': time.time()
        }
        
        # Apply middleware
        for middleware in self.middleware:
            try:
                message_data = middleware(message_data)
                if message_data is None:
                    return  # Middleware stopped processing
            except Exception as e:
                print(f"Middleware error: {e}")
                continue
        
        # Find matching routes
        for pattern, handlers in self.routes.items():
            regex_pattern = self._convert_mqtt_pattern_to_regex(pattern)
            if re.match(regex_pattern, topic):
                for handler in handlers:
                    try:
                        handler(message_data)
                    except Exception as e:
                        print(f"Handler error for pattern {pattern}: {e}")
    
    def start_routing(self):
        """Start message routing by subscribing to all patterns"""
        for pattern in self.routes.keys():
            self.mqtt_manager.subscribe(
                pattern, 
                callback=lambda t, p, q, r: self.process_message(t, p, q, r)
            )

# Example usage with message routing
def create_mqtt_application():
    """Create MQTT application with routing"""
    mqtt_manager = MQTTManager(broker_host="localhost")
    router = MQTTMessageRouter(mqtt_manager)
    
    # Middleware for logging
    def logging_middleware(message_data):
        print(f"[MIDDLEWARE] Message on {message_data['topic']}: {message_data['payload'][:100]}")
        return message_data
    
    # Middleware for message validation
    def validation_middleware(message_data):
        try:
            if message_data['topic'].startswith('sensors/'):
                # Validate sensor data format
                data = json.loads(message_data['payload'])
                required_fields = ['device_id', 'timestamp', 'value']
                
                for field in required_fields:
                    if field not in data:
                        print(f"Invalid sensor message: missing {field}")
                        return None
                
                message_data['parsed_payload'] = data
        except json.JSONDecodeError:
            print("Invalid JSON in sensor message")
            return None
        
        return message_data
    
    # Add middleware
    router.add_middleware(logging_middleware)
    router.add_middleware(validation_middleware)
    
    # Route handlers
    @router.route('sensors/+/temperature')
    def handle_temperature(message_data):
        """Handle temperature sensor data"""
        data = message_data.get('parsed_payload', {})
        device_id = data.get('device_id')
        temperature = data.get('value')
        
        print(f"Temperature from {device_id}: {temperature}°C")
        
        # Send alert if temperature is too high
        if temperature > 35:
            alert = {
                "alert_type": "high_temperature",
                "device_id": device_id,
                "temperature": temperature,
                "timestamp": datetime.utcnow().isoformat()
            }
            mqtt_manager.publish("alerts/temperature", alert, qos=1)
    
    @router.route('sensors/+/humidity')
    def handle_humidity(message_data):
        """Handle humidity sensor data"""
        data = message_data.get('parsed_payload', {})
        device_id = data.get('device_id')
        humidity = data.get('value')
        
        print(f"Humidity from {device_id}: {humidity}%")
    
    @router.route('devices/+/status')
    def handle_device_status(message_data):
        """Handle device status updates"""
        try:
            data = json.loads(message_data['payload'])
            device_id = data.get('device_id')
            status = data.get('status')
            battery = data.get('battery_level', 'Unknown')
            
            print(f"Device {device_id} status: {status} (Battery: {battery}%)")
            
            # Alert on low battery
            if isinstance(battery, (int, float)) and battery < 20:
                alert = {
                    "alert_type": "low_battery",
                    "device_id": device_id,
                    "battery_level": battery,
                    "timestamp": datetime.utcnow().isoformat()
                }
                mqtt_manager.publish("alerts/battery", alert, qos=1)
        except json.JSONDecodeError:
            print("Invalid JSON in device status message")
    
    @router.route('alerts/#')
    def handle_alerts(message_data):
        """Handle all alert messages"""
        print(f"🚨 ALERT: {message_data['topic']} - {message_data['payload']}")
        # Here you could integrate with notification systems
        # send_to_slack(message_data)
        # send_email_alert(message_data)
    
    return mqtt_manager, router

# Run the application
if __name__ == "__main__":
    mqtt_manager, router = create_mqtt_application()
    
    if mqtt_manager.connect():
        router.start_routing()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")
            mqtt_manager.disconnect()
```

## MQTT Security and Authentication

### TLS/SSL Certificate Setup
```bash
#!/bin/bash
# create_mqtt_certs.sh - Create certificates for MQTT TLS

# Create CA private key
openssl genrsa -out ca.key 2048

# Create CA certificate
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/CN=MyCA"

# Create server private key
openssl genrsa -out server.key 2048

# Create server certificate signing request
openssl req -new -key server.key -out server.csr -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/CN=mqtt.example.com"

# Sign server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Create client private key
openssl genrsa -out client.key 2048

# Create client certificate signing request
openssl req -new -key client.key -out client.csr -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/CN=mqtt-client"

# Sign client certificate with CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

echo "Certificates created successfully!"
```

### Secure MQTT Client
```python
import ssl
import paho.mqtt.client as mqtt

class SecureMQTTClient:
    def __init__(self, broker_host, broker_port=8883, client_id=None,
                 ca_cert_path=None, client_cert_path=None, client_key_path=None,
                 username=None, password=None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id or f"secure_client_{int(time.time())}"
        
        # Initialize client
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Set up TLS/SSL
        if ca_cert_path:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False  # Disable for self-signed certificates
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Load CA certificate
            context.load_verify_locations(ca_cert_path)
            
            # Load client certificate and key if provided
            if client_cert_path and client_key_path:
                context.load_cert_chain(client_cert_path, client_key_path)
            
            self.client.tls_set_context(context)
        
        # Set up authentication
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to secure MQTT broker")
        else:
            print(f"Failed to connect: {rc}")
    
    def _on_message(self, client, userdata, msg):
        print(f"Received: {msg.topic} - {msg.payload.decode()}")
    
    def connect(self):
        """Connect to secure MQTT broker"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def publish(self, topic, payload, qos=0):
        """Publish message securely"""
        result = self.client.publish(topic, payload, qos)
        return result.rc == mqtt.MQTT_ERR_SUCCESS
    
    def subscribe(self, topic, qos=0):
        """Subscribe to topic"""
        result = self.client.subscribe(topic, qos)
        return result[0] == mqtt.MQTT_ERR_SUCCESS

# Usage
secure_client = SecureMQTTClient(
    broker_host="mqtt.example.com",
    broker_port=8883,
    ca_cert_path="/path/to/ca.crt",
    client_cert_path="/path/to/client.crt",
    client_key_path="/path/to/client.key",
    username="secure_user",
    password="secure_password"
)

if secure_client.connect():
    secure_client.subscribe("secure/topic")
    secure_client.publish("secure/topic", "Hello secure MQTT!")
```

## MQTT Access Control Lists (ACL)
```conf
# /etc/mosquitto/acl.conf
# MQTT Access Control Configuration

# Admin user has full access
user admin
topic readwrite #

# Sensor devices can only publish to their own topics
pattern read sensors/%u/+
pattern write sensors/%u/+

# Gateway devices can read all sensor data
user gateway_01
topic read sensors/+/+
topic write gateways/gateway_01/+

# Application users can read sensor data and write to commands
user app_user
topic read sensors/+/+
topic read devices/+/status
topic write commands/+/+

# Analytics service can read all data
user analytics
topic read #

# Alert service can read alerts and send notifications
user alert_service
topic read alerts/+
topic write notifications/+
```

## Monitoring and Metrics

### MQTT Monitoring Dashboard
```python
import time
import json
from collections import defaultdict, deque
from datetime import datetime, timedelta

class MQTTMonitor:
    def __init__(self, mqtt_manager):
        self.mqtt_manager = mqtt_manager
        self.message_counts = defaultdict(int)
        self.topic_stats = defaultdict(lambda: {
            'count': 0,
            'last_seen': None,
            'avg_interval': 0,
            'message_sizes': deque(maxlen=100)
        })
        self.client_stats = defaultdict(lambda: {
            'last_seen': None,
            'message_count': 0,
            'topics': set()
        })
        
    def start_monitoring(self):
        """Start monitoring all MQTT traffic"""
        # Subscribe to all topics using wildcard
        self.mqtt_manager.subscribe("#", callback=self._monitor_message)
        
        # Subscribe to system topics for broker stats
        self.mqtt_manager.subscribe("$SYS/#", callback=self._monitor_system)
    
    def _monitor_message(self, topic, payload, qos, retain):
        """Monitor individual messages"""
        current_time = datetime.utcnow()
        
        # Update topic statistics
        topic_stat = self.topic_stats[topic]
        topic_stat['count'] += 1
        topic_stat['message_sizes'].append(len(payload))
        
        # Calculate average interval
        if topic_stat['last_seen']:
            interval = (current_time - topic_stat['last_seen']).total_seconds()
            if topic_stat['avg_interval'] == 0:
                topic_stat['avg_interval'] = interval
            else:
                # Exponential moving average
                topic_stat['avg_interval'] = 0.9 * topic_stat['avg_interval'] + 0.1 * interval
        
        topic_stat['last_seen'] = current_time
        
        # Extract client info from payload if available
        try:
            data = json.loads(payload)
            if 'device_id' in data:
                client_id = data['device_id']
                client_stat = self.client_stats[client_id]
                client_stat['last_seen'] = current_time
                client_stat['message_count'] += 1
                client_stat['topics'].add(topic)
        except json.JSONDecodeError:
            pass
        
        # Update message counts
        self.message_counts[topic] += 1
    
    def _monitor_system(self, topic, payload, qos, retain):
        """Monitor system/broker messages"""
        print(f"System: {topic} = {payload}")
    
    def get_statistics(self):
        """Get monitoring statistics"""
        current_time = datetime.utcnow()
        
        # Calculate inactive topics and clients
        inactive_threshold = timedelta(minutes=5)
        
        active_topics = []
        inactive_topics = []
        
        for topic, stats in self.topic_stats.items():
            if stats['last_seen'] and (current_time - stats['last_seen']) < inactive_threshold:
                active_topics.append({
                    'topic': topic,
                    'count': stats['count'],
                    'last_seen': stats['last_seen'].isoformat(),
                    'avg_interval': round(stats['avg_interval'], 2),
                    'avg_size': sum(stats['message_sizes']) / len(stats['message_sizes']) if stats['message_sizes'] else 0
                })
            else:
                inactive_topics.append({
                    'topic': topic,
                    'count': stats['count'],
                    'last_seen': stats['last_seen'].isoformat() if stats['last_seen'] else None
                })
        
        active_clients = []
        inactive_clients = []
        
        for client_id, stats in self.client_stats.items():
            if stats['last_seen'] and (current_time - stats['last_seen']) < inactive_threshold:
                active_clients.append({
                    'client_id': client_id,
                    'message_count': stats['message_count'],
                    'topic_count': len(stats['topics']),
                    'last_seen': stats['last_seen'].isoformat()
                })
            else:
                inactive_clients.append({
                    'client_id': client_id,
                    'message_count': stats['message_count'],
                    'last_seen': stats['last_seen'].isoformat() if stats['last_seen'] else None
                })
        
        return {
            'timestamp': current_time.isoformat(),
            'total_messages': sum(self.message_counts.values()),
            'total_topics': len(self.topic_stats),
            'total_clients': len(self.client_stats),
            'active_topics': sorted(active_topics, key=lambda x: x['count'], reverse=True),
            'inactive_topics': inactive_topics,
            'active_clients': active_clients,
            'inactive_clients': inactive_clients,
            'top_topics': sorted([
                {'topic': topic, 'count': count} 
                for topic, count in self.message_counts.items()
            ], key=lambda x: x['count'], reverse=True)[:10]
        }
    
    def print_dashboard(self):
        """Print monitoring dashboard to console"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("MQTT MONITORING DASHBOARD")
        print("="*60)
        print(f"Timestamp: {stats['timestamp']}")
        print(f"Total Messages: {stats['total_messages']}")
        print(f"Total Topics: {stats['total_topics']}")
        print(f"Total Clients: {stats['total_clients']}")
        print(f"Active Topics: {len(stats['active_topics'])}")
        print(f"Active Clients: {len(stats['active_clients'])}")
        
        print(f"\nTop 10 Topics by Message Count:")
        print("-" * 40)
        for item in stats['top_topics']:
            print(f"{item['topic']:<30} {item['count']:>8}")
        
        print(f"\nActive Clients:")
        print("-" * 50)
        for client in stats['active_clients'][:10]:
            print(f"{client['client_id']:<20} {client['message_count']:>8} msgs, {client['topic_count']:>3} topics")
        
        if stats['inactive_clients']:
            print(f"\nInactive Clients: {len(stats['inactive_clients'])}")

# Usage
monitor = MQTTMonitor(mqtt_manager)
monitor.start_monitoring()

# Print dashboard every 30 seconds
import threading

def dashboard_loop():
    while True:
        time.sleep(30)
        monitor.print_dashboard()

dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
dashboard_thread.start()
```

## Best Practices

### MQTT Topic Design
```python
# Good topic structure examples
GOOD_TOPICS = [
    "sensors/building1/floor2/room101/temperature",
    "devices/gateway001/status",
    "alerts/fire/building1/floor2",
    "commands/lighting/zone1/dimmer1",
    "events/access/door/front_entrance",
    "telemetry/vehicle/truck001/gps/latitude"
]

# Bad topic structure examples
BAD_TOPICS = [
    "data",  # Too generic
    "sensor_temp_room_101_building_1_floor_2",  # Underscores, hard to filter
    "devices/gateway001/temp/humidity/pressure",  # Multiple data types in one topic
    "building1/sensors/temperature/room101",  # Inconsistent hierarchy
]

# Topic validation function
def validate_topic_structure(topic):
    """Validate MQTT topic structure"""
    rules = [
        (lambda t: len(t) <= 65535, "Topic too long"),
        (lambda t: not t.startswith('/'), "Topic should not start with /"),
        (lambda t: not t.endswith('/'), "Topic should not end with /"),
        (lambda t: '//' not in t, "Topic should not contain double slashes"),
        (lambda t: all(c.isprintable() for c in t), "Topic should contain only printable characters"),
        (lambda t: '+' not in t or all(level.strip() != '' for level in t.split('/')), "Invalid wildcard usage"),
        (lambda t: '#' not in t or (t.endswith('#') and t.count('#') == 1), "Invalid multi-level wildcard"),
    ]
    
    for rule, message in rules:
        if not rule(topic):
            return False, message
    
    return True, "Valid topic"

# Message payload design
def create_sensor_message(device_id, sensor_type, value, unit, **kwargs):
    """Create standardized sensor message"""
    message = {
        "device_id": device_id,
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0"
    }
    
    # Add optional fields
    for key, val in kwargs.items():
        message[key] = val
    
    return message

# Good: Structured sensor data
sensor_data = create_sensor_message(
    device_id="temp_sensor_001",
    sensor_type="temperature",
    value=23.5,
    unit="celsius",
    location={"building": "A", "floor": 2, "room": "101"},
    accuracy=0.1,
    calibration_date="2024-01-01"
)
```

### Error Handling and Resilience
```python
class ResilientMQTTClient:
    def __init__(self, broker_configs, max_retries=5):
        """
        broker_configs: List of broker configurations for failover
        """
        self.broker_configs = broker_configs
        self.current_broker_index = 0
        self.max_retries = max_retries
        self.connected = False
        self.retry_count = 0
        
    def connect_with_failover(self):
        """Connect with automatic failover to backup brokers"""
        for attempt in range(self.max_retries):
            for i, config in enumerate(self.broker_configs):
                try:
                    self.current_broker_index = i
                    client = mqtt.Client()
                    
                    if config.get('username') and config.get('password'):
                        client.username_pw_set(config['username'], config['password'])
                    
                    if config.get('use_tls'):
                        client.tls_set()
                    
                    client.connect(config['host'], config['port'], 60)
                    client.loop_start()
                    
                    self.connected = True
                    self.retry_count = 0
                    print(f"Connected to broker {config['host']}:{config['port']}")
                    return client
                    
                except Exception as e:
                    print(f"Failed to connect to {config['host']}:{config['port']}: {e}")
                    continue
            
            # Wait before retrying all brokers
            time.sleep(2 ** attempt)
        
        raise Exception("Failed to connect to any broker after all retries")
    
    def publish_with_retry(self, client, topic, payload, qos=0, retry_delay=1):
        """Publish with automatic retry and exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                result = client.publish(topic, payload, qos)
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    return True
                else:
                    print(f"Publish failed with code {result.rc}, attempt {attempt + 1}")
                    
            except Exception as e:
                print(f"Publish error: {e}, attempt {attempt + 1}")
            
            if attempt < self.max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
        
        return False

# Example usage
broker_configs = [
    {"host": "primary-mqtt.example.com", "port": 1883, "username": "user", "password": "pass"},
    {"host": "backup-mqtt.example.com", "port": 1883, "username": "user", "password": "pass"},
    {"host": "localhost", "port": 1883}
]

resilient_client = ResilientMQTTClient(broker_configs)
mqtt_client = resilient_client.connect_with_failover()
```

## Resources

- [MQTT Official Specification](https://mqtt.org/mqtt-specification/) - Complete MQTT 3.1.1 and 5.0 specifications
- [Eclipse Mosquitto](https://mosquitto.org/) - Open source MQTT broker documentation
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/) - Python MQTT client library
- [MQTT.js](https://github.com/mqttjs/MQTT.js) - JavaScript MQTT client for web and Node.js
- [HiveMQ](https://www.hivemq.com/docs/) - Enterprise MQTT broker documentation
- [MQTT Security Best Practices](https://www.hivemq.com/blog/mqtt-security-fundamentals/) - Security guidelines
- [MQTT Topic Best Practices](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/) - Topic design guidelines
- [AWS IoT Core MQTT](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html) - AWS managed MQTT service
- [Azure IoT Hub MQTT](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support) - Azure MQTT support
- [Google Cloud IoT Core](https://cloud.google.com/iot-core/docs/concepts/protocols) - Google Cloud MQTT protocols