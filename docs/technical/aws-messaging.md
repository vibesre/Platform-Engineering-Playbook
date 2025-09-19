# AWS Messaging

AWS provides a comprehensive suite of messaging services that enable reliable, scalable, and secure communication between distributed applications and microservices. These services are essential for building event-driven architectures and decoupled systems in platform engineering.

## Overview

AWS messaging services are widely used in platform engineering for:
- Decoupling microservices and distributed applications
- Building event-driven architectures
- Implementing reliable message queuing and pub/sub patterns
- Processing high-throughput streaming data
- Handling asynchronous workloads and batch processing

## Core AWS Messaging Services

### Amazon SQS (Simple Queue Service)
- **Type**: Fully managed message queuing service
- **Pattern**: Point-to-point messaging
- **Use Cases**: Decoupling components, task queues, batch processing
- **Features**: Dead letter queues, FIFO ordering, visibility timeout

### Amazon SNS (Simple Notification Service)
- **Type**: Fully managed pub/sub messaging service
- **Pattern**: Publish/subscribe
- **Use Cases**: Fan-out messaging, mobile push notifications, email/SMS alerts
- **Features**: Topic-based routing, message filtering, delivery retries

### Amazon EventBridge
- **Type**: Serverless event bus service
- **Pattern**: Event-driven architecture
- **Use Cases**: Application integration, SaaS integration, event routing
- **Features**: Custom event buses, schema registry, event replay

### Amazon Kinesis
- **Type**: Real-time data streaming platform
- **Pattern**: Streaming data processing
- **Use Cases**: Real-time analytics, log processing, IoT data streams
- **Features**: Sharding, checkpointing, real-time processing

### Amazon MQ
- **Type**: Managed message broker service
- **Pattern**: Traditional message brokers
- **Use Cases**: Migrating from on-premises brokers, Apache ActiveMQ/RabbitMQ compatibility
- **Features**: JMS compatibility, high availability, encryption

## Amazon SQS Implementation

### Basic SQS Setup
```python
import boto3
import json
from botocore.exceptions import ClientError

class SQSManager:
    def __init__(self, region_name='us-west-2'):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.resource = boto3.resource('sqs', region_name=region_name)
    
    def create_queue(self, queue_name, attributes=None):
        """Create an SQS queue with optional attributes"""
        try:
            if attributes is None:
                attributes = {
                    'DelaySeconds': '0',
                    'MessageRetentionPeriod': '1209600',  # 14 days
                    'VisibilityTimeoutSeconds': '60',
                    'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
                }
            
            response = self.sqs.create_queue(
                QueueName=queue_name,
                Attributes=attributes
            )
            
            queue_url = response['QueueUrl']
            print(f"Queue created: {queue_url}")
            return queue_url
            
        except ClientError as e:
            print(f"Error creating queue: {e}")
            return None
    
    def create_fifo_queue(self, queue_name):
        """Create a FIFO queue for ordered message processing"""
        fifo_queue_name = f"{queue_name}.fifo"
        attributes = {
            'FifoQueue': 'true',
            'ContentBasedDeduplication': 'true',
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '1209600',
            'VisibilityTimeoutSeconds': '60'
        }
        
        return self.create_queue(fifo_queue_name, attributes)
    
    def send_message(self, queue_url, message_body, attributes=None, group_id=None):
        """Send a message to SQS queue"""
        try:
            params = {
                'QueueUrl': queue_url,
                'MessageBody': json.dumps(message_body) if isinstance(message_body, dict) else message_body
            }
            
            if attributes:
                params['MessageAttributes'] = attributes
            
            # For FIFO queues
            if group_id:
                params['MessageGroupId'] = group_id
                params['MessageDeduplicationId'] = str(hash(json.dumps(message_body, sort_keys=True)))
            
            response = self.sqs.send_message(**params)
            print(f"Message sent. MessageId: {response['MessageId']}")
            return response['MessageId']
            
        except ClientError as e:
            print(f"Error sending message: {e}")
            return None
    
    def receive_messages(self, queue_url, max_messages=10, wait_time=20):
        """Receive messages from SQS queue"""
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=['All']
            )
            
            return response.get('Messages', [])
            
        except ClientError as e:
            print(f"Error receiving messages: {e}")
            return []
    
    def delete_message(self, queue_url, receipt_handle):
        """Delete a processed message"""
        try:
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print("Message deleted successfully")
            
        except ClientError as e:
            print(f"Error deleting message: {e}")
    
    def setup_dead_letter_queue(self, main_queue_name, dlq_name, max_receive_count=3):
        """Setup dead letter queue for failed messages"""
        # Create DLQ first
        dlq_url = self.create_queue(dlq_name)
        
        # Get DLQ ARN
        dlq_attributes = self.sqs.get_queue_attributes(
            QueueUrl=dlq_url,
            AttributeNames=['QueueArn']
        )
        dlq_arn = dlq_attributes['Attributes']['QueueArn']
        
        # Create main queue with DLQ policy
        redrive_policy = {
            'deadLetterTargetArn': dlq_arn,
            'maxReceiveCount': max_receive_count
        }
        
        attributes = {
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '1209600',
            'VisibilityTimeoutSeconds': '60',
            'RedrivePolicy': json.dumps(redrive_policy)
        }
        
        main_queue_url = self.create_queue(main_queue_name, attributes)
        
        return main_queue_url, dlq_url

# Usage example
if __name__ == "__main__":
    sqs_manager = SQSManager()
    
    # Create queue
    queue_url = sqs_manager.create_queue('order-processing-queue')
    
    # Send message
    order_data = {
        'order_id': '12345',
        'customer_id': 'cust_789',
        'items': [
            {'product_id': 'prod_1', 'quantity': 2},
            {'product_id': 'prod_2', 'quantity': 1}
        ],
        'total_amount': 89.99
    }
    
    message_id = sqs_manager.send_message(queue_url, order_data)
    
    # Receive and process messages
    messages = sqs_manager.receive_messages(queue_url)
    for message in messages:
        print(f"Processing message: {message['Body']}")
        
        # Process the message here
        order = json.loads(message['Body'])
        print(f"Processing order {order['order_id']}")
        
        # Delete message after successful processing
        sqs_manager.delete_message(queue_url, message['ReceiptHandle'])
```

