# AppDynamics

## Overview

AppDynamics is an enterprise application performance monitoring (APM) platform that provides deep visibility into application performance, user experience, and business metrics. It's essential for platform engineers managing complex enterprise environments with comprehensive monitoring and business intelligence capabilities.

## Key Features

- **Application Performance Monitoring**: Code-level visibility and diagnostics
- **Business iQ**: Correlate performance with business metrics
- **Real User Monitoring**: End-user experience tracking
- **Infrastructure Monitoring**: Server, database, and network monitoring
- **Machine Learning**: AI-powered anomaly detection and root cause analysis

## Installation

### Java Agent Installation
```bash
# Download AppDynamics Java Agent
wget https://download.appdynamics.com/download/prox/download-file/java/4.5.18.30660/AppServerAgent-4.5.18.30660.zip
unzip AppServerAgent-4.5.18.30660.zip

# Install agent
sudo mkdir -p /opt/appdynamics
sudo cp -r AppServerAgent-4.5.18.30660/* /opt/appdynamics/

# Configure JVM arguments
JAVA_OPTS="$JAVA_OPTS -javaagent:/opt/appdynamics/javaagent.jar"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.agent.applicationName=MyApp"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.agent.tierName=AppServer"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.agent.nodeName=$(hostname)"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.controller.hostName=controller.appdynamics.com"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.controller.port=443"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.controller.ssl.enabled=true"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.agent.accountName=customer1"
JAVA_OPTS="$JAVA_OPTS -Dappdynamics.agent.accountAccessKey=your-access-key"

export JAVA_OPTS
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: java-app
  template:
    metadata:
      labels:
        app: java-app
    spec:
      initContainers:
      - name: appd-agent-attach
        image: appdynamics/java-agent:latest
        command: ['cp', '-ra', '/opt/appdynamics/.', '/opt/temp']
        volumeMounts:
        - mountPath: /opt/temp
          name: appd-agent-repo
      containers:
      - name: java-app
        image: myapp:latest
        env:
        - name: JAVA_OPTS
          value: >-
            -javaagent:/opt/appdynamics/javaagent.jar
            -Dappdynamics.agent.applicationName=$(APPD_APP_NAME)
            -Dappdynamics.agent.tierName=$(APPD_TIER_NAME)
            -Dappdynamics.agent.nodeName=$(HOSTNAME)
            -Dappdynamics.controller.hostName=$(APPD_CONTROLLER_HOST)
            -Dappdynamics.controller.port=$(APPD_CONTROLLER_PORT)
            -Dappdynamics.controller.ssl.enabled=$(APPD_SSL_ENABLED)
            -Dappdynamics.agent.accountName=$(APPD_ACCOUNT_NAME)
            -Dappdynamics.agent.accountAccessKey=$(APPD_ACCESS_KEY)
        - name: APPD_APP_NAME
          value: "MyKubernetesApp"
        - name: APPD_TIER_NAME
          value: "AppServer"
        - name: APPD_CONTROLLER_HOST
          value: "controller.appdynamics.com"
        - name: APPD_CONTROLLER_PORT
          value: "443"
        - name: APPD_SSL_ENABLED
          value: "true"
        - name: APPD_ACCOUNT_NAME
          valueFrom:
            secretKeyRef:
              name: appd-secret
              key: account-name
        - name: APPD_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: appd-secret
              key: access-key
        volumeMounts:
        - mountPath: /opt/appdynamics
          name: appd-agent-repo
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: appd-agent-repo
        emptyDir: {}
---
apiVersion: v1
kind: Secret
metadata:
  name: appd-secret
  namespace: production
type: Opaque
stringData:
  account-name: "customer1"
  access-key: "your-access-key"
```

### Machine Agent for Infrastructure Monitoring
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: appd-machine-agent
  namespace: appdynamics
