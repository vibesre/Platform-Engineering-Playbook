# Amazon DynamoDB

## Overview

Amazon DynamoDB is a fully managed NoSQL database service designed for platform engineers who need single-digit millisecond performance at any scale. It provides seamless scaling, built-in security, backup and restore, and in-memory caching for internet-scale applications.

## Key Features

- **Serverless**: Fully managed with no infrastructure to manage
- **Performance at Scale**: Single-digit millisecond response times
- **Global Tables**: Multi-region, multi-active database replication
- **On-Demand Scaling**: Automatic scaling based on traffic patterns
- **Built-in Security**: Encryption at rest and in transit, VPC endpoints

## Setup and Configuration

### AWS CLI Setup
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json

# Test connection
aws dynamodb list-tables
```

### Table Creation with AWS CLI
```bash
# Create a simple table
aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1

# Create table with composite key
aws dynamodb create-table \
    --table-name Orders \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
        AttributeName=OrderId,AttributeType=S \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
        AttributeName=OrderId,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1

# Create table with Global Secondary Index
aws dynamodb create-table \
    --table-name Products \
    --attribute-definitions \
        AttributeName=ProductId,AttributeType=S \
        AttributeName=Category,AttributeType=S \
        AttributeName=Price,AttributeType=N \
    --key-schema \
        AttributeName=ProductId,KeyType=HASH \
    --global-secondary-indexes \
        'IndexName=CategoryPriceIndex,KeySchema=[{AttributeName=Category,KeyType=HASH},{AttributeName=Price,KeyType=RANGE}],Projection={ProjectionType=ALL},BillingMode=PAY_PER_REQUEST' \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### Terraform Configuration
```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

# Users table
resource "aws_dynamodb_table" "users" {
  name           = "Users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "Email"
    type = "S"
  }

  global_secondary_index {
    name     = "EmailIndex"
    hash_key = "Email"
    projection_type = "ALL"
  }

  tags = {
    Name        = "Users"
    Environment = "production"
  }
}

# Orders table with composite key
resource "aws_dynamodb_table" "orders" {
  name           = "Orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"
  range_key      = "OrderId"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "OrderId"
    type = "S"
  }

  attribute {
    name = "OrderDate"
    type = "S"
  }

  attribute {
    name = "Status"
    type = "S"
  }

  global_secondary_index {
    name     = "OrderDateIndex"
    hash_key = "UserId"
    range_key = "OrderDate"
    projection_type = "ALL"
  }

  global_secondary_index {
    name     = "StatusIndex"
    hash_key = "Status"
    range_key = "OrderDate"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "TTL"
    enabled        = true
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  tags = {
    Name        = "Orders"
    Environment = "production"
  }
}

# Products table with provisioned billing
resource "aws_dynamodb_table" "products" {
  name           = "Products"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "ProductId"

  attribute {
    name = "ProductId"
    type = "S"
  }

  attribute {
    name = "Category"
    type = "S"
  }

  attribute {
    name = "Price"
    type = "N"
  }

  global_secondary_index {
    name               = "CategoryPriceIndex"
    hash_key           = "Category"
    range_key          = "Price"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "ALL"
  }

  tags = {
    Name        = "Products"
    Environment = "production"
  }
}

# DynamoDB Global Table
resource "aws_dynamodb_global_table" "orders_global" {
  depends_on = [aws_dynamodb_table.orders]
  name       = "Orders"

  replica {
    region_name = "us-east-1"
  }

  replica {
    region_name = "us-west-2"
  }

  replica {
    region_name = "eu-west-1"
  }
}

# Output table ARNs
output "users_table_arn" {
  value = aws_dynamodb_table.users.arn
}

output "orders_table_arn" {
  value = aws_dynamodb_table.orders.arn
}

output "products_table_arn" {
  value = aws_dynamodb_table.products.arn
}
```

