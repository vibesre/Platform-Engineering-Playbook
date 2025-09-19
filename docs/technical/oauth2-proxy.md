# OAuth2 Proxy

OAuth2 Proxy is a reverse proxy that provides authentication using OAuth2 providers. It acts as a security layer to authenticate users before they can access applications.

## Installation

### Binary Installation
```bash
# Download latest release
curl -LO https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.4.0/oauth2-proxy-v7.4.0.linux-amd64.tar.gz
tar -xzf oauth2-proxy-v7.4.0.linux-amd64.tar.gz
sudo mv oauth2-proxy-v7.4.0.linux-amd64/oauth2-proxy /usr/local/bin/

# Verify installation
oauth2-proxy --version
```

### Docker
```bash
# Run with Docker
docker run -p 4180:4180 \
  -e OAUTH2_PROXY_CLIENT_ID=your-client-id \
  -e OAUTH2_PROXY_CLIENT_SECRET=your-client-secret \
  -e OAUTH2_PROXY_COOKIE_SECRET=$(python -c 'import os,base64; print(base64.b64encode(os.urandom(32)).decode())') \
  quay.io/oauth2-proxy/oauth2-proxy:v7.4.0 \
  --provider=github \
  --email-domain=* \
  --upstream=http://127.0.0.1:8080 \
  --http-address=0.0.0.0:4180
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oauth2-proxy
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: oauth2-proxy
  template:
    metadata:
      labels:
        app: oauth2-proxy
    spec:
      containers:
      - name: oauth2-proxy
        image: quay.io/oauth2-proxy/oauth2-proxy:v7.4.0
        args:
        - --provider=oidc
        - --provider-display-name="Corporate SSO"
        - --oidc-issuer-url=https://auth.company.com
        - --email-domain=*
        - --upstream=http://app-service:8080
        - --http-address=0.0.0.0:4180
        - --cookie-secure=true
        - --cookie-httponly=true
        - --cookie-samesite=lax
        - --pass-basic-auth=false
        - --pass-access-token=true
        - --pass-user-headers=true
        - --set-authorization-header=true
        - --skip-provider-button=true
        env:
        - name: OAUTH2_PROXY_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: oauth2-proxy-secret
              key: client-id
        - name: OAUTH2_PROXY_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: oauth2-proxy-secret
              key: client-secret
        - name: OAUTH2_PROXY_COOKIE_SECRET
          valueFrom:
            secretKeyRef:
              name: oauth2-proxy-secret
              key: cookie-secret
        ports:
        - containerPort: 4180
          name: http
        livenessProbe:
          httpGet:
            path: /ping
            port: 4180
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ping
            port: 4180
            scheme: HTTP
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            cpu: 10m
            memory: 32Mi
          limits:
            cpu: 100m
            memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: oauth2-proxy-service
  namespace: default
spec:
  selector:
    app: oauth2-proxy
  ports:
  - port: 4180
    targetPort: 4180
    name: http
  type: ClusterIP
---
apiVersion: v1
kind: Secret
metadata:
  name: oauth2-proxy-secret
  namespace: default
type: Opaque
data:
  client-id: <base64-encoded-client-id>
  client-secret: <base64-encoded-client-secret>
  cookie-secret: <base64-encoded-cookie-secret>
```

## Configuration