spec:
  selector:
    matchLabels:
      name: appd-machine-agent
  template:
    metadata:
      labels:
        name: appd-machine-agent
    spec:
      serviceAccount: appd-machine-agent
      hostNetwork: true
      hostPID: true
      containers:
      - name: machine-agent
        image: appdynamics/machine-agent-analytics:latest
        env:
        - name: APPDYNAMICS_CONTROLLER_HOST_NAME
          value: "controller.appdynamics.com"
        - name: APPDYNAMICS_CONTROLLER_PORT
          value: "443"
        - name: APPDYNAMICS_CONTROLLER_SSL_ENABLED
          value: "true"
        - name: APPDYNAMICS_AGENT_ACCOUNT_NAME
          valueFrom:
            secretKeyRef:
              name: appd-secret
              key: account-name
        - name: APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: appd-secret
              key: access-key
        - name: APPDYNAMICS_SIM_ENABLED
          value: "true"
        - name: APPDYNAMICS_DOCKER_ENABLED
          value: "true"
        - name: MACHINE_HIERARCHY_PATH
          value: "Kubernetes|{tier}|{node}"
        volumeMounts:
        - name: proc
          mountPath: /hostroot/proc
          readOnly: true
        - name: sys
          mountPath: /hostroot/sys
          readOnly: true
        - name: docker-sock
          mountPath: /var/run/docker.sock
          readOnly: true
        resources:
          limits:
            memory: 300Mi
            cpu: 200m
          requests:
            memory: 150Mi
            cpu: 100m
        securityContext:
          privileged: true
      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
      tolerations:
      - operator: Exists
        effect: NoSchedule
      - operator: Exists
        effect: NoExecute
```

## Application Configuration

### Java Application Instrumentation
```java
// Custom Business Transaction Detection
@Component
public class PaymentService {
    
    @AppDynamics(value = "process-payment", tier = "PaymentTier")
    public PaymentResult processPayment(PaymentRequest request) {
        // Add custom data collectors
        AppDynamicsAgent.addCustomData("payment.amount", request.getAmount());
        AppDynamicsAgent.addCustomData("payment.method", request.getMethod());
        AppDynamicsAgent.addCustomData("customer.tier", request.getCustomerTier());
        
        try {
            // Business logic
            PaymentResult result = performPayment(request);
            
            // Record business metrics
            AppDynamicsAgent.reportMetric("Payment|Revenue", request.getAmount());
            AppDynamicsAgent.reportMetric("Payment|Count", 1);
            
            return result;
        } catch (PaymentException e) {
            // Record errors with context
            AppDynamicsAgent.reportError(e);
            AppDynamicsAgent.addCustomData("error.code", e.getErrorCode());
            throw e;
        }
    }
    
    @AppDynamics(value = "validate-payment", exitCall = true)
    private boolean validatePayment(PaymentRequest request) {
        // External service call tracking
        AppDynamicsAgent.startExitCall("HTTPS", "payment-gateway.com", 443, "validate");
        
        try {
            // Call external payment gateway
            return paymentGateway.validate(request);
        } finally {
            AppDynamicsAgent.endExitCall();
        }
    }
}

// Custom Health Rules and Metrics
@RestController
public class HealthController {
    
    @GetMapping("/health")
    @AppDynamics("health-check")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> health = new HashMap<>();
        
        // Custom health metrics
        health.put("database", checkDatabaseHealth());
        health.put("cache", checkCacheHealth());
        health.put("external_apis", checkExternalAPIs());
        
        // Report to AppDynamics
        health.entrySet().forEach(entry -> {
            boolean isHealthy = "healthy".equals(entry.getValue());
            AppDynamicsAgent.reportMetric(
                "Health|" + entry.getKey(), 
                isHealthy ? 1 : 0
            );
        });
        
        return ResponseEntity.ok(health);
    }
}
```

### .NET Application Instrumentation
```csharp
// AppDynamics.config
<?xml version="1.0" encoding="utf-8"?>
<appdynamics-agent>
  <controller host="controller.appdynamics.com" 
              port="443" 
              ssl="true"
              account="customer1" 
              access-key="your-access-key" />
  <application name="MyDotNetApp" />
  <tier name="WebTier" />
  <node name="WebServer1" />
  
  <business-transactions>
    <auto-detect>
      <enabled>true</enabled>
    </auto-detect>
    <custom>
      <transaction name="ProcessOrder" 
                   class="OrderService" 
                   method="ProcessOrder" />
    </custom>
  </business-transactions>
  
  <call-graph>
    <max-depth>10</max-depth>
    <include>
      <package name="MyApp.*" />
      <package name="System.Data.*" />
    </include>
  </call-graph>
</appdynamics-agent>

// Custom instrumentation in C#
using AppDynamics.Agent.Api;

[BusinessTransaction]
public class OrderService
{
    [Transaction]
    public async Task<OrderResult> ProcessOrder(Order order)
    {
        // Add custom data
        AppDynamicsSDK.AddCustomData("order.id", order.Id);
        AppDynamicsSDK.AddCustomData("order.amount", order.Amount);
        AppDynamicsSDK.AddCustomData("customer.tier", order.Customer.Tier);
        
        try
        {
            // Start timer for custom metric
            var stopwatch = Stopwatch.StartNew();
            
            // Business logic
            var result = await ProcessOrderInternal(order);
            
            stopwatch.Stop();
            
            // Report custom metrics
            AppDynamicsSDK.ReportMetric("Order|ProcessingTime", stopwatch.ElapsedMilliseconds);
            AppDynamicsSDK.ReportMetric("Order|Revenue", order.Amount);
            
            return result;
        }
        catch (Exception ex)
        {
            AppDynamicsSDK.ReportError(ex);
            AppDynamicsSDK.AddCustomData("error.type", ex.GetType().Name);
            throw;
        }
    }
    
