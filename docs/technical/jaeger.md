# Jaeger

## Overview

Jaeger is an open-source distributed tracing platform that helps monitor and troubleshoot microservices-based distributed systems. It provides visibility into request flows across multiple services, helping identify performance bottlenecks and failures.

## Key Features

- **Distributed Tracing**: Track requests across multiple services
- **Performance Monitoring**: Identify latency and performance issues
- **Root Cause Analysis**: Quickly identify failing services and components
- **Service Dependencies**: Visualize service topology and dependencies
- **Scalable Architecture**: Handle high-throughput production environments

## Common Use Cases

### Basic Deployment with Docker
```bash
# Run Jaeger all-in-one for development
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14268:14268 \
  jaegertracing/all-in-one:latest

# Access Jaeger UI at http://localhost:16686
```

### Application Instrumentation (Python)
```python
from jaeger_client import Config
from opentracing.ext import tags
from opentracing.propagation import Format
import opentracing

# Initialize Jaeger tracer
config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='user-service',
    validate=True,
)
tracer = config.initialize_tracer()

# Create spans
def get_user(user_id):
    with tracer.start_span('get_user') as span:
        span.set_tag('user.id', user_id)
        span.set_tag(tags.COMPONENT, 'user-service')
        
        # Simulate database call
        with tracer.start_span('db_query', child_of=span) as db_span:
            db_span.set_tag(tags.DATABASE_TYPE, 'postgresql')
            db_span.set_tag(tags.DATABASE_STATEMENT, 'SELECT * FROM users WHERE id = ?')
            
            # Your database logic here
            user = fetch_user_from_db(user_id)
            
        span.set_tag('user.found', user is not None)
        return user
```

### Service Communication Tracing
```python
import requests
from opentracing.propagation import Format

def call_downstream_service(data):
    with tracer.start_span('call_payment_service') as span:
        span.set_tag(tags.HTTP_METHOD, 'POST')
        span.set_tag(tags.HTTP_URL, 'http://payment-service/process')
        
        # Inject trace context into HTTP headers
        headers = {}
        tracer.inject(
            span_context=span.context,
            format=Format.HTTP_HEADERS,
            carrier=headers
        )
        
        response = requests.post(
            'http://payment-service/process',
            json=data,
            headers=headers
        )
        
        span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        if response.status_code >= 400:
            span.set_tag(tags.ERROR, True)
            span.log_kv({'error.message': response.text})
            
        return response
```

## Production Deployment

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        env:
        - name: COLLECTOR_ZIPKIN_HTTP_PORT
          value: "9411"
        - name: SPAN_STORAGE_TYPE
          value: "elasticsearch"
        - name: ES_SERVER_URLS
          value: "http://elasticsearch:9200"
        ports:
        - containerPort: 16686
        - containerPort: 14268
        - containerPort: 9411
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger-service
spec:
  selector:
    app: jaeger
  ports:
  - name: ui
    port: 16686
    targetPort: 16686
  - name: collector
    port: 14268
    targetPort: 14268
  type: LoadBalancer
```

### Jaeger with Elasticsearch Backend
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
data:
  jaeger.yaml: |
    span_storage:
      type: elasticsearch
      elasticsearch:
        server_urls: ["http://elasticsearch:9200"]
        index_prefix: "jaeger"
        num_shards: 5
        num_replicas: 1
    collector:
      zipkin:
        http_port: 9411
    query:
      max_clock_skew_adjustment: 0s
```

## Integration with OpenTelemetry

### OpenTelemetry Configuration
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument common libraries
RequestsInstrumentor().instrument()
FlaskInstrumentor().instrument_app(app)
```

## Monitoring and Analysis

### Custom Metrics and Tags
```python
def process_order(order_id):
    with tracer.start_span('process_order') as span:
        span.set_tag('order.id', order_id)
        span.set_tag('order.priority', 'high')
        
        # Add custom metrics
        span.log_kv({
            'event': 'order_received',
            'timestamp': time.time(),
            'order_value': 150.00
        })
        
        try:
            result = validate_order(order_id)
            span.set_tag('validation.success', True)
        except Exception as e:
            span.set_tag(tags.ERROR, True)
            span.log_kv({
                'event': 'error',
                'error.object': str(e),
                'error.kind': type(e).__name__
            })
            raise
        
        return result
```

### Performance Analysis Queries
```bash
# Find slowest operations
# Use Jaeger UI to search for:
# - Service: user-service
# - Operation: get_user
# - Min Duration: 1s

# Find error traces
# Search with tags: error=true

# Analyze service dependencies
# Use the "Dependencies" view in Jaeger UI
```

## Configuration Best Practices

### Sampling Configuration
```yaml
# Probabilistic sampling (sample 1% of traces)
sampler:
  type: probabilistic
  param: 0.01

# Rate limiting sampling (max 10 traces per second)
sampler:
  type: ratelimiting
  param: 10

# Adaptive sampling (adjust based on service volume)
sampler:
  type: remote
  param: 1
```

### Storage Configuration
```yaml
# Cassandra backend
span_storage:
  type: cassandra
  cassandra:
    servers: ["cassandra:9042"]
    keyspace: jaeger_v1_dc1
    local_dc: dc1

# Kafka for span collection
collector:
  kafka:
    brokers: ["kafka:9092"]
    topic: jaeger-spans
```

## Troubleshooting

### Common Issues
```bash
# Check Jaeger agent connectivity
curl http://localhost:14268/api/traces

# Verify span collection
curl "http://localhost:16686/api/traces?service=your-service"

# Debug missing traces
# 1. Check sampling configuration
# 2. Verify network connectivity
# 3. Check application instrumentation
# 4. Review Jaeger collector logs
```

## Best Practices

- Implement appropriate sampling to manage trace volume
- Use meaningful span names and consistent tagging
- Include business context in trace metadata
- Set up alerts for high error rates and latency
- Regularly review service dependency maps
- Use trace correlation for debugging production issues
- Implement distributed context propagation correctly

## Great Resources

- [Jaeger Documentation](https://www.jaegertracing.io/docs/) - Official comprehensive documentation
- [OpenTracing Specification](https://opentracing.io/specification/) - Tracing standards and best practices
- [Jaeger Operator](https://github.com/jaegertracing/jaeger-operator) - Kubernetes operator for Jaeger
- [OpenTelemetry](https://opentelemetry.io/) - Modern observability framework
- [Distributed Tracing in Practice](https://www.jaegertracing.io/docs/1.6/getting-started/) - Getting started guide
- [awesome-distributed-tracing](https://github.com/dgrijalva/awesome-distributed-tracing) - Curated tracing resources
- [Jaeger Performance Tuning](https://www.jaegertracing.io/docs/1.6/performance-tuning/) - Production optimization guide