### CloudFormation Template
```yaml
# dynamodb-stack.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'DynamoDB tables for e-commerce application'

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    Description: Environment name for resource tagging

Resources:
  # Users table
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${EnvironmentName}-Users"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: UserId
          AttributeType: S
        - AttributeName: Email
          AttributeType: S
      KeySchema:
        - AttributeName: UserId
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: EmailIndex
          KeySchema:
            - AttributeName: Email
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Application
          Value: ecommerce

  # Orders table
  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${EnvironmentName}-Orders"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: UserId
          AttributeType: S
        - AttributeName: OrderId
          AttributeType: S
        - AttributeName: OrderDate
          AttributeType: S
        - AttributeName: Status
          AttributeType: S
      KeySchema:
        - AttributeName: UserId
          KeyType: HASH
        - AttributeName: OrderId
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: OrderDateIndex
          KeySchema:
            - AttributeName: UserId
              KeyType: HASH
            - AttributeName: OrderDate
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
        - IndexName: StatusIndex
          KeySchema:
            - AttributeName: Status
              KeyType: HASH
            - AttributeName: OrderDate
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      TimeToLiveSpecification:
        AttributeName: TTL
        Enabled: true
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Application
          Value: ecommerce

  # Products table with auto-scaling
  ProductsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${EnvironmentName}-Products"
      BillingMode: PROVISIONED
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      AttributeDefinitions:
        - AttributeName: ProductId
          AttributeType: S
        - AttributeName: Category
          AttributeType: S
        - AttributeName: Price
          AttributeType: N
      KeySchema:
        - AttributeName: ProductId
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: CategoryPriceIndex
          KeySchema:
            - AttributeName: Category
              KeyType: HASH
            - AttributeName: Price
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref EnvironmentName
        - Key: Application
          Value: ecommerce

Outputs:
  UsersTableName:
    Description: Name of the Users table
    Value: !Ref UsersTable
    Export:
      Name: !Sub "${EnvironmentName}-UsersTable"

  OrdersTableName:
    Description: Name of the Orders table
    Value: !Ref OrdersTable
    Export:
      Name: !Sub "${EnvironmentName}-OrdersTable"

  ProductsTableName:
    Description: Name of the Products table
    Value: !Ref ProductsTable
    Export:
      Name: !Sub "${EnvironmentName}-ProductsTable"
```

## Application Integration

