# Splunk

## Overview

Splunk is a powerful platform for searching, monitoring, and analyzing machine-generated big data. It's widely used for log analysis, security monitoring, operational intelligence, and business analytics in enterprise environments.

## Key Features

- **Universal Data Ingestion**: Collect data from any source
- **Search Processing Language (SPL)**: Powerful query language
- **Real-time Processing**: Stream processing and real-time analytics
- **Machine Learning**: Built-in ML capabilities for anomaly detection
- **Dashboards and Visualizations**: Rich visualization capabilities

## Basic Concepts

### Data Pipeline
```
Data Sources → Forwarders → Indexers → Search Heads
```

### SPL (Search Processing Language)
```spl
# Basic search
index=web_logs error

# Time range search
index=web_logs earliest=-24h@h latest=@h

# Field extraction
index=web_logs | rex field=_raw "(?<ip>\d+\.\d+\.\d+\.\d+)"

# Statistical operations
index=web_logs | stats count by status_code

# Timechart
index=web_logs | timechart span=1h count by status_code
```

## Common Use Cases

### Log Analysis
```spl
# Find all error events in the last hour
index=application_logs level=ERROR earliest=-1h

# Top error messages
index=application_logs level=ERROR 
| stats count by message 
| sort -count 
| head 10

# Error rate over time
index=application_logs 
| eval is_error=if(level="ERROR", 1, 0) 
| timechart span=15m avg(is_error) as error_rate

# Failed login attempts
index=security_logs action=login result=failure 
| stats count by user, src_ip 
| where count > 5

# Response time analysis
index=web_logs 
| rex field=_raw "response_time=(?<response_time>\d+)" 
| eval response_time=tonumber(response_time) 
| stats avg(response_time) as avg_response, max(response_time) as max_response by endpoint
```

### Infrastructure Monitoring
```spl
# CPU usage monitoring
index=infrastructure_metrics metric_name="cpu.usage" 
| timechart span=5m avg(value) by host

# Memory usage alerts
index=infrastructure_metrics metric_name="memory.usage" 
| where value > 80 
| stats count by host 
| where count > 10

# Disk space monitoring
index=infrastructure_metrics metric_name="disk.usage" 
| where value > 90 
| eval alert_level=case(value > 95, "critical", value > 90, "warning") 
| table _time, host, filesystem, value, alert_level

# Network traffic analysis
index=network_logs 
| eval bytes_mb=bytes/1024/1024 
| timechart span=1h sum(bytes_mb) as total_mb by direction
```

### Security Analysis
```spl
# Suspicious login patterns
index=security_logs action=login 
| stats dc(src_ip) as unique_ips by user 
| where unique_ips > 10

# Failed authentication analysis
index=security_logs action=authentication result=failure 
| stats count by user, src_ip, app 
| sort -count

# Privilege escalation detection
index=security_logs action=privilege_change 
| eval risk_score=case(
    old_role="user" AND new_role="admin", 10,
    old_role="user" AND new_role="power_user", 5,
    1=1, 1
) 
| where risk_score > 5

# Data exfiltration detection
index=network_logs 
| where bytes_out > 1000000 
| stats sum(bytes_out) as total_bytes by src_ip, dest_ip 
| where total_bytes > 10000000
```

## Configuration

### inputs.conf
```ini
# Monitor log files
[monitor:///var/log/app/*.log]
index = application_logs
sourcetype = app_logs
host_segment = 3

# Monitor Windows Event Logs
[WinEventLog:Security]
index = windows_security
disabled = 0

# TCP input
[tcp://9997]
index = network_data
sourcetype = syslog

# Universal Forwarder configuration
[tcpout]
defaultGroup = default-autolb-group

[tcpout:default-autolb-group]
server = splunk-indexer1:9997, splunk-indexer2:9997
```

### props.conf
```ini
# Custom sourcetype
[app_logs]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%d %H:%M:%S
MAX_TIMESTAMP_LOOKAHEAD = 19
TRUNCATE = 10000

# JSON log extraction
[json_logs]
KV_MODE = json
AUTO_KV_JSON = true
SHOULD_LINEMERGE = false

# Regular expression field extraction
[web_logs]
EXTRACT-fields = ^(?<client_ip>\S+) \S+ \S+ \[(?<timestamp>[^\]]+)\] "(?<method>\S+) (?<uri>\S+) (?<protocol>\S+)" (?<status_code>\d+) (?<bytes>\d+)
```

### transforms.conf
```ini
# Field transformation
[extract_user_agent]
REGEX = User-Agent:\s*(.*)
FORMAT = user_agent::$1

# Lookup table
[user_lookup]
filename = users.csv
case_sensitive_match = false
```

## Dashboard Creation

### Simple Dashboard XML
```xml
<dashboard>
  <label>Application Performance</label>
  <row>
    <panel>
      <title>Request Volume</title>
      <chart>
        <search>
          <query>
            index=web_logs 
            | timechart span=1h count as requests
          </query>
          <earliest>-24h@h</earliest>
          <latest>@h</latest>
        </search>
        <option name="charting.chart">line</option>
      </chart>
    </panel>
    <panel>
      <title>Error Rate</title>
      <single>
        <search>
          <query>
            index=web_logs 
            | eval is_error=if(status_code >= 400, 1, 0) 
            | stats sum(is_error) as errors, count as total 
            | eval error_rate=round((errors/total)*100, 2)
          </query>
          <earliest>-1h@h</earliest>
          <latest>@h</latest>
        </search>
        <option name="drilldown">none</option>
        <option name="unit">%</option>
      </single>
    </panel>
  </row>
  <row>
    <panel>
      <title>Top Errors</title>
      <table>
        <search>
          <query>
            index=application_logs level=ERROR 
            | stats count by message 
            | sort -count 
            | head 10
          </query>
          <earliest>-4h@h</earliest>
          <latest>@h</latest>
        </search>
      </table>
    </panel>
  </row>
</dashboard>
```