### SQS with Lambda Processing
```python
import json
import boto3
import logging

# Lambda function for processing SQS messages
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Process SQS messages in Lambda"""
    
    # Initialize services
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')
    
    # Process each record
    for record in event['Records']:
        try:
            # Parse message body
            message_body = json.loads(record['body'])
            
            # Extract order information
            order_id = message_body['order_id']
            customer_id = message_body['customer_id']
            total_amount = message_body['total_amount']
            
            logger.info(f"Processing order {order_id} for customer {customer_id}")
            
            # Process order (example: save to DynamoDB)
            table = dynamodb.Table('Orders')
            table.put_item(
                Item={
                    'order_id': order_id,
                    'customer_id': customer_id,
                    'total_amount': total_amount,
                    'status': 'processing',
                    'timestamp': context.aws_request_id
                }
            )
            
            # Send notification
            sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:order-notifications',
                Message=json.dumps({
                    'order_id': order_id,
                    'status': 'processing',
                    'customer_id': customer_id
                }),
                Subject='Order Processing Started'
            )
            
            logger.info(f"Successfully processed order {order_id}")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Message will be retried or sent to DLQ based on configuration
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully processed {len(event["Records"])} messages')
    }
```

## Amazon SNS Implementation

### SNS Topic and Subscription Management
```python
import boto3
import json
from botocore.exceptions import ClientError

class SNSManager:
    def __init__(self, region_name='us-west-2'):
        self.sns = boto3.client('sns', region_name=region_name)
    
    def create_topic(self, topic_name, attributes=None):
        """Create an SNS topic"""
        try:
            if attributes is None:
                attributes = {
                    'DisplayName': topic_name,
                    'DeliveryPolicy': json.dumps({
                        'http': {
                            'defaultHealthyRetryPolicy': {
                                'minDelayTarget': 20,
                                'maxDelayTarget': 20,
                                'numRetries': 3,
                                'numMaxDelayRetries': 0,
                                'numMinDelayRetries': 0,
                                'numNoDelayRetries': 0,
                                'backoffFunction': 'linear'
                            }
                        }
                    })
                }
            
            response = self.sns.create_topic(
                Name=topic_name,
                Attributes=attributes
            )
            
            topic_arn = response['TopicArn']
            print(f"Topic created: {topic_arn}")
            return topic_arn
            
        except ClientError as e:
            print(f"Error creating topic: {e}")
            return None
    
    def subscribe_email(self, topic_arn, email_address):
        """Subscribe email to SNS topic"""
        try:
            response = self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email_address
            )
            
            subscription_arn = response['SubscriptionArn']
            print(f"Email subscription created: {subscription_arn}")
            return subscription_arn
            
        except ClientError as e:
            print(f"Error creating email subscription: {e}")
            return None
    
    def subscribe_sqs(self, topic_arn, queue_arn):
        """Subscribe SQS queue to SNS topic"""
        try:
            response = self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='sqs',
                Endpoint=queue_arn
            )
            
            subscription_arn = response['SubscriptionArn']
            print(f"SQS subscription created: {subscription_arn}")
            return subscription_arn
            
        except ClientError as e:
            print(f"Error creating SQS subscription: {e}")
            return None
    
    def subscribe_lambda(self, topic_arn, lambda_arn):
        """Subscribe Lambda function to SNS topic"""
        try:
            response = self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='lambda',
                Endpoint=lambda_arn
            )
            
            subscription_arn = response['SubscriptionArn']
            print(f"Lambda subscription created: {subscription_arn}")
            return subscription_arn
            
        except ClientError as e:
            print(f"Error creating Lambda subscription: {e}")
            return None
    
    def publish_message(self, topic_arn, message, subject=None, attributes=None):
        """Publish message to SNS topic"""
        try:
            params = {
                'TopicArn': topic_arn,
                'Message': json.dumps(message) if isinstance(message, dict) else message
            }
            
            if subject:
                params['Subject'] = subject
            
            if attributes:
                params['MessageAttributes'] = attributes
            
            response = self.sns.publish(**params)
            print(f"Message published. MessageId: {response['MessageId']}")
            return response['MessageId']
            
        except ClientError as e:
            print(f"Error publishing message: {e}")
            return None
    
    def set_subscription_filter(self, subscription_arn, filter_policy):
        """Set message filtering for subscription"""
        try:
            self.sns.set_subscription_attributes(
                SubscriptionArn=subscription_arn,
                AttributeName='FilterPolicy',
                AttributeValue=json.dumps(filter_policy)
            )
            print("Filter policy set successfully")
            
        except ClientError as e:
            print(f"Error setting filter policy: {e}")

# Usage example
if __name__ == "__main__":
    sns_manager = SNSManager()
    
    # Create topic
    topic_arn = sns_manager.create_topic('order-events')
    
    # Subscribe services
    email_sub = sns_manager.subscribe_email(topic_arn, 'admin@example.com')
    
    # Publish event
    event_data = {
        'event_type': 'order_created',
        'order_id': '12345',
        'customer_id': 'cust_789',
        'timestamp': '2024-01-01T12:00:00Z',
        'total_amount': 89.99
    }
    
    message_attributes = {
        'event_type': {
            'DataType': 'String',
            'StringValue': 'order_created'
        },
        'priority': {
            'DataType': 'String',
            'StringValue': 'high'
        }
    }
    
    sns_manager.publish_message(
        topic_arn,
        event_data,
        subject='New Order Created',
        attributes=message_attributes
    )
    
    # Set filter for high priority messages only
    filter_policy = {
        'priority': ['high', 'critical']
    }
    sns_manager.set_subscription_filter(email_sub, filter_policy)
```

