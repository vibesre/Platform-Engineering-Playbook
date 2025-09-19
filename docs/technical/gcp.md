# Google Cloud Platform (GCP)

## Overview

Google Cloud Platform (GCP) is a suite of cloud computing services offered by Google that runs on the same infrastructure Google uses internally for its end-user products. GCP provides a comprehensive set of management tools and enterprise-grade solutions that help businesses build, deploy, and scale applications, websites, and services on the same infrastructure as Google.

### Why GCP?

- **Global Infrastructure**: 35+ regions, 106+ zones, 200+ countries
- **Industry-Leading AI/ML**: TensorFlow, Vertex AI, and pre-trained APIs
- **Data Analytics**: BigQuery, Dataflow, and advanced analytics tools
- **Open Source Friendly**: Strong Kubernetes support (GKE), commitment to open standards
- **Competitive Pricing**: Sustained use discounts, per-second billing
- **Security**: Enterprise-grade security with encryption at rest and in transit

## Key Services

### Compute Services

#### Compute Engine (GCE)
Virtual machines running in Google's data centers.

```bash
# Create a VM instance
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# List all instances
gcloud compute instances list
```

#### Google Kubernetes Engine (GKE)
Managed Kubernetes service for containerized applications.

```bash
# Create a GKE cluster
gcloud container clusters create my-cluster \
  --num-nodes=3 \
  --zone=us-central1-a \
  --machine-type=e2-standard-4

# Get cluster credentials
gcloud container clusters get-credentials my-cluster --zone=us-central1-a

# Deploy an application
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0
kubectl expose deployment hello-server --type=LoadBalancer --port=8080
```

#### App Engine
Fully managed serverless platform for web applications.

```yaml
# app.yaml
runtime: python39
instance_class: F2

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

```bash
# Deploy to App Engine
gcloud app deploy

# View application
gcloud app browse
```

#### Cloud Functions
Event-driven serverless compute platform.

```python
# main.py
import functions_framework

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    name = request_json.get('name', 'World') if request_json else 'World'
    return f'Hello {name}!'
```

```bash
# Deploy function
gcloud functions deploy hello_http \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --region=us-central1
```

### Storage Services

#### Cloud Storage
Object storage for companies of all sizes.

```bash
# Create a bucket
gsutil mb -p PROJECT_ID -c STANDARD -l us-central1 gs://my-bucket/

# Upload files
gsutil cp local-file.txt gs://my-bucket/
gsutil -m cp -r local-directory gs://my-bucket/

# Set bucket lifecycle
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 30,
          "isLive": true
        }
      }
    ]
  }
}
EOF
gsutil lifecycle set lifecycle.json gs://my-bucket/
```

#### Cloud SQL
Fully managed relational database service.

```bash
# Create Cloud SQL instance
gcloud sql instances create myinstance \
  --database-version=MYSQL_8_0 \
  --tier=db-n1-standard-2 \
  --region=us-central1

# Create database
gcloud sql databases create mydatabase --instance=myinstance

# Connect to instance
gcloud sql connect myinstance --user=root
```

#### Cloud Spanner
Globally distributed, strongly consistent database.

```bash
# Create Spanner instance
gcloud spanner instances create my-spanner-instance \
  --config=regional-us-central1 \
  --nodes=1 \
  --description="My Spanner Instance"

# Create database with schema
gcloud spanner databases create my-database \
  --instance=my-spanner-instance \
  --ddl="CREATE TABLE Users (
    UserId INT64 NOT NULL,
    UserName STRING(1024)
  ) PRIMARY KEY(UserId)"
```

### Data Analytics

#### BigQuery
Serverless, highly scalable data warehouse.

```sql
-- Create dataset
CREATE SCHEMA IF NOT EXISTS my_dataset
OPTIONS(
  description="My analytics dataset",
  location="US"
);

-- Create table
CREATE OR REPLACE TABLE my_dataset.sales (
  transaction_id INT64,
  product_id INT64,
  quantity INT64,
  price NUMERIC,
  timestamp TIMESTAMP
)
PARTITION BY DATE(timestamp)
CLUSTER BY product_id;

-- Query with CTE
WITH daily_sales AS (
  SELECT 
    DATE(timestamp) as sale_date,
    SUM(quantity * price) as total_revenue,
    COUNT(DISTINCT transaction_id) as num_transactions
  FROM my_dataset.sales
  WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  GROUP BY sale_date
)
SELECT * FROM daily_sales
ORDER BY sale_date DESC;
```

```python
# Python client
from google.cloud import bigquery

client = bigquery.Client()

