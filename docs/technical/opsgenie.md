# Opsgenie

## Overview

Opsgenie is an incident management platform by Atlassian that provides alerting, on-call management, and incident response for platform engineering teams. It offers powerful routing, escalation policies, and integrations to ensure critical issues are addressed quickly.

## Key Features

- **Intelligent Alerting**: Advanced alert routing and filtering
- **On-Call Management**: Flexible scheduling and escalations
- **Incident Response**: Coordinated response workflows
- **Integrations**: 200+ monitoring tool integrations
- **Mobile-First**: Full-featured mobile apps for on-the-go management

## Setup and Configuration

### Team Configuration
```json
{
  "name": "Platform Engineering",
  "description": "Platform and infrastructure team",
  "members": [
    {
      "user": {
        "username": "alice@company.com"
      },
      "role": "admin"
    },
    {
      "user": {
        "username": "bob@company.com"
      },
      "role": "user"
    }
  ]
}
```

### Escalation Policy
```json
{
  "name": "Production Escalation",
  "description": "Escalation policy for production alerts",
  "rules": [
    {
      "condition": "if-not-acked",
      "notifyType": "default",
      "delay": {
        "timeAmount": 0,
        "timeUnit": "minutes"
      },
      "recipient": {
        "type": "schedule",
        "id": "primary-oncall"
      }
    },
    {
      "condition": "if-not-acked",
      "notifyType": "default",
      "delay": {
        "timeAmount": 15,
        "timeUnit": "minutes"
      },
      "recipient": {
        "type": "team",
        "id": "platform-engineering"
      }
    },
    {
      "condition": "if-not-acked",
      "notifyType": "default",
      "delay": {
        "timeAmount": 30,
        "timeUnit": "minutes"
      },
      "recipient": {
        "type": "user",
        "id": "manager@company.com"
      }
    }
  ],
  "repeat": {
    "waitInterval": 0,
    "count": 0,
    "resetRecipientStates": false,
    "closeAlertAfter": 0
  }
}
```

### On-Call Schedule
```json
{
  "name": "Primary On-Call",
  "description": "Primary on-call rotation for platform team",
  "timezone": "America/New_York",
  "enabled": true,
  "ownerTeam": {
    "name": "Platform Engineering"
  },
  "rotations": [
    {
      "name": "Daily Rotation",
      "startDate": "2024-01-01T09:00:00Z",
      "endDate": "2024-12-31T09:00:00Z",
      "type": "daily",
      "length": 1,
      "participants": [
        {
          "type": "user",
          "username": "alice@company.com"
        },
        {
          "type": "user",
          "username": "bob@company.com"
        },
        {
          "type": "user",
          "username": "charlie@company.com"
        }
      ],
      "timeRestriction": {
        "type": "time-of-day",
        "restrictions": [
          {
            "startHour": 9,
            "startMin": 0,
            "endHour": 17,
            "endMin": 0
          }
        ]
      }
    },
    {
      "name": "Weekend Rotation",
      "startDate": "2024-01-06T00:00:00Z",
      "endDate": "2024-12-31T23:59:59Z",
      "type": "weekly",
      "length": 1,
      "participants": [
        {
          "type": "user",
          "username": "weekend1@company.com"
        },
        {
          "type": "user",
          "username": "weekend2@company.com"
        }
      ],
      "timeRestriction": {
        "type": "weekday-and-time-of-day",
        "restrictions": [
          {
            "startDay": "saturday",
            "startHour": 0,
            "startMin": 0,
            "endDay": "sunday",
            "endHour": 23,
            "endMin": 59
          }
        ]
      }
    }
  ]
}
```

## Integration Examples

