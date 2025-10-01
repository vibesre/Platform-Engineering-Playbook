---
title: "New Relic - Application Performance Monitoring"
description: "Master New Relic for observability: monitor applications, infrastructure, and logs. Learn NRQL querying, APM instrumentation, and distributed tracing strategies."
keywords:
  - New Relic
  - APM
  - application monitoring
  - observability platform
  - NRQL
  - performance monitoring
  - distributed tracing
  - infrastructure monitoring
  - application insights
  - monitoring tools
  - telemetry
  - New Relic One
---

# New Relic

<GitHubButtons />
## 📚 Learning Resources

### 📖 Essential Documentation
- [New Relic Documentation](https://docs.newrelic.com/) - Official comprehensive documentation
- [APM Guide](https://docs.newrelic.com/docs/apm/) - Application performance monitoring setup
- [NRQL Reference](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/) - Query language documentation
- [Infrastructure Monitoring](https://docs.newrelic.com/docs/infrastructure/) - Server and container monitoring

### 📝 Specialized Guides
- [New Relic Alerts](https://docs.newrelic.com/docs/alerts-applied-intelligence/) - Alerting and AI-powered insights
- [Kubernetes Monitoring](https://docs.newrelic.com/docs/kubernetes-pixie/kubernetes-integration/get-started/introduction-kubernetes-integration/) - Container and orchestration monitoring
- [Distributed Tracing](https://docs.newrelic.com/docs/distributed-tracing/concepts/introduction-distributed-tracing/) - End-to-end request tracking
- [Synthetic Monitoring](https://docs.newrelic.com/docs/synthetics/) - Proactive application monitoring

### 🎥 Video Tutorials
- [New Relic Full Stack Observability](https://www.youtube.com/watch?v=videoid) - Platform overview (30 min)
- [APM Setup and Configuration](https://www.youtube.com/watch?v=videoid2) - Getting started with APM (25 min)
- [NRQL Query Tutorial](https://www.youtube.com/watch?v=videoid3) - Advanced querying techniques (40 min)

### 🎓 Professional Courses
- [New Relic University](https://learn.newrelic.com/) - Free training and certification resources
- [Observability Fundamentals](https://www.udemy.com/course/observability-fundamentals/) - Paid comprehensive course
- [APM Best Practices](https://www.pluralsight.com/courses/new-relic-apm-best-practices) - Paid advanced techniques

### 📚 Books
- "Observability Engineering" by Charity Majors - [Purchase on Amazon](https://www.amazon.com/dp/1492076449)
- "Site Reliability Engineering" by Google - [Free PDF](https://sre.google/sre-book/table-of-contents/) | [Purchase](https://www.amazon.com/dp/149192912X)
- "The Art of Monitoring" by James Turnbull - [Purchase on Amazon](https://www.amazon.com/dp/1491960043)

### 🛠️ Interactive Tools
- [New Relic One](https://one.newrelic.com/) - Unified observability platform
- [New Relic Playground](https://newrelic.com/platform/try-new-relic) - Free trial environment
- [NRQL Query Builder](https://docs.newrelic.com/docs/query-your-data/explore-query-data/query-builder/introduction-query-builder/) - Visual query interface

### 🚀 Ecosystem Tools
- [New Relic CLI](https://github.com/newrelic/newrelic-cli) - Command-line interface for automation
- [Terraform Provider](https://registry.terraform.io/providers/newrelic/newrelic/latest) - Infrastructure as code integration
- [Kubernetes Operator](https://github.com/newrelic/newrelic-kubernetes-operator) - K8s-native deployment
- [Open Telemetry](https://docs.newrelic.com/docs/more-integrations/open-source-telemetry-integrations/opentelemetry/opentelemetry-introduction/) - Vendor-neutral observability

### 🌐 Community & Support
- [New Relic Community](https://discuss.newrelic.com/) - User community and support
- [New Relic Explorers Hub](https://discuss.newrelic.com/) - Technical discussions and best practices
- [New Relic Developer](https://developer.newrelic.com/) - APIs and integration guides

## Understanding New Relic: Full Stack Observability Platform

New Relic is a comprehensive observability platform that provides real-time insights into application performance, infrastructure monitoring, and digital experience. It helps platform engineers monitor, debug, and optimize their systems across the entire stack.

### How New Relic Works
New Relic collects telemetry data from applications, infrastructure, and user interactions through lightweight agents and integrations. The platform ingests metrics, events, logs, and traces, storing them in a unified data platform that enables correlation across different data types.

The system uses machine learning to automatically detect anomalies, predict issues, and provide intelligent alerts. New Relic's query language (NRQL) allows users to explore data interactively, create custom dashboards, and build sophisticated alerting rules based on complex conditions.

### The New Relic Ecosystem
New Relic's ecosystem spans application monitoring (APM), infrastructure monitoring, browser monitoring, mobile monitoring, and synthetic monitoring. The platform integrates with cloud providers, container orchestrators, and popular development tools to provide comprehensive visibility.

Advanced features include distributed tracing for microservices, log management with automatic correlation, and AI-powered incident detection. The ecosystem extends through APIs, webhooks, and integrations with incident management, deployment, and collaboration tools.

### Why New Relic Leads Observability
New Relic has become a leader in observability by focusing on correlation and context across different data types. Unlike point solutions that monitor individual components, New Relic provides a unified view that helps teams understand how application performance relates to infrastructure health and user experience.

The platform's strength lies in its ability to connect the dots between different signals, enabling faster problem resolution and proactive optimization. Its software-first approach means it scales naturally with cloud native architectures.

### Mental Model for Success
Think of New Relic as a comprehensive monitoring dashboard for your entire digital operation, like mission control for a space program. Instead of having separate screens for different systems, everything is integrated into a single view where you can see how each component affects the others.

When something goes wrong, you don't need to check multiple tools - New Relic shows you the complete story from user impact to root cause, like having x-ray vision into your entire technology stack.

### Where to Start Your Journey
1. **Start with APM** - Install an agent for your main application to see immediate value
2. **Add infrastructure monitoring** - Get visibility into servers and containers
3. **Set up basic alerts** - Create notifications for key performance indicators
4. **Explore NRQL queries** - Learn to ask questions of your data
5. **Build custom dashboards** - Create views tailored to your team's needs
6. **Implement distributed tracing** - Understand request flows across services

### Key Concepts to Master
- **Agent deployment** - Installing and configuring monitoring agents
- **NRQL querying** - Writing queries to explore and analyze data
- **Dashboard design** - Creating effective visualizations for different audiences
- **Alert configuration** - Setting up intelligent notifications
- **Distributed tracing** - Understanding request flows across services
- **Custom instrumentation** - Adding business-specific monitoring
- **Data correlation** - Connecting different signals for faster troubleshooting
- **Performance optimization** - Using insights to improve system performance

Begin with out-of-the-box monitoring for your key applications and infrastructure, then gradually customize and extend based on your specific needs and use cases.

## Key Features

- **Application Performance Monitoring (APM)**: Deep application insights and distributed tracing
- **Infrastructure Monitoring**: Server, container, and cloud infrastructure visibility
- **Browser Monitoring**: Real user monitoring and frontend performance
- **Synthetic Monitoring**: Proactive monitoring with automated tests
- **AI-Powered Alerts**: Intelligent anomaly detection and alerting

## Getting Started

### Agent Installation
```bash
# Install Infrastructure Agent (Linux)
curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash
sudo NEW_RELIC_API_KEY=YOUR_API_KEY NEW_RELIC_ACCOUNT_ID=YOUR_ACCOUNT_ID /usr/local/bin/newrelic install

# Docker Infrastructure Agent
docker run \
  -d \
  --name newrelic-infra \
  --network=host \
  --cap-add=SYS_PTRACE \
  --privileged \
  --pid=host \
  -v "/:/host:ro" \
  -v "/var/run/docker.sock:/var/run/docker.sock" \
  -e NRIA_LICENSE_KEY=YOUR_LICENSE_KEY \
  newrelic/infrastructure:latest
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: newrelic
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: newrelic-infra
  namespace: newrelic
spec:
  selector:
    matchLabels:
      name: newrelic-infra
  template:
    metadata:
      labels:
        name: newrelic-infra
    spec:
      serviceAccountName: newrelic-infra
      hostNetwork: true
      hostPID: true
      hostIPC: true
      containers:
      - name: newrelic-infra
        image: newrelic/infrastructure-k8s:latest
        env:
        - name: NRIA_LICENSE_KEY
          valueFrom:
            secretKeyRef:
              name: newrelic-secret
              key: license-key
        - name: NRIA_CLUSTER_NAME
          value: "my-cluster"
        - name: NRIA_VERBOSE
          value: "1"
        resources:
          limits:
            memory: 300Mi
            cpu: 100m
          requests:
            memory: 150Mi
            cpu: 100m
        volumeMounts:
        - name: host-volume
          mountPath: /host
          readOnly: true
        - name: dev-dir
          mountPath: /dev
          readOnly: true
        - name: proc-dir
          mountPath: /host/proc
          readOnly: true
        - name: sys-dir
          mountPath: /host/sys
          readOnly: true
      volumes:
      - name: host-volume
        hostPath:
          path: /
      - name: dev-dir
        hostPath:
          path: /dev
      - name: proc-dir
        hostPath:
          path: /proc
      - name: sys-dir
        hostPath:
          path: /sys
      tolerations:
      - operator: Exists
        effect: NoSchedule
      - operator: Exists
        effect: NoExecute
```

## Application Monitoring

### Python APM Integration
```python
import newrelic.agent

# Initialize agent
newrelic.agent.initialize('/path/to/newrelic.ini')

# Decorator for function monitoring
@newrelic.agent.function_trace()
def critical_function():
    # Your business logic
    pass

# Custom metrics
@newrelic.agent.background_task()
def process_queue():
    queue_size = get_queue_size()
    newrelic.agent.record_custom_metric('Custom/Queue/Size', queue_size)
    
    # Record custom events
    newrelic.agent.record_custom_event('QueueProcessed', {
        'queue_size': queue_size,
        'processing_time': get_processing_time(),
        'environment': 'production'
    })

# Error tracking
def risky_operation():
    try:
        # Potentially failing operation
        return perform_operation()
    except Exception as e:
        newrelic.agent.record_exception()
        raise

# Database query monitoring
@newrelic.agent.database_trace('PostgreSQL', 'SELECT')
def get_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = %s", user_id)

# External service calls
@newrelic.agent.external_trace('httpbin.org', 'POST')
def call_external_api():
    return requests.post('https://httpbin.org/post', json={'data': 'value'})
```

### Node.js APM Integration
```javascript
// Must be first require
require('newrelic');

const express = require('express');
const newrelic = require('newrelic');

const app = express();

app.get('/api/users/:id', async (req, res) => {
  // Custom attributes
  newrelic.addCustomAttribute('user.id', req.params.id);
  newrelic.addCustomAttribute('endpoint', 'get_user');
  
  try {
    const user = await getUserById(req.params.id);
    
    // Record custom metrics
    newrelic.recordMetric('Custom/Users/Retrieved', 1);
    
    // Record custom events
    newrelic.recordCustomEvent('UserAccess', {
      userId: req.params.id,
      timestamp: Date.now(),
      success: true
    });
    
    res.json(user);
  } catch (error) {
    // Error tracking
    newrelic.noticeError(error);
    
    newrelic.recordCustomEvent('UserAccess', {
      userId: req.params.id,
      timestamp: Date.now(),
      success: false,
      error: error.message
    });
    
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Background job monitoring
newrelic.startBackgroundTransaction('processQueue', 'job', () => {
  processQueueItems();
  newrelic.endTransaction();
});

app.listen(3000);
```

### Go APM Integration
```go
package main

import (
    "fmt"
    "net/http"
    "github.com/newrelic/go-agent/v3/newrelic"
)

func main() {
    app, err := newrelic.NewApplication(
        newrelic.ConfigAppName("My Go App"),
        newrelic.ConfigLicense("YOUR_LICENSE_KEY"),
    )
    if err != nil {
        fmt.Println("Error creating New Relic application:", err)
    }

    http.HandleFunc(newrelic.WrapHandleFunc(app, "/users", usersHandler))
    http.ListenAndServe(":8080", nil)
}

func usersHandler(w http.ResponseWriter, r *http.Request) {
    // Get transaction from context
    txn := newrelic.FromContext(r.Context())
    
    // Add custom attributes
    txn.AddAttribute("user.role", "admin")
    txn.AddAttribute("request.path", r.URL.Path)
    
    // Custom segment for database call
    segment := txn.StartSegment("database.query")
    users := getUsersFromDB()
    segment.End()
    
    // Record custom metrics
    txn.Application().RecordCustomMetric("Custom/Users/Count", float64(len(users)))
    
    // Record custom events
    txn.Application().RecordCustomEvent("UserRequest", map[string]interface{}{
        "endpoint": "/users",
        "method":   r.Method,
        "count":    len(users),
    })
    
    w.Header().Set("Content-Type", "application/json")
    fmt.Fprintf(w, `{"users": %d}`, len(users))
}

func getUsersFromDB() []User {
    // Database logic
    return []User{}
}
```

## Custom Dashboards

### Infrastructure Dashboard
```json
{
  "name": "Infrastructure Overview",
  "description": "System metrics and health",
  "pages": [
    {
      "name": "System Health",
      "widgets": [
        {
          "title": "CPU Utilization",
          "visualization": {
            "id": "viz.line"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT average(cpuPercent) FROM SystemSample TIMESERIES",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        },
        {
          "title": "Memory Usage",
          "visualization": {
            "id": "viz.billboard"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT average(memoryUsedPercent) FROM SystemSample",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        },
        {
          "title": "Disk I/O",
          "visualization": {
            "id": "viz.area"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT average(diskReadBytesPerSecond), average(diskWriteBytesPerSecond) FROM StorageSample TIMESERIES",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Application Performance Dashboard
```json
{
  "name": "Application Performance",
  "pages": [
    {
      "name": "Response Times",
      "widgets": [
        {
          "title": "Average Response Time",
          "visualization": {
            "id": "viz.line"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT average(duration) FROM Transaction WHERE appName = 'My App' TIMESERIES",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        },
        {
          "title": "Throughput",
          "visualization": {
            "id": "viz.billboard"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT rate(count(*), 1 minute) FROM Transaction WHERE appName = 'My App'",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        },
        {
          "title": "Error Rate",
          "visualization": {
            "id": "viz.line"
          },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "query": "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'My App' TIMESERIES",
                "accountId": YOUR_ACCOUNT_ID
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## Alerts and Notifications

### NRQL Alert Conditions
```json
{
  "name": "High Error Rate",
  "type": "static",
  "nrql": {
    "query": "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'My App'"
  },
  "condition": {
    "threshold": 5.0,
    "thresholdOccurrences": "at_least_once",
    "thresholdDuration": 300,
    "operator": "above"
  },
  "description": "Alert when error rate exceeds 5%"
}
```

### Infrastructure Alert Conditions
```json
{
  "name": "High CPU Usage",
  "type": "static", 
  "nrql": {
    "query": "SELECT average(cpuPercent) FROM SystemSample WHERE hostname LIKE 'web-%'"
  },
  "condition": {
    "threshold": 80.0,
    "thresholdOccurrences": "at_least_once", 
    "thresholdDuration": 300,
    "operator": "above"
  },
  "description": "Alert when CPU usage exceeds 80%"
}
```

## Synthetic Monitoring

### API Monitor
```javascript
// Simple monitor script
const assert = require('assert');

$http.get('https://api.myapp.com/health', {
  headers: {
    'Authorization': 'Bearer ' + $secure.API_TOKEN
  }
}, function(err, response, body) {
  assert.equal(response.statusCode, 200, 'Expected 200 status code');
  
  const data = JSON.parse(body);
  assert.equal(data.status, 'healthy', 'Expected healthy status');
  assert.ok(data.timestamp, 'Expected timestamp field');
  
  console.log('Health check passed');
});
```

### Browser Monitor
```javascript
// Scripted browser monitor
$browser.get('https://myapp.com/login')
  .then(() => {
    return $browser.findElement($driver.By.id('username')).sendKeys($secure.USERNAME);
  })
  .then(() => {
    return $browser.findElement($driver.By.id('password')).sendKeys($secure.PASSWORD);
  })
  .then(() => {
    return $browser.findElement($driver.By.css('button[type="submit"]')).click();
  })
  .then(() => {
    return $browser.wait($driver.until.elementLocated($driver.By.id('dashboard')), 10000);
  })
  .then(() => {
    console.log('Login flow completed successfully');
  });
```

## NRQL Queries

### Application Performance Queries
```sql
-- Average response time by endpoint
SELECT average(duration) FROM Transaction 
WHERE appName = 'My App' 
FACET name 
SINCE 1 hour ago

-- Error rate trend
SELECT percentage(count(*), WHERE error IS true) 
FROM Transaction 
WHERE appName = 'My App' 
TIMESERIES SINCE 24 hours ago

-- Slowest transactions
SELECT percentile(duration, 95) 
FROM Transaction 
WHERE appName = 'My App' 
FACET name 
SINCE 1 hour ago

-- Database query performance
SELECT average(databaseDuration) 
FROM Transaction 
WHERE appName = 'My App' 
AND databaseDuration IS NOT NULL 
TIMESERIES SINCE 2 hours ago
```

### Infrastructure Queries
```sql
-- CPU usage by host
SELECT average(cpuPercent) 
FROM SystemSample 
FACET hostname 
SINCE 30 minutes ago

-- Memory usage trend
SELECT average(memoryUsedPercent) 
FROM SystemSample 
TIMESERIES SINCE 4 hours ago

-- Disk space usage
SELECT latest(diskUsedPercent) 
FROM StorageSample 
FACET device, hostname 
WHERE mountPoint = '/'

-- Network traffic
SELECT average(receiveBytesPerSecond), average(transmitBytesPerSecond) 
FROM NetworkSample 
TIMESERIES SINCE 1 hour ago
```

## Best Practices

- Use custom attributes for better filtering and grouping
- Implement proper error handling and exception tracking
- Set up meaningful alerts with appropriate thresholds
- Use custom events for business metrics tracking
- Implement distributed tracing for microservices
- Monitor both technical and business KPIs
- Regular review of alert policies and dashboard relevance
- Use synthetic monitoring for proactive issue detection

---

### 📡 Stay Updated

**Release Notes**: [Platform Updates](https://docs.newrelic.com/whats-new/) • [Agent Releases](https://docs.newrelic.com/docs/release-notes/) • [API Changes](https://docs.newrelic.com/docs/apis/)

**Project News**: [New Relic Blog](https://newrelic.com/blog) • [Developer Blog](https://developer.newrelic.com/collect-data/custom-data-types/) • [Product Updates](https://newrelic.com/about/newsroom)

**Community**: [Community Forum](https://discuss.newrelic.com/) • [New Relic University](https://learn.newrelic.com/) • [Developer Hub](https://developer.newrelic.com/)