# Run query
query = """
    SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
"""
query_job = client.query(query)
results = query_job.result()

for row in results:
    print(f"{row.name}: {row.total}")
```

#### Dataflow
Stream and batch data processing service.

```python
# Apache Beam pipeline
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions(
    runner='DataflowRunner',
    project='my-project',
    region='us-central1',
    temp_location='gs://my-bucket/temp',
    job_name='my-dataflow-job'
)

with beam.Pipeline(options=options) as p:
    (p
     | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(topic='projects/my-project/topics/my-topic')
     | 'ParseJSON' >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
     | 'FilterEvents' >> beam.Filter(lambda x: x['event_type'] == 'purchase')
     | 'WindowInto' >> beam.WindowInto(beam.window.FixedWindows(60))
     | 'CountByProduct' >> beam.Map(lambda x: (x['product_id'], 1))
     | 'SumCounts' >> beam.CombinePerKey(sum)
     | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
         'my-project:my_dataset.product_counts',
         schema='product_id:STRING,count:INTEGER',
         write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
     ))
```

### Networking

#### Virtual Private Cloud (VPC)
Private network within GCP.

```bash
# Create custom VPC
gcloud compute networks create my-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create my-subnet \
  --network=my-vpc \
  --range=10.0.0.0/24 \
  --region=us-central1

# Create firewall rule
gcloud compute firewall-rules create allow-ssh \
  --network=my-vpc \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0
```

#### Cloud Load Balancing
Global load balancing for applications.

```bash
# Create instance template
gcloud compute instance-templates create web-server-template \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y nginx
    echo "Hello from $(hostname)" > /var/www/html/index.html'

# Create managed instance group
gcloud compute instance-groups managed create web-server-group \
  --template=web-server-template \
  --size=3 \
  --zone=us-central1-a

# Create health check
gcloud compute health-checks create http web-server-health \
  --port=80 \
  --request-path=/

# Create backend service
gcloud compute backend-services create web-backend-service \
  --protocol=HTTP \
  --health-checks=web-server-health \
  --global

# Add backend
gcloud compute backend-services add-backend web-backend-service \
  --instance-group=web-server-group \
  --instance-group-zone=us-central1-a \
  --global
```

## Infrastructure as Code

### Terraform Example

```hcl
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "${var.prefix}-vpc"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.prefix}-subnet"
  ip_cidr_range = var.subnet_cidr
  network       = google_compute_network.vpc.id
  region        = var.region
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "${var.prefix}-gke-cluster"
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

# GKE Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.prefix}-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = var.machine_type

    service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
    }

    tags = ["gke-node", "${var.prefix}-gke"]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }
}

# Service Account
resource "google_service_account" "default" {
  account_id   = "${var.prefix}-sa"
  display_name = "Service Account"
}

# Cloud Storage Bucket
resource "google_storage_bucket" "static" {
  name          = "${var.prefix}-static-assets"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "${var.prefix}_analytics"
  friendly_name               = "Analytics Dataset"
  description                 = "This is our analytics dataset"
  location                    = var.region
  default_table_expiration_ms = 3600000

  labels = {
    env = var.environment
  }
}
```

### Deployment Manager Example

```yaml
# config.yaml
imports:
- path: templates/network.py
- path: templates/compute.py

resources:
- name: my-network
  type: templates/network.py
  properties:
    region: us-central1

- name: my-instance
  type: templates/compute.py
  properties:
    zone: us-central1-a
    machineType: e2-medium
    network: $(ref.my-network.selfLink)
```

```python
# templates/network.py
def GenerateConfig(context):
    """Creates the network."""
    
    resources = [{
        'name': context.env['name'],
        'type': 'compute.v1.network',
        'properties': {
            'routingConfig': {
                'routingMode': 'REGIONAL'
            },
            'autoCreateSubnetworks': False
        }
    }, {
        'name': context.env['name'] + '-subnet',
        'type': 'compute.v1.subnetwork',
        'properties': {
            'network': '$(ref.' + context.env['name'] + '.selfLink)',
            'ipCidrRange': '10.0.0.0/24',
            'region': context.properties['region']
        }
    }]
    
    return {'resources': resources}
```

## Best Practices

### Cost Optimization

1. **Use Preemptible VMs**
   - Up to 80% cheaper than regular instances
   - Ideal for batch jobs and fault-tolerant workloads

```bash
# Create preemptible instance
gcloud compute instances create my-preemptible \
  --preemptible \
  --zone=us-central1-a \
  --machine-type=n1-standard-4