### Prometheus AlertManager
```yaml
global:
  opsgenie_api_url: 'https://api.opsgenie.com/'

route:
  receiver: 'default-receiver'
  routes:
  - match:
      severity: critical
    receiver: opsgenie-critical
  - match:
      severity: warning
    receiver: opsgenie-warning

receivers:
- name: 'default-receiver'
  webhook_configs:
  - url: 'http://localhost:5001/'

- name: opsgenie-critical
  opsgenie_configs:
  - api_key: 'your-integration-key'
    description: 'Critical Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    message: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    priority: 'P1'
    tags: 'critical,production,{{ range .Alerts }}{{ .Labels.service }}{{ end }}'
    details:
      AlertName: '{{ .GroupLabels.alertname }}'
      Instance: '{{ range .Alerts }}{{ .Labels.instance }}{{ end }}'
      Severity: '{{ range .Alerts }}{{ .Labels.severity }}{{ end }}'
      Description: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
      Runbook: '{{ range .Alerts }}{{ .Annotations.runbook_url }}{{ end }}'
    actions:
      - 'View Dashboard'
      - 'Check Logs'
      - 'Escalate'

- name: opsgenie-warning
  opsgenie_configs:
  - api_key: 'your-integration-key'
    description: 'Warning Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    priority: 'P3'
    tags: 'warning,{{ range .Alerts }}{{ .Labels.service }}{{ end }}'
```

