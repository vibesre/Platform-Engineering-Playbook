# OpenTelemetry

## Overview

OpenTelemetry is an open-source observability framework that provides a single set of APIs, libraries, agents, and instrumentation to capture distributed traces and metrics from applications. It's the successor to OpenTracing and OpenCensus projects.

## Key Features

- **Vendor Neutral**: Works with any observability backend
- **Auto-Instrumentation**: Automatic instrumentation for popular frameworks
- **Multiple Languages**: Support for Java, Python, Go, JavaScript, and more
- **Unified Standards**: Single API for traces, metrics, and logs
- **Extensible**: Plugin architecture for custom requirements

## Common Use Cases

### Python Application Instrumentation
```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument libraries
RequestsInstrumentor().instrument()
FlaskInstrumentor().instrument_app(app)

# Manual instrumentation
@app.route('/api/users/<user_id>')
def get_user(user_id):
    with tracer.start_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("http.method", "GET")
        
        user = database.get_user(user_id)
        span.set_attribute("user.found", user is not None)
        return jsonify(user)
```

### Go Application Instrumentation
```go
package main

import (
    "context"
    "log"
    "net/http"
    
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
    "go.opentelemetry.io/otel/instrumentation/net/http/otelhttp"
)

func initTracer() {
    exporter, err := otlptracegrpc.New(
        context.Background(),
        otlptracegrpc.WithEndpoint("http://otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        log.Fatal(err)
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
    )
    
    otel.SetTracerProvider(tp)
}

func main() {
    initTracer()
    
    // Wrap HTTP handlers
    http.Handle("/api/", otelhttp.NewHandler(
        http.HandlerFunc(apiHandler), 
        "api",
    ))
    
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
    tracer := otel.Tracer("api-service")
    ctx, span := tracer.Start(r.Context(), "handle_request")
    defer span.End()
    
    // Add custom attributes
    span.SetAttributes(
        attribute.String("user.id", getUserID(r)),
        attribute.String("request.path", r.URL.Path),
    )
    
    // Your business logic here
    processRequest(ctx, r)
}
```

### Kubernetes Deployment with Collector
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  otel-collector-config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
      
    processors:
      batch:
        timeout: 1s
        send_batch_size: 1024
      memory_limiter:
        limit_mib: 512
    
    exporters:
      jaeger:
        endpoint: jaeger-collector:14250
        tls:
          insecure: true
      
      prometheus:
        endpoint: "0.0.0.0:8889"
      
      logging:
        loglevel: debug
    
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [jaeger, logging]
        
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [prometheus, logging]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
spec:
  replicas: 1
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector:latest
        command:
        - "/otelcol"
        - "--config=/conf/otel-collector-config.yaml"
        volumeMounts:
        - name: config
          mountPath: /conf
        ports:
        - containerPort: 4317
        - containerPort: 4318
        - containerPort: 8889
      volumes:
      - name: config
        configMap:
          name: otel-collector-config
```

### Auto-Instrumentation with Operators
```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: my-instrumentation
spec:
  exporter:
    endpoint: http://otel-collector:4318
  propagators:
    - tracecontext
    - baggage
  sampler:
    type: parentbased_traceidratio
    argument: "0.1"
  python:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-python:latest
  java:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-java:latest
  nodejs:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-nodejs:latest
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-python: "true"
    spec:
      containers:
      - name: myapp
        image: myapp:latest
```

## Metrics Collection

### Custom Metrics
```python
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Configure metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="http://otel-collector:4317",
        insecure=True
    ),
    export_interval_millis=5000,
)

metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
meter = metrics.get_meter(__name__)

# Create instruments
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1"
)

response_time_histogram = meter.create_histogram(
    name="http_request_duration_seconds",
    description="HTTP request duration",
    unit="s"
)

active_connections = meter.create_up_down_counter(
    name="active_connections",
    description="Number of active connections",
    unit="1"
)

# Use instruments
def handle_request():
    start_time = time.time()
    
    request_counter.add(1, {
        "method": "GET",
        "endpoint": "/api/users"
    })
    
    # Process request
    process_request()
    
    duration = time.time() - start_time
    response_time_histogram.record(duration, {
        "method": "GET",
        "status_code": "200"
    })
```

## Configuration Examples

### Environment Variables
```bash
# Basic configuration
export OTEL_SERVICE_NAME="my-service"
export OTEL_SERVICE_VERSION="1.0.0"
export OTEL_RESOURCE_ATTRIBUTES="environment=production,team=platform"

# Exporter configuration
export OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_EXPORTER_OTLP_HEADERS="authorization=Bearer token123"

# Sampling configuration
export OTEL_TRACES_SAMPLER="traceidratio"
export OTEL_TRACES_SAMPLER_ARG="0.1"

# Instrumentation configuration
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="true"
export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST="content-type,accept"
```

### Docker Compose Setup
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - OTEL_SERVICE_NAME=my-app
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
      - OTEL_RESOURCE_ATTRIBUTES=environment=production
    depends_on:
      - otel-collector

  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8889:8889"   # Prometheus metrics
    depends_on:
      - jaeger

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
```

## Advanced Features

### Custom Sampling
```python
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision

class CustomSampler(Sampler):
    def should_sample(self, parent_context, trace_id, name, kind, attributes, links, trace_state):
        # Sample all error traces
        if attributes and attributes.get("error"):
            return SamplingResult(Decision.RECORD_AND_SAMPLE)
        
        # Sample 10% of normal traces
        if trace_id % 10 == 0:
            return SamplingResult(Decision.RECORD_AND_SAMPLE)
        
        return SamplingResult(Decision.DROP)

# Use custom sampler
tracer_provider = TracerProvider(sampler=CustomSampler())
```

### Resource Detection
```python
from opentelemetry.sdk.resources import Resource
from opentelemetry.resourcedetector.gcp import GoogleCloudResourceDetector
from opentelemetry.resourcedetector.aws import AwsEcsResourceDetector

# Auto-detect resources
resource = Resource.create().merge(
    GoogleCloudResourceDetector().detect()
).merge(
    AwsEcsResourceDetector().detect()
)

tracer_provider = TracerProvider(resource=resource)
```

## Best Practices

- Use semantic conventions for consistent attribute naming
- Implement appropriate sampling strategies for production
- Configure resource attributes for better service identification
- Use batch processors for better performance
- Monitor collector performance and resource usage
- Implement proper error handling for telemetry failures
- Use correlation IDs to link traces across services

## Great Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) - Official comprehensive documentation
- [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification) - Technical specifications and standards
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) - Data collection and processing
- [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator) - Kubernetes deployment automation
- [Semantic Conventions](https://opentelemetry.io/docs/reference/specification/semantic-conventions/) - Standard attribute naming
- [Auto-Instrumentation](https://opentelemetry.io/docs/instrumentation/) - Language-specific instrumentation guides
- [OpenTelemetry Registry](https://opentelemetry.io/registry/) - Community packages and integrations