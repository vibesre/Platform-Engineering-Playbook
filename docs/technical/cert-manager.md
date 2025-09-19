# cert-manager

## Overview

cert-manager is a Kubernetes-native certificate management controller that automates the provisioning and management of TLS certificates. It integrates with various certificate authorities and provides a declarative approach to certificate lifecycle management.

## Key Features

- **Automated Certificate Provisioning**: Automatic certificate issuance and renewal
- **Multiple CA Support**: Let's Encrypt, HashiCorp Vault, Venafi, self-signed
- **Kubernetes Native**: Custom resources and controllers for certificate management
- **Webhook Integration**: Automatic certificate injection into workloads
- **DNS Challenge Support**: ACME DNS-01 challenges for wildcard certificates

## Common Use Cases

### Installation
```bash
# Install cert-manager using Helm
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set installCRDs=true

# Verify installation
kubectl get pods --namespace cert-manager
```

### Let's Encrypt ClusterIssuer
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
    - http01:
        ingress:
          class: nginx
```

### Certificate Resource
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
  namespace: default
spec:
  secretName: myapp-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - myapp.example.com
  - api.myapp.example.com
```

### Ingress with Automatic Certificates
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## Advanced Configuration

### DNS Challenge for Wildcard Certificates
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-dns
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-dns
    solvers:
    - dns01:
        cloudflare:
          email: admin@example.com
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token
      selector:
        dnsNames:
        - "*.example.com"
        - "example.com"
```

### Vault Integration
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-issuer
spec:
  vault:
    server: https://vault.example.com:8200
    path: pki/sign/example-dot-com
    auth:
      kubernetes:
        role: cert-manager
        mountPath: /v1/auth/kubernetes
        secretRef:
          name: cert-manager-vault-token
          key: token
```

### Self-Signed Certificates for Development
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-selfsigned-ca
spec:
  isCA: true
  commonName: my-selfsigned-ca
  secretName: root-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
    group: cert-manager.io
```

## Monitoring and Troubleshooting

### Check Certificate Status
```bash
# List certificates
kubectl get certificates -A

# Describe certificate
kubectl describe certificate myapp-tls

# Check certificate events
kubectl get events --field-selector involvedObject.name=myapp-tls

# View certificate details
kubectl get secret myapp-tls-secret -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

### Debug Certificate Requests
```bash
# List certificate requests
kubectl get certificaterequests

# Describe failed request
kubectl describe certificaterequest myapp-tls-xxx

# Check orders (ACME)
kubectl get orders
kubectl describe order myapp-tls-xxx

# Check challenges
kubectl get challenges
kubectl describe challenge myapp-tls-xxx
```

### Logs and Debugging
```bash
# cert-manager controller logs
kubectl logs -n cert-manager deployment/cert-manager

# cert-manager webhook logs
kubectl logs -n cert-manager deployment/cert-manager-webhook

# cert-manager cainjector logs
kubectl logs -n cert-manager deployment/cert-manager-cainjector

# Enable debug logging
kubectl patch deployment cert-manager -n cert-manager --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--v=2"}]'
```

## Best Practices

- Use staging issuers for testing to avoid rate limits
- Implement monitoring and alerting for certificate expiration
- Use DNS challenges for wildcard certificates
- Backup certificate secrets and issuer credentials
- Regular updates of cert-manager for security and features
- Use appropriate certificate duration and renewal policies
- Implement proper RBAC for cert-manager resources

## Production Considerations

### High Availability Setup
```yaml
# values.yaml for Helm chart
replicaCount: 2

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

nodeSelector:
  kubernetes.io/os: linux

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values:
            - cert-manager
        topologyKey: kubernetes.io/hostname
```

## Great Resources

- [cert-manager Documentation](https://cert-manager.io/docs/) - Official comprehensive documentation
- [cert-manager Helm Chart](https://github.com/jetstack/cert-manager) - Official Helm chart repository
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/) - ACME protocol and Let's Encrypt specifics
- [cert-manager Community](https://cert-manager.io/docs/contributing/) - Community support and contributions
- [Kubernetes TLS Best Practices](https://kubernetes.io/docs/concepts/configuration/tls/) - Official Kubernetes TLS guidance
- [ACME Client Implementations](https://letsencrypt.org/docs/client-options/) - Alternative ACME clients
- [cert-manager Tutorials](https://cert-manager.io/docs/tutorials/) - Step-by-step implementation guides