# PagerDuty

## Overview

PagerDuty is an incident management platform that helps platform engineers respond to critical issues quickly and effectively. It provides intelligent alerting, on-call scheduling, and incident response coordination to minimize downtime and improve system reliability.

## Key Features

- **Intelligent Alerting**: ML-powered alert correlation and noise reduction
- **On-Call Scheduling**: Flexible rotation and escalation policies
- **Incident Response**: Coordinated response workflows and communication
- **Event Intelligence**: Alert grouping and correlation
- **Post-Incident Analysis**: Detailed reporting and retrospectives

## Setup and Configuration

### Service Configuration
```json
{
  "service": {
    "name": "Production API",
    "description": "Critical production API service",
    "status": "active",
    "escalation_policy": {
      "id": "P123ABC",
      "type": "escalation_policy_reference"
    },
    "incident_urgency_rule": {
      "type": "constant",
      "urgency": "high"
    },
    "acknowledgement_timeout": 1800,
    "auto_resolve_timeout": 14400,
    "alert_creation": "create_alerts_and_incidents",
    "alert_grouping": "time",
    "alert_grouping_timeout": 300
  }
}
```

### Escalation Policy
```json
{
  "escalation_policy": {
    "name": "Production Escalation",
    "description": "Escalation policy for production services",
    "num_loops": 2,
    "on_call_handoff_notifications": "if_has_services",
    "escalation_rules": [
      {
        "escalation_delay_in_minutes": 0,
        "targets": [
          {
            "id": "PUSER1",
            "type": "user_reference"
          },
          {
            "id": "PUSER2",
            "type": "user_reference"
          }
        ]
      },
      {
        "escalation_delay_in_minutes": 15,
        "targets": [
          {
            "id": "PTEAM1",
            "type": "schedule_reference"
          }
        ]
      },
      {
        "escalation_delay_in_minutes": 30,
        "targets": [
          {
            "id": "PMGR1",
            "type": "user_reference"
          }
        ]
      }
    ]
  }
}
```

### On-Call Schedule
```json
{
  "schedule": {
    "name": "Platform Team Primary",
    "description": "Primary on-call rotation for platform team",
    "time_zone": "America/New_York",
    "schedule_layers": [
      {
        "name": "Layer 1",
        "start": "2024-01-01T00:00:00Z",
        "rotation_virtual_start": "2024-01-01T00:00:00Z",
        "rotation_turn_length_seconds": 604800,
        "users": [
          {
            "user": {
              "id": "PUSER1",
              "type": "user_reference"
            }
          },
          {
            "user": {
              "id": "PUSER2",
              "type": "user_reference"
            }
          },
          {
            "user": {
              "id": "PUSER3",
              "type": "user_reference"
            }
          }
        ],
        "restrictions": [
          {
            "type": "daily_restriction",
            "start_time_of_day": "08:00:00",
            "duration_seconds": 43200
          }
        ]
      },
      {
        "name": "Layer 2 - Weekends",
        "start": "2024-01-06T00:00:00Z",
        "rotation_virtual_start": "2024-01-06T00:00:00Z",
        "rotation_turn_length_seconds": 1209600,
        "users": [
          {
            "user": {
              "id": "PUSER4",
              "type": "user_reference"
            }
          },
          {
            "user": {
              "id": "PUSER5",
              "type": "user_reference"
            }
          }
        ],
        "restrictions": [
          {
            "type": "weekly_restriction",
            "start_day_of_week": 6,
            "start_time_of_day": "00:00:00",
            "duration_seconds": 172800
          }
        ]
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
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
  - match:
      severity: critical
    receiver: pagerduty-critical
  - match:
      severity: warning
    receiver: pagerduty-warning

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'

- name: pagerduty-critical
  pagerduty_configs:
  - routing_key: 'your-integration-key-critical'
    description: 'Critical Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    details:
      alertname: '{{ .GroupLabels.alertname }}'
      instance: '{{ range .Alerts }}{{ .Labels.instance }}{{ end }}'
      severity: '{{ range .Alerts }}{{ .Labels.severity }}{{ end }}'
      description: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    links:
    - href: 'https://grafana.example.com/d/alerts'
      text: 'Grafana Dashboard'
    - href: 'https://prometheus.example.com/alerts'
      text: 'Prometheus Alerts'

- name: pagerduty-warning
  pagerduty_configs:
  - routing_key: 'your-integration-key-warning'
    description: 'Warning Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
    severity: 'warning'
```