## Amazon EventBridge Implementation

### EventBridge Custom Event Bus
```python
import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

class EventBridgeManager:
    def __init__(self, region_name='us-west-2'):
        self.eventbridge = boto3.client('events', region_name=region_name)
    
    def create_custom_bus(self, bus_name, description=""):
        """Create custom event bus"""
        try:
            response = self.eventbridge.create_event_bus(
                Name=bus_name,
                EventSourceName=f"custom.{bus_name}",
                Description=description
            )
            
            bus_arn = response['EventBusArn']
            print(f"Event bus created: {bus_arn}")
            return bus_arn
            
        except ClientError as e:
            print(f"Error creating event bus: {e}")
            return None
    
    def create_rule(self, rule_name, event_pattern, target_arn, bus_name=None):
        """Create EventBridge rule with event pattern"""
        try:
            params = {
                'Name': rule_name,
                'EventPattern': json.dumps(event_pattern),
                'State': 'ENABLED',
                'Description': f"Rule for {rule_name}"
            }
            
            if bus_name:
                params['EventBusName'] = bus_name
            
            response = self.eventbridge.put_rule(**params)
            rule_arn = response['RuleArn']
            
            # Add target
            self.eventbridge.put_targets(
                Rule=rule_name,
                EventBusName=bus_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': target_arn
                    }
                ]
            )
            
            print(f"Rule created: {rule_arn}")
            return rule_arn
            
        except ClientError as e:
            print(f"Error creating rule: {e}")
            return None
    
    def put_event(self, source, detail_type, detail, bus_name=None):
        """Send custom event to EventBridge"""
        try:
            entry = {
                'Source': source,
                'DetailType': detail_type,
                'Detail': json.dumps(detail) if isinstance(detail, dict) else detail,
                'Time': datetime.utcnow()
            }
            
            if bus_name:
                entry['EventBusName'] = bus_name
            
            response = self.eventbridge.put_events(
                Entries=[entry]
            )
            
            if response['FailedEntryCount'] == 0:
                print(f"Event sent successfully. EventId: {response['Entries'][0]['EventId']}")
                return response['Entries'][0]['EventId']
            else:
                print(f"Failed to send event: {response['Entries'][0]['ErrorMessage']}")
                return None
                
        except ClientError as e:
            print(f"Error sending event: {e}")
            return None
    
    def create_scheduled_rule(self, rule_name, schedule_expression, target_arn):
        """Create scheduled rule (cron/rate)"""
        try:
            # Create rule
            response = self.eventbridge.put_rule(
                Name=rule_name,
                ScheduleExpression=schedule_expression,
                State='ENABLED',
                Description=f"Scheduled rule: {rule_name}"
            )
            
            rule_arn = response['RuleArn']
            
            # Add target
            self.eventbridge.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': target_arn
                    }
                ]
            )
            
            print(f"Scheduled rule created: {rule_arn}")
            return rule_arn
            
        except ClientError as e:
            print(f"Error creating scheduled rule: {e}")
            return None

# Usage example
if __name__ == "__main__":
    eb_manager = EventBridgeManager()
    
    # Create custom event bus
    bus_arn = eb_manager.create_custom_bus('ecommerce-events', 'E-commerce application events')
    
    # Create rule for order events
    order_pattern = {
        'source': ['ecommerce.orders'],
        'detail-type': ['Order Created', 'Order Updated'],
        'detail': {
            'status': ['confirmed', 'shipped']
        }
    }
    
    lambda_arn = 'arn:aws:lambda:us-west-2:123456789012:function:process-orders'
    rule_arn = eb_manager.create_rule(
        'process-confirmed-orders',
        order_pattern,
        lambda_arn,
        'ecommerce-events'
    )
    
    # Send order event
    order_detail = {
        'order_id': '12345',
        'customer_id': 'cust_789',
        'status': 'confirmed',
        'total_amount': 89.99,
        'items': [
            {'product_id': 'prod_1', 'quantity': 2}
        ]
    }
    
    event_id = eb_manager.put_event(
        'ecommerce.orders',
        'Order Created',
        order_detail,
        'ecommerce-events'
    )
    
    # Create scheduled rule for daily reports
    daily_report_rule = eb_manager.create_scheduled_rule(
        'daily-sales-report',
        'cron(0 9 * * ? *)',  # Daily at 9 AM UTC
        'arn:aws:lambda:us-west-2:123456789012:function:generate-daily-report'
    )
```

