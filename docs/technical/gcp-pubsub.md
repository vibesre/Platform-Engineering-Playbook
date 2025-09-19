# Google Cloud Pub/Sub

Google Cloud Pub/Sub is a fully managed real-time messaging service that enables reliable, many-to-many communication between applications and services. It's essential for building event-driven architectures, microservices communication, and real-time data processing pipelines in platform engineering.

## Overview

Google Cloud Pub/Sub is widely used in platform engineering for:
- Decoupling microservices and distributed applications
- Building event-driven architectures and streaming analytics
- Implementing reliable message queuing and pub/sub patterns
- Processing real-time data streams and IoT events
- Enabling asynchronous workloads and batch processing

## Key Features

- **Global Scale**: Automatically scales to handle millions of messages per second
- **At-Least-Once Delivery**: Guarantees message delivery with acknowledgment
- **Exactly-Once Processing**: Optional exactly-once delivery semantics
- **Dead Letter Topics**: Automatic handling of undeliverable messages
- **Message Ordering**: Ordered delivery within message keys
- **Replay and Seek**: Message replay and seeking to specific timestamps

## Core Concepts

### Topics and Subscriptions
- **Topic**: Named resource to which publishers send messages
- **Subscription**: Named resource representing message stream from topic
- **Publisher**: Application that sends messages to topics
- **Subscriber**: Application that receives messages from subscriptions

### Message Flow
```
Publisher → Topic → Subscription → Subscriber
                 ↘ Subscription → Subscriber
                 ↘ Subscription → Subscriber
```

## Installation and Setup

### Authentication Setup
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
source ~/.bashrc
gcloud init

# Set project
gcloud config set project your-project-id

# Create service account
gcloud iam service-accounts create pubsub-service-account \
    --display-name="Pub/Sub Service Account"

# Grant Pub/Sub roles
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:pubsub-service-account@your-project-id.iam.gserviceaccount.com" \
    --role="roles/pubsub.admin"

# Generate service account key
gcloud iam service-accounts keys create pubsub-key.json \
    --iam-account=pubsub-service-account@your-project-id.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/pubsub-key.json"
```

### Python Client Installation
```bash
# Install Pub/Sub client library
pip install google-cloud-pubsub

# Install additional dependencies
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

## Basic Pub/Sub Implementation

