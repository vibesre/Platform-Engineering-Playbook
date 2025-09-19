# Keycloak

## Overview

Keycloak is an open-source identity and access management solution that provides authentication, authorization, user management, and single sign-on (SSO) capabilities for modern applications and services.

## Key Features

- **Single Sign-On (SSO)**: Centralized authentication across multiple applications
- **Identity Federation**: Support for SAML, OpenID Connect, OAuth 2.0
- **User Management**: Complete user lifecycle management
- **Social Login**: Integration with Google, Facebook, GitHub, etc.
- **Multi-Factor Authentication**: TOTP, WebAuthn, SMS support

## Common Use Cases

### Basic Setup and Configuration
```bash
# Run Keycloak with Docker
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev

# Access admin console at http://localhost:8080/admin
```

### Realm and Client Configuration
```bash
# Create realm using Admin CLI
/opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin
/opt/keycloak/bin/kcadm.sh create realms -s realm=myrealm -s enabled=true

# Create client application
/opt/keycloak/bin/kcadm.sh create clients -r myrealm -s clientId=myapp -s enabled=true -s publicClient=false -s serviceAccountsEnabled=true
```

### Application Integration
```javascript
// Node.js with Keycloak adapter
const Keycloak = require('keycloak-connect');
const session = require('express-session');

const memoryStore = new session.MemoryStore();
const keycloak = new Keycloak({ store: memoryStore }, {
  realm: 'myrealm',
  'auth-server-url': 'http://localhost:8080/',
  'ssl-required': 'external',
  resource: 'myapp',
  credentials: {
    secret: 'your-client-secret'
  }
});

app.use(session({
  secret: 'session-secret',
  resave: false,
  saveUninitialized: true,
  store: memoryStore
}));

app.use(keycloak.middleware());

// Protected route
app.get('/protected', keycloak.protect(), (req, res) => {
  res.json({ message: 'Access granted', user: req.kauth.grant.access_token.content });
});
```

### User Management
```bash
# Create user
/opt/keycloak/bin/kcadm.sh create users -r myrealm -s username=john -s enabled=true -s firstName=John -s lastName=Doe -s email=john@example.com

# Set user password
/opt/keycloak/bin/kcadm.sh set-password -r myrealm --username john --new-password mypassword

# Assign roles
/opt/keycloak/bin/kcadm.sh add-roles -r myrealm --uusername john --rolename user
```

## Advanced Configuration

### LDAP Integration
```json
{
  "id": "ldap-provider",
  "name": "ldap",
  "providerId": "ldap",
  "providerType": "org.keycloak.storage.UserStorageProvider",
  "config": {
    "connectionUrl": ["ldap://ldap.example.com:389"],
    "usersDn": ["ou=users,dc=example,dc=com"],
    "bindDn": ["cn=admin,dc=example,dc=com"],
    "bindCredential": ["admin-password"],
    "usernameLDAPAttribute": ["uid"],
    "rdnLDAPAttribute": ["uid"]
  }
}
```

### Custom Authentication Flow
```json
{
  "alias": "custom-browser-flow",
  "description": "Custom browser authentication flow",
  "providerId": "basic-flow",
  "topLevel": true,
  "builtIn": false,
  "authenticationExecutions": [
    {
      "authenticator": "auth-cookie",
      "requirement": "ALTERNATIVE"
    },
    {
      "authenticator": "auth-username-password-form",
      "requirement": "REQUIRED"
    },
    {
      "authenticator": "auth-otp-form",
      "requirement": "CONDITIONAL"
    }
  ]
}
```

## Production Deployment

### Database Configuration
```bash
# PostgreSQL configuration
export KC_DB=postgres
export KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
export KC_DB_USERNAME=keycloak
export KC_DB_PASSWORD=password

# Start Keycloak
/opt/keycloak/bin/kc.sh start --hostname=keycloak.example.com
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak
spec:
  replicas: 2
  selector:
    matchLabels:
      app: keycloak
  template:
    metadata:
      labels:
        app: keycloak
    spec:
      containers:
      - name: keycloak
        image: quay.io/keycloak/keycloak:latest
        env:
        - name: KC_DB
          value: postgres
        - name: KC_DB_URL
          value: jdbc:postgresql://postgres:5432/keycloak
        - name: KC_HOSTNAME
          value: keycloak.example.com
        - name: KEYCLOAK_ADMIN
          value: admin
        - name: KEYCLOAK_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: keycloak-secret
              key: admin-password
        command: ["/opt/keycloak/bin/kc.sh", "start"]
        ports:
        - containerPort: 8080
```

## Monitoring and Maintenance

### Health Checks
```bash
# Health check endpoint
curl http://keycloak.example.com:8080/health

# Metrics endpoint
curl http://keycloak.example.com:8080/metrics

# Admin REST API health
curl -X GET http://keycloak.example.com:8080/admin/realms/master
```

### Backup and Recovery
```bash
# Export realm configuration
/opt/keycloak/bin/kc.sh export --realm myrealm --file myrealm-backup.json

# Import realm configuration
/opt/keycloak/bin/kc.sh import --file myrealm-backup.json

# Database backup (PostgreSQL)
pg_dump keycloak > keycloak-backup.sql
```

## Security Best Practices

- Enable HTTPS/TLS for all communications
- Use strong admin passwords and rotate regularly
- Configure proper CORS settings for web applications
- Implement rate limiting and brute force protection
- Regular security updates and patch management
- Audit logs monitoring and alerting
- Proper realm isolation for multi-tenant environments

## Great Resources

- [Keycloak Documentation](https://www.keycloak.org/documentation) - Official comprehensive documentation
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/) - Complete REST API reference
- [Keycloak Adapters](https://www.keycloak.org/docs/latest/securing_apps/) - Client adapters for various platforms
- [Keycloak Helm Chart](https://github.com/codecentric/helm-charts/tree/master/charts/keycloak) - Kubernetes deployment
- [Keycloak Extensions](https://github.com/keycloak/keycloak-extensions-for-fapi) - Community extensions and customizations
- [awesome-keycloak](https://github.com/thomasdarimont/awesome-keycloak) - Curated list of Keycloak resources
- [Keycloak Quickstarts](https://github.com/keycloak/keycloak-quickstarts) - Example applications and integrations