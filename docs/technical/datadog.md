# Datadog

## Overview

Datadog is a comprehensive monitoring and analytics platform for cloud-scale applications. It provides real-time visibility into infrastructure, applications, and logs, enabling teams to monitor, troubleshoot, and optimize their systems.

## Key Features

- **Infrastructure Monitoring**: Servers, containers, and cloud services
- **Application Performance Monitoring (APM)**: Distributed tracing and performance insights
- **Log Management**: Centralized log collection and analysis
- **Real User Monitoring (RUM)**: Frontend performance monitoring
- **Alerting**: Intelligent alerts and notifications

## Installation and Setup

### Agent Installation
```bash
# Install on Ubuntu/Debian
DD_API_KEY=your_api_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"

# Install on CentOS/RHEL
DD_API_KEY=your_api_key bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_rpm.sh)"

# Docker installation
docker run -d --name datadog-agent \
  -e DD_API_KEY=your_api_key \
  -e DD_SITE="datadoghq.com" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  datadog/agent:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    metadata:
      labels:
        app: datadog-agent
    spec:
      serviceAccountName: datadog-agent
      containers:
      - name: datadog-agent
        image: datadog/agent:latest
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_SITE
          value: "datadoghq.com"
        - name: DD_KUBERNETES_KUBELET_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
        - name: DD_CLUSTER_NAME
          value: "my-cluster"
        - name: DD_COLLECT_KUBERNETES_EVENTS
          value: "true"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_LOGS_ENABLED
          value: "true"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "200m"
        volumeMounts:
        - name: dockersocketdir
          mountPath: /host/var/run
        - name: procdir
          mountPath: /host/proc
          readOnly: true
        - name: cgroups
          mountPath: /host/sys/fs/cgroup
          readOnly: true
      volumes:
      - name: dockersocketdir
        hostPath:
          path: /var/run
      - name: procdir
        hostPath:
          path: /proc
      - name: cgroups
        hostPath:
          path: /sys/fs/cgroup
```

## Application Monitoring

### Python APM Integration
```python
from ddtrace import tracer, patch_all
import logging

# Auto-instrument common libraries
patch_all()

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s'
)

@tracer.wrap("database.query")
def get_user(user_id):
    # Custom span with tags
    span = tracer.current_span()
    span.set_tag("user.id", user_id)
    span.set_tag("component", "database")
    
    try:
        user = db.query("SELECT * FROM users WHERE id = %s", user_id)
        span.set_tag("user.found", user is not None)
        return user
    except Exception as e:
        span.set_error(e)
        raise

# Custom metrics
from datadog import DogStatsdClient

statsd = DogStatsdClient(host="localhost", port=8125)

def process_order(order):
    # Increment counter
    statsd.increment('orders.processed', tags=['environment:production'])
    
    # Record timing
    with statsd.timed('orders.processing_time'):
        result = handle_order(order)
    
    # Record gauge
    statsd.gauge('orders.queue_size', get_queue_size())
    
    return result
```

### Node.js APM Integration
```javascript
// Must be imported before any other modules
const tracer = require('dd-trace').init({
  service: 'my-app',
  env: 'production',
  version: '1.0.0'
});

const StatsD = require('hot-shots');
const dogstatsd = new StatsD({
  host: 'localhost',
  port: 8125,
  globalTags: ['env:production']
});

const express = require('express');
const app = express();

app.get('/api/users/:id', async (req, res) => {
  const span = tracer.scope().active();
  span.setTag('user.id', req.params.id);
  
  try {
    // Custom timing
    const start = Date.now();
    const user = await getUserById(req.params.id);
    const duration = Date.now() - start;
    
    // Send custom metrics
    dogstatsd.timing('api.user_lookup.duration', duration);
    dogstatsd.increment('api.user_lookup.success');
    
    res.json(user);
  } catch (error) {
    span.setTag('error', true);
    dogstatsd.increment('api.user_lookup.error');
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Log Management

### Log Collection Configuration
```yaml
# datadog.yaml
logs_enabled: true
logs_config:
  container_collect_all: true
  