    [ExitCall("Database")]
    private async Task<Customer> GetCustomer(int customerId)
    {
        AppDynamicsSDK.StartExitCall("Database", "CustomerDB", "GetCustomer");
        
        try
        {
            return await customerRepository.GetByIdAsync(customerId);
        }
        finally
        {
            AppDynamicsSDK.EndExitCall();
        }
    }
}
```

### Node.js Application Instrumentation
```javascript
// Install AppDynamics agent
// npm install appdynamics

// app.js - Must be first require
require('appdynamics').profile({
    controllerHostName: 'controller.appdynamics.com',
    controllerPort: 443,
    controllerSslEnabled: true,
    accountName: 'customer1',
    accountAccessKey: 'your-access-key',
    applicationName: 'MyNodeApp',
    tierName: 'NodeTier',
    nodeName: require('os').hostname()
});

const express = require('express');
const appdynamics = require('appdynamics');

const app = express();

app.post('/orders', async (req, res) => {
    const transaction = appdynamics.startTransaction('ProcessOrder');
    
    try {
        const order = req.body;
        
        // Add custom data
        appdynamics.addCustomData(transaction, 'order.id', order.id);
        appdynamics.addCustomData(transaction, 'order.amount', order.amount);
        appdynamics.addCustomData(transaction, 'customer.tier', order.customerTier);
        
        // Start custom timer
        const timer = appdynamics.startTimer('OrderProcessing');
        
        // Process order
        const result = await processOrder(order);
        
        // End timer and report metric
        const duration = appdynamics.endTimer(timer);
        appdynamics.reportMetric('Order|ProcessingTime', duration);
        appdynamics.reportMetric('Order|Revenue', order.amount);
        
        res.json(result);
    } catch (error) {
        appdynamics.reportError(transaction, error);
        appdynamics.addCustomData(transaction, 'error.type', error.name);
        res.status(500).json({ error: error.message });
    } finally {
        appdynamics.endTransaction(transaction);
    }
});

async function processOrder(order) {
    // External API call tracking
    const exitCall = appdynamics.startExitCall(
        'HTTP',
        'payment-service.com',
        443,
        'processPayment'
    );
    
    try {
        const response = await fetch('https://payment-service.com/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(order)
        });
        
        return await response.json();
    } finally {
        appdynamics.endExitCall(exitCall);
    }
}