### Python Integration with Boto3
```python
# requirements.txt
boto3==1.34.0
botocore==1.34.0

# dynamodb_client.py
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import json
from decimal import Decimal
from datetime import datetime, timedelta
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamoDBClient:
    def __init__(self, region_name='us-east-1', endpoint_url=None):
        """Initialize DynamoDB client"""
        self.region_name = region_name
        
        # For local DynamoDB development
        if endpoint_url:
            self.dynamodb = boto3.resource('dynamodb', 
                                         region_name=region_name,
                                         endpoint_url=endpoint_url)
            self.client = boto3.client('dynamodb',
                                     region_name=region_name,
                                     endpoint_url=endpoint_url)
        else:
            self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
            self.client = boto3.client('dynamodb', region_name=region_name)
    
    def get_table(self, table_name):
        """Get DynamoDB table resource"""
        return self.dynamodb.Table(table_name)
    
    def decimal_default(self, obj):
        """JSON serializer for Decimal objects"""
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

class UserRepository:
    def __init__(self, dynamodb_client, table_name='Users'):
        self.client = dynamodb_client
        self.table = self.client.get_table(table_name)
    
    def create_user(self, username, email, first_name, last_name):
        """Create a new user"""
        user_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'UserId': user_id,
            'Username': username,
            'Email': email,
            'FirstName': first_name,
            'LastName': last_name,
            'CreatedAt': timestamp,
            'UpdatedAt': timestamp,
            'IsActive': True
        }
        
        try:
            # Use condition expression to ensure email uniqueness
            self.table.put_item(
                Item=item,
                ConditionExpression=Attr('Email').not_exists()
            )
            logger.info(f"Created user: {user_id}")
            return user_id
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.error(f"User with email {email} already exists")
                raise ValueError(f"User with email {email} already exists")
            else:
                logger.error(f"Failed to create user: {e}")
                raise
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            response = self.table.get_item(Key={'UserId': user_id})
            if 'Item' in response:
                return response['Item']
            return None
        except ClientError as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email using GSI"""
        try:
            response = self.table.query(
                IndexName='EmailIndex',
                KeyConditionExpression=Key('Email').eq(email)
            )
            
            if response['Items']:
                return response['Items'][0]
            return None
        except ClientError as e:
            logger.error(f"Failed to get user by email {email}: {e}")
            return None
    
    def update_user(self, user_id, **kwargs):
        """Update user attributes"""
        update_expression = "SET UpdatedAt = :updated_at"
        expression_values = {':updated_at': datetime.utcnow().isoformat()}
        
        # Build update expression dynamically
        for key, value in kwargs.items():
            if key not in ['UserId', 'CreatedAt']:  # Skip immutable fields
                attr_name = f":{key.lower()}"
                update_expression += f", {key} = {attr_name}"
                expression_values[attr_name] = value
        
        try:
            response = self.table.update_item(
                Key={'UserId': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues='ALL_NEW'
            )
            
            logger.info(f"Updated user: {user_id}")
            return response['Attributes']
        except ClientError as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            return None
    
    def delete_user(self, user_id):
        """Soft delete user by setting IsActive to False"""
        try:
            response = self.table.update_item(
                Key={'UserId': user_id},
                UpdateExpression="SET IsActive = :active, UpdatedAt = :updated_at",
                ExpressionAttributeValues={
                    ':active': False,
                    ':updated_at': datetime.utcnow().isoformat()
                },
                ConditionExpression=Attr('UserId').exists(),
                ReturnValues='ALL_NEW'
            )
            
            logger.info(f"Deleted user: {user_id}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.error(f"User {user_id} not found")
                return False
            else:
                logger.error(f"Failed to delete user {user_id}: {e}")
                return False

class OrderRepository:
    def __init__(self, dynamodb_client, table_name='Orders'):
        self.client = dynamodb_client
        self.table = self.client.get_table(table_name)
    
    def create_order(self, user_id, items, shipping_address, total_amount):
        """Create a new order"""
        order_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Calculate TTL (30 days for completed orders)
        ttl = int((timestamp + timedelta(days=30)).timestamp())
        
        item = {
            'UserId': user_id,
            'OrderId': order_id,
            'OrderDate': timestamp.strftime('%Y-%m-%d'),
            'CreatedAt': timestamp.isoformat(),
            'Status': 'pending',
            'Items': items,
            'ShippingAddress': shipping_address,
            'TotalAmount': Decimal(str(total_amount)),
            'TTL': ttl
        }
        
        try:
            self.table.put_item(Item=item)
            logger.info(f"Created order: {order_id} for user: {user_id}")
            return order_id
        except ClientError as e:
            logger.error(f"Failed to create order: {e}")
            raise
    
    def get_order(self, user_id, order_id):
        """Get specific order"""
        try:
            response = self.table.get_item(
                Key={
                    'UserId': user_id,
                    'OrderId': order_id
                }
            )
            
            if 'Item' in response:
                return response['Item']
            return None
        except ClientError as e:
            logger.error(f"Failed to get order {order_id}: {e}")
            return None
    
    def get_user_orders(self, user_id, limit=20):
        """Get orders for a user"""
        try:
            response = self.table.query(
                KeyConditionExpression=Key('UserId').eq(user_id),
                ScanIndexForward=False,  # Sort by OrderId descending
                Limit=limit
            )
            
            return response['Items']
        except ClientError as e:
            logger.error(f"Failed to get orders for user {user_id}: {e}")
            return []
    
    def get_orders_by_date_range(self, user_id, start_date, end_date):
        """Get orders for a user within date range using GSI"""
        try:
            response = self.table.query(
                IndexName='OrderDateIndex',
                KeyConditionExpression=Key('UserId').eq(user_id) & 
                                     Key('OrderDate').between(start_date, end_date),
                ScanIndexForward=False
            )
            
            return response['Items']
        except ClientError as e:
            logger.error(f"Failed to get orders by date range: {e}")
            return []
    
    def update_order_status(self, user_id, order_id, status):
        """Update order status"""
        try:
            response = self.table.update_item(
                Key={
                    'UserId': user_id,
                    'OrderId': order_id
                },
                UpdateExpression="SET #status = :status, UpdatedAt = :updated_at",
                ExpressionAttributeNames={'#status': 'Status'},
                ExpressionAttributeValues={
                    ':status': status,
                    ':updated_at': datetime.utcnow().isoformat()
                },
                ConditionExpression=Attr('UserId').exists(),
                ReturnValues='ALL_NEW'
            )
            
            logger.info(f"Updated order {order_id} status to {status}")
            return response['Attributes']
        except ClientError as e:
            logger.error(f"Failed to update order status: {e}")
            return None
    
    def get_orders_by_status(self, status, limit=100):
        """Get orders by status using GSI"""
        try:
            response = self.table.query(
                IndexName='StatusIndex',
                KeyConditionExpression=Key('Status').eq(status),
                ScanIndexForward=False,
                Limit=limit
            )
            
            return response['Items']
        except ClientError as e:
            logger.error(f"Failed to get orders by status {status}: {e}")
            return []

class ProductRepository:
    def __init__(self, dynamodb_client, table_name='Products'):
        self.client = dynamodb_client
        self.table = self.client.get_table(table_name)
    
    def create_product(self, name, description, category, price, stock_quantity):
        """Create a new product"""
        product_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'ProductId': product_id,
            'Name': name,
            'Description': description,
            'Category': category,
            'Price': Decimal(str(price)),
            'StockQuantity': stock_quantity,
            'CreatedAt': timestamp,
            'UpdatedAt': timestamp,
            'IsActive': True
        }
        
        try:
            self.table.put_item(Item=item)
            logger.info(f"Created product: {product_id}")
            return product_id
        except ClientError as e:
            logger.error(f"Failed to create product: {e}")
            raise
    
    def get_product(self, product_id):
        """Get product by ID"""
        try:
            response = self.table.get_item(Key={'ProductId': product_id})
            if 'Item' in response:
                return response['Item']
            return None
        except ClientError as e:
            logger.error(f"Failed to get product {product_id}: {e}")
            return None
    
    def get_products_by_category(self, category, min_price=None, max_price=None, limit=50):
        """Get products by category and price range using GSI"""
        try:
            if min_price is not None and max_price is not None:
                key_condition = Key('Category').eq(category) & Key('Price').between(
                    Decimal(str(min_price)), Decimal(str(max_price))
                )
            elif min_price is not None:
                key_condition = Key('Category').eq(category) & Key('Price').gte(
                    Decimal(str(min_price))
                )
            elif max_price is not None:
                key_condition = Key('Category').eq(category) & Key('Price').lte(
                    Decimal(str(max_price))
                )
            else:
                key_condition = Key('Category').eq(category)
            
            response = self.table.query(
                IndexName='CategoryPriceIndex',
                KeyConditionExpression=key_condition,
                ScanIndexForward=True,  # Sort by price ascending
                Limit=limit
            )
            
            return response['Items']
        except ClientError as e:
            logger.error(f"Failed to get products by category {category}: {e}")
            return []
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock quantity atomically"""
        try:
            response = self.table.update_item(
                Key={'ProductId': product_id},
                UpdateExpression="ADD StockQuantity :change SET UpdatedAt = :updated_at",
                ExpressionAttributeValues={
                    ':change': quantity_change,
                    ':updated_at': datetime.utcnow().isoformat(),
                    ':zero': 0
                },
                ConditionExpression=Attr('StockQuantity').gte(Attr(':zero')) & 
                                  Attr('IsActive').eq(True),
                ReturnValues='ALL_NEW'
            )
            
            logger.info(f"Updated stock for product {product_id} by {quantity_change}")
            return response['Attributes']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                logger.error(f"Insufficient stock or inactive product: {product_id}")
                raise ValueError("Insufficient stock or inactive product")
            else:
                logger.error(f"Failed to update stock: {e}")
                raise

# Advanced features
class DynamoDBBatchOperations:
    def __init__(self, dynamodb_client):
        self.client = dynamodb_client
    
    def batch_write_items(self, table_name, items, operation='put'):
        """Batch write items to DynamoDB table"""
        table = self.client.get_table(table_name)
        
        try:
            with table.batch_writer() as batch:
                for item in items:
                    if operation == 'put':
                        batch.put_item(Item=item)
                    elif operation == 'delete':
                        batch.delete_item(Key=item)
            
            logger.info(f"Batch {operation} completed for {len(items)} items")
            return True
        except ClientError as e:
            logger.error(f"Batch {operation} failed: {e}")
            return False
    
    def batch_get_items(self, table_name, keys):
        """Batch get items from DynamoDB table"""
        try:
            response = self.client.client.batch_get_item(
                RequestItems={
                    table_name: {
                        'Keys': keys
                    }
                }
            )
            
            return response['Responses'].get(table_name, [])
        except ClientError as e:
            logger.error(f"Batch get failed: {e}")
            return []

# Usage example
if __name__ == "__main__":
    # Initialize DynamoDB client
    client = DynamoDBClient(region_name='us-east-1')
    
    # Initialize repositories
    user_repo = UserRepository(client)
    order_repo = OrderRepository(client)
    product_repo = ProductRepository(client)
    
    try:
        # Create a user
        user_id = user_repo.create_user(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Created user: {user_id}")
        
        # Get user
        user = user_repo.get_user(user_id)
        print(f"User: {user['Username']} ({user['Email']})")
        
        # Create products
        product1_id = product_repo.create_product(
            name="Laptop",
            description="High-performance laptop",
            category="Electronics",
            price=999.99,
            stock_quantity=50
        )
        
        product2_id = product_repo.create_product(
            name="Mouse",
            description="Wireless mouse",
            category="Electronics",
            price=29.99,
            stock_quantity=100
        )
        
        # Create an order
        order_items = [
            {
                'ProductId': product1_id,
                'Quantity': 1,
                'UnitPrice': Decimal('999.99')
            },
            {
                'ProductId': product2_id,
                'Quantity': 2,
                'UnitPrice': Decimal('29.99')
            }
        ]
        
        order_id = order_repo.create_order(
            user_id=user_id,
            items=order_items,
            shipping_address="123 Main St, City, State",
            total_amount=1059.97
        )
        print(f"Created order: {order_id}")
        
        # Get user orders
        orders = order_repo.get_user_orders(user_id)
        print(f"User has {len(orders)} orders")
        
        # Update order status
        updated_order = order_repo.update_order_status(user_id, order_id, "processing")
        print(f"Updated order status: {updated_order['Status']}")
        
        # Get products by category
        electronics = product_repo.get_products_by_category("Electronics")
        print(f"Found {len(electronics)} electronics products")
        
        # Update stock
        updated_product = product_repo.update_stock(product1_id, -1)
        print(f"Updated stock quantity: {updated_product['StockQuantity']}")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
```

