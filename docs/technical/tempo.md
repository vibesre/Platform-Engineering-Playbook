# Grafana Tempo

## Overview

Grafana Tempo is a high-scale distributed tracing backend designed for platform engineers who need cost-effective trace storage and seamless integration with Grafana. It requires only object storage and provides excellent performance with minimal operational overhead.

## Key Features

- **Object Storage Only**: No complex databases required
- **High Scale**: Handle millions of spans per second
- **Cost Effective**: Low operational overhead
- **Grafana Integration**: Native support in Grafana
- **Multi-tenant**: Built-in multi-tenancy support

## Installation

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  tempo:
    image: grafana/tempo:latest
    command: ["-config.file=/etc/tempo.yaml"]
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
      - tempo-data:/tmp/tempo
    ports:
      - "3200:3200"   # Tempo HTTP
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "9411:9411"   # Zipkin
      - "14268:14268" # Jaeger HTTP
      - "14250:14250" # Jaeger gRPC

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml

volumes:
  tempo-data:
  grafana-data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tempo
  namespace: tracing
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tempo
  template:
    metadata:
      labels:
        app: tempo
    spec:
      containers:
      - name: tempo
        image: grafana/tempo:latest
        args:
          - "-config.file=/etc/tempo/tempo.yaml"
        ports:
        - containerPort: 3200
          name: http
        - containerPort: 4317
          name: otlp-grpc
        - containerPort: 4318
          name: otlp-http
        - containerPort: 9411
          name: zipkin
        - containerPort: 14268
          name: jaeger-http
        - containerPort: 14250
          name: jaeger-grpc
        resources:
          limits:
            memory: 2Gi
            cpu: 1000m
          requests:
            memory: 1Gi
            cpu: 500m
        volumeMounts:
        - name: config
          mountPath: /etc/tempo
        - name: storage
          mountPath: /tmp/tempo
        readinessProbe:
          httpGet:
            path: /ready
            port: 3200
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /ready
            port: 3200
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: config
        configMap:
          name: tempo-config
      - name: storage
        persistentVolumeClaim:
          claimName: tempo-storage
---
apiVersion: v1
kind: Service
metadata:
  name: tempo
  namespace: tracing
spec:
  selector:
    app: tempo
  ports:
  - name: http
    port: 3200
    targetPort: 3200
  - name: otlp-grpc
    port: 4317
    targetPort: 4317
  - name: otlp-http
    port: 4318
    targetPort: 4318
  - name: zipkin
    port: 9411
    targetPort: 9411
  - name: jaeger-http
    port: 14268
    targetPort: 14268
  - name: jaeger-grpc
    port: 14250
    targetPort: 14250
```

## Configuration

### Basic Configuration
```yaml
# tempo.yaml
server:
  http_listen_port: 3200
  log_level: info

distributor:
  receivers:
    zipkin:
      endpoint: 0.0.0.0:9411
    jaeger:
      protocols:
        thrift_http:
          endpoint: 0.0.0.0:14268
        grpc:
          endpoint: 0.0.0.0:14250
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1048576
  max_block_duration: 5m

compactor:
  compaction:
    compaction_window: 1h
    max_compaction_objects: 1000000
    retention_duration: 72h
    v2_in_buffer_bytes: 5242880
    v2_out_buffer_bytes: 20971520

storage:
  trace:
    backend: local
    local:
      path: /tmp/tempo/traces
    wal:
      path: /tmp/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000

querier:
  frontend_worker:
    frontend_address: tempo-query-frontend:9095

query_frontend:
  search:
    duration_slo: 5s
    throughput_bytes_slo: 1.073741824e+09
  trace_by_id:
    duration_slo: 5s

metrics_generator:
  registry:
    external_labels:
      source: tempo
      cluster: docker-compose
  storage:
    path: /tmp/tempo/generator/wal
    remote_write:
      - url: http://prometheus:9090/api/v1/write
        send_exemplars: true
```

### S3 Storage Configuration
```yaml
# tempo-s3.yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318
    zipkin:
      endpoint: 0.0.0.0:9411
    jaeger:
      protocols:
        thrift_http:
          endpoint: 0.0.0.0:14268
        grpc:
          endpoint: 0.0.0.0:14250

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1048576
  max_block_duration: 5m

compactor:
  compaction:
    compaction_window: 1h
    max_compaction_objects: 1000000
    retention_duration: 168h  # 7 days
    v2_in_buffer_bytes: 5242880
    v2_out_buffer_bytes: 20971520

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
      region: us-east-1
      access_key: ${AWS_ACCESS_KEY_ID}
      secret_key: ${AWS_SECRET_ACCESS_KEY}
      insecure: false
    wal:
      path: /tmp/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000