```

2. **Committed Use Discounts**
   - 1 or 3-year commitments
   - Up to 57% discount for compute
   - Up to 70% discount for memory-optimized machines

3. **Resource Monitoring**
   ```bash
   # Set up budget alerts
   gcloud billing budgets create \
     --billing-account=BILLING_ACCOUNT_ID \
     --display-name="Monthly Budget" \
     --budget-amount=1000 \
     --threshold-rule=percent=50 \
     --threshold-rule=percent=90
   ```

4. **Rightsizing Recommendations**
   - Use GCP's recommender API
   - Automatic machine type suggestions

5. **Storage Lifecycle Policies**
   ```json
   {
     "lifecycle": {
       "rule": [
         {
           "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
           "condition": {"age": 30}
         },
         {
           "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
           "condition": {"age": 90}
         }
       ]
     }
   }
   ```

### Security Best Practices

1. **Identity and Access Management (IAM)**
   ```bash
   # Create custom role
   gcloud iam roles create myCustomRole \
     --project=my-project \
     --title="My Custom Role" \
     --description="Description of my custom role" \
     --permissions=compute.instances.get,compute.instances.list

   # Grant role to user
   gcloud projects add-iam-policy-binding my-project \
     --member=user:user@example.com \
     --role=projects/my-project/roles/myCustomRole
   ```

2. **Service Account Security**
   ```bash
   # Create service account
   gcloud iam service-accounts create my-sa \
     --display-name="My Service Account"

   # Create and download key
   gcloud iam service-accounts keys create ~/key.json \
     --iam-account=my-sa@my-project.iam.gserviceaccount.com

   # Use workload identity for GKE
   kubectl annotate serviceaccount default \
     iam.gke.io/gcp-service-account=my-sa@my-project.iam.gserviceaccount.com
   ```

3. **VPC Security**
   ```bash
   # Create VPC with private Google access
   gcloud compute networks subnets create private-subnet \
     --network=my-vpc \
     --range=10.0.0.0/24 \
     --region=us-central1 \
     --enable-private-ip-google-access

   # Create Cloud NAT for outbound traffic
   gcloud compute routers create my-router \
     --network=my-vpc \
     --region=us-central1

   gcloud compute routers nats create my-nat \
     --router=my-router \
     --region=us-central1 \
     --nat-all-subnet-ip-ranges \
     --auto-allocate-nat-external-ips
   ```

4. **Encryption**
   - Encryption at rest by default
   - Customer-managed encryption keys (CMEK)
   - Cloud HSM for key management

5. **Security Command Center**
   ```bash
   # Enable Security Command Center API
   gcloud services enable securitycenter.googleapis.com

   # List findings
   gcloud scc findings list my-org \
     --source=source-id \
     --filter="state=\"ACTIVE\""
   ```

## Common Architectures

### 1. Three-Tier Web Application

```yaml
# Architecture Components:
# - Cloud Load Balancer (Global)
# - Compute Engine instances (Web tier)
# - Internal Load Balancer
# - Compute Engine instances (App tier)
# - Cloud SQL (Database tier)

# Terraform configuration
resource "google_compute_global_forwarding_rule" "default" {
  name       = "global-rule"
  target     = google_compute_target_http_proxy.default.id
  port_range = "80"
}

resource "google_compute_target_http_proxy" "default" {
  name    = "target-proxy"
  url_map = google_compute_url_map.default.id
}

resource "google_compute_url_map" "default" {
  name            = "url-map"
  default_service = google_compute_backend_service.default.id
}

resource "google_compute_backend_service" "default" {
  name        = "backend-service"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10

  backend {
    group = google_compute_instance_group_manager.web.instance_group
  }

  health_checks = [google_compute_http_health_check.default.id]
}
```

### 2. Microservices on GKE

```yaml
# microservices-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: gcr.io/my-project/frontend:v1.0
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_URL
          value: "http://backend-service:8080"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 5
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: gcr.io/my-project/backend:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: host
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - port: 8080
    targetPort: 8080
```

### 3. Data Processing Pipeline

```python
# Real-time streaming pipeline with Dataflow
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import json

class ParseEventFn(beam.DoFn):
    def process(self, element):
        try:
            event = json.loads(element.decode('utf-8'))
            yield {
                'user_id': event.get('user_id'),
                'event_type': event.get('event_type'),
                'timestamp': event.get('timestamp'),
                'properties': event.get('properties', {})
            }
        except Exception as e:
            yield beam.pvalue.TaggedOutput('errors', element)

