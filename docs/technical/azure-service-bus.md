# Azure Service Bus

Azure Service Bus is a fully managed enterprise integration message broker that provides reliable cloud messaging between applications and services. It's essential for building distributed applications, microservices architectures, and enterprise integration patterns in Azure platform engineering.

## Overview

Azure Service Bus is widely used in platform engineering for:
- Decoupling applications and services in microservices architectures
- Building enterprise messaging patterns (pub/sub, request/response)
- Implementing reliable message queuing with advanced features
- Processing high-throughput messaging workloads
- Handling complex routing scenarios and message sessions

## Key Features

- **Message Queues**: Point-to-point messaging with FIFO ordering
- **Topics and Subscriptions**: Publish/subscribe messaging patterns
- **Message Sessions**: Ordered processing of related messages
- **Dead Letter Queues**: Automatic handling of poison messages
- **Duplicate Detection**: Automatic duplicate message detection
- **Transaction Support**: Transactional message processing
- **Auto-forwarding**: Automatic message forwarding between entities

## Core Concepts

### Messaging Entities
- **Namespace**: Container for messaging entities
- **Queue**: Point-to-point messaging entity
- **Topic**: Publish/subscribe messaging entity  
- **Subscription**: Named subscription to a topic
- **Rules and Filters**: Message routing and filtering

### Message Types
- **Standard Messages**: Regular messages with at-least-once delivery
- **Scheduled Messages**: Messages delivered at a future time
- **Session Messages**: Related messages processed in order
- **Transactional Messages**: Messages processed within transactions

## Installation and Setup

### Azure CLI Setup
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Create resource group
az group create --name rg-messaging --location "East US"

# Create Service Bus namespace
az servicebus namespace create \
    --resource-group rg-messaging \
    --name sb-platform-messaging \
    --location "East US" \
    --sku Standard
```

### Python SDK Installation
```bash
# Install Azure Service Bus SDK
pip install azure-servicebus

# Install additional dependencies
pip install azure-identity azure-mgmt-servicebus
```

### Connection String Setup
```bash
# Get connection string
az servicebus namespace authorization-rule keys list \
    --resource-group rg-messaging \
    --namespace-name sb-platform-messaging \
    --name RootManageSharedAccessKey
```

## Basic Service Bus Implementation

### Queue Operations
```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient
from azure.identity import DefaultAzureCredential
import json
import time
from datetime import datetime, timedelta