### Basic Configuration File
```yaml
# oauth2-proxy.cfg
http_address = "0.0.0.0:4180"
upstreams = [
    "http://127.0.0.1:8080/"
]

# Provider configuration
provider = "oidc"
provider_display_name = "Corporate SSO"
oidc_issuer_url = "https://auth.company.com"
client_id = "your-client-id"
client_secret = "your-client-secret"
redirect_url = "https://app.company.com/oauth2/callback"

# Cookie configuration
cookie_secret = "your-cookie-secret"
cookie_secure = true
cookie_httponly = true
cookie_samesite = "lax"
cookie_expire = "168h"  # 7 days
cookie_refresh = "1h"

# Email and authorization
email_domains = ["company.com"]
whitelist_domains = [".company.com"]

# Headers and authentication
pass_basic_auth = false
pass_access_token = true
pass_user_headers = true
set_authorization_header = true
set_xauthrequest = true

# Session storage
session_store_type = "redis"
redis_connection_url = "redis://localhost:6379"

# Logging
request_logging = true
auth_logging = true
standard_logging = true
standard_logging_format = "[{{.Timestamp}}] [{{.File}}] {{.Message}}"

# TLS
tls_cert_file = "/etc/ssl/certs/server.crt"
tls_key_file = "/etc/ssl/private/server.key"

# Skip authentication for specific paths
skip_auth_regex = [
    "^/health$",
    "^/metrics$",
    "^/static/.*"
]

# Custom pages
custom_templates_dir = "/etc/oauth2-proxy/templates"
```

### Provider-Specific Configurations

#### GitHub Provider
```yaml
provider = "github"
github_org = "your-organization"
github_team = "developers,admins"
client_id = "github-client-id"
client_secret = "github-client-secret"
scope = "user:email,read:org"
```

#### Google Provider
```yaml
provider = "google"
google_group = ["developers@company.com"]
google_admin_email = "admin@company.com"
google_service_account_json = "/etc/oauth2-proxy/service-account.json"
client_id = "google-client-id.apps.googleusercontent.com"
client_secret = "google-client-secret"
```

#### Azure Provider
```yaml
provider = "azure"
azure_tenant = "your-tenant-id"
oidc_issuer_url = "https://login.microsoftonline.com/your-tenant-id/v2.0"
client_id = "azure-client-id"
client_secret = "azure-client-secret"
scope = "openid profile email"
```

#### Keycloak Provider
```yaml
provider = "keycloak-oidc"
oidc_issuer_url = "https://keycloak.company.com/auth/realms/master"
client_id = "oauth2-proxy"
client_secret = "keycloak-client-secret"
scope = "openid profile email groups"
oidc_groups_claim = "groups"
oidc_email_claim = "email"
```

## Advanced Configuration

### Multiple Upstreams
```yaml
# oauth2-proxy.cfg
upstreams = [
    "http://app1.internal:8080/",
    "http://app2.internal:8081/",
    "file:///var/www/static#/static/"
]

# Route-specific configuration
upstream_timeout = "30s"
flush_interval = "1s"
pass_host_header = true
proxy_prefix = "/oauth2"
```

### Session Management
```yaml
# Redis session store
session_store_type = "redis"
redis_connection_url = "redis://redis.company.com:6379"
redis_password = "redis-password"
redis_use_sentinel = true
redis_sentinel_master_name = "mymaster"
redis_sentinel_connection_urls = [
    "redis://sentinel1.company.com:26379",
    "redis://sentinel2.company.com:26379",
    "redis://sentinel3.company.com:26379"
]

# Cookie store (default)
session_store_type = "cookie"
cookie_domains = [".company.com"]
cookie_path = "/"
cookie_expire = "24h"
cookie_refresh = "1h"
```

### JWT Verification
```yaml
# JWT token verification
jwt_key_file = "/etc/oauth2-proxy/jwt-key.pem"
jwt_key = "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
oidc_jwks_url = "https://auth.company.com/.well-known/jwks.json"
skip_jwt_bearer_tokens = false
extra_jwt_issuers = ["https://additional-issuer.com"]
```

### Headers and Claims
```yaml
# Custom headers
pass_authorization_header = true
pass_access_token = true
pass_user_headers = true
set_authorization_header = true
set_xauthrequest = true

# Custom header mappings
user_id_claim = "sub"
preferred_username_claim = "preferred_username"
oidc_email_claim = "email"
oidc_groups_claim = "groups"

# Inject custom headers
inject_request_headers = [
    "X-User: {{.User}}",
    "X-Email: {{.Email}}",
    "X-Groups: {{.Groups}}"
]

inject_response_headers = [
    "X-Auth-Request-User: {{.User}}",
    "X-Auth-Request-Email: {{.Email}}"
]
```

