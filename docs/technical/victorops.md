# VictorOps (Splunk On-Call)

## Overview

VictorOps, now known as Splunk On-Call, is an incident management platform that helps platform engineering teams respond to critical incidents efficiently. It provides intelligent alert routing, collaborative incident response, and comprehensive post-incident analysis to minimize downtime and improve system reliability.

## Key Features

- **Intelligent Alert Routing**: Context-aware alert routing and escalation
- **Real-Time Collaboration**: Team coordination during incident response
- **Timeline Management**: Complete incident timeline and communication history
- **Mobile-First Response**: Full-featured mobile apps for on-the-go incident management
- **Post-Incident Analysis**: Detailed reporting and continuous improvement tools

## Setup and Configuration

### Team Configuration
```json
{
  "team": {
    "name": "Platform Engineering",
    "slug": "platform-eng",
    "membership_type": "specified",
    "members": [
      {
        "username": "alice@company.com",
        "role": "admin"
      },
      {
        "username": "bob@company.com",
        "role": "user"
      },
      {
        "username": "charlie@company.com",
        "role": "user"
      }
    ]
  }
}
```

### Escalation Policy
```json
{
  "policy": {
    "name": "Production Critical Escalation",
    "team_id": "team-platform-eng",
    "steps": [
      {
        "timeout": 300,
        "entries": [
          {
            "type": "user",
            "username": "oncall-primary"
          }
        ]
      },
      {
        "timeout": 900,
        "entries": [
          {
            "type": "rotation_group",
            "slug": "platform-secondary"
          }
        ]
      },
      {
        "timeout": 1800,
        "entries": [
          {
            "type": "user",
            "username": "platform-manager"
          }
        ]
      }
    ],
    "ignore_custom_paging_policies": false
  }
}
```

### On-Call Schedule
```json
{
  "rotation": {
    "name": "Platform Primary On-Call",
    "team_id": "team-platform-eng",
    "start": "2024-01-01T00:00:00Z",
    "rotation_type": "manual",
    "shift_length": 604800,
    "shifts": [
      {
        "start": "2024-01-01T08:00:00Z",
        "end": "2024-01-08T08:00:00Z",
        "user": {
          "username": "alice@company.com"
        }
      },
      {
        "start": "2024-01-08T08:00:00Z",
        "end": "2024-01-15T08:00:00Z",
        "user": {
          "username": "bob@company.com"
        }
      },
      {
        "start": "2024-01-15T08:00:00Z",
        "end": "2024-01-22T08:00:00Z",
        "user": {
          "username": "charlie@company.com"
        }
      }
    ],
    "restrictions": [
      {
        "type": "weekly_restriction",
        "start_day": 1,
        "start_time": "08:00",
        "end_day": 5,
        "end_time": "18:00"
      }
    ]
  }
}
```

## Integration Examples

### Prometheus AlertManager
```yaml
# alertmanager.yml
global:
  victorops_api_url: 'https://alert.victorops.com/integrations/generic/20131114/alert/'

route:
  receiver: 'default'
  routes:
  - match:
      severity: critical
    receiver: victorops-critical
  - match:
      severity: warning
    receiver: victorops-warning

receivers:
- name: 'default'
  webhook_configs:
  - url: 'http://localhost:9093/api/v1/alerts'

- name: victorops-critical
  victorops_configs:
  - api_key: 'your-api-key'
    routing_key: 'platform-critical'
    message_type: 'CRITICAL'
    entity_display_name: '{{ range .Alerts }}{{ .Labels.alertname }}{{ end }}'
    state_message: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    custom_fields:
      alertname: '{{ .GroupLabels.alertname }}'
      instance: '{{ range .Alerts }}{{ .Labels.instance }}{{ end }}'
      severity: '{{ range .Alerts }}{{ .Labels.severity }}{{ end }}'
      description: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
      runbook_url: '{{ range .Alerts }}{{ .Annotations.runbook_url }}{{ end }}'
      grafana_url: 'https://grafana.example.com/d/alerts'

- name: victorops-warning
  victorops_configs:
  - api_key: 'your-api-key'
    routing_key: 'platform-warning'
    message_type: 'WARNING'
    entity_display_name: '{{ range .Alerts }}{{ .Labels.alertname }}{{ end }}'
    state_message: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

### Kubernetes Alert Integration
```yaml
# kubernetes-alert-rules.yml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kubernetes-victorops-alerts
  namespace: monitoring