### Topic and Subscription Management
```python
from google.cloud import pubsub_v1
from google.api_core import retry
from google.auth import jwt
import json
import time
from concurrent.futures import ThreadPoolExecutor

class PubSubManager:
    def __init__(self, project_id, credentials_path=None):
        self.project_id = project_id
        
        if credentials_path:
            # Load service account credentials
            self.publisher = pubsub_v1.PublisherClient.from_service_account_json(credentials_path)
            self.subscriber = pubsub_v1.SubscriberClient.from_service_account_json(credentials_path)
        else:
            # Use default credentials
            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()
        
        self.project_path = f"projects/{project_id}"
    
    def create_topic(self, topic_name):
        """Create a Pub/Sub topic"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        
        try:
            topic = self.publisher.create_topic(request={"name": topic_path})
            print(f"Topic created: {topic.name}")
            return topic_path
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Topic {topic_name} already exists")
                return topic_path
            else:
                print(f"Error creating topic: {e}")
                return None
    
    def create_subscription(self, topic_name, subscription_name, 
                          dead_letter_topic=None, max_delivery_attempts=5):
        """Create a subscription to a topic"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        try:
            request = {
                "name": subscription_path,
                "topic": topic_path,
                "ack_deadline_seconds": 60,
                "message_retention_duration": {"seconds": 604800},  # 7 days
                "expiration_policy": {"ttl": {"seconds": 2592000}}  # 30 days
            }
            
            # Configure dead letter topic if provided
            if dead_letter_topic:
                dlq_topic_path = self.publisher.topic_path(self.project_id, dead_letter_topic)
                request["dead_letter_policy"] = {
                    "dead_letter_topic": dlq_topic_path,
                    "max_delivery_attempts": max_delivery_attempts
                }
            
            subscription = self.subscriber.create_subscription(request=request)
            print(f"Subscription created: {subscription.name}")
            return subscription_path
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Subscription {subscription_name} already exists")
                return subscription_path
            else:
                print(f"Error creating subscription: {e}")
                return None
    
    def create_push_subscription(self, topic_name, subscription_name, endpoint_url):
        """Create a push subscription"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        try:
            request = {
                "name": subscription_path,
                "topic": topic_path,
                "push_config": {
                    "push_endpoint": endpoint_url
                },
                "ack_deadline_seconds": 60
            }
            
            subscription = self.subscriber.create_subscription(request=request)
            print(f"Push subscription created: {subscription.name}")
            return subscription_path
        except Exception as e:
            print(f"Error creating push subscription: {e}")
            return None
    
    def publish_message(self, topic_name, message_data, attributes=None, ordering_key=None):
        """Publish a message to a topic"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        
        # Convert message to bytes
        if isinstance(message_data, dict):
            data = json.dumps(message_data).encode('utf-8')
        elif isinstance(message_data, str):
            data = message_data.encode('utf-8')
        else:
            data = message_data
        
        # Prepare message
        message = {"data": data}
        
        if attributes:
            message["attributes"] = attributes
        
        if ordering_key:
            message["ordering_key"] = ordering_key
        
        try:
            future = self.publisher.publish(topic_path, **message)
            message_id = future.result()
            print(f"Message published: {message_id}")
            return message_id
        except Exception as e:
            print(f"Error publishing message: {e}")
            return None
    
    def publish_batch(self, topic_name, messages, batch_settings=None):
        """Publish multiple messages in batch"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        
        if batch_settings:
            # Configure batch settings
            batch_settings_obj = pubsub_v1.types.BatchSettings(**batch_settings)
            publisher = pubsub_v1.PublisherClient(batch_settings_obj)
        else:
            publisher = self.publisher
        
        futures = []
        
        for message in messages:
            if isinstance(message, dict):
                data = json.dumps(message).encode('utf-8')
            else:
                data = message.encode('utf-8')
            
            future = publisher.publish(topic_path, data=data)
            futures.append(future)
        
        # Wait for all messages to be published
        message_ids = []
        for future in futures:
            try:
                message_id = future.result()
                message_ids.append(message_id)
            except Exception as e:
                print(f"Error publishing message: {e}")
        
        print(f"Published {len(message_ids)} messages")
        return message_ids
    
    def subscribe_pull(self, subscription_name, callback_func, max_messages=100, timeout=None):
        """Subscribe to messages using pull delivery"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        # Configure flow control
        flow_control = pubsub_v1.types.FlowControl(max_messages=max_messages)
        
        print(f"Listening for messages on {subscription_path}...")
        
        try:
            streaming_pull_future = self.subscriber.subscribe(
                subscription_path,
                callback=callback_func,
                flow_control=flow_control
            )
            
            if timeout:
                try:
                    streaming_pull_future.result(timeout=timeout)
                except TimeoutError:
                    streaming_pull_future.cancel()
                    print("Subscription timed out")
            else:
                streaming_pull_future.result()
                
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            print("Subscription cancelled")
    
    def synchronous_pull(self, subscription_name, max_messages=10, ack_deadline=60):
        """Synchronously pull messages"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        # Configure pull request
        request = {
            "subscription": subscription_path,
            "max_messages": max_messages,
            "allow_ack_time_extension": True
        }
        
        try:
            response = self.subscriber.pull(request=request)
            
            ack_ids = []
            messages = []
            
            for received_message in response.received_messages:
                message = received_message.message
                ack_id = received_message.ack_id
                
                # Decode message data
                try:
                    data = json.loads(message.data.decode('utf-8'))
                except json.JSONDecodeError:
                    data = message.data.decode('utf-8')
                
                messages.append({
                    'data': data,
                    'attributes': dict(message.attributes),
                    'message_id': message.message_id,
                    'publish_time': message.publish_time,
                    'ack_id': ack_id
                })
                
                ack_ids.append(ack_id)
            
            return messages, ack_ids
            
        except Exception as e:
            print(f"Error pulling messages: {e}")
            return [], []
    
    def acknowledge_messages(self, subscription_name, ack_ids):
        """Acknowledge processed messages"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        try:
            self.subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )
            print(f"Acknowledged {len(ack_ids)} messages")
        except Exception as e:
            print(f"Error acknowledging messages: {e}")
    
    def modify_ack_deadline(self, subscription_name, ack_ids, ack_deadline_seconds):
        """Modify acknowledgment deadline for messages"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        try:
            self.subscriber.modify_ack_deadline(
                request={
                    "subscription": subscription_path,
                    "ack_ids": ack_ids,
                    "ack_deadline_seconds": ack_deadline_seconds
                }
            )
            print(f"Modified ack deadline for {len(ack_ids)} messages")
        except Exception as e:
            print(f"Error modifying ack deadline: {e}")

# Usage example
if __name__ == "__main__":
    project_id = "your-project-id"
    pubsub_manager = PubSubManager(project_id)
    
    # Create topic and subscription
    topic_name = "order-events"
    subscription_name = "order-processing-sub"
    dead_letter_topic = "order-events-dlq"
    
    # Create topics
    pubsub_manager.create_topic(topic_name)
    pubsub_manager.create_topic(dead_letter_topic)
    
    # Create subscription with dead letter queue
    pubsub_manager.create_subscription(
        topic_name, 
        subscription_name,
        dead_letter_topic=dead_letter_topic,
        max_delivery_attempts=3
    )
    
    # Publish message
    order_data = {
        'order_id': '12345',
        'customer_id': 'cust_789',
        'total_amount': 89.99,
        'timestamp': time.time()
    }
    
    attributes = {
        'event_type': 'order_created',
        'source': 'ecommerce_api',
        'version': '1.0'
    }
    
    message_id = pubsub_manager.publish_message(
        topic_name, 
        order_data, 
        attributes=attributes
    )
    
    # Message callback function
    def message_callback(message):
        try:
            # Decode message data
            data = json.loads(message.data.decode('utf-8'))
            print(f"Received message: {data}")
            
            # Process the order
            order_id = data['order_id']
            print(f"Processing order {order_id}")
            
            # Simulate processing time
            time.sleep(1)
            
            # Acknowledge message
            message.ack()
            print(f"Order {order_id} processed successfully")
            
        except Exception as e:
            print(f"Error processing message: {e}")
            message.nack()
    
    # Subscribe to messages
    print("Starting message subscription...")
    pubsub_manager.subscribe_pull(subscription_name, message_callback, timeout=30)
```