### Application Integration (Python)
```python
import requests
import json
from datetime import datetime
from enum import Enum

class OpsgeniePriority(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"

class OpsgenieClient:
    def __init__(self, api_key, eu=False):
        self.api_key = api_key
        self.base_url = "https://api.eu.opsgenie.com" if eu else "https://api.opsgenie.com"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"GenieKey {api_key}"
        }
    
    def create_alert(self, message, alias=None, description=None, 
                    priority=OpsgeniePriority.P3, tags=None, details=None,
                    actions=None, responders=None, visible_to=None):
        """Create a new alert"""
        payload = {
            "message": message
        }
        
        if alias:
            payload["alias"] = alias
        if description:
            payload["description"] = description
        if priority:
            payload["priority"] = priority.value
        if tags:
            payload["tags"] = tags
        if details:
            payload["details"] = details
        if actions:
            payload["actions"] = actions
        if responders:
            payload["responders"] = responders
        if visible_to:
            payload["visibleTo"] = visible_to
        
        response = requests.post(
            f"{self.base_url}/v2/alerts",
            headers=self.headers,
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def close_alert(self, identifier, identifier_type="alias", note=None, source=None):
        """Close an alert"""
        payload = {}
        if note:
            payload["note"] = note
        if source:
            payload["source"] = source
        
        params = {"identifierType": identifier_type}
        
        response = requests.post(
            f"{self.base_url}/v2/alerts/{identifier}/close",
            headers=self.headers,
            params=params,
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def acknowledge_alert(self, identifier, identifier_type="alias", note=None, source=None):
        """Acknowledge an alert"""
        payload = {}
        if note:
            payload["note"] = note
        if source:
            payload["source"] = source
        
        params = {"identifierType": identifier_type}
        
        response = requests.post(
            f"{self.base_url}/v2/alerts/{identifier}/acknowledge",
            headers=self.headers,
            params=params,
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def get_alerts(self, query=None, search_identifier=None, 
                  search_identifier_type=None, offset=0, limit=20, sort="createdAt", order="desc"):
        """Get alerts"""
        params = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "order": order
        }
        
        if query:
            params["query"] = query
        if search_identifier:
            params["searchIdentifier"] = search_identifier
        if search_identifier_type:
            params["searchIdentifierType"] = search_identifier_type
        
        response = requests.get(
            f"{self.base_url}/v2/alerts",
            headers=self.headers,
            params=params
        )
        
        return response.json()
    
    def create_incident(self, message, description=None, tags=None, 
                       details=None, priority=OpsgeniePriority.P3, 
                       responders=None, actions=None):
        """Create an incident"""
        payload = {
            "message": message
        }
        
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if details:
            payload["details"] = details
        if priority:
            payload["priority"] = priority.value
        if responders:
            payload["responders"] = responders
        if actions:
            payload["actions"] = actions
        
        response = requests.post(
            f"{self.base_url}/v1/incidents/create",
            headers=self.headers,
            data=json.dumps(payload)
        )
        
        return response.json()

# Usage examples
opsgenie = OpsgenieClient("your-api-key")

# Application monitoring
def handle_application_error(error, context):
    """Handle application errors with Opsgenie"""
    details = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "environment": context.get("environment", "production"),
        "service": context.get("service", "unknown"),
        "version": context.get("version", "unknown"),
        "user_id": context.get("user_id"),
        "request_id": context.get("request_id"),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Create responders list
    responders = [
        {"type": "team", "name": "Platform Engineering"},
        {"type": "schedule", "name": "Primary On-Call"}
    ]
    
    # Create actions
    actions = [
        "Check Application Logs",
        "View Monitoring Dashboard",
        "Restart Service",
        "Scale Up Resources"
    ]
    
    # Determine priority based on error type
    priority = OpsgeniePriority.P1 if "Critical" in str(error) else OpsgeniePriority.P2
    
    response = opsgenie.create_alert(
        message=f"Application Error: {str(error)}",
        alias=f"app-error-{context.get('service', 'unknown')}-{context.get('request_id', 'unknown')}",
        description=f"Critical application error in {context.get('service')} service",
        priority=priority,
        tags=["application", "error", context.get("environment", "production")],
        details=details,
        actions=actions,
        responders=responders
    )
    
    return response

# Infrastructure monitoring
def monitor_kubernetes_cluster():
    """Monitor Kubernetes cluster health"""
    try:
        # Check cluster health
        cluster_health = check_cluster_health()
        
        if not cluster_health["healthy"]:
            details = {
                "cluster_name": cluster_health["cluster_name"],
                "unhealthy_nodes": cluster_health["unhealthy_nodes"],
                "failed_pods": cluster_health["failed_pods"],
                "resource_pressure": cluster_health["resource_pressure"],
                "check_time": datetime.utcnow().isoformat()
            }
            
            opsgenie.create_alert(
                message="Kubernetes Cluster Health Issue",
                alias=f"k8s-health-{cluster_health['cluster_name']}",
                description="Kubernetes cluster health check failed",
                priority=OpsgeniePriority.P1,
                tags=["kubernetes", "infrastructure", "cluster-health"],
                details=details,
                actions=[
                    "Check Node Status",
                    "View Pod Logs",
                    "Check Resource Usage",
                    "Drain Unhealthy Nodes"
                ],
                responders=[
                    {"type": "team", "name": "Platform Engineering"}
                ]
            )
        
        # Check individual services
        service_health = check_service_health()
        for service, health in service_health.items():
            if not health["healthy"]:
                opsgenie.create_alert(
                    message=f"Service {service} is unhealthy",
                    alias=f"service-health-{service}",
                    description=f"Health check failed for service {service}",
                    priority=OpsgeniePriority.P2,
                    tags=["service", "health-check", service],
                    details={
                        "service_name": service,
                        "error_rate": health["error_rate"],
                        "response_time": health["response_time"],
                        "uptime": health["uptime"]
                    }
                )
    
    except Exception as e:
        # Alert on monitoring system failure
        opsgenie.create_alert(
            message="Monitoring System Failure",
            description=f"Failed to perform health checks: {str(e)}",
            priority=OpsgeniePriority.P1,
            tags=["monitoring", "system-failure"]
        )
```

## Alert Routing and Filtering

### Route Configuration
```json
{
  "name": "Production Alerts Routing",
  "criteria": {
    "type": "match-all-conditions",
    "conditions": [
      {
        "field": "tags",
        "operation": "contains",
        "expectedValue": "production"
      }
    ]
  },
  "notify": [
    {
      "type": "schedule",
      "name": "Primary On-Call"
    }
  ],
  "timeRestriction": {
    "type": "time-of-day",
    "restrictions": [
      {
        "startHour": 9,
        "startMin": 0,
        "endHour": 17,
        "endMin": 0
      }
    ]
  }
}
```