spec:
  groups:
  - name: kubernetes.rules
    rules:
    - alert: KubernetesNodeDown
      expr: up{job="kubernetes-nodes"} == 0
      for: 5m
      labels:
        severity: critical
        team: platform
        service: kubernetes
        routing_key: platform-critical
      annotations:
        summary: "Kubernetes node {{ $labels.instance }} is down"
        description: "Node {{ $labels.instance }} has been unreachable for more than 5 minutes"
        runbook_url: "https://runbooks.example.com/kubernetes/node-down"
        
    - alert: KubernetesPodCrashLooping
      expr: increase(kube_pod_container_status_restarts_total[1h]) > 5
      for: 2m
      labels:
        severity: warning
        team: platform
        service: kubernetes
        routing_key: platform-warning
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
        description: "Pod has restarted {{ $value }} times in the last hour"
        runbook_url: "https://runbooks.example.com/kubernetes/crashloop"
        
    - alert: KubernetesDeploymentReplicasMismatch
      expr: kube_deployment_spec_replicas != kube_deployment_status_ready_replicas
      for: 10m
      labels:
        severity: warning
        team: platform
        service: kubernetes
        routing_key: platform-warning
      annotations:
        summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} has mismatched replicas"
        description: "Deployment has {{ $labels.spec_replicas }} desired but {{ $labels.ready_replicas }} ready replicas"
```

### Application Integration (Python)
```python
import requests
import json
from datetime import datetime
from enum import Enum

class VictorOpsMessageType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ACKNOWLEDGEMENT = "ACKNOWLEDGEMENT"
    CRITICAL = "CRITICAL"
    RECOVERY = "RECOVERY"

class VictorOpsClient:
    def __init__(self, api_key, routing_key):
        self.api_key = api_key
        self.routing_key = routing_key
        self.base_url = "https://alert.victorops.com/integrations/generic/20131114/alert"
    
    def send_alert(self, message_type, entity_id, entity_display_name, 
                   state_message, details=None, monitoring_tool="custom"):
        """Send alert to VictorOps"""
        url = f"{self.base_url}/{self.api_key}/{self.routing_key}"
        
        payload = {
            "message_type": message_type.value,
            "entity_id": entity_id,
            "entity_display_name": entity_display_name,
            "state_message": state_message,
            "state_start_time": int(datetime.utcnow().timestamp()),
            "monitoring_tool": monitoring_tool
        }
        
        if details:
            payload.update(details)
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        return response
    
    def create_incident(self, entity_id, title, description, severity="CRITICAL", 
                       custom_fields=None):
        """Create a new incident"""
        details = {
            "incident_title": title,
            "incident_description": description,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "application"
        }
        
        if custom_fields:
            details.update(custom_fields)
        
        return self.send_alert(
            message_type=VictorOpsMessageType.CRITICAL,
            entity_id=entity_id,
            entity_display_name=title,
            state_message=description,
            details=details
        )
    
    def resolve_incident(self, entity_id, resolution_message="Issue resolved"):
        """Resolve an existing incident"""
        return self.send_alert(
            message_type=VictorOpsMessageType.RECOVERY,
            entity_id=entity_id,
            entity_display_name="Incident Resolved",
            state_message=resolution_message,
            details={"resolution_time": datetime.utcnow().isoformat()}
        )

# Usage examples
vo_client = VictorOpsClient(
    api_key="your-api-key",
    routing_key="platform-critical"
)

