---
title: Security & Compliance Deep Dive
sidebar_position: 12
---

# Security & Compliance for Platform Engineering

Master the security practices and compliance requirements essential for building and operating secure platforms. From zero-trust architecture to regulatory compliance, learn how to protect infrastructure at scale.

## Zero Trust Architecture

### Principles and Implementation

**Core Zero Trust Principles:**
1. **Never trust, always verify**
2. **Least privilege access**
3. **Assume breach**
4. **Verify explicitly**

```python
# Zero Trust Network Access (ZTNA) Implementation
import jwt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import asyncio
from typing import Dict, List, Optional

class ZeroTrustGateway:
    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.identity_provider = IdentityProvider()
        self.device_trust = DeviceTrustService()
        self.risk_engine = RiskAssessmentEngine()
    
    async def authenticate_request(self, request):
        """Multi-factor authentication flow"""
        # 1. Device attestation
        device_score = await self.device_trust.verify_device(
            request.device_id,
            request.device_fingerprint
        )
        
        # 2. User authentication
        user = await self.identity_provider.authenticate(
            request.credentials,
            require_mfa=True
        )
        
        # 3. Context evaluation
        context = {
            'user': user,
            'device_score': device_score,
            'location': request.geo_location,
            'time': request.timestamp,
            'network': request.source_network,
            'behavior_score': await self.get_behavior_score(user.id)
        }
        
        # 4. Risk assessment
        risk_score = await self.risk_engine.assess(context)
        
        # 5. Policy decision
        decision = await self.policy_engine.evaluate(
            subject=user,
            resource=request.resource,
            action=request.action,
            context=context,
            risk_score=risk_score
        )
        
        if decision.allowed:
            # Generate short-lived token
            return self.generate_access_token(
                user=user,
                permissions=decision.permissions,
                ttl=min(300, decision.max_ttl)  # 5 minutes max
            )
        
        raise AccessDeniedException(decision.reason)

class PolicyEngine:
    def __init__(self):
        self.policies = self.load_policies()
    
    async def evaluate(self, subject, resource, action, context, risk_score):
        """OPA-style policy evaluation"""
        # Example policy in Rego-like syntax
        policy = f"""
        allow = true {{
            input.subject.role in {resource.allowed_roles}
            input.action in {resource.allowed_actions}
            input.context.device_score > 0.8
            input.risk_score < 0.3
            input.context.location.country in ["US", "EU"]
        }}
        
        # Require additional authentication for sensitive resources
        require_step_up = true {{
            input.resource.sensitivity == "high"
            input.context.last_auth_time > 600  # 10 minutes
        }}
        """
        
        return await self.execute_policy(policy, {
            'subject': subject,
            'resource': resource,
            'action': action,
            'context': context,
            'risk_score': risk_score
        })
```

### Service Mesh Security

```yaml
# Istio security configuration
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-gateway-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/*"]
    when:
    - key: request.headers[x-request-id]
      notValues: [""]
    - key: source.ip
      notValues: ["0.0.0.0/0"]
```