### Kubernetes Monitoring Integration
```yaml
# kubernetes-alert-rules.yml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kubernetes-alerts
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
        service: kubernetes
        team: platform
      annotations:
        summary: "Kubernetes node {{ $labels.instance }} is down"
        description: "Node {{ $labels.instance }} has been down for more than 5 minutes"
        runbook_url: "https://runbooks.example.com/kubernetes/node-down"
        
    - alert: KubernetesPodCrashLooping
      expr: increase(kube_pod_container_status_restarts_total[1h]) > 5
      for: 0m
      labels:
        severity: warning
        service: kubernetes
        team: platform
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
        description: "Pod has restarted {{ $value }} times in the last hour"
        runbook_url: "https://runbooks.example.com/kubernetes/crashloop"
        
    - alert: KubernetesMemoryPressure
      expr: kube_node_status_condition{condition="MemoryPressure",status="true"} == 1
      for: 2m
      labels:
        severity: warning
        service: kubernetes
        team: platform
      annotations:
        summary: "Memory pressure on node {{ $labels.node }}"
        description: "Node {{ $labels.node }} is experiencing memory pressure"
        runbook_url: "https://runbooks.example.com/kubernetes/memory-pressure"
        
    - alert: KubernetesPersistentVolumeFull
      expr: kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes > 0.9
      for: 2m
      labels:
        severity: critical
        service: kubernetes
        team: platform
      annotations:
        summary: "PVC {{ $labels.persistentvolumeclaim }} is 90% full"
        description: "PVC {{ $labels.persistentvolumeclaim }} in namespace {{ $labels.namespace }} is {{ $value | humanizePercentage }} full"
        runbook_url: "https://runbooks.example.com/kubernetes/pvc-full"
```

### Application Integration (Python)
```python
import requests
import json
from datetime import datetime
from enum import Enum

class PagerDutySeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class PagerDutyClient:
    def __init__(self, routing_key, api_token=None):
        self.routing_key = routing_key
        self.api_token = api_token
        self.events_url = "https://events.pagerduty.com/v2/enqueue"
        self.api_url = "https://api.pagerduty.com"
    
    def trigger_incident(self, summary, source, severity=PagerDutySeverity.ERROR, 
                        custom_details=None, links=None, images=None):
        """Trigger a new incident"""
        payload = {
            "routing_key": self.routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "source": source,
                "severity": severity.value,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "component": "application",
                "group": "platform",
                "class": "error"
            }
        }
        
        if custom_details:
            payload["payload"]["custom_details"] = custom_details
        
        if links:
            payload["payload"]["links"] = links
            
        if images:
            payload["payload"]["images"] = images
        
        response = requests.post(
            self.events_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def acknowledge_incident(self, dedup_key):
        """Acknowledge an existing incident"""
        payload = {
            "routing_key": self.routing_key,
            "event_action": "acknowledge",
            "dedup_key": dedup_key
        }
        
        response = requests.post(
            self.events_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def resolve_incident(self, dedup_key):
        """Resolve an existing incident"""
        payload = {
            "routing_key": self.routing_key,
            "event_action": "resolve",
            "dedup_key": dedup_key
        }
        
        response = requests.post(
            self.events_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        return response.json()
    
    def get_incidents(self, status="triggered,acknowledged", limit=25):
        """Get incidents using REST API"""
        if not self.api_token:
            raise ValueError("API token required for REST API calls")
        
        headers = {
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Authorization": f"Token token={self.api_token}"
        }
        
        params = {
            "statuses[]": status.split(","),
            "limit": limit,
            "sort_by": "created_at:desc"
        }
        
        response = requests.get(
            f"{self.api_url}/incidents",
            headers=headers,
            params=params
        )
        
        return response.json()

# Usage examples
pd_client = PagerDutyClient(
    routing_key="your-integration-key",
    api_token="your-api-token"
)

# Application error monitoring
def handle_critical_error(error, context):
    """Handle critical application errors"""
    custom_details = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "stack_trace": str(error.__traceback__),
        "user_id": context.get("user_id"),
        "request_id": context.get("request_id"),
        "environment": context.get("environment", "production")
    }
    
    links = [
        {
            "href": f"https://grafana.example.com/d/app-errors?var-request_id={context.get('request_id')}",
            "text": "Grafana Dashboard"
        },
        {
            "href": f"https://logs.example.com/search?request_id={context.get('request_id')}",
            "text": "Application Logs"
        }
    ]
    
    response = pd_client.trigger_incident(
        summary=f"Critical application error: {str(error)}",
        source="application-server",
        severity=PagerDutySeverity.CRITICAL,
        custom_details=custom_details,
        links=links
    )
    
    print(f"PagerDuty incident triggered: {response.get('dedup_key')}")
    return response.get('dedup_key')

# Infrastructure monitoring
def check_service_health():
    """Monitor service health and alert on issues"""
    try:
        # Check database connectivity
        db_status = check_database_connection()
        if not db_status['healthy']:
            pd_client.trigger_incident(
                summary="Database connectivity issue detected",
                source="health-check",
                severity=PagerDutySeverity.CRITICAL,
                custom_details={
                    "component": "database",
                    "error": db_status['error'],
                    "last_successful_check": db_status['last_success']
                }
            )
        
        # Check external API dependencies
        api_status = check_external_apis()
        for api, status in api_status.items():
            if not status['healthy']:
                pd_client.trigger_incident(
                    summary=f"External API {api} is unavailable",
                    source="health-check",
                    severity=PagerDutySeverity.WARNING,
                    custom_details={
                        "component": "external_api",
                        "api_name": api,
                        "response_time": status['response_time'],
                        "error_rate": status['error_rate']
                    }
                )
    
    except Exception as e:
        handle_critical_error(e, {"context": "health_check"})
```