# Application error monitoring
def handle_application_error(error, context):
    """Handle critical application errors"""
    entity_id = f"app-error-{context.get('service', 'unknown')}-{context.get('request_id', 'unknown')}"
    
    custom_fields = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "service_name": context.get("service", "unknown"),
        "environment": context.get("environment", "production"),
        "user_id": context.get("user_id"),
        "request_id": context.get("request_id"),
        "stack_trace": str(error.__traceback__) if error.__traceback__ else None,
        "grafana_dashboard": f"https://grafana.example.com/d/app-errors?var-service={context.get('service')}",
        "logs_url": f"https://logs.example.com/search?request_id={context.get('request_id')}"
    }
    
    response = vo_client.create_incident(
        entity_id=entity_id,
        title=f"Critical Application Error: {str(error)}",
        description=f"Critical error in {context.get('service')} service: {str(error)}",
        severity="CRITICAL",
        custom_fields=custom_fields
    )
    
    print(f"VictorOps incident created: {response.status_code}")
    return response

# Infrastructure monitoring
def monitor_infrastructure_health():
    """Monitor infrastructure components"""
    try:
        # Check database connectivity
        db_health = check_database_health()
        if not db_health['healthy']:
            vo_client.create_incident(
                entity_id="database-connectivity",
                title="Database Connectivity Issue",
                description=f"Database connection failed: {db_health['error']}",
                severity="CRITICAL",
                custom_fields={
                    "component": "database",
                    "database_type": "postgresql",
                    "last_successful_check": db_health.get('last_success'),
                    "error_details": db_health['error'],
                    "health_check_url": "https://monitoring.example.com/db-health"
                }
            )
        
        # Check Kubernetes cluster health
        k8s_health = check_kubernetes_health()
        if not k8s_health['healthy']:
            vo_client.create_incident(
                entity_id="kubernetes-cluster-health",
                title="Kubernetes Cluster Health Issue",
                description=f"Cluster health check failed: {k8s_health['issues']}",
                severity="CRITICAL",
                custom_fields={
                    "component": "kubernetes",
                    "cluster_name": k8s_health['cluster_name'],
                    "unhealthy_nodes": k8s_health.get('unhealthy_nodes', []),
                    "failed_pods": k8s_health.get('failed_pods', []),
                    "kubectl_dashboard": "https://k8s-dashboard.example.com"
                }
            )
        
        # Check external service dependencies
        external_services = check_external_services()
        for service, status in external_services.items():
            if not status['healthy']:
                vo_client.create_incident(
                    entity_id=f"external-service-{service}",
                    title=f"External Service {service} Unavailable",
                    description=f"External dependency {service} is experiencing issues",
                    severity="WARNING",
                    custom_fields={
                        "component": "external_dependency",
                        "service_name": service,
                        "response_time": status.get('response_time'),
                        "error_rate": status.get('error_rate'),
                        "last_success": status.get('last_success'),
                        "service_url": status.get('url')
                    }
                )
    
    except Exception as e:
        # Alert on monitoring system failure
        vo_client.create_incident(
            entity_id="monitoring-system-failure",
            title="Infrastructure Monitoring Failure",
            description=f"Health monitoring system failed: {str(e)}",
            severity="CRITICAL",
            custom_fields={
                "component": "monitoring",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )

# Performance monitoring
def monitor_application_performance():
    """Monitor application performance metrics"""
    try:
        metrics = get_application_metrics()
        
        # Check response time thresholds
        if metrics['avg_response_time'] > 2000:  # 2 seconds
            vo_client.send_alert(
                message_type=VictorOpsMessageType.WARNING,
                entity_id="high-response-time",
                entity_display_name="High Response Time Detected",
                state_message=f"Average response time is {metrics['avg_response_time']}ms",
                details={
                    "metric_type": "performance",
                    "current_value": metrics['avg_response_time'],
                    "threshold": 2000,
                    "unit": "milliseconds",
                    "dashboard_url": "https://grafana.example.com/d/performance"
                }
            )
        
        # Check error rate thresholds
        if metrics['error_rate'] > 0.05:  # 5% error rate
            vo_client.send_alert(
                message_type=VictorOpsMessageType.CRITICAL,
                entity_id="high-error-rate",
                entity_display_name="High Error Rate Detected",
                state_message=f"Error rate is {metrics['error_rate']*100:.1f}%",
                details={
                    "metric_type": "error_rate",
                    "current_value": metrics['error_rate'],
                    "threshold": 0.05,
                    "errors_dashboard": "https://grafana.example.com/d/errors"
                }
            )
        
        # Check throughput drops
        if metrics['requests_per_minute'] < metrics['baseline_rpm'] * 0.5:
            vo_client.send_alert(
                message_type=VictorOpsMessageType.WARNING,
                entity_id="low-throughput",
                entity_display_name="Low Traffic Volume",
                state_message=f"Traffic is {metrics['requests_per_minute']} RPM (expected: {metrics['baseline_rpm']})",
                details={
                    "metric_type": "throughput",
                    "current_rpm": metrics['requests_per_minute'],
                    "baseline_rpm": metrics['baseline_rpm'],
                    "traffic_dashboard": "https://grafana.example.com/d/traffic"
                }
            )
    
    except Exception as e:
        vo_client.create_incident(
            entity_id="performance-monitoring-failure",
            title="Performance Monitoring Error",
            description=f"Failed to collect performance metrics: {str(e)}",
            severity="WARNING"
        )

# Placeholder functions for health checks
def check_database_health():
    """Check database connectivity and performance"""
    # Implementation would check actual database
    return {"healthy": True, "last_success": datetime.utcnow().isoformat()}

def check_kubernetes_health():
    """Check Kubernetes cluster health"""
    # Implementation would check actual K8s cluster
    return {"healthy": True, "cluster_name": "production"}

def check_external_services():
    """Check external service dependencies"""
    # Implementation would check actual external services
    return {
        "payment-gateway": {"healthy": True, "response_time": 150},
        "email-service": {"healthy": True, "response_time": 75}
    }

def get_application_metrics():
    """Get current application performance metrics"""
    # Implementation would get actual metrics
    return {
        "avg_response_time": 150,
        "error_rate": 0.01,
        "requests_per_minute": 1000,
        "baseline_rpm": 1200
    }
```

### Slack Integration
```python
def setup_victorops_slack_integration():
    """Configure VictorOps Slack integration"""
    integration_config = {
        "name": "Platform Team Slack",
        "type": "slack",
        "settings": {
            "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
            "channel": "#platform-incidents",
            "username": "VictorOps",
            "icon_emoji": ":rotating_light:",
            "notify_on": [
                "incident.triggered",
                "incident.acknowledged",
                "incident.resolved",
                "incident.escalated"
            ],
            "message_template": {
                "triggered": "🚨 *INCIDENT TRIGGERED*\n*Title:* {incident_title}\n*State:* {state_message}\n*Assigned:* {assigned_user}\n*Timeline:* <{timeline_url}|View Timeline>",
                "acknowledged": "✅ *INCIDENT ACKNOWLEDGED*\n*Title:* {incident_title}\n*Acknowledged by:* {ack_user}\n*Timeline:* <{timeline_url}|View Timeline>",
                "resolved": "🎉 *INCIDENT RESOLVED*\n*Title:* {incident_title}\n*Resolved by:* {resolved_user}\n*Duration:* {incident_duration}\n*Timeline:* <{timeline_url}|View Timeline>"
            }
        }
    }
    
    return integration_config

# Custom Slack notification for complex incidents
def send_detailed_slack_notification(incident_data):
    """Send detailed incident information to Slack"""
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    
    # Determine color based on severity
    color_map = {
        "CRITICAL": "#FF0000",
        "WARNING": "#FFA500",
        "INFO": "#00FF00"
    }
    
    color = color_map.get(incident_data.get('severity', 'WARNING'), "#FFA500")
    
    # Build rich Slack message
    slack_message = {
        "username": "VictorOps",
        "icon_emoji": ":rotating_light:",
        "attachments": [
            {
                "color": color,
                "fallback": f"VictorOps Incident: {incident_data['title']}",
                "title": f"🚨 {incident_data['title']}",
                "title_link": incident_data.get('timeline_url'),
                "text": incident_data['description'],
                "fields": [
                    {
                        "title": "Severity",
                        "value": incident_data.get('severity', 'Unknown'),
                        "short": True
                    },
                    {
                        "title": "Service",
                        "value": incident_data.get('service', 'Unknown'),
                        "short": True
                    },
                    {
                        "title": "Environment",
                        "value": incident_data.get('environment', 'Production'),
                        "short": True
                    },
                    {
                        "title": "On-Call Engineer",
                        "value": incident_data.get('assigned_user', 'Unassigned'),
                        "short": True
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": "View Timeline",
                        "url": incident_data.get('timeline_url'),
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": "View Runbook",
                        "url": incident_data.get('runbook_url'),
                        "style": "default"
                    },
                    {
                        "type": "button",
                        "text": "Check Grafana",
                        "url": incident_data.get('grafana_url'),
                        "style": "default"
                    }
                ],
                "footer": "VictorOps",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }
    
    response = requests.post(webhook_url, json=slack_message)
    return response
```

## REST API Integration

### VictorOps REST API Usage
```python
import requests
from datetime import datetime, timedelta

class VictorOpsAPI:
    def __init__(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key
        self.base_url = "https://api.victorops.com/api-public/v1"
        self.headers = {
            "X-VO-Api-Id": api_id,
            "X-VO-Api-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def get_incidents(self, status="triggered,acknowledged", limit=25):
        """Get current incidents"""
        url = f"{self.base_url}/incidents"
        params = {
            "statuses": status,
            "limit": limit,
            "sortOrder": "desc"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def get_oncall_users(self, team=None):
        """Get current on-call users"""
        url = f"{self.base_url}/oncall/current"
        params = {}
        if team:
            params["team"] = team
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def create_maintenance_mode(self, team, description, start_time, end_time):
        """Create maintenance mode"""
        url = f"{self.base_url}/maintenancemode"
        data = {
            "teams": [team],
            "description": description,
            "startTime": start_time,
            "endTime": end_time
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def acknowledge_incident(self, incident_number, ack_user, ack_message=""):
        """Acknowledge an incident"""
        url = f"{self.base_url}/incidents/ack"
        data = {
            "userName": ack_user,
            "incidentNames": [incident_number],
            "message": ack_message
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()
    
    def resolve_incident(self, incident_number, resolve_user, resolve_message=""):
        """Resolve an incident"""
        url = f"{self.base_url}/incidents/resolve"
        data = {
            "userName": resolve_user,
            "incidentNames": [incident_number],
            "message": resolve_message
        }
        
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()
    
    def get_incident_timeline(self, incident_number):
        """Get incident timeline"""
        url = f"{self.base_url}/incidents/{incident_number}/log"
        
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def create_incident_postmortem(self, incident_number, postmortem_data):
        """Create incident postmortem"""
        url = f"{self.base_url}/incidents/{incident_number}/postmortem"
        
        response = requests.post(url, headers=self.headers, json=postmortem_data)
        return response.json()

# Usage examples
vo_api = VictorOpsAPI(
    api_id="your-api-id",
    api_key="your-api-key"
)

# Automated incident management
def automated_incident_workflow():
    """Automated incident management workflow"""
    # Get current critical incidents
    incidents = vo_api.get_incidents(status="triggered")
    
    for incident in incidents.get('incidents', []):
        incident_number = incident['incidentNumber']
        entity_id = incident['entityId']
        
        # Check if incident is infrastructure-related and auto-remediable
        if 'disk-space' in entity_id.lower():
            success = attempt_disk_cleanup(entity_id)
            if success:
                vo_api.resolve_incident(
                    incident_number,
                    "automation-bot",
                    "Automatically resolved: Disk space cleaned up successfully"
                )
        
        elif 'service-restart' in entity_id.lower():
            success = attempt_service_restart(entity_id)
            if success:
                vo_api.acknowledge_incident(
                    incident_number,
                    "automation-bot",
                    "Service restart initiated. Monitoring for recovery."
                )

def attempt_disk_cleanup(entity_id):
    """Attempt automated disk cleanup"""
    # Implementation would perform actual cleanup
    print(f"Attempting disk cleanup for {entity_id}")
    return True

def attempt_service_restart(entity_id):
    """Attempt automated service restart"""
    # Implementation would restart actual service
    print(f"Attempting service restart for {entity_id}")
    return True

# Reporting and analytics
def generate_incident_report(days=30):
    """Generate incident summary report"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get all incidents from the period
    all_incidents = []
    offset = 0
    limit = 100
    
    while True:
        incidents = vo_api.get_incidents(limit=limit, offset=offset)
        incident_list = incidents.get('incidents', [])
        
        if not incident_list:
            break
        
        # Filter by date range
        for incident in incident_list:
            incident_date = datetime.fromisoformat(incident['startTime'].replace('Z', '+00:00'))
            if start_date <= incident_date <= end_date:
                all_incidents.append(incident)
        
        offset += limit
    
    # Calculate metrics
    total_incidents = len(all_incidents)
    critical_incidents = len([i for i in all_incidents if i.get('currentPhase') == 'UNACKED'])
    resolved_incidents = len([i for i in all_incidents if i.get('currentPhase') == 'RESOLVED'])
    
    # Calculate MTTR (Mean Time To Resolution)
    resolution_times = []
    for incident in all_incidents:
        if incident.get('currentPhase') == 'RESOLVED' and incident.get('startTime') and incident.get('endTime'):
            start = datetime.fromisoformat(incident['startTime'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(incident['endTime'].replace('Z', '+00:00'))
            resolution_times.append((end - start).total_seconds() / 3600)  # hours
    
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    report = {
        "period_days": days,
        "total_incidents": total_incidents,
        "critical_incidents": critical_incidents,
        "resolved_incidents": resolved_incidents,
        "resolution_rate": (resolved_incidents / total_incidents * 100) if total_incidents > 0 else 0,
        "avg_resolution_time_hours": avg_resolution_time,
        "incidents_by_service": {},
        "incidents_by_severity": {}
    }
    
    # Group by service and severity
    for incident in all_incidents:
        service = incident.get('service', 'unknown')
        severity = incident.get('currentPhase', 'unknown')
        
        report["incidents_by_service"][service] = report["incidents_by_service"].get(service, 0) + 1
        report["incidents_by_severity"][severity] = report["incidents_by_severity"].get(severity, 0) + 1
    
    return report

# Generate and print report
report = generate_incident_report(30)
print(f"Incident Report (Last 30 days):")
print(f"Total Incidents: {report['total_incidents']}")
print(f"Resolution Rate: {report['resolution_rate']:.1f}%")
print(f"Average Resolution Time: {report['avg_resolution_time_hours']:.1f} hours")
print(f"Service Breakdown: {report['incidents_by_service']}")
```

## Automation and Workflows

### Incident Response Automation
```python
class VictorOpsAutomation:
    def __init__(self, vo_api, vo_client):
        self.vo_api = vo_api
        self.vo_client = vo_client
        self.response_rules = []
    
    def add_response_rule(self, pattern, action, conditions=None):
        """Add automated response rule"""
        rule = {
            "pattern": pattern,
            "action": action,
            "conditions": conditions or {}
        }
        self.response_rules.append(rule)
    
    def process_incident(self, incident):
        """Process incident with automated responses"""
        entity_id = incident.get('entityId', '')
        current_phase = incident.get('currentPhase', '')
        
        for rule in self.response_rules:
            if self._matches_pattern(entity_id, rule['pattern']):
                if self._meets_conditions(incident, rule['conditions']):
                    self._execute_action(incident, rule['action'])
    
    def _matches_pattern(self, entity_id, pattern):
        """Check if entity_id matches pattern"""
        return pattern.lower() in entity_id.lower()
    
    def _meets_conditions(self, incident, conditions):
        """Check if incident meets conditions"""
        for key, value in conditions.items():
            if incident.get(key) != value:
                return False
        return True
    
    def _execute_action(self, incident, action):
        """Execute automated action"""
        action_type = action.get('type')
        
        if action_type == 'auto_acknowledge':
            self._auto_acknowledge(incident, action)
        elif action_type == 'auto_resolve':
            self._auto_resolve(incident, action)
        elif action_type == 'escalate':
            self._escalate_incident(incident, action)
        elif action_type == 'create_ticket':
            self._create_support_ticket(incident, action)
        elif action_type == 'run_playbook':
            self._execute_playbook(incident, action)
    
    def _auto_acknowledge(self, incident, action):
        """Automatically acknowledge incident"""
        incident_number = incident.get('incidentNumber')
        message = action.get('message', 'Automatically acknowledged by automation')
        
        self.vo_api.acknowledge_incident(
            incident_number,
            "automation-bot",
            message
        )
        
        print(f"Auto-acknowledged incident {incident_number}")
    
    def _auto_resolve(self, incident, action):
        """Automatically resolve incident"""
        incident_number = incident.get('incidentNumber')
        
        # Verify resolution conditions
        if self._verify_resolution_conditions(incident, action):
            self.vo_api.resolve_incident(
                incident_number,
                "automation-bot",
                action.get('resolution_message', 'Automatically resolved')
            )
            print(f"Auto-resolved incident {incident_number}")
    
    def _verify_resolution_conditions(self, incident, action):
        """Verify conditions for auto-resolution"""
        entity_id = incident.get('entityId', '')
        
        # Custom verification logic based on incident type
        if 'disk-space' in entity_id:
            return self._verify_disk_space_resolution(entity_id)
        elif 'service-health' in entity_id:
            return self._verify_service_health_resolution(entity_id)
        
        return False
    
    def _verify_disk_space_resolution(self, entity_id):
        """Verify disk space issue is resolved"""
        # Implementation would check actual disk usage
        return True
    
    def _verify_service_health_resolution(self, entity_id):
        """Verify service health is restored"""
        # Implementation would check actual service health
        return True
    
    def _escalate_incident(self, incident, action):
        """Escalate incident to higher priority"""
        # Implementation would escalate to different team or priority
        print(f"Escalating incident {incident.get('incidentNumber')}")
    
    def _create_support_ticket(self, incident, action):
        """Create support ticket for incident tracking"""
        ticket_data = {
            'title': f"Support Ticket: {incident.get('entityDisplayName')}",
            'description': incident.get('stateMessage'),
            'priority': 'high' if incident.get('currentPhase') == 'UNACKED' else 'medium',
            'source': 'victorops_automation'
        }
        
        print(f"Creating support ticket for incident {incident.get('incidentNumber')}")
    
    def _execute_playbook(self, incident, action):
        """Execute automated playbook"""
        playbook_name = action.get('playbook')
        print(f"Executing playbook {playbook_name} for incident {incident.get('incidentNumber')}")

# Example automation setup
automation = VictorOpsAutomation(vo_api, vo_client)

# Auto-acknowledge low-priority disk space alerts
automation.add_response_rule(
    pattern="disk-space-warning",
    action={
        "type": "auto_acknowledge",
        "message": "Disk space warning acknowledged. Monitoring for escalation."
    },
    conditions={"currentPhase": "UNACKED"}
)

# Auto-resolve resolved service health checks
automation.add_response_rule(
    pattern="service-health",
    action={
        "type": "auto_resolve",
        "resolution_message": "Service health restored automatically"
    }
)

# Escalate database issues immediately
automation.add_response_rule(
    pattern="database",
    action={
        "type": "escalate",
        "escalation_team": "database-team"
    },
    conditions={"currentPhase": "UNACKED"}
)
```

## Best Practices

- Implement clear escalation policies with appropriate timeouts
- Use meaningful entity IDs and display names for easy identification
- Set up proper routing keys for different teams and services
- Monitor incident response metrics (MTTA, MTTR) for continuous improvement
- Create comprehensive runbooks linked to common incident types
- Use timeline annotations to document troubleshooting steps
- Regular review and optimization of alert routing rules
- Implement post-incident review processes for learning

## Great Resources

- [VictorOps Documentation](https://help.victorops.com/) - Official comprehensive documentation
- [Splunk On-Call API](https://portal.victorops.com/public/api-docs.html) - Complete API reference
- [VictorOps Integrations](https://help.victorops.com/knowledge-base/victorops-integrations-overview/) - Integration guides
- [Incident Response Best Practices](https://victorops.com/incident-response/) - Response methodology
- [VictorOps Community](https://community.splunk.com/t5/Splunk-On-Call/ct-p/splunk-on-call) - User forums
- [Alert Fatigue Guide](https://victorops.com/blog/alert-fatigue/) - Managing alert noise
- [On-Call Management](https://victorops.com/blog/on-call-management-best-practices/) - On-call optimization
- [Post-Incident Reviews](https://victorops.com/blog/post-incident-review-template/) - Learning from incidents