class EnrichEventFn(beam.DoFn):
    def __init__(self, redis_host):
        self.redis_host = redis_host
        self.redis_client = None
    
    def setup(self):
        import redis
        self.redis_client = redis.Redis(host=self.redis_host)
    
    def process(self, element):
        user_profile = self.redis_client.get(f"user:{element['user_id']}")
        if user_profile:
            element['user_profile'] = json.loads(user_profile)
        yield element

# Pipeline options
options = PipelineOptions(
    runner='DataflowRunner',
    project='my-project',
    region='us-central1',
    temp_location='gs://my-bucket/temp',
    streaming=True
)

# Build pipeline
with beam.Pipeline(options=options) as pipeline:
    events = (pipeline
        | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(
            topic='projects/my-project/topics/events')
        | 'ParseEvents' >> beam.ParDo(ParseEventFn()).with_outputs(
            'errors', main='events')
    )
    
    # Process valid events
    processed = (events.events
        | 'EnrichEvents' >> beam.ParDo(EnrichEventFn('redis-host'))
        | 'WindowEvents' >> beam.WindowInto(
            beam.window.FixedWindows(60))
        | 'FormatForBQ' >> beam.Map(lambda x: {
            'user_id': x['user_id'],
            'event_type': x['event_type'],
            'timestamp': x['timestamp'],
            'user_segment': x.get('user_profile', {}).get('segment', 'unknown')
        })
    )
    
    # Write to BigQuery
    processed | 'WriteToBQ' >> beam.io.WriteToBigQuery(
        'my-project:analytics.events',
        schema='user_id:STRING,event_type:STRING,timestamp:TIMESTAMP,user_segment:STRING',
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    )
    
    # Handle errors
    events.errors | 'WriteErrors' >> beam.io.WriteToText(
        'gs://my-bucket/errors/events',
        file_name_suffix='.json'
    )
```

### 4. Serverless API

```python
# main.py - Cloud Functions
import functions_framework
from google.cloud import firestore
from google.cloud import pubsub_v1
import json

# Initialize clients
db = firestore.Client()
publisher = pubsub_v1.PublisherClient()

@functions_framework.http
def handle_order(request):
    """Process order requests."""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Parse request
        order_data = request.get_json()
        
        # Validate order
        if not all(k in order_data for k in ['user_id', 'items', 'total']):
            return ({'error': 'Missing required fields'}, 400, headers)
        
        # Store in Firestore
        order_ref = db.collection('orders').document()
        order_data['order_id'] = order_ref.id
        order_data['status'] = 'pending'
        order_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        order_ref.set(order_data)
        
        # Publish to Pub/Sub for processing
        topic_path = publisher.topic_path('my-project', 'order-processing')
        message_data = json.dumps(order_data).encode('utf-8')
        future = publisher.publish(topic_path, message_data)
        
        return ({
            'order_id': order_ref.id,
            'status': 'accepted',
            'message': 'Order is being processed'
        }, 201, headers)
        
    except Exception as e:
        return ({'error': str(e)}, 500, headers)

@functions_framework.cloud_event
def process_order(cloud_event):
    """Process orders from Pub/Sub."""
    
    # Decode message
    message = base64.b64decode(cloud_event.data['message']['data']).decode()
    order_data = json.loads(message)
    
    # Process order logic here
    # - Validate inventory
    # - Calculate shipping
    # - Process payment
    # - Update order status
    
    # Update Firestore
    order_ref = db.collection('orders').document(order_data['order_id'])
    order_ref.update({
        'status': 'processed',
        'processed_at': firestore.SERVER_TIMESTAMP
    })
```

## Monitoring and Logging

### Cloud Monitoring (Stackdriver)

```bash
# Create alerting policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High CPU Usage" \
  --condition-threshold-value=80 \
  --condition-threshold-duration=300s \
  --condition-threshold-filter='metric.type="compute.googleapis.com/instance/cpu/utilization"'
```

### Custom Metrics

```python
from google.cloud import monitoring_v3
import time

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

# Create custom metric
series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/my_app/request_count"
series.resource.type = "gce_instance"
series.resource.labels["instance_id"] = "1234567890"
series.resource.labels["zone"] = "us-central1-a"

now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)
interval = monitoring_v3.TimeInterval(
    {"end_time": {"seconds": seconds, "nanos": nanos}}
)
point = monitoring_v3.Point(
    {"interval": interval, "value": {"double_value": 123.45}}
)
series.points = [point]

client.create_time_series(name=project_name, time_series=[series])
```

### Logging

```python
from google.cloud import logging

# Setup client
logging_client = logging.Client()
logger = logging_client.logger("my-app")

