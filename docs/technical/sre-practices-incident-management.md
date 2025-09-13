---
title: SRE Practices & Incident Management
sidebar_position: 10
---

# SRE Practices & Incident Management

Master the principles and practices of Site Reliability Engineering, from SLOs and error budgets to incident response and post-mortems. Learn how to build and operate systems that are reliable, scalable, and maintainable.

## 📚 Essential Resources

### 📖 Must-Read Books (Free from Google!)
- **[Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)** - Google SRE Book
- **[The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/)** - Practical SRE
- **[Building Secure & Reliable Systems](https://sre.google/books/building-secure-reliable-systems/)** - Security + SRE
- **[Seeking SRE](https://www.oreilly.com/library/view/seeking-sre/9781491978856/)** - David Blank-Edelman
- **[The Phoenix Project](https://itrevolution.com/the-phoenix-project/)** - Gene Kim (DevOps novel)

### 🎥 Video Resources
- **[SREcon Videos](https://www.usenix.org/conferences/byname/925)** - USENIX SRE conference
- **[Google SRE Classroom](https://sre.google/classroom/)** - Free training from Google
- **[Breaking Things on Purpose](https://www.youtube.com/c/Gremlin)** - Gremlin's channel
- **[Incident Response Training](https://www.youtube.com/watch?v=0bPJKOJIkWQ)** - PagerDuty
- **[SLIs, SLOs, SLAs Course](https://www.youtube.com/watch?v=tEylFyxbDLE)** - Google Cloud

### 🎓 Courses & Training
- **[School of SRE](https://linkedin.github.io/school-of-sre/)** - LinkedIn's free curriculum
- **[Google SRE Training](https://sre.google/training/)** - Official Google training
- **[Coursera SRE Course](https://www.coursera.org/learn/site-reliability-engineering-slos)** - Google Cloud
- **[Linux Foundation SRE Path](https://training.linuxfoundation.org/training/site-reliability-engineer-fundamentals/)** - LF training
- **[Udacity SRE Nanodegree](https://www.udacity.com/course/site-reliability-engineer-nanodegree--nd082)** - Full program

### 📰 Blogs & Articles
- **[Google Cloud SRE Blog](https://cloud.google.com/blog/products/devops-sre)** - GCP SRE articles
- **[SRE Weekly](https://sreweekly.com/)** - Curated newsletter
- **[Honeycomb Blog](https://www.honeycomb.io/blog)** - Observability focus
- **[Increment Magazine](https://increment.com/)** - Stripe's engineering magazine
- **[Uber Engineering](https://eng.uber.com/)** - SRE at scale

### 🔧 Essential Tools & Platforms
- **[Prometheus](https://prometheus.io/)** - Monitoring system
- **[Grafana](https://grafana.com/)** - Observability platform
- **[PagerDuty](https://www.pagerduty.com/)** - Incident management
- **[Blameless](https://www.blameless.com/)** - SRE platform
- **[Datadog](https://www.datadoghq.com/)** - Monitoring & analytics

### 💬 Communities & Forums
- **[SRE Reddit](https://reddit.com/r/sre)** - r/sre community
- **[Google SRE Discussion](https://groups.google.com/g/sre-discuss)** - Google group
- **[SREcon Community](https://www.usenix.org/srecon)** - Conference community
- **[DevOps Chat](https://devopschat.co/)** - Slack community
- **[Monitoring Weekly](https://monitoring.love/)** - Newsletter

### 🏆 Incident Management Resources
- **[PagerDuty Incident Response](https://response.pagerduty.com/)** - Free docs
- **[Atlassian Incident Management](https://www.atlassian.com/incident-management)** - Handbook
- **[Google Incident Management](https://sre.google/workbook/incident-response/)** - Google's approach
- **[Post-Mortem Templates](https://github.com/dastergon/postmortem-templates)** - Collection
- **[Wheel of Misfortune](https://github.com/dastergon/wheel-of-misfortune)** - Training game



## SRE Fundamentals

### The SRE Model

**Key Principles:**
1. **Embrace Risk**: 100% reliability is neither achievable nor desirable
2. **Service Level Objectives**: Define and measure what matters
3. **Eliminate Toil**: Automate repetitive tasks
4. **Monitoring**: Observability is fundamental
5. **Emergency Response**: Be prepared for incidents
6. **Change Management**: Most outages come from changes
7. **Capacity Planning**: Stay ahead of demand

### SLIs, SLOs, and SLAs

#### Service Level Indicators (SLIs)
```python
# Example SLI definitions
class SLIMetrics:
    def __init__(self, prometheus_client):
        self.prom = prometheus_client
        
    def availability_sli(self, service, time_range='5m'):
        """Ratio of successful requests to total requests"""
        query = f'''
        sum(rate(http_requests_total{{
            service="{service}",
            status!~"5.."
        }}[{time_range}]))
        /
        sum(rate(http_requests_total{{
            service="{service}"
        }}[{time_range}]))
        '''
        return self.prom.query(query)
    
    def latency_sli(self, service, percentile=95):
        """Nth percentile of request latency"""
        query = f'''
        histogram_quantile({percentile/100},
            sum(rate(http_request_duration_seconds_bucket{{
                service="{service}"
            }}[5m])) by (le)
        )
        '''
        return self.prom.query(query)
    
    def error_rate_sli(self, service):
        """Percentage of failed requests"""
        query = f'''
        sum(rate(http_requests_total{{
            service="{service}",
            status=~"5.."
        }}[5m]))
        /
        sum(rate(http_requests_total{{
            service="{service}"
        }}[5m]))
        * 100
        '''
        return self.prom.query(query)
```

#### Service Level Objectives (SLOs)
```yaml
# slo_config.yaml
service: api-gateway
slos:
  - name: availability
    sli: availability_ratio
    target: 99.9  # Three 9s
    window: 30d
    
  - name: latency_p95
    sli: latency_percentile_95
    target: 
      threshold: 200  # milliseconds
      percentage: 99  # 99% of requests under 200ms
    window: 7d
    
  - name: error_rate
    sli: error_percentage
    target:
      threshold: 1  # percent
      percentage: 99.5
    window: 1d
```

#### Error Budget Calculation
```python
class ErrorBudget:
    def __init__(self, slo_target, measurement_window_days=30):
        self.slo_target = slo_target
        self.window_days = measurement_window_days
        
    def calculate_budget_minutes(self):
        """Calculate error budget in minutes"""
        total_minutes = self.window_days * 24 * 60
        allowed_downtime = total_minutes * (1 - self.slo_target)
        return allowed_downtime
    
    def calculate_remaining_budget(self, current_availability):
        """Calculate remaining error budget"""
        total_minutes = self.window_days * 24 * 60
        used_minutes = total_minutes * (1 - current_availability)
        budget_minutes = self.calculate_budget_minutes()
        
        return {
            'total_budget_minutes': budget_minutes,
            'used_minutes': used_minutes,
            'remaining_minutes': budget_minutes - used_minutes,
            'remaining_percentage': (budget_minutes - used_minutes) / budget_minutes * 100
        }
    
    def time_until_budget_exhausted(self, burn_rate):
        """Predict when error budget will be exhausted"""
        remaining = self.calculate_remaining_budget()
        if burn_rate <= 0:
            return float('inf')
        
        hours_remaining = remaining['remaining_minutes'] / 60 / burn_rate
        return hours_remaining
```

**Resources:**
- 📚 [Google SRE Book - SLOs Chapter](https://sre.google/sre-book/service-level-objectives/)
- 📖 [The SLO Adoption Framework](https://cloud.google.com/blog/products/management-tools/slo-adoption-framework)
- 🎥 [SLOs for Everyone](https://www.youtube.com/watch?v=tesPwjL3CK0)
- 📖 [SLO Generator](https://github.com/google/slo-generator)

## Incident Management

### Incident Response Framework

#### Incident Classification
```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class Severity(Enum):
    P0 = "Critical - Full outage"
    P1 = "Major - Significant degradation"
    P2 = "Minor - Limited impact"
    P3 = "Low - Minimal impact"

@dataclass
class Incident:
    id: str
    title: str
    severity: Severity
    affected_services: list
    start_time: datetime
    status: str = "ACTIVE"
    incident_commander: str = None
    comm_lead: str = None
    responders: list = None
    
    def escalate(self):
        """Escalate incident severity"""
        severity_order = [Severity.P3, Severity.P2, Severity.P1, Severity.P0]
        current_index = severity_order.index(self.severity)
        if current_index < len(severity_order) - 1:
            self.severity = severity_order[current_index + 1]
            self.notify_escalation()
    
    def assign_roles(self, ic, comm_lead):
        self.incident_commander = ic
        self.comm_lead = comm_lead
        self.notify_role_assignment()
```

#### Incident Response Runbook
```yaml
# incident_response_runbook.yaml
name: "API Gateway High Latency"
severity: P1
detection:
  - alert: "APIGatewayHighLatency"
    condition: "p95 latency > 1s for 5 minutes"

steps:
  - step: 1
    action: "Verify the alert"
    commands:
      - "Check Grafana dashboard: https://grafana.example.com/d/api-gateway"
      - "Run: kubectl top pods -n api-gateway"
    
  - step: 2
    action: "Check recent deployments"
    commands:
      - "kubectl rollout history deployment/api-gateway -n api-gateway"
      - "Check CI/CD pipeline: https://jenkins.example.com/job/api-gateway"
    
  - step: 3
    action: "Scale up if CPU/memory constrained"
    commands:
      - "kubectl scale deployment/api-gateway --replicas=10 -n api-gateway"
    
  - step: 4
    action: "Enable debug logging"
    commands:
      - "kubectl set env deployment/api-gateway LOG_LEVEL=debug -n api-gateway"
    
  - step: 5
    action: "Rollback if recent deployment"
    commands:
      - "kubectl rollout undo deployment/api-gateway -n api-gateway"

escalation:
  - after_minutes: 15
    notify: ["senior-sre-oncall"]
  - after_minutes: 30
    notify: ["sre-manager", "vp-engineering"]
```

### On-Call Management

#### On-Call Rotation System
```python
class OnCallRotation:
    def __init__(self, engineers, rotation_days=7):
        self.engineers = engineers
        self.rotation_days = rotation_days
        self.schedule = {}
        self.overrides = {}
        
    def generate_schedule(self, start_date, weeks=12):
        """Generate on-call schedule"""
        current_date = start_date
        engineer_index = 0
        
        for week in range(weeks):
            engineer = self.engineers[engineer_index % len(self.engineers)]
            
            # Check for overrides
            if current_date in self.overrides:
                engineer = self.overrides[current_date]
            
            self.schedule[current_date] = {
                'primary': engineer,
                'secondary': self.engineers[(engineer_index + 1) % len(self.engineers)],
                'start': current_date,
                'end': current_date + timedelta(days=self.rotation_days)
            }
            
            current_date += timedelta(days=self.rotation_days)
            engineer_index += 1
    
    def swap_shifts(self, date1, date2):
        """Allow engineers to swap shifts"""
        if date1 in self.schedule and date2 in self.schedule:
            self.schedule[date1], self.schedule[date2] = \
                self.schedule[date2], self.schedule[date1]
    
    def get_current_oncall(self):
        """Get current on-call engineer"""
        now = datetime.now().date()
        for date, shift in self.schedule.items():
            if shift['start'] <= now < shift['end']:
                return shift
        return None
```

#### On-Call Best Practices
```python
# On-call toolkit
class OnCallToolkit:
    def __init__(self):
        self.runbooks = {}
        self.contacts = {}
        self.escalation_policies = {}
        
    def page_oncall(self, severity, message):
        """Page the on-call engineer"""
        oncall = self.get_current_oncall()
        
        if severity in [Severity.P0, Severity.P1]:
            # High severity - page immediately
            self.send_page(oncall['primary'], message)
            # Also notify secondary
            self.send_sms(oncall['secondary'], message)
        else:
            # Lower severity - start with Slack
            self.send_slack(oncall['primary'], message)
        
    def handoff_checklist(self):
        """Weekly on-call handoff checklist"""
        return {
            'review_incidents': self.get_past_week_incidents(),
            'update_runbooks': self.get_outdated_runbooks(),
            'verify_access': self.check_system_access(),
            'review_alerts': self.get_alert_statistics(),
            'known_issues': self.get_open_issues(),
            'planned_changes': self.get_upcoming_changes()
        }
```

**Resources:**
- 📚 [On-Call Handbook](https://increment.com/on-call/)
- 📖 [PagerDuty Incident Response](https://response.pagerduty.com/)
- 🎥 [Effective On-Call](https://www.youtube.com/watch?v=J7XLPRbDl4w)

## Post-Mortem Culture

### Blameless Post-Mortems

#### Post-Mortem Template
```markdown
# Incident Post-Mortem: [Incident ID]

## Incident Summary
- **Date**: 2024-01-15
- **Duration**: 2 hours 15 minutes
- **Severity**: P1
- **Services Affected**: API Gateway, User Service
- **Customer Impact**: 15% of users experienced errors

## Timeline
- **14:00** - First alert triggered for high error rate
- **14:05** - On-call engineer acknowledged
- **14:15** - Incident declared, IC assigned
- **14:30** - Root cause identified
- **15:00** - Fix deployed
- **16:15** - Incident resolved, monitoring normal

## Root Cause Analysis

### What Happened
The API Gateway began rejecting requests due to memory exhaustion caused by a memory leak in the new authentication middleware.

### Contributing Factors
1. Memory leak in JWT token validation library
2. Insufficient memory limits in K8s deployment
3. Missing memory usage alerts
4. Load testing didn't catch the gradual memory increase

### 5 Whys Analysis
1. Why did the API Gateway fail? → Out of memory
2. Why did it run out of memory? → Memory leak
3. Why was there a memory leak? → JWT library bug
4. Why wasn't it caught? → Gradual increase over hours
5. Why didn't monitoring catch it? → No memory trend alerts

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Update JWT library to v2.3.1 | @john | 2024-01-20 | In Progress |
| Add memory trend alerts | @sarah | 2024-01-22 | Planned |
| Increase memory limits | @mike | 2024-01-16 | Complete |
| Add memory leak detection to CI | @lisa | 2024-01-25 | Planned |

## Lessons Learned
1. **What went well**
   - Quick detection and response
   - Effective incident communication
   - Rollback procedure worked smoothly

2. **What could be improved**
   - Memory monitoring gaps
   - Load testing scenarios
   - Library update process

3. **Lucky incidents**
   - Issue occurred during business hours
   - Only affected one region
```

#### Post-Mortem Automation
```python
class PostMortemAutomation:
    def __init__(self, incident_db, monitoring_api):
        self.incident_db = incident_db
        self.monitoring = monitoring_api
        
    def generate_timeline(self, incident_id):
        """Auto-generate incident timeline from logs and alerts"""
        incident = self.incident_db.get(incident_id)
        timeline = []
        
        # Get all alerts during incident window
        alerts = self.monitoring.get_alerts(
            start=incident.start_time,
            end=incident.end_time
        )
        
        # Get deployment events
        deployments = self.get_deployments(
            incident.start_time - timedelta(hours=2),
            incident.end_time
        )
        
        # Get on-call actions
        actions = self.get_oncall_actions(incident_id)
        
        # Merge and sort chronologically
        for alert in alerts:
            timeline.append({
                'time': alert.timestamp,
                'event': f"Alert: {alert.name}",
                'type': 'alert'
            })
            
        return sorted(timeline, key=lambda x: x['time'])
    
    def analyze_patterns(self, incident):
        """Identify patterns from past incidents"""
        similar_incidents = self.incident_db.find_similar(
            services=incident.affected_services,
            time_window=timedelta(days=90)
        )
        
        patterns = {
            'recurring_issues': self.find_recurring_issues(similar_incidents),
            'common_root_causes': self.analyze_root_causes(similar_incidents),
            'time_patterns': self.analyze_time_patterns(similar_incidents)
        }
        
        return patterns
```

**Resources:**
- 📖 [Google's Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- 📖 [Etsy's Debriefing Guide](https://github.com/etsy/DebriefingFacilitationGuide)
- 🎥 [Building a Learning Culture](https://www.youtube.com/watch?v=7Oe2xFX8HdI)

## Monitoring and Alerting

### The Four Golden Signals

```python
# Golden signals monitoring
class GoldenSignals:
    def __init__(self, prometheus):
        self.prom = prometheus
        
    def latency(self, service):
        """Request latency distribution"""
        return {
            'p50': self.get_percentile(service, 50),
            'p95': self.get_percentile(service, 95),
            'p99': self.get_percentile(service, 99),
            'p999': self.get_percentile(service, 99.9)
        }
    
    def traffic(self, service):
        """Request rate"""
        query = f'sum(rate(http_requests_total{{service="{service}"}}[5m]))'
        return self.prom.query(query)
    
    def errors(self, service):
        """Error rate and types"""
        query = f'''
        sum by (status) (
            rate(http_requests_total{{
                service="{service}",
                status=~"4..|5.."
            }}[5m])
        )
        '''
        return self.prom.query(query)
    
    def saturation(self, service):
        """Resource utilization"""
        return {
            'cpu': self.get_cpu_usage(service),
            'memory': self.get_memory_usage(service),
            'disk_io': self.get_disk_io(service),
            'network': self.get_network_usage(service)
        }
```

### Alert Design

```yaml
# Effective alerting rules
groups:
  - name: api_alerts
    interval: 30s
    rules:
      # Alert on SLO burn rate
      - alert: HighErrorBurnRate
        expr: |
          (
            rate(http_requests_total{status=~"5.."}[5m])
            /
            rate(http_requests_total[5m])
          ) > 0.01  # 1% error rate
        for: 5m
        labels:
          severity: page
          team: platform
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "https://runbooks.example.com/high-error-rate"
      
      # Multi-window multi-burn-rate alerts
      - alert: SLOBurnRateHigh
        expr: |
          (
            error_budget_burn_rate_1h > 14.4
            and
            error_budget_burn_rate_5m > 14.4
          )
          or
          (
            error_budget_burn_rate_6h > 6
            and
            error_budget_burn_rate_30m > 6
          )
        labels:
          severity: page
        annotations:
          summary: "SLO burn rate is too high"
```

## Chaos Engineering

### Chaos Testing Framework

```python
import random
from datetime import datetime, timedelta

class ChaosMonkey:
    def __init__(self, kubernetes_client, config):
        self.k8s = kubernetes_client
        self.config = config
        self.enabled = config.get('enabled', False)
        self.dry_run = config.get('dry_run', True)
        
    def run_experiment(self, experiment_type):
        """Run a chaos experiment"""
        if not self.enabled:
            return
            
        experiments = {
            'pod_failure': self.kill_random_pod,
            'network_latency': self.inject_network_latency,
            'cpu_stress': self.inject_cpu_stress,
            'disk_fill': self.fill_disk,
            'clock_skew': self.inject_clock_skew
        }
        
        if experiment_type in experiments:
            self.log_experiment_start(experiment_type)
            result = experiments[experiment_type]()
            self.log_experiment_result(result)
            return result
    
    def kill_random_pod(self, namespace=None):
        """Randomly terminate a pod"""
        if namespace is None:
            namespace = random.choice(self.config['target_namespaces'])
        
        pods = self.k8s.list_namespaced_pod(namespace)
        if not pods.items:
            return
        
        victim = random.choice(pods.items)
        
        if not self.dry_run:
            self.k8s.delete_namespaced_pod(
                name=victim.metadata.name,
                namespace=namespace,
                grace_period_seconds=0
            )
        
        return {
            'experiment': 'pod_failure',
            'target': f"{namespace}/{victim.metadata.name}",
            'dry_run': self.dry_run,
            'timestamp': datetime.utcnow()
        }
    
    def inject_network_latency(self, latency_ms=100, jitter_ms=50):
        """Inject network latency using tc"""
        target_pod = self.select_target_pod()
        
        command = f'''
        tc qdisc add dev eth0 root netem delay {latency_ms}ms {jitter_ms}ms
        '''
        
        if not self.dry_run:
            self.k8s.exec_in_pod(target_pod, command)
        
        # Schedule cleanup
        self.schedule_cleanup(
            target_pod,
            'tc qdisc del dev eth0 root netem',
            delay_minutes=5
        )
```

**Resources:**
- 📚 [Chaos Engineering](https://www.oreilly.com/library/view/chaos-engineering/9781491988459/)
- 🔧 [Chaos Toolkit](https://chaostoolkit.org/)
- 🎥 [Principles of Chaos Engineering](https://www.youtube.com/watch?v=HmBQasGknhI)
- 📖 [Gremlin Chaos Engineering Guide](https://www.gremlin.com/community/tutorials/)

## Capacity Planning

### Capacity Modeling

```python
class CapacityPlanner:
    def __init__(self, metrics_db):
        self.metrics = metrics_db
        
    def forecast_growth(self, metric, days_ahead=90):
        """Forecast resource usage using linear regression"""
        from sklearn.linear_model import LinearRegression
        import numpy as np
        
        # Get historical data
        history = self.metrics.get_metric_history(
            metric,
            days_back=180
        )
        
        # Prepare data for regression
        X = np.array(range(len(history))).reshape(-1, 1)
        y = np.array([point.value for point in history])
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast
        future_X = np.array(range(len(history), len(history) + days_ahead)).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        return {
            'current_value': y[-1],
            'forecast_value': forecast[-1],
            'growth_rate': (forecast[-1] - y[-1]) / y[-1] * 100,
            'reaches_capacity_in_days': self.days_until_capacity(model, y[-1])
        }
    
    def recommend_scaling(self, service):
        """Recommend scaling based on usage patterns"""
        cpu_forecast = self.forecast_growth(f'{service}_cpu_usage')
        memory_forecast = self.forecast_growth(f'{service}_memory_usage')
        traffic_forecast = self.forecast_growth(f'{service}_requests_per_second')
        
        recommendations = []
        
        if cpu_forecast['reaches_capacity_in_days'] < 30:
            recommendations.append({
                'action': 'scale_up',
                'resource': 'cpu',
                'urgency': 'high',
                'reason': f"CPU will reach capacity in {cpu_forecast['reaches_capacity_in_days']} days"
            })
        
        return recommendations
```

## SRE Tools and Automation

### Toil Reduction

```python
class ToilTracker:
    def __init__(self):
        self.toil_tasks = {}
        
    def record_toil(self, task_name, time_spent_minutes, frequency_per_week):
        """Track toil activities"""
        self.toil_tasks[task_name] = {
            'time_per_occurrence': time_spent_minutes,
            'frequency_per_week': frequency_per_week,
            'total_time_per_week': time_spent_minutes * frequency_per_week,
            'automation_potential': self.assess_automation_potential(task_name)
        }
    
    def prioritize_automation(self):
        """Prioritize toil reduction efforts"""
        priorities = []
        
        for task, data in self.toil_tasks.items():
            score = (
                data['total_time_per_week'] * 
                data['automation_potential'] / 100
            )
            priorities.append({
                'task': task,
                'score': score,
                'time_saved_per_week': data['total_time_per_week'],
                'effort_estimate': self.estimate_automation_effort(task)
            })
        
        return sorted(priorities, key=lambda x: x['score'], reverse=True)
```

### SRE Dashboards

```yaml
# Grafana dashboard for SRE metrics
{
  "dashboard": {
    "title": "SRE Golden Signals",
    "panels": [
      {
        "title": "Error Budget Burn Rate",
        "targets": [{
          "expr": "1 - (sum(rate(http_requests_total{status!~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])))"
        }]
      },
      {
        "title": "Latency Percentiles",
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))"
        }]
      },
      {
        "title": "Alert Fatigue Score",
        "targets": [{
          "expr": "sum(increase(alerts_fired_total[1d])) / sum(increase(alerts_acknowledged_total[1d]))"
        }]
      }
    ]
  }
}
```

## Interview Questions

### Conceptual Questions
1. Explain the difference between SLI, SLO, and SLA
2. How do you calculate and use error budgets?
3. What makes a good alert?
4. Describe the incident commander role
5. How do you balance reliability vs feature velocity?

### Practical Scenarios
1. Design an on-call rotation for a global team
2. Create SLOs for a payment processing system
3. Plan a chaos engineering program
4. Build a capacity planning model
5. Reduce toil in a manual deployment process

## Essential Resources

### Books
- 📚 [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) - Google (Free)
- 📚 [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/) - Google (Free)
- 📚 [Seeking SRE](https://www.oreilly.com/library/view/seeking-sre/9781491978856/) - David Blank-Edelman

### Courses
- 🎓 [Google SRE Training](https://sre.google/classroom/)
- 🎓 [School of SRE](https://linkedin.github.io/school-of-sre/) - LinkedIn
- 🎓 [SREcon Videos](https://www.usenix.org/conferences/byname/925) - USENIX

### Tools
- 🔧 [Prometheus](https://prometheus.io/) - Monitoring
- 🔧 [PagerDuty](https://www.pagerduty.com/) - Incident management
- 🔧 [Blameless](https://www.blameless.com/) - SRE platform
- 🔧 [SLO Generator](https://github.com/google/slo-generator) - Google

### Communities
- 💬 [SRE Weekly Newsletter](https://sreweekly.com/)
- 💬 [r/SRE](https://reddit.com/r/sre) - Reddit community
- 💬 [SREcon](https://www.usenix.org/srecon) - Conference
- 💬 [Google SRE Discussion Group](https://groups.google.com/g/sre-discuss)

Remember: SRE is about applying software engineering principles to operations problems. Focus on automation, measurement, and continuous improvement to build reliable systems at scale.