class ServiceBusManager:
    def __init__(self, connection_string=None, namespace=None):
        if connection_string:
            self.client = ServiceBusClient.from_connection_string(connection_string)
            self.admin_client = ServiceBusAdministrationClient.from_connection_string(connection_string)
        elif namespace:
            # Use managed identity
            credential = DefaultAzureCredential()
            self.client = ServiceBusClient(
                fully_qualified_namespace=f"{namespace}.servicebus.windows.net",
                credential=credential
            )
            self.admin_client = ServiceBusAdministrationClient(
                fully_qualified_namespace=f"{namespace}.servicebus.windows.net",
                credential=credential
            )
        else:
            raise ValueError("Either connection_string or namespace must be provided")
    
    def create_queue(self, queue_name, **kwargs):
        """Create a Service Bus queue"""
        from azure.servicebus.management import QueueProperties
        
        try:
            queue_properties = QueueProperties(
                max_size_in_megabytes=1024,
                default_message_time_to_live=timedelta(days=14),
                dead_lettering_on_message_expiration=True,
                duplicate_detection_history_time_window=timedelta(minutes=10),
                requires_duplicate_detection=True,
                requires_session=kwargs.get('requires_session', False),
                max_delivery_count=10,
                enable_batched_operations=True,
                **kwargs
            )
            
            queue = self.admin_client.create_queue(queue_name, queue_properties)
            print(f"Queue created: {queue.name}")
            return queue
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Queue {queue_name} already exists")
                return self.admin_client.get_queue(queue_name)
            else:
                print(f"Error creating queue: {e}")
                return None
    
    def create_topic(self, topic_name, **kwargs):
        """Create a Service Bus topic"""
        from azure.servicebus.management import TopicProperties
        
        try:
            topic_properties = TopicProperties(
                max_size_in_megabytes=1024,
                default_message_time_to_live=timedelta(days=14),
                duplicate_detection_history_time_window=timedelta(minutes=10),
                requires_duplicate_detection=True,
                enable_batched_operations=True,
                **kwargs
            )
            
            topic = self.admin_client.create_topic(topic_name, topic_properties)
            print(f"Topic created: {topic.name}")
            return topic
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Topic {topic_name} already exists")
                return self.admin_client.get_topic(topic_name)
            else:
                print(f"Error creating topic: {e}")
                return None
    
    def create_subscription(self, topic_name, subscription_name, **kwargs):
        """Create a subscription to a topic"""
        from azure.servicebus.management import SubscriptionProperties
        
        try:
            subscription_properties = SubscriptionProperties(
                default_message_time_to_live=timedelta(days=14),
                dead_lettering_on_message_expiration=True,
                dead_lettering_on_filter_evaluation_exceptions=True,
                max_delivery_count=10,
                requires_session=kwargs.get('requires_session', False),
                enable_batched_operations=True,
                **kwargs
            )
            
            subscription = self.admin_client.create_subscription(
                topic_name, 
                subscription_name, 
                subscription_properties
            )
            print(f"Subscription created: {subscription.name}")
            return subscription
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Subscription {subscription_name} already exists")
                return self.admin_client.get_subscription(topic_name, subscription_name)
            else:
                print(f"Error creating subscription: {e}")
                return None
    
    def send_message(self, queue_or_topic_name, message_data, 
                    session_id=None, message_id=None, properties=None,
                    scheduled_enqueue_time=None):
        """Send a message to queue or topic"""
        try:
            # Prepare message
            if isinstance(message_data, dict):
                message_body = json.dumps(message_data)
            else:
                message_body = str(message_data)
            
            message = ServiceBusMessage(message_body)
            
            # Set optional properties
            if session_id:
                message.session_id = session_id
            
            if message_id:
                message.message_id = message_id
            
            if properties:
                for key, value in properties.items():
                    message.application_properties[key] = value
            
            if scheduled_enqueue_time:
                message.scheduled_enqueue_time_utc = scheduled_enqueue_time
            
            # Send message
            with self.client.get_queue_sender(queue_or_topic_name) as sender:
                sender.send_messages(message)
            
            print(f"Message sent to {queue_or_topic_name}")
            return message.message_id
            
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_batch_messages(self, queue_or_topic_name, messages_data, session_id=None):
        """Send multiple messages in a batch"""
        try:
            with self.client.get_queue_sender(queue_or_topic_name) as sender:
                batch = sender.create_message_batch()
                
                for message_data in messages_data:
                    if isinstance(message_data, dict):
                        message_body = json.dumps(message_data)
                    else:
                        message_body = str(message_data)
                    
                    message = ServiceBusMessage(message_body)
                    if session_id:
                        message.session_id = session_id
                    
                    try:
                        batch.add_message(message)
                    except ValueError:
                        # Batch is full, send it and create a new one
                        sender.send_messages(batch)
                        batch = sender.create_message_batch()
                        batch.add_message(message)
                
                # Send remaining messages
                if len(batch):
                    sender.send_messages(batch)
            
            print(f"Batch of {len(messages_data)} messages sent to {queue_or_topic_name}")
            
        except Exception as e:
            print(f"Error sending batch messages: {e}")
    
    def receive_messages(self, queue_or_subscription_name, topic_name=None, 
                        max_message_count=10, max_wait_time=60):
        """Receive messages from queue or subscription"""
        try:
            if topic_name:
                # Receiving from subscription
                receiver = self.client.get_subscription_receiver(
                    topic_name=topic_name,
                    subscription_name=queue_or_subscription_name,
                    max_wait_time=max_wait_time
                )
            else:
                # Receiving from queue
                receiver = self.client.get_queue_receiver(
                    queue_name=queue_or_subscription_name,
                    max_wait_time=max_wait_time
                )
            
            with receiver:
                messages = receiver.receive_messages(
                    max_message_count=max_message_count,
                    max_wait_time=max_wait_time
                )
                
                processed_messages = []
                for message in messages:
                    try:
                        # Parse message body
                        message_data = json.loads(str(message))
                    except json.JSONDecodeError:
                        message_data = str(message)
                    
                    processed_messages.append({
                        'body': message_data,
                        'message_id': message.message_id,
                        'session_id': message.session_id,
                        'properties': dict(message.application_properties),
                        'delivery_count': message.delivery_count,
                        'enqueued_time': message.enqueued_time_utc,
                        'message_obj': message  # For completing/abandoning
                    })
                
                return processed_messages
                
        except Exception as e:
            print(f"Error receiving messages: {e}")
            return []
    
    def receive_session_messages(self, queue_or_subscription_name, session_id, 
                               topic_name=None, max_message_count=10):
        """Receive messages from a specific session"""
        try:
            if topic_name:
                # Session receiver for subscription
                session_receiver = self.client.get_subscription_receiver(
                    topic_name=topic_name,
                    subscription_name=queue_or_subscription_name,
                    session_id=session_id
                )
            else:
                # Session receiver for queue
                session_receiver = self.client.get_queue_receiver(
                    queue_name=queue_or_subscription_name,
                    session_id=session_id
                )
            
            with session_receiver:
                messages = session_receiver.receive_messages(
                    max_message_count=max_message_count,
                    max_wait_time=60
                )
                
                processed_messages = []
                for message in messages:
                    try:
                        message_data = json.loads(str(message))
                    except json.JSONDecodeError:
                        message_data = str(message)
                    
                    processed_messages.append({
                        'body': message_data,
                        'message_id': message.message_id,
                        'session_id': message.session_id,
                        'properties': dict(message.application_properties),
                        'message_obj': message
                    })
                    
                    # Complete message
                    session_receiver.complete_message(message)
                
                return processed_messages
                
        except Exception as e:
            print(f"Error receiving session messages: {e}")
            return []
    
    def complete_message(self, message):
        """Complete (acknowledge) a message"""
        try:
            # Note: In practice, you'd use the receiver to complete
            print(f"Message {message.message_id} completed")
        except Exception as e:
            print(f"Error completing message: {e}")
    
    def abandon_message(self, message):
        """Abandon a message (returns to queue)"""
        try:
            # Note: In practice, you'd use the receiver to abandon
            print(f"Message {message.message_id} abandoned")
        except Exception as e:
            print(f"Error abandoning message: {e}")
    
    def dead_letter_message(self, message, reason="Processing failed"):
        """Send message to dead letter queue"""
        try:
            # Note: In practice, you'd use the receiver to dead letter
            print(f"Message {message.message_id} sent to dead letter queue: {reason}")
        except Exception as e:
            print(f"Error dead lettering message: {e}")