## Terraform Infrastructure

### Complete Messaging Infrastructure
```hcl
# variables.tf
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
provider "aws" {
  region = "us-west-2"
}

# SQS Queues
resource "aws_sqs_queue" "order_processing_dlq" {
  name = "${var.application_name}-order-processing-dlq-${var.environment}"
  
  message_retention_seconds = 1209600  # 14 days
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_sqs_queue" "order_processing" {
  name = "${var.application_name}-order-processing-${var.environment}"
  
  delay_seconds             = 0
  max_message_size         = 262144
  message_retention_seconds = 1209600
  receive_wait_time_seconds = 20
  visibility_timeout_seconds = 60
  
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_processing_dlq.arn
    maxReceiveCount     = 3
  })
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_sqs_queue" "notification_queue" {
  name = "${var.application_name}-notifications-${var.environment}.fifo"
  
  fifo_queue                  = true
  content_based_deduplication = true
  delay_seconds              = 0
  message_retention_seconds  = 1209600
  visibility_timeout_seconds = 60
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# SNS Topics
resource "aws_sns_topic" "order_events" {
  name = "${var.application_name}-order-events-${var.environment}"
  
  delivery_policy = jsonencode({
    "http" : {
      "defaultHealthyRetryPolicy" : {
        "minDelayTarget" : 20,
        "maxDelayTarget" : 20,
        "numRetries" : 3,
        "numMaxDelayRetries" : 0,
        "numMinDelayRetries" : 0,
        "numNoDelayRetries" : 0,
        "backoffFunction" : "linear"
      },
      "disableSubscriptionOverrides" : false
    }
  })
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_sns_topic" "system_alerts" {
  name = "${var.application_name}-system-alerts-${var.environment}"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# SNS Subscriptions
resource "aws_sns_topic_subscription" "order_processing_subscription" {
  topic_arn = aws_sns_topic.order_events.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.order_processing.arn
  
  filter_policy = jsonencode({
    event_type = ["order_created", "order_updated"]
  })
}

resource "aws_sns_topic_subscription" "notification_subscription" {
  topic_arn = aws_sns_topic.order_events.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.notification_queue.arn
  
  filter_policy = jsonencode({
    event_type = ["order_confirmed", "order_shipped"]
  })
}

# EventBridge Custom Bus
resource "aws_cloudwatch_event_bus" "application_bus" {
  name = "${var.application_name}-events-${var.environment}"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# EventBridge Rules
resource "aws_cloudwatch_event_rule" "order_processing_rule" {
  name        = "${var.application_name}-order-processing-${var.environment}"
  description = "Route order events to processing queue"
  event_bus_name = aws_cloudwatch_event_bus.application_bus.name
  
  event_pattern = jsonencode({
    source      = ["${var.application_name}.orders"]
    detail-type = ["Order Created"]
  })
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_cloudwatch_event_target" "order_processing_target" {
  rule      = aws_cloudwatch_event_rule.order_processing_rule.name
  target_id = "OrderProcessingTarget"
  arn       = aws_sqs_queue.order_processing.arn
  event_bus_name = aws_cloudwatch_event_bus.application_bus.name
}

# IAM Policies for SQS/SNS Integration
resource "aws_sqs_queue_policy" "order_processing_policy" {
  queue_url = aws_sqs_queue.order_processing.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sns.amazonaws.com"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.order_processing.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.order_events.arn
          }
        }
      }
    ]
  })
}

resource "aws_sqs_queue_policy" "notification_queue_policy" {
  queue_url = aws_sqs_queue.notification_queue.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = ["sns.amazonaws.com", "events.amazonaws.com"]
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.notification_queue.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = [
              aws_sns_topic.order_events.arn,
              aws_cloudwatch_event_rule.order_processing_rule.arn
            ]
          }
        }
      }
    ]
  })
}

# Kinesis Data Stream
resource "aws_kinesis_stream" "order_stream" {
  name        = "${var.application_name}-order-stream-${var.environment}"
  shard_count = 2
  
  retention_period = 24
  
  shard_level_metrics = [
    "IncomingRecords",
    "OutgoingRecords"
  ]
  
  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Lambda Functions for Processing
resource "aws_lambda_function" "order_processor" {
  filename         = "order_processor.zip"
  function_name    = "${var.application_name}-order-processor-${var.environment}"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 60
  
  environment {
    variables = {
      ENVIRONMENT = var.environment
      DDB_TABLE   = aws_dynamodb_table.orders.name
      SNS_TOPIC   = aws_sns_topic.order_events.arn
    }
  }
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Lambda Event Source Mapping
resource "aws_lambda_event_source_mapping" "order_processing_mapping" {
  event_source_arn = aws_sqs_queue.order_processing.arn
  function_name    = aws_lambda_function.order_processor.arn
  batch_size       = 10
  
  depends_on = [aws_iam_role_policy_attachment.lambda_sqs_execution]
}

# DynamoDB Table
resource "aws_dynamodb_table" "orders" {
  name           = "${var.application_name}-orders-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "order_id"
  
  attribute {
    name = "order_id"
    type = "S"
  }
  
  attribute {
    name = "customer_id"
    type = "S"
  }
  
  global_secondary_index {
    name     = "CustomerIndex"
    hash_key = "customer_id"
  }
  
  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.application_name}-lambda-execution-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

resource "aws_iam_role_policy" "lambda_custom_policy" {
  name = "${var.application_name}-lambda-custom-${var.environment}"
  role = aws_iam_role.lambda_execution_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.orders.arn
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.order_events.arn
      }
    ]
  })
}

# Outputs
output "sqs_queue_urls" {
  description = "SQS Queue URLs"
  value = {
    order_processing = aws_sqs_queue.order_processing.id
    notifications    = aws_sqs_queue.notification_queue.id
  }
}

output "sns_topic_arns" {
  description = "SNS Topic ARNs"
  value = {
    order_events   = aws_sns_topic.order_events.arn
    system_alerts  = aws_sns_topic.system_alerts.arn
  }
}

output "eventbridge_bus_arn" {
  description = "EventBridge Custom Bus ARN"
  value       = aws_cloudwatch_event_bus.application_bus.arn
}

output "kinesis_stream_arn" {
  description = "Kinesis Stream ARN"
  value       = aws_kinesis_stream.order_stream.arn
}
```

