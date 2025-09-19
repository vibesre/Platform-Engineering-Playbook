# Kubecost

## Overview

Kubecost provides real-time cost visibility and insights for Kubernetes environments. It helps platform engineers monitor, manage, and optimize cloud costs by providing detailed breakdowns of Kubernetes spending across clusters, namespaces, deployments, and services.

## Key Features

- **Real-time Cost Monitoring**: Live cost tracking for Kubernetes resources
- **Multi-dimensional Analytics**: Cost breakdown by namespace, deployment, service, label
- **Resource Efficiency**: CPU and memory utilization insights
- **Budget Alerts**: Proactive cost monitoring and alerting
- **Multi-cloud Support**: Works across AWS, GCP, Azure, and on-premise

## Installation

### Helm Installation
```bash
# Add Kubecost helm repository
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm repo update

# Install Kubecost
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="your-token-here"

# Access the UI
kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090:9090
# Open http://localhost:9090
```

### Configuration with Cloud Billing
```yaml
# values.yaml for AWS
kubecostProductConfigs:
  awsSpotDataRegion: "us-west-2"
  spotLabel: "karpenter.sh/provisioner-name"
  spotLabelValue: "default"

# Configure AWS billing integration
awsSpotDataBucket: "s3://your-spot-data-bucket"
awsSpotDataPrefix: "spot-data-prefix/"

# Service account for AWS permissions
serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/kubecost-role

# Custom pricing
customPricing:
  enabled: true
  costModel:
    CPU: 0.031611
    RAM: 0.004237
    storage: 0.000138
    zoneNetworkEgress: 0.01
    regionNetworkEgress: 0.01
```

## Cost Analysis Queries

### Basic Cost Queries
```bash
# Get costs by namespace
curl "http://localhost:9090/model/allocation" \
  -d window=7d \
  -d aggregate=namespace \
  -G

# Get costs by deployment
curl "http://localhost:9090/model/allocation" \
  -d window=24h \
  -d aggregate=deployment \
  -G

# Get costs by label
curl "http://localhost:9090/model/allocation" \
  -d window=7d \
  -d aggregate=label:app \
  -G

# Get node costs
curl "http://localhost:9090/model/allocation" \
  -d window=24h \
  -d aggregate=node \
  -G
```

### Advanced Cost Analysis
```bash
# Filter by specific namespaces
curl "http://localhost:9090/model/allocation" \
  -d window=7d \
  -d aggregate=deployment \
  -d filterNamespaces=production,staging \
  -G

# Get efficiency metrics
curl "http://localhost:9090/model/allocation" \
  -d window=7d \
  -d aggregate=namespace \
  -d includeEfficiency=true \
  -G

# Get costs with resource breakdown
curl "http://localhost:9090/model/allocation" \
  -d window=24h \
  -d aggregate=deployment \
  -d format=json \
  -d accumulate=false \
  -G
```

## Custom Dashboards

### Grafana Integration
```yaml
# kubecost-grafana-datasource.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-grafana-datasource
  namespace: kubecost
data:
  datasource.yaml: |
    apiVersion: 1
    datasources:
    - name: Kubecost
      type: prometheus
      url: http://kubecost-prometheus-server.kubecost.svc.cluster.local:80
      access: proxy
      isDefault: false
```

### Cost Dashboard Queries
```promql
# Total cluster costs
sum(kubecost_cluster_costs)

# Costs by namespace
sum(kubecost_allocation_cpu_cost + kubecost_allocation_memory_cost + kubecost_allocation_pv_cost) by (namespace)

# CPU efficiency
avg(kubecost_allocation_cpu_efficiency) by (namespace)

# Memory efficiency  
avg(kubecost_allocation_memory_efficiency) by (namespace)

# Most expensive deployments
topk(10, sum(kubecost_allocation_cpu_cost + kubecost_allocation_memory_cost) by (deployment))

# Storage costs by namespace
sum(kubecost_allocation_pv_cost) by (namespace)
```

## Cost Optimization

