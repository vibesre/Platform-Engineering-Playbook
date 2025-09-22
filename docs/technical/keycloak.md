# Keycloak

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Keycloak Tutorial - Complete Identity Management Course**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=duawSV69LDI)
- **Why it's great**: Comprehensive introduction to Keycloak with practical setup and configuration

#### **Spring Boot Security with Keycloak**
- **Channel**: Java Brains
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=haHFoeWUz0k)
- **Why it's great**: Hands-on integration of Keycloak with Spring Boot applications

#### **Keycloak Identity and Access Management**
- **Channel**: Red Hat Developer
- **Link**: [YouTube - 45 minutes](https://www.youtube.com/watch?v=mdZauKsMDiI)
- **Why it's great**: Official overview of Keycloak features and enterprise use cases

### 📖 Essential Documentation

#### **Keycloak Official Documentation**
- **Link**: [keycloak.org/documentation](https://www.keycloak.org/documentation)
- **Why it's great**: Comprehensive official documentation with setup guides and configuration examples

#### **Keycloak Admin REST API Reference**
- **Link**: [keycloak.org/docs-api/latest/rest-api](https://www.keycloak.org/docs-api/latest/rest-api/)
- **Why it's great**: Complete REST API documentation for automated Keycloak management

#### **Keycloak Client Adapters Guide**
- **Link**: [keycloak.org/docs/latest/securing_apps](https://www.keycloak.org/docs/latest/securing_apps/)
- **Why it's great**: Integration guides for various programming languages and frameworks

### 📝 Must-Read Blogs & Articles

#### **Red Hat Developer Blog - Keycloak**
- **Source**: Red Hat
- **Link**: [developers.redhat.com/topics/keycloak](https://developers.redhat.com/topics/keycloak)
- **Why it's great**: Official updates, best practices, and advanced configuration patterns

#### **Keycloak Identity Management Guide**
- **Source**: Baeldung
- **Link**: [baeldung.com/spring-boot-keycloak](https://www.baeldung.com/spring-boot-keycloak)
- **Why it's great**: Practical tutorials for integrating Keycloak with modern applications

#### **OAuth 2.0 and OpenID Connect with Keycloak**
- **Source**: Auth0 Blog
- **Link**: [auth0.com/blog/keycloak-identity-management](https://auth0.com/blog/keycloak-identity-management/)
- **Why it's great**: Deep dive into modern authentication protocols with Keycloak

### 🎓 Structured Courses

#### **Complete Keycloak Identity Management Course**
- **Platform**: Udemy
- **Link**: [udemy.com/course/keycloak-identity-management](https://www.udemy.com/course/keycloak-identity-management/)
- **Cost**: Paid
- **Why it's great**: Comprehensive course covering Keycloak from basics to advanced features

#### **Red Hat Single Sign-On (Keycloak) Training**
- **Platform**: Red Hat Training
- **Link**: [redhat.com/en/services/training](https://www.redhat.com/en/services/training/)
- **Cost**: Paid
- **Why it's great**: Official enterprise-grade training with certification

### 🛠️ Tools & Platforms

#### **Keycloak Helm Chart**
- **Link**: [github.com/codecentric/helm-charts/tree/master/charts/keycloak](https://github.com/codecentric/helm-charts/tree/master/charts/keycloak)
- **Why it's great**: Production-ready Kubernetes deployment for Keycloak

#### **Awesome Keycloak**
- **Link**: [github.com/thomasdarimont/awesome-keycloak](https://github.com/thomasdarimont/awesome-keycloak)
- **Why it's great**: Curated list of Keycloak resources, extensions, and integrations

#### **Keycloak Quickstarts**
- **Link**: [github.com/keycloak/keycloak-quickstarts](https://github.com/keycloak/keycloak-quickstarts)
- **Why it's great**: Ready-to-use example applications and integration patterns

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