### Global Notification Rules
```json
{
  "name": "Critical Alert Notification",
  "enabled": true,
  "criteria": {
    "type": "match-all-conditions",
    "conditions": [
      {
        "field": "priority",
        "operation": "equals",
        "expectedValue": "P1"
      }
    ]
  },
  "restrictions": [
    {
      "startHour": 0,
      "startMin": 0,
      "endHour": 23,
      "endMin": 59
    }
  ],
  "schedules": [
    {
      "name": "Primary On-Call"
    }
  ],
  "steps": [
    {
      "contact": {
        "to": "all",
        "method": "mobile_app"
      },
      "sendAfter": {
        "timeAmount": 0,
        "timeUnit": "minutes"
      }
    },
    {
      "contact": {
        "to": "all",
        "method": "sms"
      },
      "sendAfter": {
        "timeAmount": 1,
        "timeUnit": "minutes"
      }
    },
    {
      "contact": {
        "to": "all",
        "method": "voice"
      },
      "sendAfter": {
        "timeAmount": 3,
        "timeUnit": "minutes"
      }
    }
  ]
}
```

## Automation and Workflows

### Custom Actions
```python
class OpsgenieAutomation:
    def __init__(self, opsgenie_client):
        self.opsgenie = opsgenie_client
        self.action_handlers = {
            "restart_service": self.restart_service,
            "scale_up": self.scale_up_service,
            "check_logs": self.check_service_logs,
            "run_diagnostics": self.run_diagnostics
        }
    
    def handle_action(self, alert_id, action, context):
        """Handle custom actions from Opsgenie"""
        if action in self.action_handlers:
            result = self.action_handlers[action](context)
            
            # Add note to alert with action result
            self.opsgenie.add_note(
                alert_id,
                f"Automated action '{action}' executed: {result['message']}"
            )
            
            # Auto-close alert if action was successful
            if result.get('success') and result.get('auto_resolve'):
                self.opsgenie.close_alert(
                    alert_id,
                    note=f"Auto-resolved after successful {action}"
                )
    
    def restart_service(self, context):
        """Restart a service"""
        service_name = context.get('service_name')
        namespace = context.get('namespace', 'default')
        
        try:
            # Kubernetes service restart
            result = kubectl_restart_deployment(service_name, namespace)
            
            return {
                'success': True,
                'message': f"Service {service_name} restarted successfully",
                'auto_resolve': False  # Don't auto-resolve, verify health first
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to restart service {service_name}: {str(e)}"
            }
    
    def scale_up_service(self, context):
        """Scale up a service"""
        service_name = context.get('service_name')
        replicas = context.get('target_replicas', 3)
        
        try:
            result = kubectl_scale_deployment(service_name, replicas)
            
            return {
                'success': True,
                'message': f"Service {service_name} scaled to {replicas} replicas",
                'auto_resolve': False
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to scale service {service_name}: {str(e)}"
            }
    
    def check_service_logs(self, context):
        """Check service logs for errors"""
        service_name = context.get('service_name')
        
        try:
            logs = get_service_logs(service_name, lines=100)
            error_count = count_error_logs(logs)
            
            return {
                'success': True,
                'message': f"Found {error_count} errors in recent logs for {service_name}",
                'details': {'error_count': error_count, 'log_sample': logs[:500]}
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to check logs for {service_name}: {str(e)}"
            }
```

## Reporting and Analytics