### Node.js Integration
```javascript
// package.json dependencies
{
  "dependencies": {
    "aws-sdk": "^2.1470.0",
    "uuid": "^9.0.0"
  }
}

// dynamodb-client.js
const AWS = require('aws-sdk');
const { v4: uuidv4 } = require('uuid');

class DynamoDBClient {
  constructor(region = 'us-east-1', endpoint = null) {
    const config = { region };
    if (endpoint) {
      config.endpoint = endpoint;
    }
    
    this.dynamodb = new AWS.DynamoDB(config);
    this.docClient = new AWS.DynamoDB.DocumentClient(config);
  }

  async putItem(tableName, item) {
    const params = {
      TableName: tableName,
      Item: item
    };

    try {
      const result = await this.docClient.put(params).promise();
      return result;
    } catch (error) {
      console.error('Put item failed:', error);
      throw error;
    }
  }

  async getItem(tableName, key) {
    const params = {
      TableName: tableName,
      Key: key
    };

    try {
      const result = await this.docClient.get(params).promise();
      return result.Item;
    } catch (error) {
      console.error('Get item failed:', error);
      throw error;
    }
  }

  async queryItems(tableName, keyCondition, indexName = null, limit = null) {
    const params = {
      TableName: tableName,
      KeyConditionExpression: keyCondition.expression,
      ExpressionAttributeValues: keyCondition.values
    };

    if (indexName) {
      params.IndexName = indexName;
    }

    if (limit) {
      params.Limit = limit;
    }

    if (keyCondition.names) {
      params.ExpressionAttributeNames = keyCondition.names;
    }

    try {
      const result = await this.docClient.query(params).promise();
      return result.Items;
    } catch (error) {
      console.error('Query failed:', error);
      throw error;
    }
  }

  async updateItem(tableName, key, updateExpression, expressionValues, conditionExpression = null) {
    const params = {
      TableName: tableName,
      Key: key,
      UpdateExpression: updateExpression,
      ExpressionAttributeValues: expressionValues,
      ReturnValues: 'ALL_NEW'
    };

    if (conditionExpression) {
      params.ConditionExpression = conditionExpression;
    }

    try {
      const result = await this.docClient.update(params).promise();
      return result.Attributes;
    } catch (error) {
      console.error('Update failed:', error);
      throw error;
    }
  }

  async batchWrite(tableName, items, operation = 'put') {
    const chunks = this.chunkArray(items, 25); // DynamoDB batch limit
    
    for (const chunk of chunks) {
      const requestItems = {};
      requestItems[tableName] = chunk.map(item => {
        if (operation === 'put') {
          return { PutRequest: { Item: item } };
        } else if (operation === 'delete') {
          return { DeleteRequest: { Key: item } };
        }
      });

      const params = { RequestItems: requestItems };

      try {
        await this.docClient.batchWrite(params).promise();
      } catch (error) {
        console.error('Batch write failed:', error);
        throw error;
      }
    }
  }

  chunkArray(array, chunkSize) {
    const chunks = [];
    for (let i = 0; i < array.length; i += chunkSize) {
      chunks.push(array.slice(i, i + chunkSize));
    }
    return chunks;
  }
}

// repositories/user-repository.js
class UserRepository {
  constructor(dynamoClient, tableName = 'Users') {
    this.client = dynamoClient;
    this.tableName = tableName;
  }

  async createUser(username, email, firstName, lastName) {
    const userId = uuidv4();
    const timestamp = new Date().toISOString();

    const item = {
      UserId: userId,
      Username: username,
      Email: email,
      FirstName: firstName,
      LastName: lastName,
      CreatedAt: timestamp,
      UpdatedAt: timestamp,
      IsActive: true
    };

    try {
      await this.client.putItem(this.tableName, item);
      console.log(`Created user: ${userId}`);
      return userId;
    } catch (error) {
      console.error('Failed to create user:', error);
      throw error;
    }
  }

  async getUser(userId) {
    try {
      const user = await this.client.getItem(this.tableName, { UserId: userId });
      return user;
    } catch (error) {
      console.error('Failed to get user:', error);
      return null;
    }
  }

  async getUserByEmail(email) {
    const keyCondition = {
      expression: 'Email = :email',
      values: { ':email': email }
    };

    try {
      const users = await this.client.queryItems(this.tableName, keyCondition, 'EmailIndex');
      return users.length > 0 ? users[0] : null;
    } catch (error) {
      console.error('Failed to get user by email:', error);
      return null;
    }
  }

  async updateUser(userId, updates) {
    const updateExpression = 'SET UpdatedAt = :updatedAt';
    const expressionValues = { ':updatedAt': new Date().toISOString() };

    // Build update expression dynamically
    Object.keys(updates).forEach((key, index) => {
      if (key !== 'UserId' && key !== 'CreatedAt') {
        const valueKey = `:${key.toLowerCase()}${index}`;
        updateExpression += `, ${key} = ${valueKey}`;
        expressionValues[valueKey] = updates[key];
      }
    });

    try {
      const updatedUser = await this.client.updateItem(
        this.tableName,
        { UserId: userId },
        updateExpression,
        expressionValues
      );
      console.log(`Updated user: ${userId}`);
      return updatedUser;
    } catch (error) {
      console.error('Failed to update user:', error);
      throw error;
    }
  }

  async deleteUser(userId) {
    try {
      const updatedUser = await this.client.updateItem(
        this.tableName,
        { UserId: userId },
        'SET IsActive = :active, UpdatedAt = :updatedAt',
        {
          ':active': false,
          ':updatedAt': new Date().toISOString()
        },
        'attribute_exists(UserId)'
      );
      console.log(`Deleted user: ${userId}`);
      return true;
    } catch (error) {
      if (error.code === 'ConditionalCheckFailedException') {
        console.error(`User ${userId} not found`);
        return false;
      }
      console.error('Failed to delete user:', error);
      throw error;
    }
  }
}

// repositories/order-repository.js
class OrderRepository {
  constructor(dynamoClient, tableName = 'Orders') {
    this.client = dynamoClient;
    this.tableName = tableName;
  }

  async createOrder(userId, items, shippingAddress, totalAmount) {
    const orderId = uuidv4();
    const timestamp = new Date();
    const ttl = Math.floor((timestamp.getTime() + (30 * 24 * 60 * 60 * 1000)) / 1000); // 30 days TTL

    const item = {
      UserId: userId,
      OrderId: orderId,
      OrderDate: timestamp.toISOString().split('T')[0], // YYYY-MM-DD format
      CreatedAt: timestamp.toISOString(),
      Status: 'pending',
      Items: items,
      ShippingAddress: shippingAddress,
      TotalAmount: totalAmount,
      TTL: ttl
    };

    try {
      await this.client.putItem(this.tableName, item);
      console.log(`Created order: ${orderId} for user: ${userId}`);
      return orderId;
    } catch (error) {
      console.error('Failed to create order:', error);
      throw error;
    }
  }

  async getOrder(userId, orderId) {
    try {
      const order = await this.client.getItem(this.tableName, {
        UserId: userId,
        OrderId: orderId
      });
      return order;
    } catch (error) {
      console.error('Failed to get order:', error);
      return null;
    }
  }

  async getUserOrders(userId, limit = 20) {
    const keyCondition = {
      expression: 'UserId = :userId',
      values: { ':userId': userId }
    };

    try {
      const orders = await this.client.queryItems(this.tableName, keyCondition, null, limit);
      return orders;
    } catch (error) {
      console.error('Failed to get user orders:', error);
      return [];
    }
  }

  async getOrdersByDateRange(userId, startDate, endDate) {
    const keyCondition = {
      expression: 'UserId = :userId AND OrderDate BETWEEN :startDate AND :endDate',
      values: {
        ':userId': userId,
        ':startDate': startDate,
        ':endDate': endDate
      }
    };

    try {
      const orders = await this.client.queryItems(this.tableName, keyCondition, 'OrderDateIndex');
      return orders;
    } catch (error) {
      console.error('Failed to get orders by date range:', error);
      return [];
    }
  }

  async updateOrderStatus(userId, orderId, status) {
    try {
      const updatedOrder = await this.client.updateItem(
        this.tableName,
        { UserId: userId, OrderId: orderId },
        'SET #status = :status, UpdatedAt = :updatedAt',
        {
          ':status': status,
          ':updatedAt': new Date().toISOString()
        },
        'attribute_exists(UserId)'
      );
      console.log(`Updated order ${orderId} status to ${status}`);
      return updatedOrder;
    } catch (error) {
      console.error('Failed to update order status:', error);
      throw error;
    }
  }

  async getOrdersByStatus(status, limit = 100) {
    const keyCondition = {
      expression: '#status = :status',
      values: { ':status': status },
      names: { '#status': 'Status' }
    };

    try {
      const orders = await this.client.queryItems(this.tableName, keyCondition, 'StatusIndex', limit);
      return orders;
    } catch (error) {
      console.error('Failed to get orders by status:', error);
      return [];
    }
  }
}

// app.js - Express application
const express = require('express');
const app = express();

// Initialize DynamoDB client
const dynamoClient = new DynamoDBClient('us-east-1');

// Initialize repositories
const userRepository = new UserRepository(dynamoClient);
const orderRepository = new OrderRepository(dynamoClient);

app.use(express.json());

// User routes
app.post('/users', async (req, res) => {
  try {
    const { username, email, firstName, lastName } = req.body;
    const userId = await userRepository.createUser(username, email, firstName, lastName);
    res.status(201).json({ userId });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/users/:id', async (req, res) => {
  try {
    const user = await userRepository.getUser(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.put('/users/:id', async (req, res) => {
  try {
    const updatedUser = await userRepository.updateUser(req.params.id, req.body);
    res.json(updatedUser);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.delete('/users/:id', async (req, res) => {
  try {
    const deleted = await userRepository.deleteUser(req.params.id);
    if (!deleted) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Order routes
app.post('/orders', async (req, res) => {
  try {
    const { userId, items, shippingAddress, totalAmount } = req.body;
    const orderId = await orderRepository.createOrder(userId, items, shippingAddress, totalAmount);
    res.status(201).json({ orderId });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/users/:userId/orders', async (req, res) => {
  try {
    const { limit } = req.query;
    const orders = await orderRepository.getUserOrders(req.params.userId, parseInt(limit) || 20);
    res.json(orders);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.put('/orders/:userId/:orderId/status', async (req, res) => {
  try {
    const { status } = req.body;
    const updatedOrder = await orderRepository.updateOrderStatus(
      req.params.userId,
      req.params.orderId,
      status
    );
    res.json(updatedOrder);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = { DynamoDBClient, UserRepository, OrderRepository };
```