### Slack Integration
```python
def setup_slack_webhook_for_pagerduty():
    """Setup Slack webhook for PagerDuty notifications"""
    webhook_config = {
        "name": "Slack Platform Team",
        "config": {
            "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
            "channel": "#platform-alerts",
            "username": "PagerDuty",
            "icon_emoji": ":rotating_light:",
            "notify_types": [
                "incident.triggered",
                "incident.acknowledged",
                "incident.resolved",
                "incident.escalated"
            ],
            "filters": {
                "severity": ["critical", "error"]
            }
        }
    }
    
    return webhook_config

# Custom Slack message formatting
def format_pagerduty_slack_message(incident_data):
    """Format PagerDuty incident for Slack"""
    incident = incident_data['incident']
    
    severity_emoji = {
        'critical': ':fire:',
        'error': ':warning:',
        'warning': ':yellow_circle:',
        'info': ':information_source:'
    }
    
    status_emoji = {
        'triggered': ':red_circle:',
        'acknowledged': ':large_yellow_circle:',
        'resolved': ':large_green_circle:'
    }
    
    message = {
        "username": "PagerDuty",
        "icon_emoji": ":rotating_light:",
        "attachments": [
            {
                "color": "danger" if incident['urgency'] == 'high' else "warning",
                "fallback": f"PagerDuty Alert: {incident['title']}",
                "title": f"{severity_emoji.get(incident['priority']['summary'], '')} {incident['title']}",
                "title_link": incident['html_url'],
                "fields": [
                    {
                        "title": "Status",
                        "value": f"{status_emoji.get(incident['status'], '')} {incident['status'].title()}",
                        "short": True
                    },
                    {
                        "title": "Priority",
                        "value": incident['priority']['summary'],
                        "short": True
                    },
                    {
                        "title": "Service",
                        "value": incident['service']['summary'],
                        "short": True
                    },
                    {
                        "title": "Assigned To",
                        "value": incident.get('assignments', [{}])[0].get('assignee', {}).get('summary', 'Unassigned'),
                        "short": True
                    }
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": "View Incident",
                        "url": incident['html_url'],
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "text": "Acknowledge",
                        "url": f"{incident['html_url']}#acknowledge",
                        "style": "default"
                    }
                ],
                "footer": "PagerDuty",
                "ts": int(datetime.fromisoformat(incident['created_at'].replace('Z', '+00:00')).timestamp())
            }
        ]
    }
    
    return message
```

## Event Intelligence and Automation

### Event Rules Configuration
```json
{
  "event_rules": [
    {
      "name": "Kubernetes Pod Restart Correlation",
      "description": "Group pod restart alerts by namespace",
      "conditions": [
        {
          "field": "source",
          "operator": "equals",
          "value": "kubernetes"
        },
        {
          "field": "summary",
          "operator": "contains",
          "value": "pod restart"
        }
      ],
      "actions": [
        {
          "type": "annotate",
          "value": "Pod restart detected - check resource limits"
        },
        {
          "type": "priority",
          "value": "P3"
        },
        {
          "type": "suppress",
          "threshold": 5,
          "threshold_time_amount": 10,
          "threshold_time_unit": "minutes"
        }
      ]
    },
    {
      "name": "Critical Service Alert Enhancement",
      "description": "Enhance critical service alerts with runbook links",
      "conditions": [
        {
          "field": "severity",
          "operator": "equals",
          "value": "critical"
        },
        {
          "field": "service",
          "operator": "matches",
          "value": "(api|database|auth)"
        }
      ],
      "actions": [
        {
          "type": "annotate",
          "value": "CRITICAL: Follow emergency response procedures"
        },
        {
          "type": "priority",
          "value": "P1"
        },
        {
          "type": "note",
          "value": "Runbook: https://runbooks.example.com/critical-services"
        }
      ]
    },
    {
      "name": "Maintenance Window Suppression",
      "description": "Suppress alerts during maintenance windows",
      "conditions": [
        {
          "field": "custom_details.maintenance_mode",
          "operator": "equals",
          "value": "true"
        }
      ],
      "actions": [
        {
          "type": "suppress"
        },
        {
          "type": "annotate",
          "value": "Suppressed: Maintenance window active"
        }
      ]
    }
  ]
}
```