## Monitoring and Observability

### CloudWatch Metrics and Alarms
```python
import boto3

def setup_messaging_monitoring():
    """Setup CloudWatch alarms for messaging services"""
    cloudwatch = boto3.client('cloudwatch')
    
    # SQS Queue Depth Alarm
    cloudwatch.put_metric_alarm(
        AlarmName='SQS-OrderProcessing-QueueDepth',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='ApproximateNumberOfVisibleMessages',
        Namespace='AWS/SQS',
        Period=300,
        Statistic='Average',
        Threshold=100.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-west-2:123456789012:system-alerts'
        ],
        AlarmDescription='Alert when SQS queue depth exceeds 100 messages',
        Dimensions=[
            {
                'Name': 'QueueName',
                'Value': 'order-processing-queue'
            }
        ]
    )
    
    # SNS Failed Messages Alarm
    cloudwatch.put_metric_alarm(
        AlarmName='SNS-OrderEvents-FailedMessages',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='NumberOfNotificationsFailed',
        Namespace='AWS/SNS',
        Period=300,
        Statistic='Sum',
        Threshold=0.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-west-2:123456789012:system-alerts'
        ],
        AlarmDescription='Alert when SNS message delivery fails',
        Dimensions=[
            {
                'Name': 'TopicName',
                'Value': 'order-events'
            }
        ]
    )
    
    # EventBridge Failed Invocations
    cloudwatch.put_metric_alarm(
        AlarmName='EventBridge-OrderProcessing-FailedInvocations',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='FailedInvocations',
        Namespace='AWS/Events',
        Period=300,
        Statistic='Sum',
        Threshold=0.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-west-2:123456789012:system-alerts'
        ],
        AlarmDescription='Alert when EventBridge rule invocations fail',
        Dimensions=[
            {
                'Name': 'RuleName',
                'Value': 'order-processing-rule'
            }
        ]
    )

if __name__ == "__main__":
    setup_messaging_monitoring()
```