## Advanced Features

### Ordered Message Processing
```python
class OrderedMessageProcessor:
    def __init__(self, project_id, topic_name, subscription_name):
        self.pubsub_manager = PubSubManager(project_id)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        
        # Create topic with message ordering enabled
        self.setup_ordered_topic()
    
    def setup_ordered_topic(self):
        """Setup topic and subscription for ordered processing"""
        topic_path = self.pubsub_manager.publisher.topic_path(
            self.pubsub_manager.project_id, 
            self.topic_name
        )
        
        # Create topic with message ordering
        try:
            topic = self.pubsub_manager.publisher.create_topic(
                request={
                    "name": topic_path,
                    "message_storage_policy": {
                        "allowed_persistence_regions": ["us-central1"]
                    }
                }
            )
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Error creating topic: {e}")
        
        # Create subscription with ordering enabled
        subscription_path = self.pubsub_manager.subscriber.subscription_path(
            self.pubsub_manager.project_id,
            self.subscription_name
        )
        
        try:
            subscription = self.pubsub_manager.subscriber.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "enable_message_ordering": True,
                    "ack_deadline_seconds": 60
                }
            )
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Error creating subscription: {e}")
    
    def publish_ordered_message(self, message_data, ordering_key, attributes=None):
        """Publish message with ordering key"""
        return self.pubsub_manager.publish_message(
            self.topic_name,
            message_data,
            attributes=attributes,
            ordering_key=ordering_key
        )
    
    def process_ordered_messages(self, callback_func):
        """Process messages in order"""
        def ordered_callback(message):
            try:
                # Process message
                callback_func(message)
                message.ack()
            except Exception as e:
                print(f"Error processing message: {e}")
                # For ordered processing, nack will pause the ordering key
                message.nack()
        
        self.pubsub_manager.subscribe_pull(
            self.subscription_name,
            ordered_callback
        )

# Example usage for ordered processing
order_processor = OrderedMessageProcessor(
    "your-project-id",
    "user-events-ordered",
    "user-events-ordered-sub"
)

# Publish ordered messages for a user
user_id = "user_123"
events = [
    {"event": "login", "timestamp": "2024-01-01T10:00:00Z"},
    {"event": "view_product", "product_id": "prod_456", "timestamp": "2024-01-01T10:01:00Z"},
    {"event": "add_to_cart", "product_id": "prod_456", "timestamp": "2024-01-01T10:02:00Z"},
    {"event": "checkout", "order_id": "order_789", "timestamp": "2024-01-01T10:03:00Z"}
]

for event in events:
    order_processor.publish_ordered_message(
        event,
        ordering_key=user_id,  # All events for this user will be ordered
        attributes={"user_id": user_id, "event_type": event["event"]}
    )
```