### Response Automation
```python
import time
from typing import Dict, List

class PagerDutyAutomation:
    def __init__(self, pd_client):
        self.pd_client = pd_client
        self.auto_response_rules = []
    
    def add_auto_response_rule(self, rule):
        """Add an automated response rule"""
        self.auto_response_rules.append(rule)
    
    def process_incident(self, incident):
        """Process incident with automated responses"""
        for rule in self.auto_response_rules:
            if self._matches_conditions(incident, rule['conditions']):
                self._execute_actions(incident, rule['actions'])
    
    def _matches_conditions(self, incident, conditions):
        """Check if incident matches rule conditions"""
        for condition in conditions:
            field_value = self._get_nested_value(incident, condition['field'])
            if not self._evaluate_condition(field_value, condition):
                return False
        return True
    
    def _execute_actions(self, incident, actions):
        """Execute automated actions"""
        for action in actions:
            action_type = action['type']
            
            if action_type == 'auto_resolve':
                self._auto_resolve_incident(incident, action)
            elif action_type == 'escalate':
                self._escalate_incident(incident, action)
            elif action_type == 'create_ticket':
                self._create_support_ticket(incident, action)
            elif action_type == 'run_playbook':
                self._execute_playbook(incident, action)
    
    def _auto_resolve_incident(self, incident, action):
        """Automatically resolve incident based on conditions"""
        # Check if conditions for auto-resolution are met
        if self._verify_resolution_conditions(incident, action):
            self.pd_client.resolve_incident(incident['id'])
            print(f"Auto-resolved incident {incident['id']}")
    
    def _escalate_incident(self, incident, action):
        """Escalate incident to higher priority"""
        escalation_policy = action.get('escalation_policy')
        if escalation_policy:
            # Update incident priority and escalation
            print(f"Escalating incident {incident['id']} to {escalation_policy}")
    
    def _create_support_ticket(self, incident, action):
        """Create support ticket for incident tracking"""
        ticket_data = {
            'title': f"Support Ticket: {incident['title']}",
            'description': incident['description'],
            'priority': incident['priority']['summary'],
            'source': 'pagerduty_automation'
        }
        
        # Integration with ticketing system
        print(f"Creating support ticket for incident {incident['id']}")
    
    def _execute_playbook(self, incident, action):
        """Execute automated playbook"""
        playbook_name = action.get('playbook')
        playbook_params = action.get('parameters', {})
        
        # Execute automated remediation
        print(f"Executing playbook {playbook_name} for incident {incident['id']}")

# Example automation rules
automation = PagerDutyAutomation(pd_client)

# Auto-resolve disk space alerts when usage drops
automation.add_auto_response_rule({
    'name': 'Auto-resolve disk space alerts',
    'conditions': [
        {'field': 'title', 'operator': 'contains', 'value': 'disk space'},
        {'field': 'custom_details.current_usage', 'operator': 'less_than', 'value': 80}
    ],
    'actions': [
        {'type': 'auto_resolve'}
    ]
})

# Escalate database connectivity issues
automation.add_auto_response_rule({
    'name': 'Escalate database issues',
    'conditions': [
        {'field': 'service.name', 'operator': 'contains', 'value': 'database'},
        {'field': 'priority.summary', 'operator': 'equals', 'value': 'P1'}
    ],
    'actions': [
        {'type': 'escalate', 'escalation_policy': 'database_team'},
        {'type': 'run_playbook', 'playbook': 'database_failover'}
    ]
})
```

## Monitoring and Analytics