## Performance Optimization

### DynamoDB Accelerator (DAX)
```yaml
# dax-cluster.yaml
apiVersion: dax.aws.crossplane.io/v1alpha1
kind: Cluster
metadata:
  name: production-dax-cluster
spec:
  forProvider:
    clusterName: production-dax
    nodeType: dax.r4.large
    replicationFactor: 3
    availabilityZones:
      - us-east-1a
      - us-east-1b
      - us-east-1c
    iamRoleArn: arn:aws:iam::123456789012:role/DAXServiceRole
    subnetGroupName: dax-subnet-group
    securityGroupIds:
      - sg-12345678
    parameterGroupName: default.dax1.0
    description: "Production DAX cluster for DynamoDB caching"
    
    # Maintenance window
    preferredMaintenanceWindow: "sun:05:00-sun:06:00"
    
    # Notifications
    notificationTopicArn: arn:aws:sns:us-east-1:123456789012:dax-notifications
    
    tags:
      Environment: production
      Application: ecommerce
```

### Auto Scaling Configuration
```json
{
  "TableName": "Products",
  "BillingMode": "PROVISIONED",
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 5,
    "WriteCapacityUnits": 5
  },
  "GlobalSecondaryIndexes": [
    {
      "IndexName": "CategoryPriceIndex",
      "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
      }
    }
  ]
}
```