# Custom log configuration
logs:
  - type: file
    path: /var/log/myapp/*.log
    service: myapp
    source: custom
    sourcecategory: application
    tags: env:production
  
  - type: docker
    image: nginx
    service: nginx
    source: nginx
    log_processing_rules:
      - type: exclude_at_match
        name: exclude_debug
        pattern: DEBUG
```

### Structured Logging
```python
import json
import logging
from datetime import datetime

class DatadogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'service': 'my-app',
            'env': 'production'
        }
        
        # Add custom attributes
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_record['dd.trace_id'] = record.request_id
            
        return json.dumps(log_record)

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(DatadogFormatter())
logger.addHandler(handler)

# Usage
logger.info("User login", extra={'user_id': 12345})
```

## Custom Dashboards

### Infrastructure Dashboard
```json
{
  "title": "Infrastructure Overview",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:system.cpu.user{*} by {host}",
            "display_type": "line"
          }
        ],
        "title": "CPU Usage by Host"
      }
    },
    {
      "definition": {
        "type": "query_value",
        "requests": [
          {
            "q": "avg:system.mem.pct_usable{*}",
            "aggregator": "avg"
          }
        ],
        "title": "Memory Usage"
      }
    },
    {
      "definition": {
        "type": "toplist",
        "requests": [
          {
            "q": "top(avg:docker.containers.running{*} by {docker_image}, 10, 'mean', 'desc')"
          }
        ],
        "title": "Top Running Containers"
      }
    }
  ]
}
```

### Application Performance Dashboard
```json
{
  "title": "Application Performance",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:trace.flask.request.duration{service:my-app} by {resource_name}",
            "display_type": "line"
          }
        ],
        "title": "Request Duration by Endpoint"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "sum:trace.flask.request.hits{service:my-app}.as_rate()",
            "display_type": "bars"
          }
        ],
        "title": "Request Rate"
      }
    },
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "sum:trace.flask.request.errors{service:my-app}.as_rate()",
            "display_type": "line"
          }
        ],
        "title": "Error Rate"
      }
    }
  ]
}
```

## Alerting and Monitoring

### Metric Alerts
```json
{
  "name": "High CPU Usage",
  "type": "metric alert",
  "query": "avg(last_5m):avg:system.cpu.user{*} by {host} > 80",
  "message": "CPU usage is high on {{host.name}}. Current value: {{value}}%",
  "tags": ["team:infrastructure"],
  "options": {
    "thresholds": {
      "critical": 80,
      "warning": 70
    },
    "notify_no_data": true,
    "no_data_timeframe": 10,
    "evaluation_delay": 60
  }
}
```

### Log Alerts
```json
{
  "name": "Application Errors",
  "type": "log alert",
  "query": "logs(\"service:my-app status:error\").index(\"*\").rollup(\"count\").last(\"5m\") > 10",
  "message": "High error rate detected in application logs",
  "tags": ["team:backend"],
  "options": {
    "enable_logs_sample": true
  }
}
```

### Composite Alerts
```json
{
  "name": "Service Health",
  "type": "composite",
  "query": "a && b",
  "subqueries": {
    "a": "avg(last_5m):avg:trace.flask.request.duration{service:my-app} > 1000",
    "b": "avg(last_5m):sum:trace.flask.request.errors{service:my-app}.as_rate() > 0.05"
  },
  "message": "Service my-app is experiencing high latency and errors"
}
```

## Synthetic Monitoring

### API Tests
```json
{
  "name": "API Health Check",
  "type": "api",
  "config": {
    "request": {
      "method": "GET",
      "url": "https://api.myapp.com/health",
      "headers": {
        "Authorization": "Bearer {{API_TOKEN}}"
      }
    },
    "assertions": [
      {
        "type": "statusCode",
        "operator": "is",
        "target": 200
      },
      {
        "type": "responseTime",
        "operator": "lessThan",
        "target": 1000
      },
      {
        "type": "body",
        "operator": "contains",
        "target": "healthy"
      }
    ]
  },
  "locations": ["aws:us-east-1", "aws:eu-west-1"],
  "options": {
    "tick_every": 60,
    "min_failure_duration": 120,
    "min_location_failed": 1
  }
}
```

## Integration with CI/CD

### Quality Gates
```yaml
# .github/workflows/deploy.yml
name: Deploy with Quality Gates

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy Application
      run: kubectl apply -f k8s/
    
    - name: Wait for Deployment
      run: kubectl rollout status deployment/my-app
    
    - name: Run Datadog Quality Gate
      uses: DataDog/datadog-ci-github-action@v1
      with:
        api-key: ${{ secrets.DD_API_KEY }}
        app-key: ${{ secrets.DD_APP_KEY }}
        datadog-site: datadoghq.com
        cmd: |
          datadog-ci synthetics run-tests \
            --public-id abc-123-def \
            --variable API_URL=https://staging.myapp.com
```

## Best Practices

- Use consistent tagging strategy across all resources
- Implement proper log sampling for high-volume applications
- Set up meaningful alerts with appropriate thresholds
- Use dashboards to visualize key business metrics
- Implement distributed tracing for microservices
- Monitor both technical and business metrics
- Regular review and optimization of monitoring costs

## Great Resources

- [Datadog Documentation](https://docs.datadoghq.com/) - Official comprehensive documentation
- [Datadog Agent](https://github.com/DataDog/datadog-agent) - Open-source monitoring agent
- [APM Documentation](https://docs.datadoghq.com/tracing/) - Application performance monitoring guide
- [Log Management](https://docs.datadoghq.com/logs/) - Centralized logging documentation
- [Synthetic Monitoring](https://docs.datadoghq.com/synthetics/) - Proactive monitoring setup
- [Datadog Learning Center](https://learn.datadoghq.com/) - Training and certification resources
- [Community Integrations](https://docs.datadoghq.com/integrations/) - Third-party integrations and plugins