### Resource Right-sizing
```python
import requests
import json

def get_recommendations():
    """Get right-sizing recommendations from Kubecost"""
    
    url = "http://localhost:9090/model/allocation"
    params = {
        'window': '7d',
        'aggregate': 'deployment',
        'includeEfficiency': 'true'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    recommendations = []
    
    for deployment, metrics in data['data'].items():
        cpu_efficiency = metrics.get('cpuEfficiency', 0)
        memory_efficiency = metrics.get('memoryEfficiency', 0)
        
        if cpu_efficiency < 0.5:  # Less than 50% CPU efficiency
            recommendations.append({
                'deployment': deployment,
                'type': 'cpu_downsize',
                'current_efficiency': cpu_efficiency,
                'potential_savings': metrics['cpuCost'] * (1 - cpu_efficiency)
            })
        
        if memory_efficiency < 0.5:  # Less than 50% memory efficiency
            recommendations.append({
                'deployment': deployment,
                'type': 'memory_downsize', 
                'current_efficiency': memory_efficiency,
                'potential_savings': metrics['memoryCost'] * (1 - memory_efficiency)
            })
    
    return recommendations

# Generate optimization report
recommendations = get_recommendations()
for rec in sorted(recommendations, key=lambda x: x['potential_savings'], reverse=True):
    print(f"Deployment: {rec['deployment']}")
    print(f"Optimization: {rec['type']}")
    print(f"Current Efficiency: {rec['current_efficiency']:.2%}")
    print(f"Potential Monthly Savings: ${rec['potential_savings']:.2f}")
    print("---")
```

### Automated Cost Alerts
```yaml
# kubecost-alerts.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-alerts
  namespace: kubecost
data:
  alerts.yaml: |
    global:
      slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
    
    alerts:
    - name: "namespace-budget-alert"
      aggregateBy: "namespace"
      threshold: 100.0  # $100 threshold
      window: "24h"
      filter:
        - field: "namespace"
          op: "!="
          value: "kube-system"
      actions:
        - type: "slack"
          webhook: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
          channel: "#cost-alerts"
    
    - name: "cluster-daily-spend"
      aggregateBy: "cluster"
      threshold: 500.0  # $500 daily threshold
      window: "24h"
      actions:
        - type: "email"
          emails: ["platform-team@company.com"]
```

## Budgets and Governance

### Budget Configuration
```yaml
# budget-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-budgets
  namespace: kubecost
data:
  budgets.json: |
    {
      "budgets": [
        {
          "name": "production-monthly",
          "amount": 5000,
          "window": "month",
          "aggregateBy": "namespace",
          "filter": {
            "namespace": "production"
          },
          "actions": [
            {
              "type": "alert",
              "threshold": 80,
              "webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
            }
          ]
        },
        {
          "name": "development-weekly", 
          "amount": 200,
          "window": "week",
          "aggregateBy": "namespace",
          "filter": {
            "namespace": "development"
          },
          "actions": [
            {
              "type": "scale_down",
              "threshold": 100,
              "target": "deployment"
            }
          ]
        }
      ]
    }
```

### Policy Enforcement
```yaml
# resource-quotas.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: cost-quota
  namespace: development
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    requests.nvidia.com/gpu: "1"
    persistentvolumeclaims: "10"
    count/pods: "20"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: cost-limits
  namespace: development
spec:
  limits:
  - default:
      cpu: "0.5"
      memory: "512Mi"
    defaultRequest:
      cpu: "0.1"
      memory: "128Mi"
    type: Container
```

## Multi-cluster Cost Management

### Federated Setup
```yaml
# federated-kubecost.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubecost-aggregator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubecost-aggregator
  template:
    metadata:
      labels:
        app: kubecost-aggregator
    spec:
      containers:
      - name: aggregator
        image: kubecost/cost-analyzer:latest
        env:
        - name: AGGREGATOR_MODE
          value: "true"
        - name: FEDERATED_CLUSTERS
          value: "cluster1:http://cluster1-kubecost:9090,cluster2:http://cluster2-kubecost:9090"
        ports:
        - containerPort: 9090
```

