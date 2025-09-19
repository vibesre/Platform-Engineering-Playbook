# Apache CouchDB

## Overview

Apache CouchDB is a NoSQL document database that uses JSON for documents, HTTP for API, and JavaScript for MapReduce. It's designed for platform engineers who need a database that embraces the web, offering multi-master replication, conflict resolution, and eventual consistency across distributed systems.

## Key Features

- **Document-Oriented**: Store data as JSON documents with flexible schemas
- **RESTful HTTP API**: All database operations via HTTP requests
- **Multi-Master Replication**: Bidirectional replication with conflict resolution
- **MapReduce Views**: Query data using JavaScript MapReduce functions
- **ACID Compliance**: Full ACID semantics for document operations
- **Web-First Design**: Built-in web server and admin interface

## Installation

### Docker Installation
```bash
# Basic CouchDB container
docker run -d \
  --name couchdb \
  -p 5984:5984 \
  -e COUCHDB_USER=admin \
  -e COUCHDB_PASSWORD=password \
  couchdb:latest

# With persistent storage
docker run -d \
  --name couchdb \
  -p 5984:5984 \
  -e COUCHDB_USER=admin \
  -e COUCHDB_PASSWORD=password \
  -v couchdb_data:/opt/couchdb/data \
  -v couchdb_config:/opt/couchdb/etc/local.d \
  couchdb:latest

# Access Fauxton admin interface at http://localhost:5984/_utils
```

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  couchdb:
    image: couchdb:latest
    restart: always
    ports:
      - "5984:5984"
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secretpassword
      COUCHDB_SECRET: mysecret
    volumes:
      - couchdb_data:/opt/couchdb/data
      - couchdb_config:/opt/couchdb/etc/local.d
      - ./couchdb-config:/opt/couchdb/etc/local.d
    networks:
      - couchdb-network

  # CouchDB cluster setup
  couchdb1:
    image: couchdb:latest
    restart: always
    ports:
      - "5984:5984"
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secretpassword
      COUCHDB_SECRET: mysecret
      NODENAME: couchdb1@couchdb1.local
    volumes:
      - couchdb1_data:/opt/couchdb/data
    networks:
      - couchdb-network

  couchdb2:
    image: couchdb:latest
    restart: always
    ports:
      - "5985:5984"
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secretpassword
      COUCHDB_SECRET: mysecret
      NODENAME: couchdb2@couchdb2.local
    volumes:
      - couchdb2_data:/opt/couchdb/data
    networks:
      - couchdb-network

  couchdb3:
    image: couchdb:latest
    restart: always
    ports:
      - "5986:5984"
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secretpassword
      COUCHDB_SECRET: mysecret
      NODENAME: couchdb3@couchdb3.local
    volumes:
      - couchdb3_data:/opt/couchdb/data
    networks:
      - couchdb-network

volumes:
  couchdb_data:
  couchdb_config:
  couchdb1_data:
  couchdb2_data:
  couchdb3_data:

networks:
  couchdb-network:
    driver: bridge
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: couchdb-secret
  namespace: database
type: Opaque
stringData:
  adminUsername: admin
  adminPassword: secretpassword
  cookieAuthSecret: mysecret
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: couchdb-config
  namespace: database
data:
  local.ini: |
    [couchdb]
    single_node=false
    
    [cluster]
    q=2
    n=3
    
    [chttpd]
    bind_address = 0.0.0.0
    port = 5984
    
    [httpd]
    bind_address = 0.0.0.0
    port = 5986
    
    [cors]
    enable_cors = true
    origins = *
    credentials = true
    methods = GET, PUT, POST, HEAD, DELETE
    headers = accept, authorization, content-type, origin, referer, x-csrf-token
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: couchdb
  namespace: database