```bash
# Configure auto scaling for table
aws application-autoscaling register-scalable-target \
    --service-namespace dynamodb \
    --scalable-dimension dynamodb:table:ReadCapacityUnits \
    --resource-id table/Products \
    --min-capacity 5 \
    --max-capacity 4000

aws application-autoscaling register-scalable-target \
    --service-namespace dynamodb \
    --scalable-dimension dynamodb:table:WriteCapacityUnits \
    --resource-id table/Products \
    --min-capacity 5 \
    --max-capacity 4000

# Configure scaling policies
aws application-autoscaling put-scaling-policy \
    --service-namespace dynamodb \
    --scalable-dimension dynamodb:table:ReadCapacityUnits \
    --resource-id table/Products \
    --policy-name ProductsReadScalingPolicy \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration '{
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "DynamoDBReadCapacityUtilization"
        },
        "ScaleOutCooldown": 60,
        "ScaleInCooldown": 60
    }'
```

## Monitoring and Alerting

### CloudWatch Metrics
```python
# cloudwatch_monitoring.py
import boto3
from datetime import datetime, timedelta

class DynamoDBMonitoring:
    def __init__(self, region_name='us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)
        self.dynamodb = boto3.client('dynamodb', region_name=region_name)
    
    def get_table_metrics(self, table_name, start_time, end_time):
        """Get comprehensive table metrics"""
        metrics = {}
        
        # Define metrics to collect
        metric_queries = [
            ('ConsumedReadCapacityUnits', 'Sum'),
            ('ConsumedWriteCapacityUnits', 'Sum'),
            ('ProvisionedReadCapacityUnits', 'Average'),
            ('ProvisionedWriteCapacityUnits', 'Average'),
            ('ReadThrottles', 'Sum'),
            ('WriteThrottles', 'Sum'),
            ('SystemErrors', 'Sum'),
            ('UserErrors', 'Sum'),
            ('SuccessfulRequestLatency', 'Average'),
            ('ItemCount', 'Average'),
            ('TableSizeBytes', 'Average')
        ]
        
        for metric_name, statistic in metric_queries:
            try:
                response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/DynamoDB',
                    MetricName=metric_name,
                    Dimensions=[
                        {
                            'Name': 'TableName',
                            'Value': table_name
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1 hour periods
                    Statistics=[statistic]
                )
                
                metrics[metric_name] = response['Datapoints']
            except Exception as e:
                print(f"Failed to get metric {metric_name}: {e}")
        
        return metrics
    
    def create_alarms(self, table_name):
        """Create CloudWatch alarms for DynamoDB table"""
        alarms = [
            {
                'AlarmName': f'{table_name}-ReadThrottles',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 2,
                'MetricName': 'ReadThrottles',
                'Namespace': 'AWS/DynamoDB',
                'Period': 300,
                'Statistic': 'Sum',
                'Threshold': 0.0,
                'ActionsEnabled': True,
                'AlarmActions': [
                    'arn:aws:sns:us-east-1:123456789012:dynamodb-alerts'
                ],
                'AlarmDescription': f'Read throttles detected on {table_name}',
                'Dimensions': [
                    {
                        'Name': 'TableName',
                        'Value': table_name
                    }
                ],
                'Unit': 'Count'
            },
            {
                'AlarmName': f'{table_name}-WriteThrottles',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 2,
                'MetricName': 'WriteThrottles',
                'Namespace': 'AWS/DynamoDB',
                'Period': 300,
                'Statistic': 'Sum',
                'Threshold': 0.0,
                'ActionsEnabled': True,
                'AlarmActions': [
                    'arn:aws:sns:us-east-1:123456789012:dynamodb-alerts'
                ],
                'AlarmDescription': f'Write throttles detected on {table_name}',
                'Dimensions': [
                    {
                        'Name': 'TableName',
                        'Value': table_name
                    }
                ],
                'Unit': 'Count'
            },
            {
                'AlarmName': f'{table_name}-HighLatency',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 3,
                'MetricName': 'SuccessfulRequestLatency',
                'Namespace': 'AWS/DynamoDB',
                'Period': 300,
                'Statistic': 'Average',
                'Threshold': 100.0,  # 100ms
                'ActionsEnabled': True,
                'AlarmActions': [
                    'arn:aws:sns:us-east-1:123456789012:dynamodb-alerts'
                ],
                'AlarmDescription': f'High latency detected on {table_name}',
                'Dimensions': [
                    {
                        'Name': 'TableName',
                        'Value': table_name
                    }
                ],
                'Unit': 'Milliseconds'
            }
        ]
        
        for alarm in alarms:
            try:
                self.cloudwatch.put_metric_alarm(**alarm)
                print(f"Created alarm: {alarm['AlarmName']}")
            except Exception as e:
                print(f"Failed to create alarm {alarm['AlarmName']}: {e}")

# Usage
monitoring = DynamoDBMonitoring()

# Get metrics for last 24 hours
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=1)

metrics = monitoring.get_table_metrics('Users', start_time, end_time)
print("Table metrics:", metrics)

# Create alarms
monitoring.create_alarms('Users')
monitoring.create_alarms('Orders')
monitoring.create_alarms('Products')
```