querier:
  frontend_worker:
    frontend_address: tempo-query-frontend:9095

query_frontend:
  search:
    duration_slo: 5s
    throughput_bytes_slo: 1.073741824e+09
  trace_by_id:
    duration_slo: 5s

metrics_generator:
  registry:
    external_labels:
      source: tempo
      cluster: production
  storage:
    path: /tmp/tempo/generator/wal
    remote_write:
      - url: http://prometheus:9090/api/v1/write
        send_exemplars: true
  processor:
    service_graphs:
      histogram_buckets: [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
      dimensions: ["service.name", "service.namespace"]
    span_metrics:
      histogram_buckets: [0.002, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
      dimensions: ["service.name", "operation", "status_code"]
```

### Multi-tenant Configuration
```yaml
# tempo-multitenant.yaml
server:
  http_listen_port: 3200

multitenancy_enabled: true

auth:
  type: header
  header: X-Scope-OrgID

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1048576
  max_block_duration: 5m

limits:
  per_tenant_override_config: /etc/tempo/overrides.yaml
  per_tenant_override_period: 10s

compactor:
  compaction:
    compaction_window: 1h
    max_compaction_objects: 1000000
    retention_duration: 72h

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces-multitenant
      endpoint: s3.amazonaws.com
      region: us-east-1
    wal:
      path: /tmp/tempo/wal
```

## Application Instrumentation

### OpenTelemetry with Tempo
```python
# Python application with OpenTelemetry
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from flask import Flask
import requests

# Configure OpenTelemetry
resource = Resource.create({
    "service.name": "user-service",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter for Tempo
otlp_exporter = OTLPSpanExporter(
    endpoint="http://tempo:4317",
    insecure=True
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)

# Auto-instrument Flask and requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/users/<user_id>')
def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("operation.name", "get_user")
        
        try:
            # Database call
            user_data = get_user_from_db(user_id)
            
            # External service call
            profile_data = get_profile_data(user_id)
            
            span.set_attribute("user.found", True)
            span.add_event("User data retrieved successfully")
            
            return {
                "user": user_data,
                "profile": profile_data
            }
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise

def get_user_from_db(user_id):
    with tracer.start_as_current_span("db_query") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.statement", "SELECT * FROM users WHERE id = %s")
        span.set_attribute("db.operation", "SELECT")
        span.set_attribute("db.name", "userdb")
        
        # Simulate database call
        import time
        time.sleep(0.05)
        
        return {"id": user_id, "name": f"User {user_id}"}

def get_profile_data(user_id):
    with tracer.start_as_current_span("external_service_call") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", f"http://profile-service/profiles/{user_id}")
        span.set_attribute("service.name", "profile-service")
        
        # This will be auto-instrumented by RequestsInstrumentor
        response = requests.get(f"http://profile-service/profiles/{user_id}")
        
        span.set_attribute("http.status_code", response.status_code)
        
        return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Java Spring Boot with OpenTelemetry
```java
// pom.xml dependencies
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-api</artifactId>
    <version>1.32.0</version>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-sdk</artifactId>
    <version>1.32.0</version>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
    <version>1.32.0</version>
</dependency>
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
    <version>1.32.0-alpha</version>
</dependency>

// application.yml
otel:
  service:
    name: user-service
    version: 1.0.0
  exporter:
    otlp:
      endpoint: http://tempo:4317
      protocol: grpc
  resource:
    attributes:
      deployment.environment: production
      service.namespace: user-management

// UserController.java
@RestController
public class UserController {
    
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("user-service");
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<Map<String, Object>> getUser(@PathVariable String id) {
        Span span = tracer.spanBuilder("get_user")
            .setAttribute("user.id", id)
            .setAttribute("operation.name", "get_user")
            .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            logger.info("Fetching user with ID: {}", id);
            
            User user = userService.findById(id);
            Map<String, Object> profile = userService.getProfile(id);
            
            span.setAttribute("user.found", user != null);
            span.addEvent("User data retrieved");
            
            Map<String, Object> response = new HashMap<>();
            response.put("user", user);
            response.put("profile", profile);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}

// UserService.java
@Service
public class UserService {
    
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("user-service");
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private WebClient webClient;
    
    public User findById(String id) {
        Span span = tracer.spanBuilder("db_query")
            .setAttribute("db.system", "postgresql")
            .setAttribute("db.operation", "SELECT")
            .setAttribute("db.statement", "SELECT * FROM users WHERE id = ?")
            .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            return userRepository.findById(id).orElse(null);
        } finally {
            span.end();
        }
    }
    
    public Map<String, Object> getProfile(String userId) {
        Span span = tracer.spanBuilder("external_service_call")
            .setAttribute("http.method", "GET")
            .setAttribute("http.url", "/profiles/" + userId)
            .setAttribute("service.name", "profile-service")
            .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            return webClient.get()
                .uri("/profiles/" + userId)
                .retrieve()
                .bodyToMono(Map.class)
                .block();
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Node.js with OpenTelemetry
```javascript
// package.json dependencies
{
  "dependencies": {
    "@opentelemetry/api": "^1.6.0",
    "@opentelemetry/sdk-node": "^0.45.0",
    "@opentelemetry/exporter-trace-otlp-grpc": "^0.45.0",
    "@opentelemetry/instrumentation-express": "^0.34.0",
    "@opentelemetry/instrumentation-http": "^0.45.0",
    "@opentelemetry/resources": "^1.18.0",
    "@opentelemetry/semantic-conventions": "^1.18.0",
    "express": "^4.18.0"
  }
}

// tracing.js - Initialize before importing other modules
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');

const traceExporter = new OTLPTraceExporter({
  url: 'http://tempo:4317',
});

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'user-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  }),
  traceExporter,
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

sdk.start();

// server.js
require('./tracing'); // Must be first

const express = require('express');
const { trace } = require('@opentelemetry/api');
const http = require('http');

const app = express();
const tracer = trace.getTracer('user-service');

app.get('/users/:id', async (req, res) => {
  const userId = req.params.id;
  const span = tracer.startSpan('get_user');
  
  span.setAttributes({
    'user.id': userId,
    'operation.name': 'get_user',
    'http.method': req.method,
    'http.route': req.route.path
  });
  
  try {
    // Database call
    const userData = await getUserFromDatabase(userId);
    
    // External service call
    const profileData = await getProfileData(userId);
    
    span.setAttributes({
      'user.found': !!userData,
      'response.status': 'success'
    });
    
    span.addEvent('User data retrieved successfully');
    
    res.json({
      user: userData,
      profile: profileData
    });
  } catch (error) {
    span.recordException(error);
    span.setStatus({
      code: trace.SpanStatusCode.ERROR,
      message: error.message
    });
    
    res.status(500).json({ error: error.message });
  } finally {
    span.end();
  }
});

async function getUserFromDatabase(userId) {
  const span = tracer.startSpan('db_query');
  
  span.setAttributes({
    'db.system': 'postgresql',
    'db.statement': 'SELECT * FROM users WHERE id = $1',
    'db.operation': 'SELECT',
    'db.name': 'userdb'
  });
  
  try {
    // Simulate database call
    await new Promise(resolve => setTimeout(resolve, 50));
    
    return { id: userId, name: `User ${userId}` };
  } finally {
    span.end();
  }
}

async function getProfileData(userId) {
  const span = tracer.startSpan('external_service_call');
  
  span.setAttributes({
    'http.method': 'GET',
    'http.url': `/profiles/${userId}`,
    'service.name': 'profile-service'
  });
  
  try {
    // HTTP call will be auto-instrumented
    const response = await new Promise((resolve) => {
      const req = http.request({
        hostname: 'profile-service',
        port: 3000,
        path: `/profiles/${userId}`,
        method: 'GET'
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      });
      
      req.end();
    });
    
    span.setAttributes({
      'http.status_code': 200,
      'response.size': JSON.stringify(response).length
    });
    
    return response;
  } catch (error) {
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

## Grafana Integration

### Grafana Data Source Configuration
```yaml
# grafana-datasources.yml
apiVersion: 1

datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    uid: tempo
    isDefault: false
    editable: true
    jsonData:
      tracesToLogs:
        datasourceUid: 'loki'
        tags: ['job', 'instance', 'pod', 'namespace']
        mappedTags: [{ key: 'service.name', value: 'service' }]
        mapTagNamesEnabled: false
        spanStartTimeShift: '1h'
        spanEndTimeShift: '1h'
        filterByTraceID: false
        filterBySpanID: false
      tracesToMetrics:
        datasourceUid: 'prometheus'
        tags: [{ key: 'service.name', value: 'service' }, { key: 'job' }]
        queries:
          - name: 'Sample query'
            query: 'sum(rate(traces_spanmetrics_latency_bucket{$__tags}[5m]))'
      serviceMap:
        datasourceUid: 'prometheus'
      search:
        hide: false
      nodeGraph:
        enabled: true
      lokiSearch:
        datasourceUid: 'loki'

  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    uid: prometheus
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    uid: loki
    isDefault: false
    editable: true
```

### Service Map Dashboard
```json
{
  "dashboard": {
    "title": "Service Map and Traces",
    "panels": [
      {
        "title": "Service Map",
        "type": "nodeGraph",
        "targets": [
          {
            "expr": "sum(rate(traces_service_graph_request_total[5m])) by (client, server)",
            "refId": "A"
          }
        ],
        "options": {
          "nodes": {
            "mainStatUnit": "ops"
          },
          "edges": {
            "mainStatUnit": "ops"
          }
        }
      },
      {
        "title": "Request Rate by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(traces_spanmetrics_calls_total[5m])) by (service_name)",
            "legendFormat": "{{service_name}}"
          }
        ]
      },
      {
        "title": "P95 Latency by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(traces_spanmetrics_latency_bucket[5m])) by (service_name, le))",
            "legendFormat": "{{service_name}}"
          }
        ]
      },
      {
        "title": "Error Rate by Service",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(traces_spanmetrics_calls_total{status_code=\"STATUS_CODE_ERROR\"}[5m])) by (service_name) / sum(rate(traces_spanmetrics_calls_total[5m])) by (service_name)",
            "legendFormat": "{{service_name}}"
          }
        ]
      }
    ]
  }
}
```

## Monitoring and Operations

### Tempo Metrics
```yaml
# Prometheus scrape config for Tempo
scrape_configs:
  - job_name: 'tempo'
    static_configs:
      - targets: ['tempo:3200']
    scrape_interval: 15s
    metrics_path: /metrics
```

### Key Metrics to Monitor
```promql
# Ingestion rate
rate(tempo_distributor_spans_received_total[5m])

# Ingestion latency
histogram_quantile(0.95, rate(tempo_request_duration_seconds_bucket{route="/tempo.Pusher/PushSpans"}[5m]))

# Query latency
histogram_quantile(0.95, rate(tempo_request_duration_seconds_bucket{route="/api/traces/{traceID}"}[5m]))

# Storage usage
tempo_ingester_blocks_total
tempo_ingester_bytes_received_total

# Compaction metrics
rate(tempo_compactor_blocks_compacted_total[5m])
tempo_compactor_compaction_duration_seconds

# Error rates
rate(tempo_request_duration_seconds_count{status_code!="200"}[5m])
```

### Alerting Rules
```yaml
# tempo-alerts.yml
groups:
  - name: tempo
    rules:
      - alert: TempoHighIngestionLatency
        expr: histogram_quantile(0.95, rate(tempo_request_duration_seconds_bucket{route="/tempo.Pusher/PushSpans"}[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Tempo ingestion latency is high"
          description: "P95 ingestion latency is {{ $value }}s"
      
      - alert: TempoQueryLatencyHigh
        expr: histogram_quantile(0.95, rate(tempo_request_duration_seconds_bucket{route="/api/traces/{traceID}"}[5m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Tempo query latency is high"
          description: "P95 query latency is {{ $value }}s"
      
      - alert: TempoCompactionFailing
        expr: increase(tempo_compactor_blocks_compacted_total[1h]) == 0
        for: 2h
        labels:
          severity: critical
        annotations:
          summary: "Tempo compaction is not working"
          description: "No blocks have been compacted in the last 2 hours"
```

## Best Practices

- Use object storage (S3, GCS, Azure Blob) for cost-effective long-term storage
- Implement appropriate retention policies based on compliance requirements
- Monitor ingestion and query performance regularly
- Use service graphs and span metrics for high-level service monitoring
- Implement proper sampling strategies to manage data volume
- Correlate traces with logs and metrics for complete observability
- Use trace exemplars to link metrics back to traces
- Regular monitoring of storage costs and optimization

## Great Resources

- [Grafana Tempo Documentation](https://grafana.com/docs/tempo/) - Official comprehensive documentation
- [Tempo GitHub](https://github.com/grafana/tempo) - Source code and community
- [OpenTelemetry](https://opentelemetry.io/) - Open standard for observability
- [Grafana Observability](https://grafana.com/products/cloud/observability/) - Complete observability stack
- [Tempo vs Jaeger](https://grafana.com/blog/2021/04/13/how-to-migrate-from-jaeger-to-grafana-tempo/) - Migration guide
- [Distributed Tracing Guide](https://grafana.com/blog/2021/01/25/distributed-tracing-101-a-guide-for-everyone/) - Tracing fundamentals
- [Tempo Best Practices](https://grafana.com/blog/2022/05/10/tips-for-migrating-from-jaeger-to-grafana-tempo/) - Migration and optimization tips
- [OTEL Collector](https://opentelemetry.io/docs/collector/) - OpenTelemetry Collector for trace collection