spec:
  serviceName: couchdb
  replicas: 3
  selector:
    matchLabels:
      app: couchdb
  template:
    metadata:
      labels:
        app: couchdb
    spec:
      containers:
      - name: couchdb
        image: couchdb:latest
        ports:
        - containerPort: 5984
          name: couchdb
        - containerPort: 5986
          name: node-local
        - containerPort: 4369
          name: epmd
        - containerPort: 9100
          name: node-comm
        env:
        - name: COUCHDB_USER
          valueFrom:
            secretKeyRef:
              name: couchdb-secret
              key: adminUsername
        - name: COUCHDB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: couchdb-secret
              key: adminPassword
        - name: COUCHDB_SECRET
          valueFrom:
            secretKeyRef:
              name: couchdb-secret
              key: cookieAuthSecret
        - name: ERL_FLAGS
          value: "-name couchdb@$(POD_NAME).couchdb.database.svc.cluster.local -setcookie $(COUCHDB_SECRET)"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        volumeMounts:
        - name: couchdb-data
          mountPath: /opt/couchdb/data
        - name: couchdb-config
          mountPath: /opt/couchdb/etc/local.d/local.ini
          subPath: local.ini
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /
            port: 5984
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_up
            port: 5984
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: couchdb-config
        configMap:
          name: couchdb-config
  volumeClaimTemplates:
  - metadata:
      name: couchdb-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
---
apiVersion: v1
kind: Service
metadata:
  name: couchdb
  namespace: database
spec:
  selector:
    app: couchdb
  ports:
  - port: 5984
    targetPort: 5984
    name: couchdb
  - port: 5986
    targetPort: 5986
    name: node-local
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: couchdb-headless
  namespace: database
spec:
  selector:
    app: couchdb
  ports:
  - port: 5984
    targetPort: 5984
    name: couchdb
  - port: 5986
    targetPort: 5986
    name: node-local
  - port: 4369
    targetPort: 4369
    name: epmd
  - port: 9100
    targetPort: 9100
    name: node-comm
  clusterIP: None
```

## Database Operations

### Basic HTTP API Usage
```bash
# Check server status
curl -X GET http://admin:password@localhost:5984/

# Create database
curl -X PUT http://admin:password@localhost:5984/ecommerce

# Get database info
curl -X GET http://admin:password@localhost:5984/ecommerce

# Create document
curl -X POST http://admin:password@localhost:5984/ecommerce \
  -H "Content-Type: application/json" \
  -d '{
    "type": "user",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }'

# Get document
curl -X GET http://admin:password@localhost:5984/ecommerce/document_id

# Update document
curl -X PUT http://admin:password@localhost:5984/ecommerce/document_id \
  -H "Content-Type: application/json" \
  -d '{
    "_id": "document_id",
    "_rev": "1-revision_hash",
    "type": "user",
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "updated_at": "2024-01-02T00:00:00Z"
  }'

# Delete document
curl -X DELETE http://admin:password@localhost:5984/ecommerce/document_id?rev=revision_hash

# Bulk operations
curl -X POST http://admin:password@localhost:5984/ecommerce/_bulk_docs \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      {
        "type": "product",
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics"
      },
      {
        "type": "product",
        "name": "Mouse",
        "price": 29.99,
        "category": "Electronics"
      }
    ]
  }'
```

### Views and Indexes
```javascript
// Create design document with views
curl -X PUT http://admin:password@localhost:5984/ecommerce/_design/users \
  -H "Content-Type: application/json" \
  -d '{
    "views": {
      "by_email": {
        "map": "function(doc) { if (doc.type === \"user\" && doc.email) { emit(doc.email, doc); } }"
      },
      "by_created_date": {
        "map": "function(doc) { if (doc.type === \"user\" && doc.created_at) { emit(doc.created_at, doc); } }"
      },
      "active_users": {
        "map": "function(doc) { if (doc.type === \"user\" && doc.is_active !== false) { emit(doc._id, doc); } }"
      }
    }
  }'

// Create products view with reduce function
curl -X PUT http://admin:password@localhost:5984/ecommerce/_design/products \
  -H "Content-Type: application/json" \
  -d '{
    "views": {
      "by_category": {
        "map": "function(doc) { if (doc.type === \"product\" && doc.category) { emit(doc.category, doc); } }"
      },
      "by_price_range": {
        "map": "function(doc) { if (doc.type === \"product\" && doc.price) { emit(Math.floor(doc.price / 100) * 100, doc); } }"
      },
      "category_stats": {
        "map": "function(doc) { if (doc.type === \"product\" && doc.category) { emit(doc.category, doc.price); } }",
        "reduce": "function(keys, values, rereduce) { if (rereduce) { var result = { sum: 0, count: 0, min: null, max: null }; for (var i = 0; i < values.length; i++) { result.sum += values[i].sum; result.count += values[i].count; result.min = result.min === null ? values[i].min : Math.min(result.min, values[i].min); result.max = result.max === null ? values[i].max : Math.max(result.max, values[i].max); } return result; } else { return { sum: values.reduce(function(a, b) { return a + b; }, 0), count: values.length, min: Math.min.apply(null, values), max: Math.max.apply(null, values) }; } }"
      }
    }
  }'