## Backup and Recovery

### Point-in-Time Recovery Setup
```bash
# Enable point-in-time recovery
aws dynamodb update-continuous-backups \
    --table-name Users \
    --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true

aws dynamodb update-continuous-backups \
    --table-name Orders \
    --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true

# Check backup status
aws dynamodb describe-continuous-backups --table-name Users

# Restore table to specific point in time
aws dynamodb restore-table-to-point-in-time \
    --source-table-name Users \
    --target-table-name Users-Restored \
    --restore-date-time 2024-01-01T12:00:00Z
```

### On-Demand Backup
```bash
# Create on-demand backup
aws dynamodb create-backup \
    --table-name Users \
    --backup-name Users-Backup-$(date +%Y-%m-%d-%H-%M-%S)

# List backups
aws dynamodb list-backups --table-name Users

# Restore from backup
aws dynamodb restore-table-from-backup \
    --target-table-name Users-Restored \
    --backup-arn arn:aws:dynamodb:us-east-1:123456789012:table/Users/backup/01234567890123-abcdefgh
```

## Best Practices

- Design partition keys for even data distribution
- Use composite primary keys for flexible querying
- Implement GSIs for additional query patterns
- Use sparse indexes to save storage and costs
- Implement proper error handling and retries
- Use batch operations for bulk data operations
- Monitor and optimize for hot partitions
- Implement data archiving strategies using TTL
- Use DAX for microsecond latency requirements

## Great Resources

- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/) - Official comprehensive documentation
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/) - Detailed development guide
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html) - Design patterns and optimization
- [AWS DynamoDB Examples](https://github.com/aws-samples/aws-dynamodb-examples) - Code examples and patterns
- [DynamoDB Toolbox](https://github.com/jeremydaly/dynamodb-toolbox) - Single-table design toolkit
- [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) - Visual design tool
- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) - Change data capture
- [DynamoDB Global Tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html) - Multi-region replication