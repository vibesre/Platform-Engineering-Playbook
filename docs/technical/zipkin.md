# Zipkin

## Overview

Zipkin is a distributed tracing system that helps platform engineers troubleshoot latency problems in service-oriented architectures. It collects timing data from applications and services to identify bottlenecks and understand request flows across microservices.

## Key Features

- **Distributed Tracing**: Track requests across multiple services
- **Latency Analysis**: Identify performance bottlenecks
- **Service Dependencies**: Visualize service interactions
- **Search and Filtering**: Find specific traces by various criteria
- **Multiple Storage Options**: Cassandra, Elasticsearch, MySQL, in-memory

## Installation

### Docker Quick Start
```bash
# Run Zipkin with in-memory storage
docker run -d \
  --name zipkin \
  -p 9411:9411 \
  openzipkin/zipkin:latest

# Access UI at http://localhost:9411
```

### Docker Compose with Elasticsearch
```yaml
# docker-compose.yml
version: '3.8'
services:
  elasticsearch:
    image: elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  zipkin:
    image: openzipkin/zipkin:latest
    environment:
      - STORAGE_TYPE=elasticsearch
      - ES_HOSTS=elasticsearch:9200
      - ES_INDEX=zipkin
      - ES_DATE_SEPARATOR=-
    ports:
      - "9411:9411"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zipkin
  namespace: tracing
spec:
  replicas: 2
  selector:
    matchLabels:
      app: zipkin
  template:
    metadata:
      labels:
        app: zipkin
    spec:
      containers:
      - name: zipkin
        image: openzipkin/zipkin:latest
        ports:
        - containerPort: 9411
        env:
        - name: STORAGE_TYPE
          value: elasticsearch
        - name: ES_HOSTS
          value: "elasticsearch:9200"
        - name: ES_INDEX
          value: zipkin
        - name: JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        resources:
          limits:
            memory: 2Gi
            cpu: 1000m
          requests:
            memory: 1Gi
            cpu: 500m
        livenessProbe:
          httpGet:
            path: /health
            port: 9411
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 9411
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: zipkin
  namespace: tracing
spec:
  selector:
    app: zipkin
  ports:
  - port: 9411
    targetPort: 9411
  type: LoadBalancer
```

## Application Instrumentation

### Java with Spring Boot
```java
// pom.xml dependencies
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zipkin</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>

// application.yml
spring:
  zipkin:
    base-url: http://zipkin:9411
    sender:
      type: web
  sleuth:
    sampler:
      probability: 0.1  # Sample 10% of traces
    zipkin:
      enabled: true
    web:
      client:
        enabled: true
    http:
      legacy:
        enabled: true

// Custom tracing in Spring Boot
@RestController
public class UserController {
    
    @Autowired
    private Tracer tracer;
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        Span span = tracer.nextSpan()
            .name("get-user")
            .tag("user.id", id.toString())
            .start();
        
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            User user = userService.findById(id);
            span.tag("user.found", user != null ? "true" : "false");
            return user;
        } catch (Exception e) {
            span.tag("error", e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}

// Database query tracing
@Service
public class UserService {
    
    @Autowired
    private Tracer tracer;
    
    @Autowired
    private UserRepository userRepository;
    
    public User findById(Long id) {
        Span dbSpan = tracer.nextSpan()
            .name("db-query")
            .tag("db.type", "postgresql")
            .tag("db.statement", "SELECT * FROM users WHERE id = ?")
            .start();
        
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(dbSpan)) {
            return userRepository.findById(id).orElse(null);
        } finally {
            dbSpan.end();
        }
    }
}
```