## Ingress Integration

### NGINX Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: oauth2-proxy-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/auth-url: "https://$host/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://$host/oauth2/start?rd=$escaped_request_uri"
    nginx.ingress.kubernetes.io/auth-response-headers: "x-auth-request-user,x-auth-request-email,x-auth-request-groups"
spec:
  tls:
  - hosts:
    - app.company.com
    secretName: app-tls
  rules:
  - host: app.company.com
    http:
      paths:
      - path: /oauth2
        pathType: Prefix
        backend:
          service:
            name: oauth2-proxy-service
            port:
              number: 4180
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 8080
```

### Traefik v2 Integration
```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: oauth2-proxy-auth
  namespace: default
spec:
  forwardAuth:
    address: http://oauth2-proxy-service:4180/oauth2/auth
    trustForwardHeader: true
    authResponseHeaders:
      - X-Auth-Request-User
      - X-Auth-Request-Email
      - X-Auth-Request-Groups
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.middlewares: default-oauth2-proxy-auth@kubernetescrd
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - app.company.com
    secretName: app-tls
  rules:
  - host: app.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 8080
```

### Istio Integration
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: oauth2-proxy-policy
  namespace: default
spec:
  selector:
    matchLabels:
      app: myapp
  rules:
  - to:
    - operation:
        paths: ["/oauth2/*"]
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/oauth2-proxy"]
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: oauth2-proxy-vs
  namespace: default
spec:
  hosts:
  - app.company.com
  gateways:
  - app-gateway
  http:
  - match:
    - uri:
        prefix: /oauth2/
    route:
    - destination:
        host: oauth2-proxy-service
        port:
          number: 4180
  - match:
    - uri:
        prefix: /
    headers:
      request:
        set:
          x-auth-request: "true"
    route:
    - destination:
        host: oauth2-proxy-service
        port:
          number: 4180
      headers:
        request:
          set:
            x-forwarded-host: app.company.com
```

## Application Integration

### Python Flask Integration
```python
from flask import Flask, request, jsonify, session
import requests
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key'

class OAuth2ProxyAuth:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        app.config.setdefault('OAUTH2_PROXY_HEADER_USER', 'X-Auth-Request-User')
        app.config.setdefault('OAUTH2_PROXY_HEADER_EMAIL', 'X-Auth-Request-Email')
        app.config.setdefault('OAUTH2_PROXY_HEADER_GROUPS', 'X-Auth-Request-Groups')
        app.config.setdefault('OAUTH2_PROXY_VERIFY_URL', 'http://oauth2-proxy:4180/oauth2/auth')
    
    def get_user_info(self):
        """Extract user information from OAuth2 Proxy headers"""
        user = request.headers.get(app.config['OAUTH2_PROXY_HEADER_USER'])
        email = request.headers.get(app.config['OAUTH2_PROXY_HEADER_EMAIL'])
        groups = request.headers.get(app.config['OAUTH2_PROXY_HEADER_GROUPS'], '').split(',')
        
        if not user:
            return None
            
        return {
            'user': user,
            'email': email,
            'groups': [g.strip() for g in groups if g.strip()]
        }
    
    def verify_auth(self):
        """Verify authentication with OAuth2 Proxy"""
        try:
            response = requests.get(
                app.config['OAUTH2_PROXY_VERIFY_URL'],
                headers={
                    'X-Forwarded-For': request.remote_addr,
                    'X-Forwarded-Proto': request.scheme,
                    'X-Forwarded-Host': request.host,
                    'Cookie': request.headers.get('Cookie', '')
                },
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

auth = OAuth2ProxyAuth(app)

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        user_info = auth.get_user_info()
        if not user_info:
            return jsonify({'error': 'Authentication required'}), 401
        
        request.user_info = user_info
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_group(required_groups):
    """Decorator to require specific group membership"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            user_info = auth.get_user_info()
            if not user_info:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_groups = user_info.get('groups', [])
            if not any(group in user_groups for group in required_groups):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            request.user_info = user_info
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

@app.route('/api/profile')
@require_auth
def get_profile():
    return jsonify(request.user_info)

@app.route('/api/admin')
@require_group(['admin', 'developers'])
def admin_endpoint():
    return jsonify({
        'message': 'Admin access granted',
        'user': request.user_info
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Node.js Express Integration
```javascript
const express = require('express');
const axios = require('axios');