## Best Practices

### Message Design Patterns
```python
# Good: Idempotent message design
{
    "message_id": "unique-id-12345",
    "timestamp": "2024-01-01T12:00:00Z",
    "event_type": "order_created",
    "version": "1.0",
    "data": {
        "order_id": "order_12345",
        "customer_id": "cust_789"
    }
}

# Good: Message correlation
{
    "correlation_id": "trace-abc123",
    "causation_id": "event-def456",
    "message_id": "msg-789012"
}

# Good: Dead letter queue handling
def process_dlq_messages():
    """Process messages from dead letter queue"""
    messages = sqs.receive_message(QueueUrl=dlq_url)
    
    for message in messages.get('Messages', []):
        # Log for analysis
        logger.error(f"DLQ Message: {message['Body']}")
        
        # Attempt reprocessing with manual intervention
        if should_retry(message):
            # Send back to main queue
            sqs.send_message(QueueUrl=main_queue_url, MessageBody=message['Body'])
        
        # Delete from DLQ
        sqs.delete_message(QueueUrl=dlq_url, ReceiptHandle=message['ReceiptHandle'])
```

### Security Best Practices
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/MessageProcessor"
      },
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage"
      ],
      "Resource": "arn:aws:sqs:us-west-2:123456789012:order-queue",
      "Condition": {
        "StringEquals": {
          "aws:SecureTransport": "true"
        }
      }
    }
  ]
}
```

## Resources

- [AWS Messaging Services Documentation](https://docs.aws.amazon.com/messaging/) - Complete AWS messaging documentation
- [Amazon SQS Developer Guide](https://docs.aws.amazon.com/sqs/) - SQS service documentation
- [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/) - SNS service documentation
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/) - EventBridge documentation
- [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/) - Kinesis streaming services
- [AWS Messaging Best Practices](https://aws.amazon.com/messaging/) - AWS messaging patterns and practices
- [Event-Driven Architecture on AWS](https://aws.amazon.com/event-driven-architecture/) - Architecture patterns guide
- [AWS Lambda with SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html) - Lambda SQS integration
- [Message Queuing Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/) - Enterprise integration patterns
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/) - Python AWS SDK documentation