// Query views
curl -X GET "http://admin:password@localhost:5984/ecommerce/_design/users/_view/by_email?key=\"john@example.com\""

curl -X GET "http://admin:password@localhost:5984/ecommerce/_design/products/_view/by_category?key=\"Electronics\""

curl -X GET "http://admin:password@localhost:5984/ecommerce/_design/products/_view/category_stats?group=true"
```

## Application Integration

### Python Integration
```python
# requirements.txt
requests==2.31.0
couchdb==1.2

# couchdb_client.py
import requests
import json
import uuid
from datetime import datetime
from urllib.parse import quote
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CouchDBClient:
    def __init__(self, host='localhost', port=5984, username=None, password=None, use_ssl=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        
        protocol = 'https' if use_ssl else 'http'
        self.base_url = f"{protocol}://{host}:{port}"
        
        # Setup authentication
        self.auth = None
        if username and password:
            self.auth = (username, password)
        
        self.session = requests.Session()
        if self.auth:
            self.session.auth = self.auth
    
    def server_info(self):
        """Get server information"""
        try:
            response = self.session.get(f"{self.base_url}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get server info: {e}")
            raise
    
    def create_database(self, db_name):
        """Create a database"""
        try:
            response = self.session.put(f"{self.base_url}/{db_name}")
            response.raise_for_status()
            logger.info(f"Created database: {db_name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 412:
                logger.info(f"Database {db_name} already exists")
                return {"ok": True}
            logger.error(f"Failed to create database {db_name}: {e}")
            raise
    
    def delete_database(self, db_name):
        """Delete a database"""
        try:
            response = self.session.delete(f"{self.base_url}/{db_name}")
            response.raise_for_status()
            logger.info(f"Deleted database: {db_name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete database {db_name}: {e}")
            raise
    
    def database_info(self, db_name):
        """Get database information"""
        try:
            response = self.session.get(f"{self.base_url}/{db_name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get database info for {db_name}: {e}")
            raise

class CouchDBDatabase:
    def __init__(self, client, db_name):
        self.client = client
        self.db_name = db_name
        self.url = f"{client.base_url}/{db_name}"
    
    def create_document(self, doc, doc_id=None):
        """Create a document"""
        if doc_id:
            # PUT with specific ID
            try:
                response = self.client.session.put(
                    f"{self.url}/{doc_id}",
                    json=doc,
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Created document with ID: {result['id']}")
                return result
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to create document: {e}")
                raise
        else:
            # POST for auto-generated ID
            try:
                response = self.client.session.post(
                    self.url,
                    json=doc,
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Created document with ID: {result['id']}")
                return result
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to create document: {e}")
                raise
    
    def get_document(self, doc_id):
        """Get a document by ID"""
        try:
            response = self.client.session.get(f"{self.url}/{doc_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                return None
            logger.error(f"Failed to get document {doc_id}: {e}")
            raise
    
    def update_document(self, doc):
        """Update a document"""
        if '_id' not in doc or '_rev' not in doc:
            raise ValueError("Document must have _id and _rev for updates")
        
        try:
            response = self.client.session.put(
                f"{self.url}/{doc['_id']}",
                json=doc,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Updated document: {result['id']}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update document: {e}")
            raise
    
    def delete_document(self, doc_id, rev):
        """Delete a document"""
        try:
            response = self.client.session.delete(f"{self.url}/{doc_id}?rev={rev}")
            response.raise_for_status()
            result = response.json()
            logger.info(f"Deleted document: {result['id']}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")
            raise
    
    def bulk_docs(self, docs):
        """Bulk document operations"""
        try:
            response = self.client.session.post(
                f"{self.url}/_bulk_docs",
                json={"docs": docs},
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Bulk operation completed for {len(docs)} documents")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Bulk operation failed: {e}")
            raise
    
    def query_view(self, design_doc, view_name, **params):
        """Query a view"""
        try:
            # Encode parameters
            query_params = []
            for key, value in params.items():
                if isinstance(value, (dict, list)):
                    query_params.append(f"{key}={quote(json.dumps(value))}")
                elif isinstance(value, bool):
                    query_params.append(f"{key}={str(value).lower()}")
                else:
                    query_params.append(f"{key}={quote(str(value))}")
            
            query_string = "&".join(query_params)
            url = f"{self.url}/_design/{design_doc}/_view/{view_name}"
            if query_string:
                url += f"?{query_string}"
            
            response = self.client.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"View query failed: {e}")
            raise
    
    def create_index(self, index_def, design_doc=None):
        """Create an index (Mango index)"""
        try:
            response = self.client.session.post(
                f"{self.url}/_index",
                json=index_def,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Created index: {result.get('id', 'unknown')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create index: {e}")
            raise
    
    def find_documents(self, selector, **options):
        """Find documents using Mango queries"""
        query = {"selector": selector}
        query.update(options)
        
        try:
            response = self.client.session.post(
                f"{self.url}/_find",
                json=query,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Find query failed: {e}")
            raise

# Repository classes
class UserRepository:
    def __init__(self, database):
        self.db = database
        self.doc_type = "user"
    
    def create_user(self, username, email, first_name, last_name):
        """Create a new user"""
        user_doc = {
            "_id": str(uuid.uuid4()),
            "type": self.doc_type,
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = self.db.create_document(user_doc, user_doc["_id"])
        return result["id"]
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.db.get_document(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email using view"""
        result = self.db.query_view("users", "by_email", key=email)
        if result["rows"]:
            return result["rows"][0]["value"]
        return None
    
    def update_user(self, user_id, **updates):
        """Update user"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Update fields
        for key, value in updates.items():
            if key not in ["_id", "_rev", "type", "created_at"]:
                user[key] = value
        
        user["updated_at"] = datetime.utcnow().isoformat()
        
        result = self.db.update_document(user)
        return self.get_user(user_id)
    
    def delete_user(self, user_id):
        """Soft delete user"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        user["is_active"] = False
        user["deleted_at"] = datetime.utcnow().isoformat()
        
        self.db.update_document(user)
        return True
    
    def get_active_users(self, limit=50, skip=0):
        """Get active users"""
        result = self.db.query_view("users", "active_users", limit=limit, skip=skip)
        return [row["value"] for row in result["rows"]]

class ProductRepository:
    def __init__(self, database):
        self.db = database
        self.doc_type = "product"
    
    def create_product(self, name, description, category, price, stock_quantity):
        """Create a new product"""
        product_doc = {
            "_id": str(uuid.uuid4()),
            "type": self.doc_type,
            "name": name,
            "description": description,
            "category": category,
            "price": price,
            "stock_quantity": stock_quantity,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = self.db.create_document(product_doc, product_doc["_id"])
        return result["id"]
    
    def get_product(self, product_id):
        """Get product by ID"""
        return self.db.get_document(product_id)
    
    def get_products_by_category(self, category, limit=50):
        """Get products by category"""
        result = self.db.query_view("products", "by_category", key=category, limit=limit)
        return [row["value"] for row in result["rows"]]
    
    def search_products(self, query_text, limit=20):
        """Search products using Mango query"""
        selector = {
            "type": self.doc_type,
            "is_active": True,
            "$or": [
                {"name": {"$regex": f"(?i).*{query_text}.*"}},
                {"description": {"$regex": f"(?i).*{query_text}.*"}},
                {"category": {"$regex": f"(?i).*{query_text}.*"}}
            ]
        }
        
        result = self.db.find_documents(selector, limit=limit)
        return result["docs"]
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock"""
        product = self.get_product(product_id)
        if not product:
            return None
        
        new_stock = product["stock_quantity"] + quantity_change
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        
        product["stock_quantity"] = new_stock
        product["updated_at"] = datetime.utcnow().isoformat()
        
        self.db.update_document(product)
        return self.get_product(product_id)

# Usage example
if __name__ == "__main__":
    # Initialize client and database
    client = CouchDBClient(username="admin", password="password")
    client.create_database("ecommerce")
    db = CouchDBDatabase(client, "ecommerce")
    
    # Create design documents with views
    users_design = {
        "_id": "_design/users",
        "views": {
            "by_email": {
                "map": "function(doc) { if (doc.type === 'user' && doc.email) { emit(doc.email, doc); } }"
            },
            "active_users": {
                "map": "function(doc) { if (doc.type === 'user' && doc.is_active !== false) { emit(doc._id, doc); } }"
            }
        }
    }
    
    products_design = {
        "_id": "_design/products",
        "views": {
            "by_category": {
                "map": "function(doc) { if (doc.type === 'product' && doc.category) { emit(doc.category, doc); } }"
            }
        }
    }
    
    db.create_document(users_design, "_design/users")
    db.create_document(products_design, "_design/products")
    
    # Create indexes for Mango queries
    db.create_index({
        "index": {"fields": ["type", "name"]},
        "name": "product-name-index"
    })
    
    # Initialize repositories
    user_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    
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
        print(f"User: {user['username']} ({user['email']})")
        
        # Create products
        laptop_id = product_repo.create_product(
            name="Gaming Laptop",
            description="High-performance gaming laptop",
            category="Electronics",
            price=1299.99,
            stock_quantity=25
        )
        
        mouse_id = product_repo.create_product(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse",
            category="Electronics",
            price=49.99,
            stock_quantity=100
        )
        
        print(f"Created products: {laptop_id}, {mouse_id}")
        
        # Search products
        electronics = product_repo.get_products_by_category("Electronics")
        print(f"Found {len(electronics)} electronics products")
        
        # Search by text
        search_results = product_repo.search_products("laptop")
        print(f"Search results: {len(search_results)} products")
        
        # Update stock
        updated_product = product_repo.update_stock(laptop_id, -1)
        print(f"Updated stock: {updated_product['stock_quantity']}")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
```

### Node.js Integration
```javascript
// package.json dependencies
{
  "dependencies": {
    "nano": "^10.1.2",
    "uuid": "^9.0.0"
  }
}

// couchdb-client.js
const nano = require('nano');
const { v4: uuidv4 } = require('uuid');

class CouchDBClient {
  constructor(url, username, password) {
    this.url = url;
    this.nano = nano({
      url: url,
      requestDefaults: {
        auth: {
          username: username,
          password: password
        }
      }
    });
  }

  async createDatabase(dbName) {
    try {
      const result = await this.nano.db.create(dbName);
      console.log(`Created database: ${dbName}`);
      return result;
    } catch (error) {
      if (error.statusCode === 412) {
        console.log(`Database ${dbName} already exists`);
        return { ok: true };
      }
      throw error;
    }
  }

  async deleteDatabase(dbName) {
    try {
      const result = await this.nano.db.destroy(dbName);
      console.log(`Deleted database: ${dbName}`);
      return result;
    } catch (error) {
      console.error(`Failed to delete database ${dbName}:`, error);
      throw error;
    }
  }

  getDatabase(dbName) {
    return this.nano.use(dbName);
  }

  async getDatabaseInfo(dbName) {
    try {
      const db = this.getDatabase(dbName);
      return await db.info();
    } catch (error) {
      console.error(`Failed to get database info for ${dbName}:`, error);
      throw error;
    }
  }
}

// repositories/user-repository.js
class UserRepository {
  constructor(database) {
    this.db = database;
    this.docType = 'user';
  }

  async createUser(username, email, firstName, lastName) {
    const userId = uuidv4();
    const userDoc = {
      _id: userId,
      type: this.docType,
      username,
      email,
      firstName,
      lastName,
      isActive: true,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    try {
      const result = await this.db.insert(userDoc);
      console.log(`Created user: ${result.id}`);
      return result.id;
    } catch (error) {
      console.error('Failed to create user:', error);
      throw error;
    }
  }

  async getUser(userId) {
    try {
      const user = await this.db.get(userId);
      return user;
    } catch (error) {
      if (error.statusCode === 404) {
        return null;
      }
      console.error('Failed to get user:', error);
      throw error;
    }
  }

  async getUserByEmail(email) {
    try {
      const result = await this.db.view('users', 'by_email', {
        key: email,
        include_docs: true
      });
      
      if (result.rows.length > 0) {
        return result.rows[0].doc;
      }
      return null;
    } catch (error) {
      console.error('Failed to get user by email:', error);
      throw error;
    }
  }

  async updateUser(userId, updates) {
    try {
      const user = await this.getUser(userId);
      if (!user) {
        return null;
      }

      // Apply updates
      Object.keys(updates).forEach(key => {
        if (key !== '_id' && key !== '_rev' && key !== 'type' && key !== 'createdAt') {
          user[key] = updates[key];
        }
      });

      user.updatedAt = new Date().toISOString();

      const result = await this.db.insert(user);
      console.log(`Updated user: ${result.id}`);
      
      return await this.getUser(userId);
    } catch (error) {
      console.error('Failed to update user:', error);
      throw error;
    }
  }

  async deleteUser(userId) {
    try {
      const user = await this.getUser(userId);
      if (!user) {
        return false;
      }

      user.isActive = false;
      user.deletedAt = new Date().toISOString();

      await this.db.insert(user);
      console.log(`Deleted user: ${userId}`);
      return true;
    } catch (error) {
      console.error('Failed to delete user:', error);
      throw error;
    }
  }

  async getActiveUsers(limit = 50, skip = 0) {
    try {
      const result = await this.db.view('users', 'active_users', {
        limit,
        skip,
        include_docs: true
      });
      
      return result.rows.map(row => row.doc);
    } catch (error) {
      console.error('Failed to get active users:', error);
      throw error;
    }
  }
}

// repositories/product-repository.js
class ProductRepository {
  constructor(database) {
    this.db = database;
    this.docType = 'product';
  }

  async createProduct(name, description, category, price, stockQuantity) {
    const productId = uuidv4();
    const productDoc = {
      _id: productId,
      type: this.docType,
      name,
      description,
      category,
      price,
      stockQuantity,
      isActive: true,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    try {
      const result = await this.db.insert(productDoc);
      console.log(`Created product: ${result.id}`);
      return result.id;
    } catch (error) {
      console.error('Failed to create product:', error);
      throw error;
    }
  }

  async getProduct(productId) {
    try {
      const product = await this.db.get(productId);
      return product;
    } catch (error) {
      if (error.statusCode === 404) {
        return null;
      }
      console.error('Failed to get product:', error);
      throw error;
    }
  }

  async getProductsByCategory(category, limit = 50) {
    try {
      const result = await this.db.view('products', 'by_category', {
        key: category,
        limit,
        include_docs: true
      });
      
      return result.rows.map(row => row.doc);
    } catch (error) {
      console.error('Failed to get products by category:', error);
      throw error;
    }
  }

  async searchProducts(queryText, limit = 20) {
    try {
      const selector = {
        type: this.docType,
        isActive: true,
        $or: [
          { name: { $regex: `(?i).*${queryText}.*` } },
          { description: { $regex: `(?i).*${queryText}.*` } },
          { category: { $regex: `(?i).*${queryText}.*` } }
        ]
      };

      const result = await this.db.find({
        selector,
        limit
      });

      return result.docs;
    } catch (error) {
      console.error('Failed to search products:', error);
      throw error;
    }
  }

  async updateStock(productId, quantityChange) {
    try {
      const product = await this.getProduct(productId);
      if (!product) {
        return null;
      }

      const newStock = product.stockQuantity + quantityChange;
      if (newStock < 0) {
        throw new Error('Insufficient stock');
      }

      product.stockQuantity = newStock;
      product.updatedAt = new Date().toISOString();

      const result = await this.db.insert(product);
      console.log(`Updated stock for product: ${result.id}`);
      
      return await this.getProduct(productId);
    } catch (error) {
      console.error('Failed to update stock:', error);
      throw error;
    }
  }

  async bulkCreateProducts(products) {
    try {
      const docs = products.map(product => ({
        _id: uuidv4(),
        type: this.docType,
        ...product,
        isActive: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }));

      const result = await this.db.bulk({ docs });
      console.log(`Bulk created ${docs.length} products`);
      return result;
    } catch (error) {
      console.error('Failed to bulk create products:', error);
      throw error;
    }
  }
}

// app.js - Express application
const express = require('express');
const app = express();

// Initialize CouchDB client
const couchClient = new CouchDBClient(
  'http://localhost:5984',
  'admin',
  'password'
);

async function initializeDatabase() {
  // Create database
  await couchClient.createDatabase('ecommerce');
  
  const db = couchClient.getDatabase('ecommerce');
  
  // Create design documents
  const usersDesign = {
    _id: '_design/users',
    views: {
      by_email: {
        map: function(doc) {
          if (doc.type === 'user' && doc.email) {
            emit(doc.email, doc);
          }
        }.toString()
      },
      active_users: {
        map: function(doc) {
          if (doc.type === 'user' && doc.isActive !== false) {
            emit(doc._id, doc);
          }
        }.toString()
      }
    }
  };

  const productsDesign = {
    _id: '_design/products',
    views: {
      by_category: {
        map: function(doc) {
          if (doc.type === 'product' && doc.category) {
            emit(doc.category, doc);
          }
        }.toString()
      }
    }
  };

  try {
    await db.insert(usersDesign);
    await db.insert(productsDesign);
    console.log('Design documents created');
  } catch (error) {
    if (error.statusCode !== 409) { // 409 = conflict (already exists)
      throw error;
    }
  }

  // Create indexes
  await db.createIndex({
    index: { fields: ['type', 'name'] },
    name: 'product-name-index'
  });

  return db;
}

// Initialize database and repositories
let userRepository, productRepository;

initializeDatabase().then(db => {
  userRepository = new UserRepository(db);
  productRepository = new ProductRepository(db);
  console.log('Database initialized');
}).catch(error => {
  console.error('Failed to initialize database:', error);
  process.exit(1);
});

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
    if (!updatedUser) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(updatedUser);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Product routes
app.post('/products', async (req, res) => {
  try {
    const { name, description, category, price, stockQuantity } = req.body;
    const productId = await productRepository.createProduct(name, description, category, price, stockQuantity);
    res.status(201).json({ productId });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/products/search', async (req, res) => {
  try {
    const { q, limit } = req.query;
    const products = await productRepository.searchProducts(q, parseInt(limit) || 20);
    res.json(products);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/products/category/:category', async (req, res) => {
  try {
    const { limit } = req.query;
    const products = await productRepository.getProductsByCategory(
      req.params.category,
      parseInt(limit) || 50
    );
    res.json(products);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = { CouchDBClient, UserRepository, ProductRepository };
```

## Replication and Clustering

### Setting up Replication
```bash
# Create replication between databases
curl -X POST http://admin:password@localhost:5984/_replicator \
  -H "Content-Type: application/json" \
  -d '{
    "_id": "ecommerce-replication",
    "source": "http://admin:password@source-server:5984/ecommerce",
    "target": "http://admin:password@target-server:5984/ecommerce",
    "continuous": true,
    "create_target": true,
    "owner": "admin"
  }'

# Check replication status
curl -X GET http://admin:password@localhost:5984/_replicator/ecommerce-replication

# Stop replication
curl -X DELETE http://admin:password@localhost:5984/_replicator/ecommerce-replication?rev=revision
```

### Cluster Configuration
```bash
# Setup cluster nodes (run on each node)
curl -X PUT http://admin:password@node1:5984/_node/_local/_config/cluster/n -d '"3"'
curl -X PUT http://admin:password@node1:5984/_node/_local/_config/cluster/q -d '"2"'

# Enable cluster
curl -X POST http://admin:password@node1:5984/_cluster_setup \
  -H "Content-Type: application/json" \
  -d '{
    "action": "enable_cluster",
    "bind_address": "0.0.0.0",
    "username": "admin",
    "password": "password",
    "port": 5984,
    "node_count": 3,
    "remote_node": "node2",
    "remote_current_user": "admin",
    "remote_current_password": "password"
  }'

# Add node to cluster
curl -X POST http://admin:password@node1:5984/_cluster_setup \
  -H "Content-Type: application/json" \
  -d '{
    "action": "add_node",
    "host": "node2",
    "port": 5984,
    "username": "admin",
    "password": "password"
  }'

# Finish cluster setup
curl -X POST http://admin:password@node1:5984/_cluster_setup \
  -H "Content-Type: application/json" \
  -d '{"action": "finish_cluster"}'

# Check cluster status
curl -X GET http://admin:password@node1:5984/_membership
```

## Monitoring and Performance

### Monitoring Metrics
```bash
# Get server statistics
curl -X GET http://admin:password@localhost:5984/_stats

# Get active tasks
curl -X GET http://admin:password@localhost:5984/_active_tasks

# Database compaction
curl -X POST http://admin:password@localhost:5984/ecommerce/_compact

# View compaction
curl -X POST http://admin:password@localhost:5984/ecommerce/_compact/users

# Check database info
curl -X GET http://admin:password@localhost:5984/ecommerce
```

### Performance Configuration
```ini
# local.ini configuration optimizations
[couchdb]
max_document_size = 67108864  ; 64MB
max_attachment_chunk_size = 4294967296  ; 4GB

[chttpd]
max_http_request_size = 67108864  ; 64MB
enable_cors = true

[compactions]
_default = [{db_fragmentation, "70%"}, {view_fragmentation, "60%"}, {from, "23:00"}, {to, "04:00"}]

[smoosh]
min_file_size = 1048576  ; 1MB

[ioq]
concurrency = 10
ratio = 0.01

[fabric]
request_timeout = 60000
all_docs_concurrency = 10
changes_duration = 60000

[rexi]
server_per_node = true
```

## Backup and Recovery

### Backup Script
```bash
#!/bin/bash
# couchdb-backup.sh

COUCH_HOST="localhost"
COUCH_PORT="5984"
COUCH_USER="admin"
COUCH_PASS="password"
BACKUP_DIR="/backups/couchdb"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p ${BACKUP_DIR}/${DATE}

# Function to backup database
backup_database() {
    local db_name=$1
    local backup_file="${BACKUP_DIR}/${DATE}/${db_name}.json"
    
    echo "Backing up database: ${db_name}"
    
    # Get all documents with _all_docs
    curl -s -X GET "http://${COUCH_USER}:${COUCH_PASS}@${COUCH_HOST}:${COUCH_PORT}/${db_name}/_all_docs?include_docs=true" \
        | jq '.rows[].doc' > ${backup_file}
    
    if [ $? -eq 0 ]; then
        echo "Backup completed: ${backup_file}"
        gzip ${backup_file}
    else
        echo "Backup failed for database: ${db_name}"
    fi
}

# Get list of databases
databases=$(curl -s -X GET "http://${COUCH_USER}:${COUCH_PASS}@${COUCH_HOST}:${COUCH_PORT}/_all_dbs" | jq -r '.[]' | grep -v '^_')

# Backup each database
for db in ${databases}; do
    backup_database ${db}
done

echo "Backup process completed"
```

## Best Practices

- Design documents to minimize conflicts in multi-master scenarios
- Use appropriate view indexing strategies for query patterns
- Implement proper conflict resolution for replicated databases
- Use bulk operations for better performance
- Monitor database fragmentation and run compaction regularly
- Implement proper authentication and authorization
- Use SSL/TLS for production deployments
- Regular backup and disaster recovery testing
- Monitor replication lag in distributed setups

## Great Resources

- [CouchDB Documentation](https://docs.couchdb.org/) - Official comprehensive documentation
- [CouchDB Guide](https://guide.couchdb.org/) - Comprehensive guide to CouchDB
- [Fauxton](https://couchdb.apache.org/fauxton-visual-guide/) - Web-based admin interface guide
- [CouchDB Replication](https://docs.couchdb.org/en/stable/replication/) - Replication and clustering guide
- [CouchDB GitHub](https://github.com/apache/couchdb) - Source code and community
- [CouchDB Mango](https://docs.couchdb.org/en/stable/api/database/find.html) - Mango query language
- [PouchDB](https://pouchdb.com/) - JavaScript client library for CouchDB
- [CouchDB Best Practices](https://blog.couchdb.org/) - Official blog with best practices