### PagerDuty Analytics API
```python
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

class PagerDutyAnalytics:
    def __init__(self, pd_client):
        self.pd_client = pd_client
    
    def get_incident_metrics(self, days=30):
        """Get incident metrics for analysis"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        incidents = self.pd_client.get_incidents(
            since=start_date.isoformat(),
            until=end_date.isoformat(),
            limit=1000
        )
        
        metrics = {
            'total_incidents': len(incidents['incidents']),
            'mttr': self._calculate_mttr(incidents['incidents']),
            'mtta': self._calculate_mtta(incidents['incidents']),
            'incidents_by_service': self._group_by_service(incidents['incidents']),
            'incidents_by_priority': self._group_by_priority(incidents['incidents']),
            'incident_trends': self._calculate_trends(incidents['incidents'])
        }
        
        return metrics
    
    def _calculate_mttr(self, incidents):
        """Calculate Mean Time To Resolution"""
        resolution_times = []
        
        for incident in incidents:
            if incident['status'] == 'resolved':
                created = datetime.fromisoformat(incident['created_at'].replace('Z', '+00:00'))
                resolved = datetime.fromisoformat(incident['last_status_change_at'].replace('Z', '+00:00'))
                resolution_times.append((resolved - created).total_seconds() / 3600)  # hours
        
        return sum(resolution_times) / len(resolution_times) if resolution_times else 0
    
    def _calculate_mtta(self, incidents):
        """Calculate Mean Time To Acknowledgment"""
        ack_times = []
        
        for incident in incidents:
            if 'first_trigger_log_entry' in incident and 'acknowledgements' in incident:
                if incident['acknowledgements']:
                    created = datetime.fromisoformat(incident['created_at'].replace('Z', '+00:00'))
                    acked = datetime.fromisoformat(incident['acknowledgements'][0]['at'].replace('Z', '+00:00'))
                    ack_times.append((acked - created).total_seconds() / 60)  # minutes
        
        return sum(ack_times) / len(ack_times) if ack_times else 0
    
    def generate_sla_report(self):
        """Generate SLA compliance report"""
        metrics = self.get_incident_metrics()
        
        sla_targets = {
            'mtta': 5,  # 5 minutes
            'mttr_p1': 60,  # 1 hour for P1
            'mttr_p2': 240,  # 4 hours for P2
            'incident_volume': 50  # max 50 incidents per month
        }
        
        compliance = {
            'mtta_compliance': metrics['mtta'] <= sla_targets['mtta'],
            'volume_compliance': metrics['total_incidents'] <= sla_targets['incident_volume'],
            'mttr_p1_compliance': self._check_priority_mttr(metrics, 'P1', sla_targets['mttr_p1']),
            'mttr_p2_compliance': self._check_priority_mttr(metrics, 'P2', sla_targets['mttr_p2'])
        }
        
        return {
            'metrics': metrics,
            'sla_targets': sla_targets,
            'compliance': compliance,
            'overall_compliance': all(compliance.values())
        }

# Generate reports
analytics = PagerDutyAnalytics(pd_client)
sla_report = analytics.generate_sla_report()

print(f"SLA Compliance Report:")
print(f"MTTA: {sla_report['metrics']['mtta']:.1f} min (Target: {sla_report['sla_targets']['mtta']} min)")
print(f"MTTR: {sla_report['metrics']['mttr']:.1f} hours")
print(f"Total Incidents: {sla_report['metrics']['total_incidents']} (Target: <{sla_report['sla_targets']['incident_volume']})")
print(f"Overall Compliance: {'✅' if sla_report['overall_compliance'] else '❌'}")
```

## Best Practices

- Implement intelligent alert grouping to reduce noise
- Set up proper escalation policies with clear responsibilities
- Use runbooks and response guides for consistent incident handling
- Regularly review and update on-call schedules
- Conduct post-incident reviews for continuous improvement
- Integrate with monitoring tools for automatic incident creation
- Use event intelligence to correlate related alerts
- Monitor MTTA and MTTR metrics for performance optimization

## Great Resources

- [PagerDuty Documentation](https://support.pagerduty.com/) - Official comprehensive documentation
- [PagerDuty API Reference](https://developer.pagerduty.com/api-reference/) - Complete API documentation
- [PagerDuty University](https://university.pagerduty.com/) - Training and best practices
- [Incident Response Guide](https://response.pagerduty.com/) - Open source incident response documentation
- [PagerDuty Community](https://community.pagerduty.com/) - Forums and user discussions
- [Event Intelligence Guide](https://support.pagerduty.com/docs/event-intelligence) - Alert correlation and automation
- [Runbook Automation](https://support.pagerduty.com/docs/runbook-automation) - Process automation guide
- [Post-Incident Reviews](https://postmortems.pagerduty.com/) - Learning from incidents