### Exactly-Once Processing
```python
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import DeadLetterPolicy

class ExactlyOnceProcessor:
    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
    
    def create_exactly_once_subscription(self, topic_name, subscription_name):
        """Create subscription with exactly-once delivery"""
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        try:
            subscription = self.subscriber.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "enable_exactly_once_delivery": True,
                    "ack_deadline_seconds": 60,
                    "message_retention_duration": {"seconds": 604800}
                }
            )
            print(f"Exactly-once subscription created: {subscription.name}")
            return subscription_path
        except Exception as e:
            print(f"Error creating exactly-once subscription: {e}")
            return None
    
    def process_with_exactly_once(self, subscription_name, processor_func):
        """Process messages with exactly-once semantics"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        def exactly_once_callback(message):
            try:
                # Process message idempotently
                result = processor_func(message)
                
                if result:
                    message.ack()
                    print(f"Message {message.message_id} processed successfully")
                else:
                    message.nack()
                    print(f"Message {message.message_id} processing failed")
                    
            except Exception as e:
                print(f"Error in exactly-once processing: {e}")
                message.nack()
        
        # Subscribe with exactly-once flow control
        flow_control = pubsub_v1.types.FlowControl(
            max_messages=100,
            max_bytes=1024*1024  # 1MB
        )
        
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=exactly_once_callback,
            flow_control=flow_control
        )
        
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()

# Example idempotent processor
def idempotent_order_processor(message):
    """Process order message idempotently"""
    try:
        data = json.loads(message.data.decode('utf-8'))
        order_id = data['order_id']
        
        # Check if order already processed (idempotency)
        if is_order_processed(order_id):
            print(f"Order {order_id} already processed, skipping")
            return True
        
        # Process order
        result = process_order(data)
        
        if result:
            # Mark as processed
            mark_order_processed(order_id)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing order: {e}")
        return False

def is_order_processed(order_id):
    # Check database/cache for processed orders
    # Implementation depends on your storage system
    pass

def process_order(order_data):
    # Your order processing logic
    pass

def mark_order_processed(order_id):
    # Mark order as processed in database/cache
    pass
```

## Cloud Functions Integration

### HTTP Triggered Function
```python
import json
import base64
from google.cloud import pubsub_v1
import functions_framework

@functions_framework.http
def pubsub_publisher(request):
    """HTTP triggered function to publish Pub/Sub messages"""
    
    # Parse request
    request_json = request.get_json(silent=True)
    
    if not request_json or 'message' not in request_json:
        return {'error': 'Invalid request'}, 400
    
    try:
        # Initialize publisher
        publisher = pubsub_v1.PublisherClient()
        project_id = "your-project-id"
        topic_name = "order-events"
        topic_path = publisher.topic_path(project_id, topic_name)
        
        # Prepare message
        message_data = json.dumps(request_json['message']).encode('utf-8')
        attributes = request_json.get('attributes', {})
        
        # Publish message
        future = publisher.publish(topic_path, data=message_data, **attributes)
        message_id = future.result()
        
        return {
            'message_id': message_id,
            'status': 'published'
        }
        
    except Exception as e:
        print(f"Error publishing message: {e}")
        return {'error': str(e)}, 500

@functions_framework.cloud_event
def pubsub_processor(cloud_event):
    """Cloud Event triggered function to process Pub/Sub messages"""
    
    try:
        # Decode Pub/Sub message
        message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        message_attributes = cloud_event.data["message"].get("attributes", {})
        
        # Parse message
        data = json.loads(message_data)
        
        print(f"Processing message: {data}")
        print(f"Message attributes: {message_attributes}")
        
        # Process based on message type
        if message_attributes.get('event_type') == 'order_created':
            process_order_created(data)
        elif message_attributes.get('event_type') == 'order_updated':
            process_order_updated(data)
        else:
            print(f"Unknown event type: {message_attributes.get('event_type')}")
        
        print("Message processed successfully")
        
    except Exception as e:
        print(f"Error processing message: {e}")
        raise e

def process_order_created(order_data):
    """Process new order creation"""
    order_id = order_data['order_id']
    customer_id = order_data['customer_id']
    
    # Your order processing logic here
    print(f"Processing new order {order_id} for customer {customer_id}")
    
    # Example: Send to inventory system, payment processing, etc.

def process_order_updated(order_data):
    """Process order updates"""
    order_id = order_data['order_id']
    status = order_data['status']
    
    # Your order update logic here
    print(f"Updating order {order_id} status to {status}")
```