const app = express();

class OAuth2ProxyMiddleware {
    constructor(options = {}) {
        this.options = {
            userHeader: options.userHeader || 'x-auth-request-user',
            emailHeader: options.emailHeader || 'x-auth-request-email',
            groupsHeader: options.groupsHeader || 'x-auth-request-groups',
            verifyUrl: options.verifyUrl || 'http://oauth2-proxy:4180/oauth2/auth',
            ...options
        };
    }

    getUserInfo(req) {
        const user = req.headers[this.options.userHeader];
        const email = req.headers[this.options.emailHeader];
        const groups = req.headers[this.options.groupsHeader];

        if (!user) {
            return null;
        }

        return {
            user,
            email,
            groups: groups ? groups.split(',').map(g => g.trim()) : []
        };
    }

    async verifyAuth(req) {
        try {
            const response = await axios.get(this.options.verifyUrl, {
                headers: {
                    'X-Forwarded-For': req.ip,
                    'X-Forwarded-Proto': req.protocol,
                    'X-Forwarded-Host': req.get('host'),
                    'Cookie': req.headers.cookie || ''
                },
                timeout: 5000
            });
            return response.status === 200;
        } catch (error) {
            console.error('Auth verification failed:', error.message);
            return false;
        }
    }

    requireAuth() {
        return (req, res, next) => {
            const userInfo = this.getUserInfo(req);
            if (!userInfo) {
                return res.status(401).json({ error: 'Authentication required' });
            }
            req.userInfo = userInfo;
            next();
        };
    }

    requireGroup(requiredGroups) {
        return (req, res, next) => {
            const userInfo = this.getUserInfo(req);
            if (!userInfo) {
                return res.status(401).json({ error: 'Authentication required' });
            }

            const userGroups = userInfo.groups || [];
            const hasAccess = requiredGroups.some(group => userGroups.includes(group));
            
            if (!hasAccess) {
                return res.status(403).json({ error: 'Insufficient permissions' });
            }

            req.userInfo = userInfo;
            next();
        };
    }
}

const auth = new OAuth2ProxyMiddleware();

app.use(express.json());

// Routes
app.get('/api/profile', auth.requireAuth(), (req, res) => {
    res.json(req.userInfo);
});