// Custom health check
app.get('/health', (req, res) => {
    const transaction = appdynamics.startTransaction('HealthCheck');
    
    try {
        const health = {
            database: checkDatabase(),
            cache: checkCache(),
            external_apis: checkExternalAPIs()
        };
        
        // Report health metrics
        Object.entries(health).forEach(([component, status]) => {
            const value = status === 'healthy' ? 1 : 0;
            appdynamics.reportMetric(`Health|${component}`, value);
        });
        
        res.json(health);
    } finally {
        appdynamics.endTransaction(transaction);
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## Business Intelligence Configuration

### Business iQ Metrics
```xml
<!-- Business Transaction Configuration -->
<business-transactions>
  <transaction name="Revenue Generation">
    <match-criteria>
      <uri-match>/api/orders</uri-match>
      <method>POST</method>
    </match-criteria>
    
    <data-collectors>
      <collector name="Order Amount" 
                 type="HTTP_PARAMETER" 
                 parameter="amount" />
      <collector name="Customer Tier" 
                 type="HTTP_PARAMETER" 
                 parameter="customerTier" />
      <collector name="Product Category" 
                 type="CUSTOM_DATA" 
                 key="product.category" />
    </data-collectors>
    
    <business-metrics>
      <metric name="Revenue" 
              type="SUM" 
              collector="Order Amount" />
      <metric name="Order Count" 
              type="COUNT" />
      <metric name="Average Order Value" 
              type="AVERAGE" 
              collector="Order Amount" />
    </business-metrics>
  </transaction>
  
  <transaction name="User Registration">
    <match-criteria>
      <uri-match>/api/users/register</uri-match>
      <method>POST</method>
    </match-criteria>
    
    <data-collectors>
      <collector name="Registration Source" 
                 type="HTTP_PARAMETER" 
                 parameter="source" />
      <collector name="User Type" 
                 type="HTTP_PARAMETER" 
                 parameter="userType" />
    </data-collectors>
    
    <business-metrics>
      <metric name="New User Registrations" 
              type="COUNT" />
    </business-metrics>
  </transaction>
</business-transactions>
```

### Custom Dashboards
```json
{
  "dashboard": {
    "name": "Business Performance Dashboard",
    "widgets": [
      {
        "type": "metric",
        "title": "Revenue Trend",
        "metric": "Business Transaction Performance|Business Transactions|Revenue Generation|Individual Nodes|*|Calls per Minute",
        "timeRange": "last_24_hours"
      },
      {
        "type": "metric",
        "title": "Average Order Value",
        "metric": "Business Transaction Performance|Business Transactions|Revenue Generation|Average Response Time (ms)",
        "timeRange": "last_24_hours"
      },
      {
        "type": "health_rule",
        "title": "Application Health",
        "healthRules": [
          "Overall Application Performance",
          "Business Transaction Performance",
          "Infrastructure Performance"
        ]
      },
      {
        "type": "flow_map",
        "title": "Application Flow",
        "application": "MyApp",
        "timeRange": "last_1_hour"
      }
    ]
  }
}
```

## Alerting and Health Rules

### Health Rule Configuration
```xml
<health-rules>
  <health-rule name="Business Transaction Performance">
    <description>Monitor critical business transaction performance</description>
    <enabled>true</enabled>
    
    <affects>
      <business-transactions>
        <transaction name="Revenue Generation" />
        <transaction name="User Registration" />
      </business-transactions>
    </affects>
    
    <critical-condition>
      <condition-expression>
        <and>
          <metric-expression>
            <metric-path>Business Transaction Performance|Business Transactions|*|Average Response Time (ms)</metric-path>
            <operator>GREATER_THAN</operator>
            <value>2000</value>
          </metric-expression>
          <metric-expression>
            <metric-path>Business Transaction Performance|Business Transactions|*|Calls per Minute</metric-path>
            <operator>GREATER_THAN</operator>
            <value>10</value>
          </metric-expression>
        </and>
      </condition-expression>
      <trigger-on-no-data>false</trigger-on-no-data>
    </critical-condition>
    
    <warning-condition>
      <condition-expression>
        <metric-expression>
          <metric-path>Business Transaction Performance|Business Transactions|*|Average Response Time (ms)</metric-path>
          <operator>GREATER_THAN</operator>
          <value>1000</value>
        </metric-expression>
      </condition-expression>
    </warning-condition>
  </health-rule>
  
  <health-rule name="Error Rate Monitoring">
    <description>Monitor application error rates</description>
    <enabled>true</enabled>
    
    <affects>
      <application-components>
        <component name="All Tiers" />
      </application-components>
    </affects>
    
    <critical-condition>
      <condition-expression>
        <metric-expression>
          <metric-path>Overall Application Performance|*|Errors per Minute</metric-path>
          <operator>GREATER_THAN</operator>
          <value>10</value>
        </metric-expression>
      </condition-expression>
    </critical-condition>
  </health-rule>
</health-rules>
```

### Notification Policies
```json
{
  "policies": [
    {
      "name": "Critical Alert Policy",
      "enabled": true,
      "events": [
        "HEALTH_RULE_VIOLATION_CRITICAL",
        "APPLICATION_ERROR_RATE_CRITICAL"
      ],
      "actions": [
        {
          "type": "EMAIL",
          "recipients": ["platform-team@company.com"],
          "subject": "Critical Alert: {{application_name}}",
          "template": "critical-alert-template"
        },
        {
          "type": "SLACK",
          "webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
          "channel": "#alerts",
          "message": "🚨 Critical Alert: {{health_rule_name}} in {{application_name}}"
        },
        {
          "type": "PAGERDUTY",
          "integration_key": "your-pagerduty-integration-key",
          "severity": "critical"
        }
      ]
    },
    {
      "name": "Warning Alert Policy",
      "enabled": true,
      "events": [
        "HEALTH_RULE_VIOLATION_WARNING"
      ],
      "actions": [
        {
          "type": "EMAIL",
          "recipients": ["dev-team@company.com"]
        },
        {
          "type": "SLACK",
          "webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
          "channel": "#monitoring",
          "message": "⚠️ Warning: {{health_rule_name}} in {{application_name}}"
        }
      ]
    }
  ]
}
```

## API Integration

### REST API Usage
```python
import requests
import json
from datetime import datetime, timedelta

class AppDynamicsAPI:
    def __init__(self, controller_url, username, password, account):
        self.base_url = f"https://{controller_url}"
        self.account = account
        self.session = requests.Session()
        self.session.auth = (f"{username}@{account}", password)
    
    def get_applications(self):
        """Get all applications"""
        url = f"{self.base_url}/controller/rest/applications"
        response = self.session.get(url, params={'output': 'json'})
        return response.json()
    
    def get_business_transactions(self, app_id):
        """Get business transactions for an application"""
        url = f"{self.base_url}/controller/rest/applications/{app_id}/business-transactions"
        response = self.session.get(url, params={'output': 'json'})
        return response.json()
    
    def get_metric_data(self, app_id, metric_path, duration_minutes=60):
        """Get metric data"""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=duration_minutes)
        
        url = f"{self.base_url}/controller/rest/applications/{app_id}/metric-data"
        params = {
            'metric-path': metric_path,
            'time-range-type': 'BETWEEN_TIMES',
            'start-time': int(start_time.timestamp() * 1000),
            'end-time': int(end_time.timestamp() * 1000),
            'rollup': 'false',
            'output': 'json'
        }
        
        response = self.session.get(url, params=params)
        return response.json()
    
    def get_snapshots(self, app_id, severity='CRITICAL', duration_minutes=60):
        """Get transaction snapshots"""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=duration_minutes)
        
        url = f"{self.base_url}/controller/rest/applications/{app_id}/request-snapshots"
        params = {
            'time-range-type': 'BETWEEN_TIMES',
            'start-time': int(start_time.timestamp() * 1000),
            'end-time': int(end_time.timestamp() * 1000),
            'severity': severity,
            'output': 'json'
        }
        
        response = self.session.get(url, params=params)
        return response.json()
    
    def create_custom_dashboard(self, dashboard_config):
        """Create custom dashboard"""
        url = f"{self.base_url}/controller/CustomDashboardImportExportServlet"
        
        response = self.session.post(
            url,
            data={'importJSON': json.dumps(dashboard_config)}
        )
        return response.text

# Usage example
api = AppDynamicsAPI(
    controller_url='controller.appdynamics.com',
    username='admin',
    password='password',
    account='customer1'
)

# Get application performance data
apps = api.get_applications()
for app in apps:
    print(f"Application: {app['name']} (ID: {app['id']})")
    
    # Get response time metrics
    response_time_data = api.get_metric_data(
        app['id'],
        'Overall Application Performance|Average Response Time (ms)'
    )
    
    # Get error snapshots
    error_snapshots = api.get_snapshots(app['id'], 'CRITICAL')
    
    print(f"  Response Time Points: {len(response_time_data)}")
    print(f"  Critical Snapshots: {len(error_snapshots)}")
```

## Integration with Other Tools

### Grafana Integration
```json
{
  "datasource": {
    "name": "AppDynamics",
    "type": "appdynamics",
    "url": "https://controller.appdynamics.com",
    "access": "proxy",
    "basicAuth": true,
    "basicAuthUser": "admin@customer1",
    "basicAuthPassword": "password",
    "jsonData": {
      "account": "customer1",
      "defaultApplication": "MyApp"
    }
  },
  "dashboard": {
    "title": "AppDynamics Metrics",
    "panels": [
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "application": "MyApp",
            "metricPath": "Overall Application Performance|Average Response Time (ms)"
          }
        ]
      },
      {
        "title": "Throughput",
        "type": "graph",
        "targets": [
          {
            "application": "MyApp",
            "metricPath": "Overall Application Performance|Calls per Minute"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

- Implement proper business transaction detection rules
- Use custom data collectors for business-relevant information
- Set up meaningful health rules with appropriate thresholds
- Correlate application performance with business metrics
- Regular review and optimization of monitoring configuration
- Implement proper role-based access control
- Use machine learning features for proactive issue detection
- Regular maintenance of custom dashboards and reports

## Great Resources

- [AppDynamics Documentation](https://docs.appdynamics.com/) - Official comprehensive documentation
- [AppDynamics University](https://university.appdynamics.com/) - Training and certification
- [AppDynamics Community](https://community.appdynamics.com/) - Forums and knowledge base
- [AppDynamics GitHub](https://github.com/Appdynamics) - Sample applications and tools
- [AppDynamics Extensions](https://www.appdynamics.com/community/exchange/) - Community extensions
- [APM Best Practices](https://www.appdynamics.com/blog/apm/apm-best-practices/) - Performance monitoring guide
- [Business iQ Guide](https://docs.appdynamics.com/display/PRO45/Business+iQ) - Business intelligence features
- [Machine Learning Guide](https://docs.appdynamics.com/display/PRO45/Cognition+Engine) - AI-powered monitoring