## Infrastructure as Code with Terraform

### Complete Pub/Sub Infrastructure
```hcl
# variables.tf
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# main.tf
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "pubsub_api" {
  service = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudfunctions_api" {
  service = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

# Pub/Sub Topics
resource "google_pubsub_topic" "order_events" {
  name = "order-events-${var.environment}"
  
  message_retention_duration = "604800s"  # 7 days
  
  message_storage_policy {
    allowed_persistence_regions = [var.region]
  }
  
  labels = {
    environment = var.environment
    component   = "messaging"
  }
}

resource "google_pubsub_topic" "order_events_dlq" {
  name = "order-events-dlq-${var.environment}"
  
  message_retention_duration = "1209600s"  # 14 days
  
  labels = {
    environment = var.environment
    component   = "messaging"
    type        = "dead-letter"
  }
}

resource "google_pubsub_topic" "user_events" {
  name = "user-events-${var.environment}"
  
  message_retention_duration = "604800s"
  
  message_storage_policy {
    allowed_persistence_regions = [var.region]
  }
  
  labels = {
    environment = var.environment
    component   = "messaging"
  }
}

# Pub/Sub Subscriptions
resource "google_pubsub_subscription" "order_processing" {
  name  = "order-processing-${var.environment}"
  topic = google_pubsub_topic.order_events.name
  
  ack_deadline_seconds       = 60
  message_retention_duration = "604800s"
  retain_acked_messages     = false
  
  expiration_policy {
    ttl = "2592000s"  # 30 days
  }
  
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.order_events_dlq.id
    max_delivery_attempts = 5
  }
  
  retry_policy {
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
  
  labels = {
    environment = var.environment
    component   = "order-processing"
  }
}

resource "google_pubsub_subscription" "order_notifications" {
  name  = "order-notifications-${var.environment}"
  topic = google_pubsub_topic.order_events.name
  
  ack_deadline_seconds       = 30
  message_retention_duration = "604800s"
  
  push_config {
    push_endpoint = "https://${var.region}-${var.project_id}.cloudfunctions.net/order-notification-handler"
    
    attributes = {
      x-goog-version = "v1"
    }
  }
  
  labels = {
    environment = var.environment
    component   = "notifications"
  }
}

resource "google_pubsub_subscription" "user_analytics" {
  name  = "user-analytics-${var.environment}"
  topic = google_pubsub_topic.user_events.name
  
  enable_message_ordering    = true
  ack_deadline_seconds      = 60
  message_retention_duration = "604800s"
  
  labels = {
    environment = var.environment
    component   = "analytics"
  }
}

# Cloud Functions for processing
resource "google_storage_bucket" "function_source" {
  name     = "${var.project_id}-function-source-${var.environment}"
  location = var.region
}

resource "google_storage_bucket_object" "order_processor_source" {
  name   = "order-processor-${var.environment}.zip"
  bucket = google_storage_bucket.function_source.name
  source = "order_processor.zip"
}

resource "google_cloudfunctions_function" "order_processor" {
  name        = "order-processor-${var.environment}"
  description = "Process order events from Pub/Sub"
  runtime     = "python39"
  region      = var.region
  
  available_memory_mb   = 256
  timeout              = 60
  max_instances        = 100
  
  source_archive_bucket = google_storage_bucket.function_source.name
  source_archive_object = google_storage_bucket_object.order_processor_source.name
  
  entry_point = "process_order_event"
  
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.order_events.id
  }
  
  environment_variables = {
    PROJECT_ID  = var.project_id
    ENVIRONMENT = var.environment
  }
  
  labels = {
    environment = var.environment
    component   = "order-processing"
  }
}

# IAM for Cloud Functions
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.order_processor.name
  
  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${var.project_id}@appspot.gserviceaccount.com"
}

# Service Account for Pub/Sub operations
resource "google_service_account" "pubsub_service_account" {
  account_id   = "pubsub-service-${var.environment}"
  display_name = "Pub/Sub Service Account"
  description  = "Service account for Pub/Sub operations"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.pubsub_service_account.email}"
}

resource "google_project_iam_member" "pubsub_subscriber" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_service_account.pubsub_service_account.email}"
}

# Monitoring and Alerting
resource "google_monitoring_alert_policy" "high_unacked_messages" {
  display_name = "High Unacked Messages - ${var.environment}"
  
  conditions {
    display_name = "Unacked messages > 1000"
    
    condition_threshold {
      filter          = "resource.type=\"pubsub_subscription\""
      comparison      = "COMPARISON_GT"
      threshold_value = 1000
      duration        = "300s"
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }
  
  notification_channels = []  # Add notification channels
  
  alert_strategy {
    auto_close = "1800s"
  }
}

# Outputs
output "topic_names" {
  description = "Created topic names"
  value = {
    order_events = google_pubsub_topic.order_events.name
    user_events  = google_pubsub_topic.user_events.name
    dlq_topic    = google_pubsub_topic.order_events_dlq.name
  }
}

output "subscription_names" {
  description = "Created subscription names"
  value = {
    order_processing    = google_pubsub_subscription.order_processing.name
    order_notifications = google_pubsub_subscription.order_notifications.name
    user_analytics     = google_pubsub_subscription.user_analytics.name
  }
}

output "service_account_email" {
  description = "Service account email for Pub/Sub operations"
  value       = google_service_account.pubsub_service_account.email
}
```