app.get('/api/admin', auth.requireGroup(['admin', 'developers']), (req, res) => {
    res.json({
        message: 'Admin access granted',
        user: req.userInfo
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

module.exports = app;
```

## Monitoring and Logging

### Prometheus Metrics
```yaml
# prometheus-config.yml
global:
  scrape_interval: 15s

scrape_configs:
- job_name: 'oauth2-proxy'
  static_configs:
  - targets: ['oauth2-proxy:4180']
  metrics_path: /oauth2/metrics
  scrape_interval: 30s
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "OAuth2 Proxy Dashboard",
    "panels": [
      {
        "title": "Authentication Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(oauth2_proxy_requests_total[5m])",
            "legendFormat": "{{method}} {{code}}"
          }
        ]
      },
      {
        "title": "Active Sessions",
        "type": "singlestat",
        "targets": [
          {
            "expr": "oauth2_proxy_sessions",
            "legendFormat": "Sessions"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(oauth2_proxy_requests_total{code!~\"2..\"}[5m])",
            "legendFormat": "Errors"
          }
        ]
      }
    ]
  }
}
```

### Structured Logging
```yaml
# oauth2-proxy configuration for structured logging
request_logging = true
request_logging_format = "{{.Client}} - {{.Username}} [{{.Timestamp}}] {{.Host}} {{.RequestMethod}} {{.Upstream}} {{.RequestURI}} {{.Protocol}} {{.UserAgent}} {{.StatusCode}} {{.ResponseSize}} {{.RequestDuration}}"

auth_logging = true
auth_logging_format = "{{.Client}} - {{.Username}} [{{.Timestamp}}] [{{.Status}}] {{.Message}}"

standard_logging = true
standard_logging_format = "[{{.Timestamp}}] [{{.File}}] {{.Message}}"
```

## High Availability Setup

### Redis Cluster for Sessions
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-cluster-config
data:
  redis.conf: |
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    appendonly yes
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
spec:
  serviceName: redis-cluster
  replicas: 6
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      containers:
      - name: redis
        image: redis:7.0-alpine
        ports:
        - containerPort: 6379
          name: client
        - containerPort: 16379
          name: gossip
        command: ["/bin/sh"]
        args:
        - -c
        - redis-server /etc/redis/redis.conf --protected-mode no
        volumeMounts:
        - name: conf
          mountPath: /etc/redis/
        - name: data
          mountPath: /data
      volumes:
      - name: conf
        configMap:
          name: redis-cluster-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 1Gi
```

### Load Balancer Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: oauth2-proxy-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: oauth2-proxy
  ports:
  - port: 443
    targetPort: 4180
    protocol: TCP
    name: https
  - port: 80
    targetPort: 4180
    protocol: TCP
    name: http
```

## Security Best Practices

### RBAC Configuration
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: oauth2-proxy
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: oauth2-proxy
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: oauth2-proxy
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: oauth2-proxy
subjects:
- kind: ServiceAccount
  name: oauth2-proxy
  namespace: default
```

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: oauth2-proxy-network-policy
spec:
  podSelector:
    matchLabels:
      app: oauth2-proxy
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 4180
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 6379
```

### Pod Security Policy
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: oauth2-proxy-psp
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
  runAsUser:
    rule: 'RunAsAny'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

## Troubleshooting

### Common Issues
```bash
# Check OAuth2 Proxy logs
kubectl logs -f deployment/oauth2-proxy

# Test authentication endpoint
curl -v https://app.company.com/oauth2/auth

# Verify provider configuration
curl https://auth.company.com/.well-known/openid_configuration

# Check Redis connectivity
kubectl exec -it oauth2-proxy-pod -- redis-cli -h redis-service ping

# Debug headers
curl -H "X-Auth-Request-User: testuser" \
     -H "X-Auth-Request-Email: test@company.com" \
     https://app.company.com/api/profile
```

### Health Checks
```bash
# OAuth2 Proxy health endpoint
curl https://app.company.com/oauth2/ping

# Verify upstream connectivity
curl -H "Authorization: Bearer $(cat token.txt)" \
     https://app.company.com/oauth2/userinfo
```

## Resources

- [OAuth2 Proxy Documentation](https://oauth2-proxy.github.io/oauth2-proxy/)
- [GitHub Repository](https://github.com/oauth2-proxy/oauth2-proxy)
- [Configuration Options](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview)
- [Provider Documentation](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/oauth_provider)
- [Kubernetes Examples](https://github.com/oauth2-proxy/manifests)
- [Helm Chart](https://github.com/oauth2-proxy/manifests/tree/main/helm/oauth2-proxy)
- [Security Best Practices](https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/tls)
- [Troubleshooting Guide](https://oauth2-proxy.github.io/oauth2-proxy/docs/troubleshooting)
- [Community Support](https://github.com/oauth2-proxy/oauth2-proxy/discussions)
- [OIDC Specification](https://openid.net/connect/)