# Log entries
logger.log_text("Hello, world!")
logger.log_struct({
    "message": "User action",
    "user_id": "12345",
    "action": "login",
    "metadata": {
        "ip": "192.168.1.1",
        "user_agent": "Chrome/96.0"
    }
})

# Query logs
FILTER = '''
resource.type="gce_instance"
AND severity>=WARNING
AND timestamp>="2023-01-01T00:00:00Z"
'''

for entry in logging_client.list_entries(filter_=FILTER):
    print(f"{entry.timestamp}: {entry.payload}")
```

## Interview Preparation

### Common GCP Interview Questions

1. **What is the difference between Compute Engine and App Engine?**
   - Compute Engine: IaaS, full control over VMs
   - App Engine: PaaS, fully managed, auto-scaling

2. **Explain GCP's network architecture**
   - Global VPC with regional subnets
   - Peering, VPN, Interconnect options
   - Load balancer types and their use cases

3. **How does BigQuery pricing work?**
   - Storage: $0.02/GB/month (active), $0.01/GB/month (long-term)
   - Queries: $5/TB processed (on-demand)
   - Flat-rate pricing available for consistent workloads

4. **What are the different storage classes in Cloud Storage?**
   - Standard: High-performance, frequent access
   - Nearline: 30+ days storage
   - Coldline: 90+ days storage
   - Archive: 365+ days storage

5. **How do you secure GKE clusters?**
   - Private clusters with private endpoints
   - Workload Identity for pod authentication
   - Binary Authorization for image verification
   - Network Policies for pod-to-pod communication

### Hands-On Scenarios

1. **Design a globally distributed application**
   - Multi-region deployment
   - Cloud Spanner for global consistency
   - Cloud CDN for static content
   - Traffic Director for service mesh

2. **Implement a data lake solution**
   - Cloud Storage for raw data
   - Dataproc for Spark/Hadoop processing
   - BigQuery for analytics
   - Data Catalog for metadata management

3. **Build a CI/CD pipeline**
   - Cloud Source Repositories
   - Cloud Build for builds
   - Artifact Registry for images
   - GKE for deployment

### Architecture Design Questions

**Q: Design a real-time analytics system for IoT devices**

```
Architecture:
1. IoT Core -> Pub/Sub (ingestion)
2. Dataflow -> BigQuery (processing & storage)
3. Cloud Functions (alerts/notifications)
4. Data Studio (visualization)

Considerations:
- Pub/Sub for reliable message delivery
- Dataflow for stream processing
- BigQuery partitioning for cost optimization
- Cloud Monitoring for system health
```

## Resources

### Official Documentation
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- [Google Cloud Solutions](https://cloud.google.com/solutions)
- [Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)

### Learning Resources
- [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) - Hands-on labs
- [Google Cloud Certifications](https://cloud.google.com/certification)
- [GCP Free Tier](https://cloud.google.com/free)
- [Google Cloud Codelabs](https://codelabs.developers.google.com/cloud)

### Tools and SDKs
- [Cloud SDK (gcloud)](https://cloud.google.com/sdk)
- [Cloud Shell](https://cloud.google.com/shell)
- [Cloud Code](https://cloud.google.com/code) - IDE extensions
- [Config Connector](https://cloud.google.com/config-connector/docs/overview) - K8s-native resource management

### Community Resources
- [Google Cloud Community](https://cloud.google.com/community)
- [Stack Overflow - google-cloud-platform](https://stackoverflow.com/questions/tagged/google-cloud-platform)
- [Reddit - r/googlecloud](https://www.reddit.com/r/googlecloud/)
- [Google Cloud Blog](https://cloud.google.com/blog)

### Sample Architectures
- [Cloud Architecture Center](https://cloud.google.com/architecture)
- [Reference Architectures](https://cloud.google.com/architecture/reference)
- [Design Patterns](https://cloud.google.com/architecture/design-patterns)

### Cost Management
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Cost Management Best Practices](https://cloud.google.com/architecture/framework/cost-optimization)
- [Billing Reports](https://cloud.google.com/billing/docs/reports)

### Migration Resources
- [Migration Center](https://cloud.google.com/migration-center)
- [Database Migration Service](https://cloud.google.com/database-migration)
- [Migrate for Compute Engine](https://cloud.google.com/migrate/compute-engine)

### Security Resources
- [Security Command Center](https://cloud.google.com/security-command-center)
- [Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [Compliance](https://cloud.google.com/security/compliance)

### YouTube Channels
- [Google Cloud Tech](https://www.youtube.com/googlecloudtech)
- [Google Cloud](https://www.youtube.com/googlecloud)
- [Firebase](https://www.youtube.com/firebase)