## Monitoring and Observability

### Custom Metrics and Monitoring
```python
from google.cloud import monitoring_v3
from google.cloud import pubsub_v1
import time

class PubSubMonitoring:
    def __init__(self, project_id):
        self.project_id = project_id
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        
    def get_subscription_metrics(self, subscription_name):
        """Get metrics for a subscription"""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)
        
        # Get subscription details
        subscription = self.subscriber.get_subscription(request={"subscription": subscription_path})
        
        # Query metrics
        project_name = f"projects/{self.project_id}"
        
        # Unacked messages
        interval = monitoring_v3.TimeInterval({
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 3600}
        })
        
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=f'metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages" '
                   f'AND resource.labels.subscription_id="{subscription_name}"',
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        )
        
        results = self.monitoring_client.list_time_series(request=request)
        
        for result in results:
            print(f"Subscription: {subscription_name}")
            for point in result.points:
                print(f"Unacked messages: {point.value.int64_value} at {point.interval.end_time}")
    
    def create_custom_metric(self, metric_type, display_name, description):
        """Create custom metric descriptor"""
        project_name = f"projects/{self.project_id}"
        
        descriptor = monitoring_v3.MetricDescriptor(
            type=f"custom.googleapis.com/{metric_type}",
            metric_kind=monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
            value_type=monitoring_v3.MetricDescriptor.ValueType.INT64,
            display_name=display_name,
            description=description
        )
        
        try:
            created_descriptor = self.monitoring_client.create_metric_descriptor(
                name=project_name, metric_descriptor=descriptor
            )
            print(f"Created metric descriptor: {created_descriptor.name}")
            return created_descriptor
        except Exception as e:
            print(f"Error creating metric descriptor: {e}")
            return None
    
    def write_custom_metric(self, metric_type, value, resource_labels=None):
        """Write custom metric data point"""
        project_name = f"projects/{self.project_id}"
        
        if resource_labels is None:
            resource_labels = {"project_id": self.project_id}
        
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{metric_type}"
        series.resource.type = "global"
        series.resource.labels.update(resource_labels)
        
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        
        point = monitoring_v3.Point({
            "interval": interval,
            "value": {"int64_value": value}
        })
        
        series.points = [point]
        
        try:
            self.monitoring_client.create_time_series(
                name=project_name, time_series=[series]
            )
            print(f"Written custom metric: {metric_type} = {value}")
        except Exception as e:
            print(f"Error writing custom metric: {e}")

# Usage example
monitoring = PubSubMonitoring("your-project-id")

# Create custom metrics
monitoring.create_custom_metric(
    "order_processing_rate",
    "Order Processing Rate",
    "Number of orders processed per minute"
)

monitoring.create_custom_metric(
    "message_processing_latency",
    "Message Processing Latency",
    "Time taken to process messages in seconds"
)

# Write custom metrics
monitoring.write_custom_metric("order_processing_rate", 150)
monitoring.write_custom_metric("message_processing_latency", 5)

# Get subscription metrics
monitoring.get_subscription_metrics("order-processing-subscription")
```