### Python with Flask
```python
# requirements.txt
flask
py_zipkin
requests

# app.py
from flask import Flask, request
from py_zipkin.zipkin import zipkin_span
from py_zipkin.transport import http_transport
import requests
import json

app = Flask(__name__)

def http_transport_handler(encoded_span):
    """Send spans to Zipkin"""
    requests.post(
        'http://zipkin:9411/api/v2/spans',
        data=encoded_span,
        headers={'Content-Type': 'application/json'}
    )

@app.route('/users/<user_id>')
def get_user(user_id):
    with zipkin_span(
        service_name='user-service',
        span_name='get_user',
        transport_handler=http_transport_handler,
        port=5000,
        sample_rate=0.1  # 10% sampling
    ) as span:
        span.update_binary_annotations({
            'user.id': user_id,
            'http.method': request.method,
            'http.url': request.url
        })
        
        try:
            # Call database
            user_data = get_user_from_db(user_id)
            
            # Call external service
            profile_data = get_user_profile(user_id)
            
            return {
                'user': user_data,
                'profile': profile_data
            }
        except Exception as e:
            span.update_binary_annotations({'error': str(e)})
            raise

def get_user_from_db(user_id):
    """Database call with tracing"""
    with zipkin_span(
        service_name='user-service',
        span_name='db_query',
        transport_handler=http_transport_handler
    ) as span:
        span.update_binary_annotations({
            'db.type': 'postgresql',
            'db.statement': 'SELECT * FROM users WHERE id = %s',
            'db.user': 'app_user'
        })
        
        # Simulate database call
        import time
        time.sleep(0.05)  # 50ms database call
        
        return {'id': user_id, 'name': f'User {user_id}'}

def get_user_profile(user_id):
    """External service call with tracing"""
    with zipkin_span(
        service_name='user-service',
        span_name='external_call',
        transport_handler=http_transport_handler
    ) as span:
        span.update_binary_annotations({
            'http.method': 'GET',
            'http.url': f'http://profile-service/profiles/{user_id}',
            'component': 'requests'
        })
        
        # Simulate external service call
        import time
        time.sleep(0.1)  # 100ms external call
        
        return {'user_id': user_id, 'bio': f'Bio for user {user_id}'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Node.js with Express
```javascript
// package.json dependencies
{
  "dependencies": {
    "express": "^4.18.0",
    "zipkin": "^0.22.0",
    "zipkin-transport-http": "^0.22.0",
    "zipkin-instrumentation-express": "^0.22.0",
    "zipkin-instrumentation-http": "^0.22.0"
  }
}

// server.js
const express = require('express');
const {
  Tracer,
  BatchRecorder,
  jsonEncoder: {JSON_V2}
} = require('zipkin');
const {HttpLogger} = require('zipkin-transport-http');
const zipkinMiddleware = require('zipkin-instrumentation-express').expressMiddleware;
const {wrapHttp} = require('zipkin-instrumentation-http');
const http = require('http');

const app = express();

// Initialize Zipkin tracer
const tracer = new Tracer({
  ctxImpl: require('zipkin-context-cls'),
  recorder: new BatchRecorder({
    logger: new HttpLogger({
      endpoint: 'http://zipkin:9411/api/v2/spans',
      jsonEncoder: JSON_V2
    })
  }),
  sampler: {shouldSample: () => Math.random() < 0.1}, // 10% sampling
  traceId128Bit: true
});

// Add Zipkin middleware
app.use(zipkinMiddleware({
  tracer,
  serviceName: 'user-api'
}));

// Instrument HTTP client
const httpInstrumented = wrapHttp(http, {
  tracer,
  serviceName: 'user-api'
});

app.get('/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  try {
    // Add custom tags
    tracer.recordBinary('user.id', userId);
    tracer.recordBinary('request.path', req.path);
    
    // Call database
    const userData = await getUserFromDatabase(userId);
    
    // Call external service
    const profileData = await getProfileData(userId);
    
    res.json({
      user: userData,
      profile: profileData
    });
  } catch (error) {
    tracer.recordBinary('error', error.message);
    res.status(500).json({error: error.message});
  }
});

async function getUserFromDatabase(userId) {
  return tracer.scoped(() => {
    tracer.setId(tracer.createChildId());
    tracer.recordServiceName('user-db');
    tracer.recordRpc('db_query');
    tracer.recordBinary('db.type', 'postgresql');
    tracer.recordBinary('db.statement', 'SELECT * FROM users WHERE id = $1');
    
    // Simulate database query
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({id: userId, name: `User ${userId}`});
      }, 50);
    });
  });
}