# Usage example
if __name__ == "__main__":
    # Initialize with connection string
    connection_string = "Endpoint=sb://sb-platform-messaging.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=your-key"
    sb_manager = ServiceBusManager(connection_string=connection_string)
    
    # Create queue
    queue_name = "order-processing-queue"
    sb_manager.create_queue(queue_name, requires_session=False)
    
    # Create topic and subscription
    topic_name = "order-events"
    subscription_name = "order-processing-sub"
    sb_manager.create_topic(topic_name)
    sb_manager.create_subscription(topic_name, subscription_name)
    
    # Send message to queue
    order_data = {
        'order_id': '12345',
        'customer_id': 'cust_789',
        'total_amount': 89.99,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    properties = {
        'event_type': 'order_created',
        'source': 'ecommerce_api',
        'version': '1.0'
    }
    
    message_id = sb_manager.send_message(
        queue_name, 
        order_data, 
        properties=properties,
        message_id=f"order_{order_data['order_id']}"
    )
    
    # Send message to topic
    sb_manager.send_message(topic_name, order_data, properties=properties)
    
    # Receive messages from queue
    messages = sb_manager.receive_messages(queue_name, max_message_count=5)
    
    for msg in messages:
        print(f"Received message: {msg['body']}")
        print(f"Message ID: {msg['message_id']}")
        print(f"Properties: {msg['properties']}")
        
        # Process message and complete
        try:
            # Your processing logic here
            print(f"Processing order {msg['body']['order_id']}")
            
            # Complete message after successful processing
            sb_manager.complete_message(msg['message_obj'])
            
        except Exception as e:
            print(f"Error processing message: {e}")
            # Abandon or dead letter the message
            sb_manager.abandon_message(msg['message_obj'])
```

## Advanced Features

### Message Sessions for Ordered Processing
```python
class SessionProcessor:
    def __init__(self, service_bus_manager):
        self.sb_manager = service_bus_manager
    
    def send_session_messages(self, queue_name, session_id, messages):
        """Send related messages in a session"""
        for i, message_data in enumerate(messages):
            # Add sequence number for ordering
            message_data['sequence_number'] = i + 1
            
            self.sb_manager.send_message(
                queue_name,
                message_data,
                session_id=session_id,
                message_id=f"{session_id}_{i+1}"
            )
        
        print(f"Sent {len(messages)} messages for session {session_id}")
    
    def process_session_messages(self, queue_name, session_id):
        """Process all messages in a session"""
        messages = self.sb_manager.receive_session_messages(
            queue_name, 
            session_id,
            max_message_count=100
        )
        
        # Sort by sequence number to ensure order
        messages.sort(key=lambda x: x['body'].get('sequence_number', 0))
        
        print(f"Processing {len(messages)} messages for session {session_id}")
        
        for message in messages:
            print(f"Processing message {message['body']['sequence_number']}: {message['body']}")
            # Your ordered processing logic here
        
        return len(messages)

# Example usage for ordered processing
session_processor = SessionProcessor(sb_manager)

# Create session-enabled queue
session_queue = "user-session-events"
sb_manager.create_queue(session_queue, requires_session=True)

# Send related events for a user session
user_session_id = "user_123_session_456"
user_events = [
    {"event": "login", "timestamp": "2024-01-01T10:00:00Z"},
    {"event": "view_product", "product_id": "prod_456", "timestamp": "2024-01-01T10:01:00Z"},
    {"event": "add_to_cart", "product_id": "prod_456", "timestamp": "2024-01-01T10:02:00Z"},
    {"event": "checkout", "order_id": "order_789", "timestamp": "2024-01-01T10:03:00Z"}
]

session_processor.send_session_messages(session_queue, user_session_id, user_events)

# Process session messages in order
session_processor.process_session_messages(session_queue, user_session_id)
```

### Message Filtering and Routing
```python
from azure.servicebus.management import SqlRuleFilter, CorrelationRuleFilter

class MessageRouting:
    def __init__(self, service_bus_manager):
        self.sb_manager = service_bus_manager
        self.admin_client = service_bus_manager.admin_client
    
    def create_filtered_subscription(self, topic_name, subscription_name, filter_expression):
        """Create subscription with SQL filter"""
        try:
            # Create subscription
            subscription = self.sb_manager.create_subscription(topic_name, subscription_name)
            
            # Remove default rule
            try:
                self.admin_client.delete_rule(topic_name, subscription_name, "$Default")
            except:
                pass  # Rule might not exist
            
            # Add custom filter rule
            sql_filter = SqlRuleFilter(filter_expression)
            self.admin_client.create_rule(
                topic_name,
                subscription_name,
                "CustomFilter",
                filter=sql_filter
            )
            
            print(f"Created subscription {subscription_name} with filter: {filter_expression}")
            return subscription
            
        except Exception as e:
            print(f"Error creating filtered subscription: {e}")
            return None
    
    def create_correlation_subscription(self, topic_name, subscription_name, 
                                      correlation_id=None, properties=None):
        """Create subscription with correlation filter"""
        try:
            # Create subscription
            subscription = self.sb_manager.create_subscription(topic_name, subscription_name)
            
            # Remove default rule
            try:
                self.admin_client.delete_rule(topic_name, subscription_name, "$Default")
            except:
                pass
            
            # Create correlation filter
            correlation_filter = CorrelationRuleFilter(
                correlation_id=correlation_id,
                properties=properties or {}
            )
            
            self.admin_client.create_rule(
                topic_name,
                subscription_name,
                "CorrelationFilter",
                filter=correlation_filter
            )
            
            print(f"Created subscription {subscription_name} with correlation filter")
            return subscription
            
        except Exception as e:
            print(f"Error creating correlation subscription: {e}")
            return None

# Example usage for message routing
routing = MessageRouting(sb_manager)

# Create topic for order events
order_topic = "order-events-topic"
sb_manager.create_topic(order_topic)

# Create subscriptions with different filters
# High-value orders subscription
routing.create_filtered_subscription(
    order_topic,
    "high-value-orders",
    "total_amount > 100"
)

# Priority orders subscription
routing.create_filtered_subscription(
    order_topic,
    "priority-orders",
    "priority = 'high' OR priority = 'urgent'"
)

# Specific customer subscription
routing.create_correlation_subscription(
    order_topic,
    "vip-customer-orders",
    properties={"customer_tier": "vip"}
)

# Send messages with different properties
orders = [
    {"order_id": "order_1", "total_amount": 150, "priority": "normal"},
    {"order_id": "order_2", "total_amount": 50, "priority": "high"},
    {"order_id": "order_3", "total_amount": 200, "priority": "urgent"}
]

for order in orders:
    properties = {
        "total_amount": order["total_amount"],
        "priority": order["priority"],
        "customer_tier": "vip" if order["total_amount"] > 100 else "regular"
    }
    
    sb_manager.send_message(order_topic, order, properties=properties)
```

### Azure Functions Integration
```python
import logging
import json
import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def main(msg: func.ServiceBusMessage) -> None:
    """Azure Function triggered by Service Bus message"""
    
    logging.info('Python ServiceBus queue trigger processed message: %s',
                msg.get_body().decode('utf-8'))
    
    try:
        # Parse message body
        message_data = json.loads(msg.get_body().decode('utf-8'))
        
        # Get message properties
        message_id = msg.message_id
        session_id = msg.session_id
        delivery_count = msg.delivery_count
        enqueued_time = msg.enqueued_time_utc
        
        logging.info(f"Processing message ID: {message_id}")
        logging.info(f"Session ID: {session_id}")
        logging.info(f"Delivery count: {delivery_count}")
        
        # Process based on message type
        event_type = message_data.get('event_type', 'unknown')
        
        if event_type == 'order_created':
            process_order_created(message_data)
        elif event_type == 'order_updated':
            process_order_updated(message_data)
        elif event_type == 'order_cancelled':
            process_order_cancelled(message_data)
        else:
            logging.warning(f"Unknown event type: {event_type}")
        
        logging.info("Message processed successfully")
        
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        
        # Check delivery count for dead lettering
        if delivery_count >= 5:
            logging.error("Message exceeded max delivery count, will be dead lettered")
        
        # Re-raise exception to trigger retry or dead lettering
        raise

def process_order_created(order_data):
    """Process new order creation"""
    order_id = order_data.get('order_id')
    customer_id = order_data.get('customer_id')
    total_amount = order_data.get('total_amount')
    
    logging.info(f"Processing new order {order_id} for customer {customer_id}")
    
    # Your order processing logic here
    # - Validate inventory
    # - Process payment
    # - Send confirmation email
    # - Update order status
    
    # Example: Send follow-up message
    connection_string = "your-service-bus-connection-string"
    with ServiceBusClient.from_connection_string(connection_string) as client:
        with client.get_queue_sender("order-confirmation-queue") as sender:
            confirmation_message = ServiceBusMessage(json.dumps({
                "order_id": order_id,
                "customer_id": customer_id,
                "status": "confirmed",
                "timestamp": "2024-01-01T10:00:00Z"
            }))
            sender.send_messages(confirmation_message)

def process_order_updated(order_data):
    """Process order updates"""
    order_id = order_data.get('order_id')
    status = order_data.get('status')
    
    logging.info(f"Updating order {order_id} to status {status}")
    
    # Your order update logic here

def process_order_cancelled(order_data):
    """Process order cancellation"""
    order_id = order_data.get('order_id')
    
    logging.info(f"Processing cancellation for order {order_id}")
    
    # Your cancellation logic here
    # - Refund payment
    # - Restore inventory
    # - Send cancellation email
```

## Infrastructure as Code with Terraform

### Complete Service Bus Infrastructure
```hcl
# variables.tf
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "rg-messaging"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "application_name" {
  description = "Application name"
  type        = string
  default     = "ecommerce"
}

# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "messaging" {
  name     = var.resource_group_name
  location = var.location
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Service Bus Namespace
resource "azurerm_servicebus_namespace" "main" {
  name                = "sb-${var.application_name}-${var.environment}"
  location            = azurerm_resource_group.messaging.location
  resource_group_name = azurerm_resource_group.messaging.name
  sku                 = "Standard"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Service Bus Queues
resource "azurerm_servicebus_queue" "order_processing" {
  name         = "order-processing-queue"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  enable_partitioning                   = false
  max_size_in_megabytes                = 1024
  default_message_ttl                  = "P14D"  # 14 days
  duplicate_detection_history_time_window = "PT10M"  # 10 minutes
  requires_duplicate_detection         = true
  dead_lettering_on_message_expiration = true
  max_delivery_count                   = 10
  requires_session                     = false
  enable_batched_operations           = true
}

resource "azurerm_servicebus_queue" "order_processing_dlq" {
  name         = "order-processing-dlq"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  max_size_in_megabytes = 1024
  default_message_ttl   = "P30D"  # 30 days
}

resource "azurerm_servicebus_queue" "user_sessions" {
  name         = "user-session-events"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  enable_partitioning                   = false
  max_size_in_megabytes                = 1024
  default_message_ttl                  = "P7D"   # 7 days
  duplicate_detection_history_time_window = "PT10M"
  requires_duplicate_detection         = true
  dead_lettering_on_message_expiration = true
  max_delivery_count                   = 5
  requires_session                     = true
  enable_batched_operations           = true
}

# Service Bus Topics
resource "azurerm_servicebus_topic" "order_events" {
  name         = "order-events"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  max_size_in_megabytes                = 1024
  default_message_ttl                  = "P14D"
  duplicate_detection_history_time_window = "PT10M"
  requires_duplicate_detection         = true
  enable_batched_operations           = true
  enable_partitioning                 = false
}

resource "azurerm_servicebus_topic" "user_events" {
  name         = "user-events"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  max_size_in_megabytes = 1024
  default_message_ttl   = "P7D"
  enable_partitioning   = false
}

# Service Bus Subscriptions
resource "azurerm_servicebus_subscription" "order_processing" {
  name     = "order-processing-sub"
  topic_id = azurerm_servicebus_topic.order_events.id
  
  max_delivery_count                   = 10
  default_message_ttl                  = "P14D"
  dead_lettering_on_message_expiration = true
  dead_lettering_on_filter_evaluation_exceptions = true
  requires_session                     = false
  enable_batched_operations           = true
}

resource "azurerm_servicebus_subscription" "high_value_orders" {
  name     = "high-value-orders"
  topic_id = azurerm_servicebus_topic.order_events.id
  
  max_delivery_count                   = 10
  default_message_ttl                  = "P14D"
  dead_lettering_on_message_expiration = true
  enable_batched_operations           = true
}

resource "azurerm_servicebus_subscription" "order_analytics" {
  name     = "order-analytics"
  topic_id = azurerm_servicebus_topic.order_events.id
  
  max_delivery_count    = 3
  default_message_ttl   = "P7D"
  enable_batched_operations = true
}

# Subscription Rules (Filters)
resource "azurerm_servicebus_subscription_rule" "high_value_filter" {
  name            = "HighValueFilter"
  subscription_id = azurerm_servicebus_subscription.high_value_orders.id
  filter_type     = "SqlFilter"
  sql_filter      = "total_amount > 100"
}

resource "azurerm_servicebus_subscription_rule" "priority_filter" {
  name            = "PriorityFilter"
  subscription_id = azurerm_servicebus_subscription.order_processing.id
  filter_type     = "SqlFilter"
  sql_filter      = "priority IN ('high', 'urgent') OR total_amount > 500"
}

# Authorization Rules
resource "azurerm_servicebus_namespace_authorization_rule" "app_send_listen" {
  name         = "${var.application_name}-app-access"
  namespace_id = azurerm_servicebus_namespace.main.id
  
  listen = true
  send   = true
  manage = false
}

resource "azurerm_servicebus_queue_authorization_rule" "order_processing_send" {
  name     = "order-processing-send"
  queue_id = azurerm_servicebus_queue.order_processing.id
  
  listen = false
  send   = true
  manage = false
}

resource "azurerm_servicebus_queue_authorization_rule" "order_processing_listen" {
  name     = "order-processing-listen"
  queue_id = azurerm_servicebus_queue.order_processing.id
  
  listen = true
  send   = false
  manage = false
}

# Function App for processing
resource "azurerm_storage_account" "function_storage" {
  name                     = "st${var.application_name}func${var.environment}"
  resource_group_name      = azurerm_resource_group.messaging.name
  location                 = azurerm_resource_group.messaging.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "azurerm_service_plan" "function_plan" {
  name                = "plan-${var.application_name}-functions-${var.environment}"
  resource_group_name = azurerm_resource_group.messaging.name
  location            = azurerm_resource_group.messaging.location
  os_type             = "Linux"
  sku_name            = "Y1"  # Consumption plan
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "azurerm_linux_function_app" "order_processor" {
  name                = "func-${var.application_name}-processor-${var.environment}"
  resource_group_name = azurerm_resource_group.messaging.name
  location            = azurerm_resource_group.messaging.location
  
  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key
  service_plan_id           = azurerm_service_plan.function_plan.id
  
  site_config {
    application_stack {
      python_version = "3.9"
    }
  }
  
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"     = "python"
    "ServiceBusConnection"         = azurerm_servicebus_namespace.main.default_primary_connection_string
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.main.instrumentation_key
  }
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Application Insights for monitoring
resource "azurerm_application_insights" "main" {
  name                = "ai-${var.application_name}-${var.environment}"
  location            = azurerm_resource_group.messaging.location
  resource_group_name = azurerm_resource_group.messaging.name
  application_type    = "web"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Outputs
output "namespace_connection_string" {
  description = "Service Bus namespace connection string"
  value       = azurerm_servicebus_namespace.main.default_primary_connection_string
  sensitive   = true
}

output "queue_names" {
  description = "Created queue names"
  value = {
    order_processing = azurerm_servicebus_queue.order_processing.name
    user_sessions    = azurerm_servicebus_queue.user_sessions.name
    dlq              = azurerm_servicebus_queue.order_processing_dlq.name
  }
}

output "topic_names" {
  description = "Created topic names"
  value = {
    order_events = azurerm_servicebus_topic.order_events.name
    user_events  = azurerm_servicebus_topic.user_events.name
  }
}

output "subscription_names" {
  description = "Created subscription names"
  value = {
    order_processing   = azurerm_servicebus_subscription.order_processing.name
    high_value_orders  = azurerm_servicebus_subscription.high_value_orders.name
    order_analytics    = azurerm_servicebus_subscription.order_analytics.name
  }
}

output "function_app_name" {
  description = "Function app name"
  value       = azurerm_linux_function_app.order_processor.name
}
```

## Monitoring and Observability

### Azure Monitor Integration
```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.azure_servicebus import ServiceBusInstrumentation
import logging

class ServiceBusMonitoring:
    def __init__(self, connection_string, instrumentation_key=None):
        self.connection_string = connection_string
        
        # Configure Azure Monitor if instrumentation key provided
        if instrumentation_key:
            configure_azure_monitor(connection_string=f"InstrumentationKey={instrumentation_key}")
        
        # Enable Service Bus instrumentation
        ServiceBusInstrumentation().instrument()
        
        # Get tracer
        self.tracer = trace.get_tracer(__name__)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def send_with_tracing(self, queue_name, message_data, operation_name="send_message"):
        """Send message with distributed tracing"""
        with self.tracer.start_as_current_span(operation_name) as span:
            try:
                # Add span attributes
                span.set_attribute("messaging.system", "servicebus")
                span.set_attribute("messaging.destination", queue_name)
                span.set_attribute("messaging.operation", "publish")
                
                # Send message
                client = ServiceBusClient.from_connection_string(self.connection_string)
                with client.get_queue_sender(queue_name) as sender:
                    message = ServiceBusMessage(json.dumps(message_data))
                    sender.send_messages(message)
                
                span.set_attribute("messaging.message_id", message.message_id)
                span.set_status(trace.Status(trace.StatusCode.OK))
                
                self.logger.info(f"Message sent successfully to {queue_name}")
                
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                span.record_exception(e)
                self.logger.error(f"Error sending message: {e}")
                raise
    
    def receive_with_tracing(self, queue_name, processor_func, operation_name="receive_message"):
        """Receive and process messages with tracing"""
        client = ServiceBusClient.from_connection_string(self.connection_string)
        
        with client.get_queue_receiver(queue_name) as receiver:
            for message in receiver:
                with self.tracer.start_as_current_span(operation_name) as span:
                    try:
                        # Add span attributes
                        span.set_attribute("messaging.system", "servicebus")
                        span.set_attribute("messaging.source", queue_name)
                        span.set_attribute("messaging.operation", "receive")
                        span.set_attribute("messaging.message_id", message.message_id)
                        span.set_attribute("messaging.delivery_count", message.delivery_count)
                        
                        # Process message
                        message_data = json.loads(str(message))
                        result = processor_func(message_data)
                        
                        if result:
                            receiver.complete_message(message)
                            span.set_status(trace.Status(trace.StatusCode.OK))
                            self.logger.info(f"Message {message.message_id} processed successfully")
                        else:
                            receiver.abandon_message(message)
                            span.set_status(trace.Status(trace.StatusCode.ERROR, "Processing failed"))
                            self.logger.warning(f"Message {message.message_id} processing failed")
                        
                    except Exception as e:
                        receiver.dead_letter_message(message, reason=str(e))
                        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                        span.record_exception(e)
                        self.logger.error(f"Error processing message {message.message_id}: {e}")

# Usage example
monitoring = ServiceBusMonitoring(
    connection_string="your-connection-string",
    instrumentation_key="your-app-insights-key"
)

# Send message with tracing
order_data = {"order_id": "12345", "total_amount": 99.99}
monitoring.send_with_tracing("order-queue", order_data)

# Process messages with tracing
def process_order(message_data):
    print(f"Processing order: {message_data}")
    return True

monitoring.receive_with_tracing("order-queue", process_order)
```

## Best Practices

### Error Handling and Resilience
```python
import time
import random
from azure.servicebus.exceptions import ServiceBusError

class ResilientServiceBusClient:
    def __init__(self, connection_string, max_retries=3):
        self.connection_string = connection_string
        self.max_retries = max_retries
    
    def send_with_retry(self, queue_name, message_data, exponential_backoff=True):
        """Send message with retry logic and exponential backoff"""
        
        for attempt in range(self.max_retries + 1):
            try:
                client = ServiceBusClient.from_connection_string(self.connection_string)
                with client.get_queue_sender(queue_name) as sender:
                    message = ServiceBusMessage(json.dumps(message_data))
                    sender.send_messages(message)
                
                print(f"Message sent successfully on attempt {attempt + 1}")
                return True
                
            except ServiceBusError as e:
                if attempt == self.max_retries:
                    print(f"Failed to send message after {self.max_retries + 1} attempts: {e}")
                    raise
                
                # Calculate backoff delay
                if exponential_backoff:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                else:
                    delay = 1
                
                print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f} seconds: {e}")
                time.sleep(delay)
        
        return False
    
    def process_with_circuit_breaker(self, queue_name, processor_func, 
                                   failure_threshold=5, timeout=60):
        """Process messages with circuit breaker pattern"""
        failure_count = 0
        last_failure_time = None
        circuit_open = False
        
        client = ServiceBusClient.from_connection_string(self.connection_string)
        
        with client.get_queue_receiver(queue_name) as receiver:
            for message in receiver:
                # Check circuit breaker state
                if circuit_open:
                    if time.time() - last_failure_time > timeout:
                        circuit_open = False
                        failure_count = 0
                        print("Circuit breaker reset")
                    else:
                        print("Circuit breaker is open, skipping message processing")
                        receiver.abandon_message(message)
                        continue
                
                try:
                    # Process message
                    message_data = json.loads(str(message))
                    result = processor_func(message_data)
                    
                    if result:
                        receiver.complete_message(message)
                        # Reset failure count on success
                        failure_count = 0
                    else:
                        receiver.abandon_message(message)
                        failure_count += 1
                
                except Exception as e:
                    print(f"Error processing message: {e}")
                    receiver.dead_letter_message(message, reason=str(e))
                    failure_count += 1
                    last_failure_time = time.time()
                
                # Check if circuit should open
                if failure_count >= failure_threshold:
                    circuit_open = True
                    print(f"Circuit breaker opened after {failure_count} failures")

# Good: Idempotent message processing
def idempotent_order_processor(order_data):
    """Process order idempotently using database constraints"""
    order_id = order_data['order_id']
    
    try:
        # Try to insert order (will fail if duplicate due to unique constraint)
        result = database.execute(
            "INSERT INTO orders (order_id, customer_id, total_amount, status) VALUES (?, ?, ?, ?)",
            (order_id, order_data['customer_id'], order_data['total_amount'], 'processing')
        )
        
        if result.rowcount > 0:
            print(f"Processing new order {order_id}")
            # Process the order
            return True
        else:
            print(f"Order {order_id} already exists, skipping")
            return True
            
    except database.IntegrityError:
        # Order already exists
        print(f"Order {order_id} already processed")
        return True
    except Exception as e:
        print(f"Error processing order {order_id}: {e}")
        return False

# Good: Dead letter queue monitoring
def monitor_dead_letter_queue(queue_name):
    """Monitor and alert on dead letter queue messages"""
    dlq_name = f"{queue_name}/$DeadLetterQueue"
    
    client = ServiceBusClient.from_connection_string(connection_string)
    
    with client.get_queue_receiver(dlq_name) as receiver:
        messages = receiver.receive_messages(max_message_count=10, max_wait_time=30)
        
        if messages:
            print(f"Found {len(messages)} messages in dead letter queue")
            
            for message in messages:
                print(f"DLQ Message ID: {message.message_id}")
                print(f"Delivery count: {message.delivery_count}")
                print(f"Dead letter reason: {message.dead_letter_reason}")
                print(f"Dead letter description: {message.dead_letter_error_description}")
                print(f"Message body: {str(message)}")
                
                # Decide whether to retry or permanently remove
                if should_retry_message(message):
                    # Send back to original queue
                    requeue_message(queue_name, message)
                    receiver.complete_message(message)
                else:
                    # Log for manual review and remove from DLQ
                    log_message_for_review(message)
                    receiver.complete_message(message)

def should_retry_message(message):
    """Determine if a dead letter message should be retried"""
    # Add your retry logic here
    # Consider factors like delivery count, error type, message age, etc.
    return message.delivery_count < 10

def requeue_message(queue_name, original_message):
    """Send message back to original queue"""
    client = ServiceBusClient.from_connection_string(connection_string)
    
    with client.get_queue_sender(queue_name) as sender:
        new_message = ServiceBusMessage(
            original_message.body,
            application_properties=original_message.application_properties
        )
        sender.send_messages(new_message)
```

## Resources

- [Azure Service Bus Documentation](https://docs.microsoft.com/en-us/azure/service-bus-messaging/) - Official Service Bus documentation
- [Azure Service Bus Python SDK](https://docs.microsoft.com/en-us/python/api/overview/azure/servicebus-readme) - Python client library reference
- [Service Bus Best Practices](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-performance-improvements) - Performance and best practices
- [Azure Functions with Service Bus](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-service-bus) - Functions integration guide
- [Service Bus Messaging Patterns](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview) - Enterprise messaging patterns
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/servicebus_namespace) - Infrastructure as code
- [Azure Monitor Integration](https://docs.microsoft.com/en-us/azure/azure-monitor/app/azure-functions-supported-features) - Monitoring and observability
- [Service Bus Security](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-authentication-and-authorization) - Authentication and authorization
- [Service Bus Transactions](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-transactions) - Transactional messaging
- [Message Sessions](https://docs.microsoft.com/en-us/azure/service-bus-messaging/message-sessions) - Ordered message processing