### Alert Analytics
```python
from datetime import datetime, timedelta
import pandas as pd

class OpsgenieAnalytics:
    def __init__(self, opsgenie_client):
        self.opsgenie = opsgenie_client
    
    def generate_alert_report(self, days=30):
        """Generate comprehensive alert report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query all alerts in date range
        query = f"createdAt >= {start_date.strftime('%Y-%m-%d')} AND createdAt <= {end_date.strftime('%Y-%m-%d')}"
        
        all_alerts = []
        offset = 0
        limit = 100
        
        while True:
            response = self.opsgenie.get_alerts(
                query=query,
                offset=offset,
                limit=limit
            )
            
            alerts = response.get('data', [])
            if not alerts:
                break
                
            all_alerts.extend(alerts)
            offset += limit
        
        # Calculate metrics
        metrics = {
            'total_alerts': len(all_alerts),
            'alerts_by_priority': self._group_by_priority(all_alerts),
            'alerts_by_team': self._group_by_team(all_alerts),
            'alerts_by_service': self._group_by_service(all_alerts),
            'mttr': self._calculate_mttr(all_alerts),
            'mtta': self._calculate_mtta(all_alerts),
            'alert_trends': self._calculate_daily_trends(all_alerts)
        }
        
        return metrics
    
    def _calculate_mttr(self, alerts):
        """Calculate Mean Time To Resolution"""
        resolution_times = []
        
        for alert in alerts:
            if alert['status'] == 'closed':
                created = datetime.fromisoformat(alert['createdAt'].replace('Z', '+00:00'))
                closed = datetime.fromisoformat(alert['updatedAt'].replace('Z', '+00:00'))
                resolution_times.append((closed - created).total_seconds() / 3600)
        
        return sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    def _calculate_mtta(self, alerts):
        """Calculate Mean Time To Acknowledgment"""
        ack_times = []
        
        for alert in alerts:
            if alert.get('acknowledged'):
                created = datetime.fromisoformat(alert['createdAt'].replace('Z', '+00:00'))
                acked = datetime.fromisoformat(alert['acknowledgedAt'].replace('Z', '+00:00'))
                ack_times.append((acked - created).total_seconds() / 60)
        
        return sum(ack_times) / len(ack_times) if ack_times else 0
    
    def generate_oncall_report(self, schedule_name, days=30):
        """Generate on-call effectiveness report"""
        # This would integrate with Opsgenie's schedule API
        # to analyze on-call performance metrics
        pass

# Generate reports
analytics = OpsgenieAnalytics(opsgenie)
report = analytics.generate_alert_report(30)

print(f"Alert Report (Last 30 days):")
print(f"Total Alerts: {report['total_alerts']}")
print(f"MTTR: {report['mttr']:.1f} hours")
print(f"MTTA: {report['mtta']:.1f} minutes")
print(f"Priority Distribution: {report['alerts_by_priority']}")
```

## Best Practices

- Use meaningful alert messages and descriptions
- Implement proper tagging strategy for easy filtering
- Set up escalation policies with clear ownership
- Use actions to provide quick remediation options
- Regularly review and tune alert routing rules
- Monitor MTTA/MTTR metrics for continuous improvement
- Integrate with monitoring tools for automatic alert creation
- Use scheduled maintenance to suppress alerts during planned work

## Great Resources

- [Opsgenie Documentation](https://support.atlassian.com/opsgenie/) - Official comprehensive documentation
- [Opsgenie API Reference](https://docs.opsgenie.com/docs/api-overview) - Complete API documentation
- [Opsgenie Integrations](https://docs.opsgenie.com/docs/integrations-overview) - Integration guides
- [Opsgenie Community](https://community.atlassian.com/t5/Opsgenie/ct-p/opsgenie) - Community forums
- [Incident Management Best Practices](https://www.atlassian.com/incident-management) - Atlassian's incident management guide
- [On-Call Management Guide](https://www.atlassian.com/software/opsgenie/what-is-on-call) - On-call best practices
- [Alert Fatigue Solutions](https://www.atlassian.com/incident-management/on-call/alert-fatigue) - Reducing alert noise