## Best Practices

### Message Design and Error Handling
```python
# Good: Well-structured message with metadata
good_message = {
    "message_id": "msg_12345",
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "1.0",
    "source": "order-service",
    "event_type": "order_created",
    "correlation_id": "trace_abc123",
    "data": {
        "order_id": "order_67890",
        "customer_id": "cust_123",
        "total_amount": 89.99
    }
}

# Good: Idempotent message processing
def idempotent_processor(message):
    """Process message idempotently"""
    try:
        data = json.loads(message.data.decode('utf-8'))
        message_id = data.get('message_id')
        
        # Check if already processed
        if is_already_processed(message_id):
            print(f"Message {message_id} already processed")
            message.ack()
            return
        
        # Process message
        result = process_message(data)
        
        if result:
            # Mark as processed
            mark_as_processed(message_id)
            message.ack()
        else:
            # Retry with exponential backoff
            message.nack()
            
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

# Good: Circuit breaker for external dependencies
class CircuitBreaker:
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
                raise Exception("Circuit breaker is OPEN")
        
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

# Good: Retry logic with exponential backoff
import random

def exponential_backoff_retry(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f} seconds")
            time.sleep(delay)
```

### Security and Access Control
```python
from google.oauth2 import service_account
from google.auth import impersonated_credentials

# Service account authentication
def create_authenticated_clients(service_account_path):
    """Create authenticated Pub/Sub clients"""
    credentials = service_account.Credentials.from_service_account_file(
        service_account_path,
        scopes=['https://www.googleapis.com/auth/pubsub']
    )
    
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    
    return publisher, subscriber

# Impersonation for cross-project access
def create_impersonated_client(source_credentials, target_service_account):
    """Create client with impersonated credentials"""
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=target_service_account,
        target_scopes=['https://www.googleapis.com/auth/pubsub']
    )
    
    return pubsub_v1.PublisherClient(credentials=target_credentials)

# Message encryption (application-level)
from cryptography.fernet import Fernet

class EncryptedPublisher:
    def __init__(self, publisher, encryption_key):
        self.publisher = publisher
        self.cipher = Fernet(encryption_key)
    
    def publish_encrypted(self, topic_path, data, attributes=None):
        """Publish encrypted message"""
        # Encrypt message data
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted_data = self.cipher.encrypt(data)
        
        # Add encryption metadata
        if attributes is None:
            attributes = {}
        attributes['encrypted'] = 'true'
        attributes['encryption_algorithm'] = 'fernet'
        
        return self.publisher.publish(topic_path, data=encrypted_data, **attributes)

class EncryptedSubscriber:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
    
    def decrypt_message(self, message):
        """Decrypt received message"""
        if message.attributes.get('encrypted') == 'true':
            decrypted_data = self.cipher.decrypt(message.data)
            return decrypted_data.decode('utf-8')
        else:
            return message.data.decode('utf-8')
```

## Resources

- [Google Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs) - Official Pub/Sub documentation
- [Pub/Sub Python Client Library](https://googleapis.dev/python/pubsub/latest/) - Python client library reference
- [Pub/Sub Best Practices](https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system) - Official best practices guide
- [Cloud Functions with Pub/Sub](https://cloud.google.com/functions/docs/calling/pubsub) - Integration patterns
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic) - Infrastructure as code
- [Pub/Sub Monitoring](https://cloud.google.com/pubsub/docs/monitoring) - Monitoring and alerting guide
- [Message Ordering](https://cloud.google.com/pubsub/docs/ordering) - Ordered message delivery
- [Exactly-Once Delivery](https://cloud.google.com/pubsub/docs/exactly-once-delivery) - Exactly-once processing guide
- [Pub/Sub Lite](https://cloud.google.com/pubsub/lite/docs) - Lower-cost regional messaging
- [Event-Driven Architecture on GCP](https://cloud.google.com/eventarc) - Event-driven patterns and Eventarc