## Alerting

### Basic Alert Configuration
```spl
# Search query for alert
index=application_logs level=ERROR 
| stats count as error_count 
| where error_count > 10

# Alert conditions
# Time range: Last 15 minutes
# Trigger condition: Search returns results
# Throttle: 5 minutes
```

### Advanced Alert with Custom Script
```python
#!/usr/bin/env python
import sys
import json
import requests

def send_alert(alert_data):
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    
    message = {
        "text": f"Splunk Alert: {alert_data['search_name']}",
        "attachments": [
            {
                "color": "danger",
                "fields": [
                    {
                        "title": "Alert",
                        "value": alert_data['search_name'],
                        "short": True
                    },
                    {
                        "title": "Count",
                        "value": alert_data['result_count'],
                        "short": True
                    }
                ]
            }
        ]
    }
    
    requests.post(webhook_url, json=message)

if __name__ == "__main__":
    alert_data = json.loads(sys.stdin.read())
    send_alert(alert_data)
```

## Data Models and Pivot

### Data Model Definition
```json
{
  "modelName": "Web_Access",
  "objects": [
    {
      "objectName": "Web_Access",
      "fields": [
        {
          "fieldName": "clientip",
          "displayName": "Client IP",
          "type": "string"
        },
        {
          "fieldName": "status",
          "displayName": "Status Code", 
          "type": "number"
        },
        {
          "fieldName": "bytes",
          "displayName": "Bytes",
          "type": "number"
        }
      ],
      "constraints": [
        {
          "search": "index=web_logs sourcetype=access_combined"
        }
      ]
    }
  ]
}
```

### Pivot Search
```spl
| pivot Web_Access Web_Access 
  count(Web_Access) AS "Count" 
  SPLITROW status AS "Status Code" 
  SPLITCOL _time AS _time PERIOD auto 
  SORT 100 _time ROWSUMMARY 0 COLSUMMARY 0 NUMCOLS 100 SHOWOTHER 1
```

## Machine Learning

### Anomaly Detection
```spl
# Train model to detect CPU usage anomalies
| inputlookup cpu_usage_data.csv 
| fit DensityFunction algorithm=OneClassSVM cpu_usage into cpu_anomaly_model

# Apply model to detect anomalies
index=infrastructure_metrics metric_name="cpu.usage" 
| apply cpu_anomaly_model 
| where IsOutlier=1
```

### Clustering
```spl
# Cluster similar error patterns
index=application_logs level=ERROR 
| cluster field=message 
| stats count by cluster_label, cluster_count 
| sort -count
```

### Forecasting
```spl
# Predict future disk usage
index=infrastructure_metrics metric_name="disk.usage" 
| timechart span=1d avg(value) as avg_usage 
| predict avg_usage as predicted_usage algorithm=LLP future_timespan=7 
| eval capacity_reached=if(predicted_usage > 90, "YES", "NO")
```

## REST API Usage

### Search API
```python
import splunklib.client as client

# Connect to Splunk
service = client.connect(
    host='localhost',
    port=8089,
    username='admin',
    password='password'
)

# Run search
search_query = 'search index=web_logs | stats count by status_code'
job = service.jobs.create(search_query)

# Wait for completion
while not job.is_done():
    time.sleep(1)

# Get results
results = job.results()
for result in results:
    print(f"Status: {result['status_code']}, Count: {result['count']}")
```

### Configuration Management
```python
# Create index
service.indexes.create('new_index', maxDataSize='auto')

# Create saved search
saved_searches = service.saved_searches
saved_searches.create(
    'daily_error_report',
    'index=application_logs level=ERROR | stats count by message'
)

# Update inputs
inputs = service.inputs
monitor_input = inputs.create(
    '/var/log/new_app/*.log',
    'monitor',
    index='new_index',
    sourcetype='new_app_logs'
)
```

## Best Practices

- Use summary indexing for frequently accessed historical data
- Implement proper time-based retention policies
- Use lookup tables for data enrichment
- Design efficient searches with proper time ranges
- Implement field extraction at search time when possible
- Use data models for consistent field naming
- Monitor license usage and optimize data ingestion
- Implement proper role-based access control

## Great Resources

- [Splunk Documentation](https://docs.splunk.com/) - Official comprehensive documentation
- [Splunk Search Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference) - Complete SPL reference
- [Splunk Education](https://education.splunk.com/) - Training courses and certifications
- [Splunkbase](https://splunkbase.splunk.com/) - Apps and add-ons marketplace
- [Splunk Answers](https://community.splunk.com/) - Community forum and knowledge base
- [Splunk GitHub](https://github.com/splunk) - Open source tools and SDKs
- [SPL Cheat Sheet](https://www.splunk.com/en_us/resources/search-cheat-sheet.html) - Quick SPL reference guide