async function getProfileData(userId) {
  return tracer.scoped(() => {
    tracer.setId(tracer.createChildId());
    tracer.recordServiceName('profile-service');
    tracer.recordRpc('get_profile');
    tracer.recordBinary('http.method', 'GET');
    tracer.recordBinary('http.url', `/profiles/${userId}`);
    
    // Simulate external service call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({userId, bio: `Bio for user ${userId}`});
      }, 100);
    });
  });
}

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Go Application
```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"

    "github.com/gorilla/mux"
    "github.com/openzipkin/zipkin-go"
    zipkinhttp "github.com/openzipkin/zipkin-go/middleware/http"
    "github.com/openzipkin/zipkin-go/reporter"
    httpreporter "github.com/openzipkin/zipkin-go/reporter/http"
)

type User struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}

func main() {
    // Create Zipkin reporter
    rep := httpreporter.NewReporter("http://zipkin:9411/api/v2/spans")
    defer rep.Close()

    // Create Zipkin tracer
    endpoint, _ := zipkin.NewEndpoint("user-service", "localhost:8080")
    tracer, err := zipkin.NewTracer(rep, zipkin.WithLocalEndpoint(endpoint))
    if err != nil {
        log.Fatal(err)
    }

    // Create HTTP client with tracing
    client, err := zipkinhttp.NewClient(tracer, zipkinhttp.ClientTrace(true))
    if err != nil {
        log.Fatal(err)
    }

    r := mux.NewRouter()
    
    // Add tracing middleware
    r.Use(zipkinhttp.NewServerMiddleware(
        tracer,
        zipkinhttp.TagResponseSize(true),
        zipkinhttp.SpanName("http_request"),
    ))

    r.HandleFunc("/users/{id}", func(w http.ResponseWriter, r *http.Request) {
        vars := mux.Vars(r)
        userID := vars["id"]

        // Get span from context
        span := zipkin.SpanFromContext(r.Context())
        span.Tag("user.id", userID)
        span.Tag("handler", "get_user")

        // Call database
        user, err := getUserFromDB(r.Context(), tracer, userID)
        if err != nil {
            span.Tag("error", err.Error())
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        // Call external service
        profile, err := getProfile(r.Context(), tracer, client, userID)
        if err != nil {
            span.Tag("error", err.Error())
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        response := map[string]interface{}{
            "user":    user,
            "profile": profile,
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
    })

    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}

func getUserFromDB(ctx context.Context, tracer *zipkin.Tracer, userID string) (*User, error) {
    span, ctx := tracer.StartSpanFromContext(ctx, "db_query")
    defer span.Finish()

    span.Tag("db.type", "postgresql")
    span.Tag("db.statement", "SELECT * FROM users WHERE id = $1")
    span.Tag("db.user", "app_user")

    // Simulate database call
    time.Sleep(50 * time.Millisecond)

    user := &User{
        ID:   userID,
        Name: fmt.Sprintf("User %s", userID),
    }

    return user, nil
}

func getProfile(ctx context.Context, tracer *zipkin.Tracer, client *http.Client, userID string) (map[string]string, error) {
    span, ctx := tracer.StartSpanFromContext(ctx, "external_call")
    defer span.Finish()

    span.Tag("http.method", "GET")
    span.Tag("http.url", fmt.Sprintf("/profiles/%s", userID))
    span.Tag("component", "http_client")

    // Simulate external service call
    time.Sleep(100 * time.Millisecond)

    profile := map[string]string{
        "user_id": userID,
        "bio":     fmt.Sprintf("Bio for user %s", userID),
    }

    return profile, nil
}
```

## Configuration and Storage

### Elasticsearch Storage
```yaml
# Zipkin with Elasticsearch storage
version: '3.8'
services:
  elasticsearch:
    image: elasticsearch:7.17.0
    environment:
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - discovery.type=single-node
      - cluster.name=zipkin
      - bootstrap.memory_lock=true
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  zipkin:
    image: openzipkin/zipkin:latest
    environment:
      - STORAGE_TYPE=elasticsearch
      - ES_HOSTS=elasticsearch:9200
      - ES_USERNAME=elastic
      - ES_PASSWORD=changeme
      - ES_INDEX=zipkin
      - ES_DATE_SEPARATOR=-
      - ES_INDEX_SHARDS=5
      - ES_INDEX_REPLICAS=1
      - JAVA_OPTS=-Xms1g -Xmx1g -XX:+UseG1GC
    ports:
      - "9411:9411"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

### Cassandra Storage
```yaml
# Zipkin with Cassandra storage
version: '3.8'
services:
  cassandra:
    image: cassandra:3.11
    environment:
      - CASSANDRA_DC=datacenter1
      - CASSANDRA_RACK=rack1
    volumes:
      - cassandra_data:/var/lib/cassandra
    ports:
      - "9042:9042"

  zipkin:
    image: openzipkin/zipkin:latest
    environment:
      - STORAGE_TYPE=cassandra3
      - CASSANDRA_CONTACT_POINTS=cassandra:9042
      - CASSANDRA_LOCAL_DC=datacenter1
      - CASSANDRA_KEYSPACE=zipkin
      - CASSANDRA_USERNAME=cassandra
      - CASSANDRA_PASSWORD=cassandra
    ports:
      - "9411:9411"
    depends_on:
      - cassandra