**Resources:**
- 📚 [Zero Trust Architecture - NIST SP 800-207](https://www.nist.gov/publications/zero-trust-architecture)
- 📖 [Google BeyondCorp](https://cloud.google.com/beyondcorp)
- 🎥 [Zero Trust Security Model](https://www.youtube.com/watch?v=wWFh_kPRMfI)

## Secrets Management

### HashiCorp Vault Implementation

```python
# Vault integration for secrets management
import hvac
from cryptography.fernet import Fernet
import base64
import os

class SecretManager:
    def __init__(self, vault_url, namespace="platform"):
        self.client = hvac.Client(url=vault_url, namespace=namespace)
        self.authenticate()
        self.setup_encryption()
    
    def authenticate(self):
        """Kubernetes service account authentication"""
        jwt_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        role = os.environ.get("VAULT_ROLE", "platform-app")
        
        with open(jwt_path, 'r') as f:
            jwt = f.read()
        
        self.client.auth.kubernetes.login(
            role=role,
            jwt=jwt
        )
    
    def get_secret(self, path, key=None, version=None):
        """Retrieve secret with caching and rotation support"""
        try:
            # Read from KV v2 secret engine
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                version=version
            )
            
            data = response['data']['data']
            
            if key:
                return data.get(key)
            return data
            
        except Exception as e:
            # Fallback to encrypted local cache
            cached = self.get_cached_secret(path, key)
            if cached:
                return cached
            raise
    
    def rotate_secret(self, path, generator_func):
        """Automatic secret rotation"""
        # Generate new secret
        new_secret = generator_func()
        
        # Store in Vault with metadata
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret={
                'value': new_secret,
                'rotated_at': datetime.utcnow().isoformat(),
                'rotation_version': self.get_rotation_version(path) + 1
            },
            cas=None  # Check-and-set for concurrent updates
        )
        
        # Trigger dependent service updates
        self.notify_secret_consumers(path)
        
        return new_secret
    
    def setup_dynamic_credentials(self, database_name):
        """Dynamic database credentials"""
        # Configure database secret engine
        self.client.secrets.database.configure(
            name=database_name,
            plugin_name='postgresql-database-plugin',
            connection_url='postgresql://{{username}}:{{password}}@postgres:5432/mydb',
            allowed_roles=['readonly', 'readwrite'],
            username='vault',
            password=self.get_secret('database/admin', 'password')
        )
        
        # Create role for dynamic credentials
        self.client.secrets.database.create_role(
            name='app-role',
            db_name=database_name,
            creation_statements=[
                "CREATE USER '{{name}}' WITH PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'",
                "GRANT SELECT ON ALL TABLES IN SCHEMA public TO '{{name}}'"
            ],
            default_ttl='1h',
            max_ttl='24h'
        )
```

### Kubernetes Secrets Management

```yaml
# Sealed Secrets for GitOps
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: api-credentials
  namespace: production
spec:
  encryptedData:
    api_key: AgBvA8kZ1H9SGqyjm8Ql5qdtCAP3U1vka...
    api_secret: AgCJL6dCgXBzAY3sgHJoNBk2xAvaG9H...
  template:
    metadata:
      name: api-credentials
      namespace: production
    type: Opaque

---
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.internal:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "platform-role"
          serviceAccountRef:
            name: "external-secrets"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 15m
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: password
    remoteRef:
      key: database/credentials
      property: password
```

**Resources:**
- 📖 [Vault Best Practices](https://learn.hashicorp.com/tutorials/vault/patterns-direct-application-integration)
- 📖 [Kubernetes Secrets Management](https://kubernetes.io/docs/concepts/configuration/secret/)
- 🔧 [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)

## Container Security

### Image Scanning and Policy

```python
# Container image security scanning
import docker
import json
from typing import Dict, List

class ContainerSecurityScanner:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.vulnerability_db = VulnerabilityDatabase()
        self.policy_engine = SecurityPolicyEngine()
    
    async def scan_image(self, image_name: str) -> Dict:
        """Comprehensive container image security scan"""
        results = {
            'image': image_name,
            'scan_time': datetime.utcnow(),
            'vulnerabilities': [],
            'misconfigurations': [],
            'secrets': [],
            'compliance': {}
        }
        
        # Pull and analyze image
        image = self.docker_client.images.pull(image_name)
        
        # 1. Vulnerability scanning
        vulns = await self.scan_vulnerabilities(image)
        results['vulnerabilities'] = vulns
        
        # 2. Configuration scanning
        configs = await self.scan_configurations(image)
        results['misconfigurations'] = configs
        
        # 3. Secret scanning
        secrets = await self.scan_secrets(image)
        results['secrets'] = secrets
        
        # 4. Compliance checking
        compliance = await self.check_compliance(image)
        results['compliance'] = compliance
        
        # 5. Generate security score
        results['security_score'] = self.calculate_security_score(results)
        
        return results
    
    async def scan_vulnerabilities(self, image):
        """Scan for CVEs in packages"""
        layers = image.attrs['RootFS']['Layers']
        vulnerabilities = []
        
        for layer in layers:
            # Extract packages from layer
            packages = await self.extract_packages(layer)
            
            for package in packages:
                vulns = await self.vulnerability_db.check_package(
                    name=package['name'],
                    version=package['version'],
                    ecosystem=package['ecosystem']
                )
                
                for vuln in vulns:
                    vulnerabilities.append({
                        'id': vuln['id'],
                        'severity': vuln['severity'],
                        'package': package['name'],
                        'version': package['version'],
                        'fixed_in': vuln.get('fixed_in'),
                        'description': vuln['description']
                    })
        
        return vulnerabilities
    
    async def enforce_policies(self, scan_results):
        """Enforce security policies on scan results"""
        policy = """
        package container.security
        
        default allow = false
        
        # Deny critical vulnerabilities
        deny[msg] {
            input.vulnerabilities[_].severity == "CRITICAL"
            msg := "Image contains critical vulnerabilities"
        }
        
        # Deny high vulnerabilities in production
        deny[msg] {
            input.environment == "production"
            count([v | v := input.vulnerabilities[_]; v.severity == "HIGH"]) > 3
            msg := "Too many high severity vulnerabilities for production"
        }
        
        # Deny exposed secrets
        deny[msg] {
            count(input.secrets) > 0
            msg := sprintf("Image contains %d exposed secrets", [count(input.secrets)])
        }
        
        # Require non-root user
        deny[msg] {
            input.config.User == ""
            msg := "Container must not run as root"
        }
        
        # Require security updates
        deny[msg] {
            input.base_image_age_days > 30
            msg := "Base image is too old, security updates required"
        }
        
        allow {
            count(deny) == 0
        }
        """
        
        return await self.policy_engine.evaluate(policy, scan_results)
```

### Runtime Security

```yaml
# Falco runtime security rules
- rule: Unauthorized Process in Container
  desc: Detect unauthorized process execution
  condition: >
    spawned_process and container and
    not proc.name in (allowed_processes) and
    not container.image.repository in (trusted_repos)
  output: >
    Unauthorized process started in container
    (user=%user.name command=%proc.cmdline container=%container.info)
  priority: WARNING
  tags: [container, process]

- rule: Container Privilege Escalation
  desc: Detect privilege escalation attempts
  condition: >
    spawned_process and container and
    proc.name in (sudo, su) and
    not user.name in (allowed_sudo_users)
  output: >
    Privilege escalation attempt in container
    (user=%user.name command=%proc.cmdline container=%container.info)
  priority: CRITICAL
  tags: [container, privilege_escalation]

---
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

## Network Security

### Network Policies and Segmentation

```yaml
# Kubernetes NetworkPolicy for microsegmentation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress
    - podSelector:
        matchLabels:
          app: load-balancer
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
    ports:
    - protocol: TCP
      port: 5432  # Database
    - protocol: TCP
      port: 6379  # Redis
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    - podSelector:
        matchLabels:
          app: prometheus
    ports:
    - protocol: TCP
      port: 9090
```

### Web Application Firewall (WAF)

```python
# ModSecurity rules integration
class WAFEngine:
    def __init__(self):
        self.rules = self.load_modsecurity_rules()
        self.anomaly_threshold = 5
        
    def analyze_request(self, request):
        """Analyze HTTP request for attacks"""
        anomaly_score = 0
        blocked = False
        matched_rules = []
        
        # Check OWASP Core Rule Set
        checks = [
            self.check_sql_injection,
            self.check_xss,
            self.check_path_traversal,
            self.check_command_injection,
            self.check_xxe,
            self.check_ssrf
        ]
        
        for check in checks:
            result = check(request)
            if result['matched']:
                anomaly_score += result['score']
                matched_rules.extend(result['rules'])
                
                if result['severity'] == 'CRITICAL':
                    blocked = True
                    break
        
        # Anomaly scoring mode
        if anomaly_score >= self.anomaly_threshold:
            blocked = True
        
        return {
            'blocked': blocked,
            'anomaly_score': anomaly_score,
            'matched_rules': matched_rules,
            'action': 'BLOCK' if blocked else 'ALLOW'
        }
    
    def check_sql_injection(self, request):
        """SQL injection detection"""
        sql_patterns = [
            r"(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\s",
            r"(\'|\")(\s)*OR(\s)*\1(\s)*=(\s)*\1",
            r"(\'|\")\s*;\s*(SELECT|INSERT|UPDATE|DELETE)",
            r"(SLEEP\s*\(\s*\d+\s*\)|BENCHMARK\s*\()"
        ]
        
        score = 0
        matched = []
        
        # Check all request parameters
        for param_value in request.get_all_params().values():
            for pattern in sql_patterns:
                if re.search(pattern, param_value, re.IGNORECASE):
                    score += 5
                    matched.append(f"SQL Injection: {pattern}")
        
        return {
            'matched': len(matched) > 0,
            'score': score,
            'rules': matched,
            'severity': 'CRITICAL' if score > 10 else 'HIGH'
        }
```

## Compliance Automation

### Compliance as Code

```python
# Compliance automation framework
class ComplianceFramework:
    def __init__(self):
        self.frameworks = {
            'pci_dss': PCIDSSCompliance(),
            'hipaa': HIPAACompliance(),
            'gdpr': GDPRCompliance(),
            'soc2': SOC2Compliance(),
            'cis': CISBenchmark()
        }
    
    async def audit_infrastructure(self, scope, frameworks):
        """Run compliance audit across infrastructure"""
        results = {
            'audit_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'scope': scope,
            'findings': {},
            'summary': {}
        }
        
        for framework_name in frameworks:
            if framework_name not in self.frameworks:
                continue
            
            framework = self.frameworks[framework_name]
            findings = await framework.audit(scope)
            
            results['findings'][framework_name] = findings
            results['summary'][framework_name] = {
                'total_controls': len(findings),
                'passed': len([f for f in findings if f['status'] == 'PASS']),
                'failed': len([f for f in findings if f['status'] == 'FAIL']),
                'compliance_score': self.calculate_compliance_score(findings)
            }
        
        # Generate remediation plan
        results['remediation'] = self.generate_remediation_plan(results['findings'])
        
        return results

class PCIDSSCompliance:
    async def audit(self, scope):
        """PCI DSS compliance checks"""
        controls = []
        
        # Requirement 2: Default passwords
        controls.append(await self.check_default_passwords(scope))
        
        # Requirement 3: Cardholder data protection
        controls.append(await self.check_encryption_at_rest(scope))
        
        # Requirement 8: User authentication
        controls.append(await self.check_mfa_enabled(scope))
        
        # Requirement 10: Logging
        controls.append(await self.check_audit_logging(scope))
        
        # Requirement 11: Security testing
        controls.append(await self.check_vulnerability_scanning(scope))
        
        return controls
    
    async def check_encryption_at_rest(self, scope):
        """Check encryption at rest for sensitive data"""
        findings = []
        
        # Check database encryption
        for database in scope.databases:
            encrypted = await self.verify_database_encryption(database)
            findings.append({
                'resource': f"database/{database.name}",
                'encrypted': encrypted,
                'algorithm': database.encryption_algorithm if encrypted else None
            })
        
        # Check volume encryption
        for volume in scope.volumes:
            encrypted = await self.verify_volume_encryption(volume)
            findings.append({
                'resource': f"volume/{volume.id}",
                'encrypted': encrypted,
                'kms_key': volume.kms_key_id if encrypted else None
            })
        
        return {
            'control_id': 'PCI-DSS-3.4',
            'description': 'Encryption at rest for cardholder data',
            'status': 'PASS' if all(f['encrypted'] for f in findings) else 'FAIL',
            'findings': findings
        }
```

### GDPR Compliance

```python
# GDPR compliance automation
class GDPRComplianceEngine:
    def __init__(self):
        self.data_map = DataMap()
        self.consent_manager = ConsentManager()
        
    async def ensure_data_privacy(self):
        """Implement GDPR privacy requirements"""
        controls = []
        
        # Data minimization
        controls.append(await self.enforce_data_minimization())
        
        # Right to erasure
        controls.append(await self.implement_data_deletion())
        
        # Data portability
        controls.append(await self.enable_data_export())
        
        # Consent management
        controls.append(await self.verify_consent_mechanisms())
        
        return controls
    
    async def implement_data_deletion(self):
        """Right to be forgotten implementation"""
        deletion_policy = """
        async def delete_user_data(user_id: str, confirmation_token: str):
            # Verify deletion request
            if not await verify_deletion_token(user_id, confirmation_token):
                raise InvalidDeletionRequest()
            
            # Start deletion transaction
            async with db.transaction():
                # 1. Export data for records
                user_data = await export_user_data(user_id)
                await store_deletion_record(user_id, user_data)
                
                # 2. Delete from primary database
                await db.users.delete(user_id)
                await db.user_profiles.delete(user_id)
                await db.user_preferences.delete(user_id)
                
                # 3. Delete from caches
                await redis.delete(f"user:{user_id}:*")
                
                # 4. Queue deletion from backups
                await queue_backup_deletion(user_id, retention_days=30)
                
                # 5. Delete from analytics
                await anonymize_analytics_data(user_id)
                
                # 6. Notify third-party processors
                await notify_data_processors(user_id, 'DELETE')
            
            return {
                'status': 'deleted',
                'timestamp': datetime.utcnow(),
                'retention_notice': 'Backup deletion in 30 days'
            }
        """
        
        return {
            'control': 'GDPR Article 17',
            'description': 'Right to erasure',
            'implementation': 'automated',
            'status': 'IMPLEMENTED'
        }
```

## Security Monitoring and SIEM

### Security Event Collection

```python
# Centralized security logging
class SecurityEventCollector:
    def __init__(self):
        self.elasticsearch = AsyncElasticsearch()
        self.alert_manager = AlertManager()
        
    async def process_security_event(self, event):
        """Process and enrich security events"""
        # Enrich with threat intelligence
        event['threat_intel'] = await self.enrich_with_threat_intel(event)
        
        # Add context
        event['context'] = {
            'user_risk_score': await self.get_user_risk_score(event.get('user_id')),
            'asset_criticality': await self.get_asset_criticality(event.get('asset_id')),
            'related_events': await self.find_related_events(event)
        }
        
        # Classify event
        event['classification'] = self.classify_event(event)
        
        # Store in SIEM
        await self.elasticsearch.index(
            index=f"security-events-{datetime.now():%Y.%m.%d}",
            body=event
        )
        
        # Check for alerts
        if await self.should_alert(event):
            await self.alert_manager.create_alert(event)
        
        return event
    
    def classify_event(self, event):
        """Classify security events using MITRE ATT&CK"""
        mitre_mapping = {
            'failed_login': 'T1110',  # Brute Force
            'privilege_escalation': 'T1068',  # Exploitation
            'data_exfiltration': 'T1048',  # Exfiltration
            'lateral_movement': 'T1021',  # Remote Services
        }
        
        return {
            'severity': self.calculate_severity(event),
            'category': event.get('category', 'unknown'),
            'mitre_attack': mitre_mapping.get(event['type'], 'unknown'),
            'kill_chain_phase': self.map_to_kill_chain(event)
        }
```

### Incident Response Automation

```python
# Automated incident response
class IncidentResponseAutomation:
    def __init__(self):
        self.playbooks = self.load_playbooks()
        self.soar_platform = SOARPlatform()
        
    async def handle_security_incident(self, incident):
        """Automated incident response orchestration"""
        # 1. Contain the threat
        containment_actions = await self.contain_threat(incident)
        
        # 2. Investigate
        investigation_results = await self.investigate(incident)
        
        # 3. Remediate
        remediation_actions = await self.remediate(
            incident, 
            investigation_results
        )
        
        # 4. Recover
        recovery_status = await self.recover(incident)
        
        # 5. Document
        report = await self.generate_incident_report({
            'incident': incident,
            'containment': containment_actions,
            'investigation': investigation_results,
            'remediation': remediation_actions,
            'recovery': recovery_status
        })
        
        return report
    
    async def contain_threat(self, incident):
        """Immediate containment actions"""
        actions = []
        
        if incident.type == 'compromised_credentials':
            # Disable affected accounts
            for user_id in incident.affected_users:
                await self.disable_user_account(user_id)
                await self.revoke_user_sessions(user_id)
                actions.append(f"Disabled account: {user_id}")
        
        elif incident.type == 'malicious_process':
            # Isolate affected systems
            for host in incident.affected_hosts:
                await self.isolate_host(host)
                await self.kill_process(host, incident.process_id)
                actions.append(f"Isolated host: {host}")
        
        elif incident.type == 'data_breach':
            # Block data exfiltration
            await self.block_outbound_traffic(incident.source_ip)
            await self.revoke_api_keys(incident.compromised_keys)
            actions.append("Blocked data exfiltration channels")
        
        return actions
```

## Cloud Security

### Multi-Cloud Security Posture

```python
# Cloud Security Posture Management (CSPM)
class CloudSecurityPostureManager:
    def __init__(self):
        self.providers = {
            'aws': AWSSecurityScanner(),
            'gcp': GCPSecurityScanner(),
            'azure': AzureSecurityScanner()
        }
        
    async def scan_cloud_resources(self):
        """Comprehensive cloud security scan"""
        findings = {
            'scan_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'providers': {}
        }
        
        for provider_name, scanner in self.providers.items():
            findings['providers'][provider_name] = {
                'misconfigurations': await scanner.find_misconfigurations(),
                'compliance': await scanner.check_compliance(),
                'vulnerabilities': await scanner.scan_vulnerabilities(),
                'cost_optimization': await scanner.find_cost_issues()
            }
        
        # Generate risk score
        findings['risk_score'] = self.calculate_risk_score(findings)
        
        # Create remediation plan
        findings['remediation'] = self.generate_remediation_plan(findings)
        
        return findings

class AWSSecurityScanner:
    async def find_misconfigurations(self):
        """Scan for AWS misconfigurations"""
        checks = [
            self.check_s3_public_access(),
            self.check_security_group_rules(),
            self.check_iam_policies(),
            self.check_encryption_settings(),
            self.check_logging_enabled(),
            self.check_mfa_enforcement()
        ]
        
        results = await asyncio.gather(*checks)
        return [r for r in results if r['severity'] != 'PASS']
    
    async def check_s3_public_access(self):
        """Check S3 buckets for public access"""
        s3 = boto3.client('s3')
        findings = []
        
        buckets = s3.list_buckets()['Buckets']
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Check bucket ACL
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            public_access = any(
                grant['Grantee'].get('Type') == 'Group' and
                grant['Grantee'].get('URI', '').endswith('AllUsers')
                for grant in acl['Grants']
            )
            
            if public_access:
                findings.append({
                    'resource': f"s3://{bucket_name}",
                    'issue': 'Bucket has public access',
                    'severity': 'HIGH',
                    'remediation': 'Remove public access permissions'
                })
        
        return {
            'check': 'S3 Public Access',
            'findings': findings,
            'severity': 'HIGH' if findings else 'PASS'
        }
```

## Interview Preparation

### Security Architecture Questions
1. Design a zero-trust architecture for a microservices platform
2. Implement end-to-end encryption for a messaging system
3. Design a secrets management system for Kubernetes
4. Create a security monitoring and incident response platform

### Compliance Questions
1. How do you implement GDPR compliance in a distributed system?
2. Design automated compliance checking for PCI DSS
3. Implement data retention policies across multiple databases
4. Create audit logging for regulatory compliance

### Practical Scenarios
1. Respond to a container escape vulnerability
2. Investigate and contain a data breach
3. Implement security scanning in CI/CD pipeline
4. Design defense against DDoS attacks

## Essential Resources

### Books
- 📚 [Container Security](https://www.oreilly.com/library/view/container-security/9781492056690/) - Liz Rice
- 📚 [Kubernetes Security](https://www.amazon.com/Kubernetes-Security-Operating-Applications-Securely/dp/1492039071) - Liz Rice & Michael Hausenblas
- 📚 [Zero Trust Networks](https://www.oreilly.com/library/view/zero-trust-networks/9781491962183/) - Evan Gilman & Doug Barth

### Certifications
- 🎓 [Certified Kubernetes Security Specialist (CKS)](https://www.cncf.io/certification/cks/)
- 🎓 [AWS Certified Security - Specialty](https://aws.amazon.com/certification/certified-security-specialty/)
- 🎓 [Google Cloud Security Engineer](https://cloud.google.com/certification/cloud-security-engineer)

### Tools
- 🔧 [Falco](https://falco.org/) - Runtime security
- 🔧 [OPA (Open Policy Agent)](https://www.openpolicyagent.org/) - Policy engine
- 🔧 [Trivy](https://github.com/aquasecurity/trivy) - Vulnerability scanner
- 🔧 [OWASP ZAP](https://www.zaproxy.org/) - Web application security

### Communities
- 💬 [Cloud Native Security](https://www.cncf.io/projects/security/)
- 💬 [OWASP](https://owasp.org/) - Application security
- 💬 [r/netsec](https://reddit.com/r/netsec) - Network security

Remember: Security is not a feature, it's a fundamental requirement. Build security into every layer of your platform from the ground up.