### Cross-cluster Cost Analysis
```python
import requests
import json
from datetime import datetime, timedelta

class MultiClusterCostAnalyzer:
    def __init__(self, clusters):
        self.clusters = clusters  # {"cluster1": "http://endpoint1:9090", ...}
    
    def get_cluster_costs(self, window="7d"):
        """Get costs from all clusters"""
        cluster_costs = {}
        
        for cluster_name, endpoint in self.clusters.items():
            try:
                response = requests.get(
                    f"{endpoint}/model/allocation",
                    params={'window': window, 'aggregate': 'cluster'}
                )
                data = response.json()
                cluster_costs[cluster_name] = data['data']
            except Exception as e:
                print(f"Error fetching costs for {cluster_name}: {e}")
                cluster_costs[cluster_name] = None
        
        return cluster_costs
    
    def compare_cluster_efficiency(self, window="7d"):
        """Compare efficiency across clusters"""
        efficiency_data = {}
        
        for cluster_name, endpoint in self.clusters.items():
            try:
                response = requests.get(
                    f"{endpoint}/model/allocation",
                    params={
                        'window': window, 
                        'aggregate': 'cluster',
                        'includeEfficiency': 'true'
                    }
                )
                data = response.json()
                efficiency_data[cluster_name] = {
                    'cpu_efficiency': data['data'][cluster_name]['cpuEfficiency'],
                    'memory_efficiency': data['data'][cluster_name]['memoryEfficiency'],
                    'total_cost': data['data'][cluster_name]['totalCost']
                }
            except Exception as e:
                print(f"Error fetching efficiency for {cluster_name}: {e}")
        
        return efficiency_data

# Usage
clusters = {
    "production": "http://prod-kubecost:9090",
    "staging": "http://staging-kubecost:9090", 
    "development": "http://dev-kubecost:9090"
}

analyzer = MultiClusterCostAnalyzer(clusters)
costs = analyzer.get_cluster_costs()
efficiency = analyzer.compare_cluster_efficiency()

print("Cluster Cost Summary:")
for cluster, data in costs.items():
    if data:
        print(f"{cluster}: ${data[cluster]['totalCost']:.2f}")
```

## Integration with CI/CD

### Cost Gates in Pipelines
```yaml
# .github/workflows/cost-check.yml
name: Cost Impact Analysis

on:
  pull_request:
    branches: [main]

jobs:
  cost-analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        kubectl apply -f k8s/ -n staging-pr-${{ github.event.number }}
    
    - name: Wait for deployment
      run: |
        kubectl wait --for=condition=available deployment/app -n staging-pr-${{ github.event.number }} --timeout=300s
    
    - name: Get cost impact
      id: cost-check
      run: |
        # Wait for cost data to populate
        sleep 300
        
        COST=$(curl -s "http://kubecost:9090/model/allocation" \
          -d window=1h \
          -d aggregate=namespace \
          -d filterNamespaces=staging-pr-${{ github.event.number }} \
          -G | jq '.data["staging-pr-${{ github.event.number }}"].totalCost')
        
        echo "cost=$COST" >> $GITHUB_OUTPUT
        
        if (( $(echo "$COST > 0.50" | bc -l) )); then
          echo "❌ High cost impact: \$$COST per hour" >> $GITHUB_STEP_SUMMARY
          exit 1
        else
          echo "✅ Cost impact acceptable: \$$COST per hour" >> $GITHUB_STEP_SUMMARY
        fi
    
    - name: Cleanup
      if: always()
      run: |
        kubectl delete namespace staging-pr-${{ github.event.number }} --ignore-not-found
```

## Best Practices

- Set up proper cloud billing integration for accurate costs
- Implement resource requests and limits for better cost attribution
- Use labels consistently for meaningful cost breakdowns
- Set up proactive budget alerts and notifications
- Regular review of right-sizing recommendations
- Monitor efficiency metrics alongside costs
- Implement cost-aware autoscaling policies
- Use spot/preemptible instances where appropriate

## Great Resources

- [Kubecost Documentation](https://docs.kubecost.com/) - Official comprehensive documentation
- [Kubecost GitHub](https://github.com/kubecost/cost-analyzer-helm-chart) - Helm chart and configuration
- [Kubecost API Reference](https://docs.kubecost.com/apis) - REST API documentation
- [OpenCost](https://www.opencost.io/) - Open source cost monitoring (Kubecost's open source project)
- [FinOps Foundation](https://www.finops.org/) - Cloud financial management best practices
- [Kubecost Slack](https://kubecost.slack.com/) - Community support and discussions
- [Cost Optimization Guide](https://docs.kubecost.com/cost-optimization) - Best practices for cost optimization