volumes:
  cassandra_data:
```

## Monitoring and Alerting

### Prometheus Metrics
```yaml
# Zipkin with Prometheus metrics
services:
  zipkin:
    image: openzipkin/zipkin:latest
    environment:
      - ZIPKIN_SELF_TRACING_ENABLED=true
      - ZIPKIN_SELF_TRACING_SAMPLE_RATE=1.0
      - ZIPKIN_SELF_TRACING_FLUSH_INTERVAL=1
    ports:
      - "9411:9411"
      - "9999:9999"  # Prometheus metrics
    command: >
      sh -c '
        echo "management.endpoints.web.exposure.include=health,info,prometheus" >> /zipkin/config/zipkin-server.properties &&
        echo "management.endpoint.prometheus.enabled=true" >> /zipkin/config/zipkin-server.properties &&
        echo "management.metrics.export.prometheus.enabled=true" >> /zipkin/config/zipkin-server.properties &&
        start-zipkin
      '

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Zipkin Tracing Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(zipkin_http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Average Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(zipkin_http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(zipkin_http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(zipkin_http_requests_total{status=~\"5..\"}[5m]) / rate(zipkin_http_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      }
    ]
  }
}
```

## Advanced Features

### Custom Annotations and Tags
```java
// Java example with custom annotations
public class OrderService {
    
    @NewSpan("process-order")
    public Order processOrder(@SpanTag("order.id") String orderId) {
        // Add custom annotations
        tracer.addTag("order.type", order.getType());
        tracer.addTag("customer.tier", customer.getTier());
        
        // Add timed annotations
        tracer.annotate("validation.start");
        validateOrder(order);
        tracer.annotate("validation.end");
        
        tracer.annotate("payment.start");
        processPayment(order);
        tracer.annotate("payment.end");
        
        return order;
    }
}
```

### Dependency Analysis
```bash
# Query Zipkin API for service dependencies
curl "http://zipkin:9411/api/v2/dependencies?endTs=$(date +%s)000&lookback=86400000" | jq .

# Get service names
curl "http://zipkin:9411/api/v2/services" | jq .

# Get span names for a service
curl "http://zipkin:9411/api/v2/spans?serviceName=user-service" | jq .

# Search traces
curl "http://zipkin:9411/api/v2/traces?serviceName=user-service&limit=10" | jq .
```

## Best Practices

- Implement appropriate sampling rates to balance observability and performance
- Use consistent service and span naming conventions
- Add meaningful tags and annotations for better search and filtering
- Monitor Zipkin server performance and storage usage
- Implement proper error handling in instrumentation code
- Use baggage sparingly to avoid performance impact
- Regular cleanup of old trace data based on retention policies
- Correlate traces with logs using trace IDs

## Great Resources

- [Zipkin Documentation](https://zipkin.io/) - Official comprehensive documentation
- [Zipkin GitHub](https://github.com/openzipkin/zipkin) - Source code and community
- [OpenTracing](https://opentracing.io/) - Vendor-neutral tracing API
- [Zipkin Instrumentation](https://zipkin.io/pages/existing_instrumentations.html) - Available instrumentation libraries
- [Zipkin Architecture](https://zipkin.io/pages/architecture.html) - System design and components
- [Brave (Java)](https://github.com/openzipkin/brave) - Java tracing library
- [Zipkin vs Jaeger](https://blog.jaegertracing.io/jaeger-and-zipkin/) - Comparison with Jaeger
- [Distributed Tracing Guide](https://opentracing.io/guides/) - OpenTracing best practices