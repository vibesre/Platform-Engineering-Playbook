# Okta

Okta is a cloud-based identity and access management platform that provides secure authentication, authorization, and user management for applications and services.

## Core Concepts

### Key Features
- **Single Sign-On (SSO)**: Centralized authentication across applications
- **Multi-Factor Authentication (MFA)**: Enhanced security with multiple authentication factors
- **Universal Directory**: Centralized user management and provisioning
- **API Access Management**: OAuth 2.0 and OpenID Connect for API security
- **Lifecycle Management**: Automated user provisioning and deprovisioning
- **Adaptive Authentication**: Risk-based authentication policies

### Architecture Components
- **Okta Org**: Your Okta tenant/organization
- **Applications**: Configured apps for SSO integration
- **Users and Groups**: Identity management entities
- **Authorization Servers**: OAuth 2.0/OIDC endpoints
- **Policies**: Authentication and authorization rules

## Setup and Configuration

### Initial Okta Org Setup
```bash
# Access your Okta admin console
# https://your-org.okta.com/admin

# Basic org configuration
1. Configure company profile
2. Set up domains and certificates
3. Configure authentication policies
4. Set up user directories
5. Configure network zones
```

### API Access Setup
```bash
# Create API token
1. Go to Security > API > Tokens
2. Create Token
3. Name: "Platform Integration"
4. Copy and securely store the token

# Create OAuth app for server-to-server
1. Go to Applications > Applications
2. Create App Integration
3. Choose "API Services" (OAuth 2.0)
4. Configure client credentials
```

### Domain and Certificate Configuration
```bash
# Custom domain setup
1. Go to Customization > Domain Name
2. Add custom domain: auth.company.com
3. Add DNS CNAME record
4. Upload SSL certificate
5. Verify domain ownership
```

## Application Integration

### OIDC Web Application
```yaml
# Okta OIDC Application Configuration
Application Type: Web Application
Grant Types:
  - Authorization Code
  - Refresh Token
Redirect URIs:
  - https://app.company.com/authorization-code/callback
  - https://app.company.com/oauth2/callback
Sign-out Redirect URIs:
  - https://app.company.com/logout
Trusted Origins:
  - https://app.company.com
  - https://api.company.com
```

### SAML Application
```xml
<!-- SAML Configuration -->
<saml2:Assertion>
  <saml2:Issuer>http://www.okta.com/${org.externalKey}</saml2:Issuer>
  <saml2:Subject>
    <saml2:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
      ${user.email}
    </saml2:NameID>
  </saml2:Subject>
  <saml2:AttributeStatement>
    <saml2:Attribute Name="email">
      <saml2:AttributeValue>${user.email}</saml2:AttributeValue>
    </saml2:Attribute>
    <saml2:Attribute Name="firstName">
      <saml2:AttributeValue>${user.firstName}</saml2:AttributeValue>
    </saml2:Attribute>
    <saml2:Attribute Name="lastName">
      <saml2:AttributeValue>${user.lastName}</saml2:AttributeValue>
    </saml2:Attribute>
    <saml2:Attribute Name="groups">
      <saml2:AttributeValue>${user.groups}</saml2:AttributeValue>
    </saml2:Attribute>
  </saml2:AttributeStatement>
</saml2:Assertion>
```

### SPA Application
```javascript
// Okta configuration for Single Page Application
const oktaConfig = {
  baseUrl: 'https://your-org.okta.com',
  clientId: 'your-spa-client-id',
  redirectUri: window.location.origin + '/authorization-code/callback',
  scope: ['openid', 'profile', 'email', 'groups'],
  responseType: ['code'],
  responseMode: 'query',
  state: true,
  pkce: true,
  disableHttpsCheck: false
};

// Initialize Okta Auth SDK
import { OktaAuth } from '@okta/okta-auth-js';
const oktaAuth = new OktaAuth(oktaConfig);

// Login function
async function login() {
  try {
    await oktaAuth.signInWithRedirect();
  } catch (error) {
    console.error('Login failed:', error);
  }
}

// Handle callback
async function handleCallback() {
  try {
    await oktaAuth.handleLoginRedirect();
    const user = await oktaAuth.getUser();
    console.log('User:', user);
  } catch (error) {
    console.error('Callback handling failed:', error);
  }
}

// Check authentication status
async function checkAuth() {
  try {
    const isAuthenticated = await oktaAuth.isAuthenticated();
    if (isAuthenticated) {
      const user = await oktaAuth.getUser();
      const accessToken = await oktaAuth.getAccessToken();
      return { user, accessToken };
    }
    return null;
  } catch (error) {
    console.error('Auth check failed:', error);
    return null;
  }
}

// Logout
async function logout() {
  try {
    await oktaAuth.signOut();
  } catch (error) {
    console.error('Logout failed:', error);
  }
}
```

## API Integration

### Node.js SDK
```javascript
const okta = require('@okta/okta-sdk-nodejs');

class OktaClient {
  constructor() {
    this.client = new okta.Client({
      orgUrl: process.env.OKTA_ORG_URL,
      token: process.env.OKTA_API_TOKEN,
      requestExecutor: new okta.DefaultRequestExecutor({
        maxRetries: 3,
        requestTimeout: 0
      })
    });
  }

  // User management
  async createUser(userProfile) {
    try {
      const user = await this.client.createUser({
        profile: {
          firstName: userProfile.firstName,
          lastName: userProfile.lastName,
          email: userProfile.email,
          login: userProfile.email,
          department: userProfile.department,
          organization: userProfile.organization
        },
        credentials: {
          password: {
            value: userProfile.tempPassword
          }
        },
        groupIds: userProfile.groupIds || []
      });
      
      console.log(`User created: ${user.id}`);
      return user;
    } catch (error) {
      console.error('Failed to create user:', error);
      throw error;
    }
  }

  async getUser(userId) {
    try {
      const user = await this.client.getUser(userId);
      return user;
    } catch (error) {
      console.error('Failed to get user:', error);
      throw error;
    }
  }

  async updateUser(userId, updates) {
    try {
      const user = await this.client.getUser(userId);
      Object.assign(user.profile, updates);
      const updatedUser = await user.update();
      return updatedUser;
    } catch (error) {
      console.error('Failed to update user:', error);
      throw error;
    }
  }

  async deactivateUser(userId) {
    try {
      const user = await this.client.getUser(userId);
      await user.deactivate();
      console.log(`User deactivated: ${userId}`);
    } catch (error) {
      console.error('Failed to deactivate user:', error);
      throw error;
    }
  }

  // Group management
  async createGroup(groupProfile) {
    try {
      const group = await this.client.createGroup({
        profile: {
          name: groupProfile.name,
          description: groupProfile.description
        }
      });
      return group;
    } catch (error) {
      console.error('Failed to create group:', error);
      throw error;
    }
  }

  async addUserToGroup(userId, groupId) {
    try {
      await this.client.addUserToGroup(groupId, userId);
      console.log(`User ${userId} added to group ${groupId}`);
    } catch (error) {
      console.error('Failed to add user to group:', error);
      throw error;
    }
  }

  async removeUserFromGroup(userId, groupId) {
    try {
      await this.client.removeUserFromGroup(groupId, userId);
      console.log(`User ${userId} removed from group ${groupId}`);
    } catch (error) {
      console.error('Failed to remove user from group:', error);
      throw error;
    }
  }

  // Application management
  async getApplications() {
    try {
      const applications = [];
      await this.client.listApplications().each(app => {
        applications.push(app);
      });
      return applications;
    } catch (error) {
      console.error('Failed to get applications:', error);
      throw error;
    }
  }

  async assignUserToApp(userId, appId) {
    try {
      const appUser = await this.client.assignUserToApplication(appId, {
        id: userId,
        scope: 'USER'
      });
      return appUser;
    } catch (error) {
      console.error('Failed to assign user to app:', error);
      throw error;
    }
  }

  // Event monitoring
  async getSystemLogs(options = {}) {
    try {
      const logs = [];
      const queryOptions = {
        since: options.since || new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24 hours
        until: options.until || new Date(),
        filter: options.filter || 'eventType eq "user.session.start"',
        limit: options.limit || 100
      };

      await this.client.getLogs(queryOptions).each(log => {
        logs.push(log);
      });
      return logs;
    } catch (error) {
      console.error('Failed to get system logs:', error);
      throw error;
    }
  }
}

// Usage
const oktaClient = new OktaClient();

// Create and manage users
async function provisionUser(userData) {
  try {
    const user = await oktaClient.createUser({
      firstName: userData.firstName,
      lastName: userData.lastName,
      email: userData.email,
      department: userData.department,
      tempPassword: 'TempPassword123!',
      groupIds: ['developers-group-id']
    });

    // Assign to applications
    await oktaClient.assignUserToApp(user.id, 'app-id-1');
    await oktaClient.assignUserToApp(user.id, 'app-id-2');

    return user;
  } catch (error) {
    console.error('User provisioning failed:', error);
    throw error;
  }
}

module.exports = OktaClient;
```

### Python SDK
```python
import asyncio
from okta.client import Client as OktaClient
from okta.models import User, Group, CreateUserRequest, UserProfile
from okta.config.config_validator import ConfigValidator
from okta import helpers
import os
from datetime import datetime, timedelta

class OktaManager:
    def __init__(self):
        config = {
            'orgUrl': os.getenv('OKTA_ORG_URL'),
            'token': os.getenv('OKTA_API_TOKEN'),
            'requestTimeout': 30,
            'maxRetries': 3
        }
        self.client = OktaClient(config)
    
    async def create_user(self, user_data):
        """Create a new user in Okta"""
        try:
            user_profile = UserProfile({
                'firstName': user_data['first_name'],
                'lastName': user_data['last_name'],
                'email': user_data['email'],
                'login': user_data['email'],
                'department': user_data.get('department'),
                'organization': user_data.get('organization')
            })
            
            password = {'value': user_data.get('temp_password', 'TempPassword123!')}
            
            create_user_req = CreateUserRequest({
                'profile': user_profile,
                'credentials': {'password': password},
                'groupIds': user_data.get('group_ids', [])
            })
            
            user, resp, err = await self.client.create_user(create_user_req)
            if err:
                raise Exception(f"Failed to create user: {err}")
            
            print(f"User created: {user.id}")
            return user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    async def get_user(self, user_id):
        """Get user by ID"""
        try:
            user, resp, err = await self.client.get_user(user_id)
            if err:
                raise Exception(f"Failed to get user: {err}")
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            raise
    
    async def update_user(self, user_id, updates):
        """Update user profile"""
        try:
            user, resp, err = await self.client.get_user(user_id)
            if err:
                raise Exception(f"Failed to get user: {err}")
            
            # Update profile fields
            for key, value in updates.items():
                setattr(user.profile, key, value)
            
            updated_user, resp, err = await self.client.update_user(user_id, user)
            if err:
                raise Exception(f"Failed to update user: {err}")
            
            return updated_user
        except Exception as e:
            print(f"Error updating user: {e}")
            raise
    
    async def deactivate_user(self, user_id):
        """Deactivate user"""
        try:
            resp, err = await self.client.deactivate_user(user_id)
            if err:
                raise Exception(f"Failed to deactivate user: {err}")
            print(f"User deactivated: {user_id}")
        except Exception as e:
            print(f"Error deactivating user: {e}")
            raise
    
    async def create_group(self, group_data):
        """Create a new group"""
        try:
            group_profile = {
                'name': group_data['name'],
                'description': group_data.get('description', '')
            }
            
            group = Group({'profile': group_profile})
            created_group, resp, err = await self.client.create_group(group)
            if err:
                raise Exception(f"Failed to create group: {err}")
            
            return created_group
        except Exception as e:
            print(f"Error creating group: {e}")
            raise
    
    async def add_user_to_group(self, user_id, group_id):
        """Add user to group"""
        try:
            resp, err = await self.client.add_user_to_group(group_id, user_id)
            if err:
                raise Exception(f"Failed to add user to group: {err}")
            print(f"User {user_id} added to group {group_id}")
        except Exception as e:
            print(f"Error adding user to group: {e}")
            raise
    
    async def get_user_groups(self, user_id):
        """Get groups for a user"""
        try:
            groups = []
            resp, err = await self.client.list_user_groups(user_id)
            if err:
                raise Exception(f"Failed to get user groups: {err}")
            
            async for group in resp:
                groups.append(group)
            
            return groups
        except Exception as e:
            print(f"Error getting user groups: {e}")
            raise
    
    async def assign_app_to_user(self, app_id, user_id):
        """Assign application to user"""
        try:
            app_user = {
                'id': user_id,
                'scope': 'USER'
            }
            
            assigned_user, resp, err = await self.client.assign_user_to_application(app_id, app_user)
            if err:
                raise Exception(f"Failed to assign app to user: {err}")
            
            return assigned_user
        except Exception as e:
            print(f"Error assigning app to user: {e}")
            raise
    
    async def get_system_logs(self, filter_expr=None, since=None, limit=100):
        """Get system logs"""
        try:
            if since is None:
                since = datetime.now() - timedelta(hours=24)
            
            query_params = {
                'since': since.isoformat(),
                'limit': limit
            }
            
            if filter_expr:
                query_params['filter'] = filter_expr
            
            logs = []
            log_events, resp, err = await self.client.get_logs(query_params)
            if err:
                raise Exception(f"Failed to get logs: {err}")
            
            async for log in log_events:
                logs.append(log)
            
            return logs
        except Exception as e:
            print(f"Error getting system logs: {e}")
            raise
    
    async def bulk_user_operation(self, users_data, operation='create'):
        """Perform bulk operations on users"""
        results = []
        
        for user_data in users_data:
            try:
                if operation == 'create':
                    result = await self.create_user(user_data)
                elif operation == 'update':
                    result = await self.update_user(user_data['id'], user_data['updates'])
                elif operation == 'deactivate':
                    result = await self.deactivate_user(user_data['id'])
                
                results.append({'success': True, 'data': result})
                
            except Exception as e:
                results.append({'success': False, 'error': str(e), 'data': user_data})
        
        return results

# Usage example
async def main():
    okta = OktaManager()
    
    # Create user
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@company.com',
        'department': 'Engineering',
        'group_ids': ['developers-group-id']
    }
    
    user = await okta.create_user(user_data)
    
    # Assign applications
    await okta.assign_app_to_user('app-id-1', user.id)
    
    # Get user groups
    groups = await okta.get_user_groups(user.id)
    print(f"User groups: {[group.profile.name for group in groups]}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Authentication Flows

### Authorization Code Flow
```javascript
// Frontend implementation
class OktaAuthHandler {
  constructor(config) {
    this.oktaAuth = new OktaAuth({
      issuer: `${config.orgUrl}/oauth2/default`,
      clientId: config.clientId,
      redirectUri: `${window.location.origin}/callback`,
      scopes: ['openid', 'profile', 'email', 'groups'],
      pkce: true,
      responseType: 'code'
    });
  }

  async login() {
    try {
      // Redirect to Okta for authentication
      await this.oktaAuth.signInWithRedirect({
        originalUri: window.location.href
      });
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  }

  async handleCallback() {
    try {
      // Handle the callback and exchange code for tokens
      await this.oktaAuth.handleLoginRedirect();
      
      // Get user information
      const user = await this.oktaAuth.getUser();
      const accessToken = await this.oktaAuth.getAccessToken();
      
      return { user, accessToken };
    } catch (error) {
      console.error('Callback handling failed:', error);
      throw error;
    }
  }

  async makeAuthenticatedRequest(url, options = {}) {
    try {
      const accessToken = await this.oktaAuth.getAccessToken();
      
      const headers = {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        ...options.headers
      };

      const response = await fetch(url, {
        ...options,
        headers
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token might be expired, try to renew
          await this.oktaAuth.renewTokens();
          return this.makeAuthenticatedRequest(url, options);
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Authenticated request failed:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await this.oktaAuth.signOut({
        postLogoutRedirectUri: window.location.origin
      });
    } catch (error) {
      console.error('Logout failed:', error);
      throw error;
    }
  }

  async isAuthenticated() {
    try {
      return await this.oktaAuth.isAuthenticated();
    } catch (error) {
      console.error('Auth check failed:', error);
      return false;
    }
  }
}

// Usage
const authHandler = new OktaAuthHandler({
  orgUrl: 'https://your-org.okta.com',
  clientId: 'your-client-id'
});

// Login button click
document.getElementById('login').addEventListener('click', () => {
  authHandler.login();
});

// Handle callback on page load
if (window.location.pathname === '/callback') {
  authHandler.handleCallback().then(({ user }) => {
    console.log('User logged in:', user);
    window.location.href = '/dashboard';
  });
}
```

### Client Credentials Flow
```python
import requests
import json
from datetime import datetime, timedelta
import base64

class OktaClientCredentials:
    def __init__(self, org_url, client_id, client_secret):
        self.org_url = org_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self):
        """Get access token using client credentials flow"""
        if self.access_token and self.token_expires_at > datetime.now():
            return self.access_token
        
        token_url = f"{self.org_url}/oauth2/default/v1/token"
        
        # Prepare credentials
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'okta.users.read okta.groups.read okta.apps.read'
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return self.access_token
            
        except requests.RequestException as e:
            print(f"Failed to get access token: {e}")
            raise
    
    def make_api_request(self, endpoint, method='GET', data=None):
        """Make authenticated API request"""
        access_token = self.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.org_url}/api/v1{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return None
            
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            raise

# Usage
client = OktaClientCredentials(
    org_url='https://your-org.okta.com',
    client_id='your-client-id',
    client_secret='your-client-secret'
)

# Get users
users = client.make_api_request('/users?limit=10')
print(f"Found {len(users)} users")

# Get groups
groups = client.make_api_request('/groups')
print(f"Found {len(groups)} groups")
```

## Webhooks and Events

### Webhook Configuration
```json
{
  "name": "User Lifecycle Webhook",
  "url": "https://api.company.com/webhooks/okta",
  "events": {
    "type": "EVENT_TYPE",
    "items": [
      "user.lifecycle.activate",
      "user.lifecycle.deactivate",
      "user.lifecycle.create",
      "user.account.update_profile",
      "group.user_membership.add",
      "group.user_membership.remove",
      "application.user_membership.add",
      "application.user_membership.remove"
    ]
  },
  "channel": {
    "type": "HTTP",
    "version": "1.0.0"
  },
  "delivery": {
    "authorization": {
      "type": "HEADER",
      "key": "Authorization",
      "value": "Bearer your-webhook-secret"
    }
  }
}
```

### Webhook Handler
```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

class OktaWebhookHandler {
  constructor(secret) {
    this.secret = secret;
  }

  verifySignature(payload, signature) {
    const expectedSignature = crypto
      .createHmac('sha256', this.secret)
      .update(payload)
      .digest('hex');
    
    return crypto.timingSafeEqual(
      Buffer.from(`sha256=${expectedSignature}`),
      Buffer.from(signature)
    );
  }

  async handleUserLifecycle(event) {
    const { eventType, target, actor } = event.data;
    
    switch (eventType) {
      case 'user.lifecycle.activate':
        await this.onUserActivated(target[0]);
        break;
      case 'user.lifecycle.deactivate':
        await this.onUserDeactivated(target[0]);
        break;
      case 'user.lifecycle.create':
        await this.onUserCreated(target[0]);
        break;
      case 'user.account.update_profile':
        await this.onUserUpdated(target[0]);
        break;
      default:
        console.log(`Unhandled event type: ${eventType}`);
    }
  }

  async handleGroupMembership(event) {
    const { eventType, target } = event.data;
    const user = target.find(t => t.type === 'User');
    const group = target.find(t => t.type === 'UserGroup');

    switch (eventType) {
      case 'group.user_membership.add':
        await this.onUserAddedToGroup(user, group);
        break;
      case 'group.user_membership.remove':
        await this.onUserRemovedFromGroup(user, group);
        break;
      default:
        console.log(`Unhandled group event: ${eventType}`);
    }
  }

  async onUserActivated(user) {
    console.log(`User activated: ${user.login}`);
    // Send welcome email, provision resources, etc.
    await this.provisionUserResources(user);
  }

  async onUserDeactivated(user) {
    console.log(`User deactivated: ${user.login}`);
    // Revoke access, backup data, etc.
    await this.deprovisionUserResources(user);
  }

  async onUserCreated(user) {
    console.log(`User created: ${user.login}`);
    // Setup user profile, send onboarding materials
    await this.setupUserProfile(user);
  }

  async onUserUpdated(user) {
    console.log(`User updated: ${user.login}`);
    // Sync profile changes to other systems
    await this.syncUserProfile(user);
  }

  async onUserAddedToGroup(user, group) {
    console.log(`User ${user.login} added to group ${group.name}`);
    // Grant group-specific permissions
    await this.grantGroupPermissions(user, group);
  }

  async onUserRemovedFromGroup(user, group) {
    console.log(`User ${user.login} removed from group ${group.name}`);
    // Revoke group-specific permissions
    await this.revokeGroupPermissions(user, group);
  }

  async provisionUserResources(user) {
    // Implementation for resource provisioning
    console.log(`Provisioning resources for ${user.login}`);
  }

  async deprovisionUserResources(user) {
    // Implementation for resource deprovisioning
    console.log(`Deprovisioning resources for ${user.login}`);
  }

  async setupUserProfile(user) {
    // Implementation for user profile setup
    console.log(`Setting up profile for ${user.login}`);
  }

  async syncUserProfile(user) {
    // Implementation for profile synchronization
    console.log(`Syncing profile for ${user.login}`);
  }

  async grantGroupPermissions(user, group) {
    // Implementation for granting permissions
    console.log(`Granting ${group.name} permissions to ${user.login}`);
  }

  async revokeGroupPermissions(user, group) {
    // Implementation for revoking permissions
    console.log(`Revoking ${group.name} permissions from ${user.login}`);
  }
}

const webhookHandler = new OktaWebhookHandler(process.env.OKTA_WEBHOOK_SECRET);

app.post('/webhooks/okta', async (req, res) => {
  try {
    const signature = req.headers['x-okta-verification-challenge'];
    
    // Verify webhook signature
    if (!webhookHandler.verifySignature(JSON.stringify(req.body), signature)) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const events = req.body.data?.events || [req.body];

    for (const event of events) {
      const eventType = event.data?.eventType;

      if (eventType?.startsWith('user.lifecycle') || eventType?.startsWith('user.account')) {
        await webhookHandler.handleUserLifecycle(event);
      } else if (eventType?.startsWith('group.user_membership')) {
        await webhookHandler.handleGroupMembership(event);
      }
    }

    res.status(200).json({ status: 'processed' });
  } catch (error) {
    console.error('Webhook processing failed:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

## Advanced Features

### Inline Hooks
```javascript
// Registration inline hook
app.post('/hooks/registration', (req, res) => {
  const { data } = req.body;
  const user = data.userProfile;

  // Custom validation logic
  const errors = [];
  
  if (!user.email.endsWith('@company.com')) {
    errors.push({
      errorSummary: 'Only company email addresses are allowed',
      errorCauses: [{
        errorSummary: 'Invalid email domain',
        reason: 'INVALID_EMAIL_DOMAIN',
        locationType: 'body',
        location: 'data.userProfile.email'
      }]
    });
  }

  if (errors.length > 0) {
    return res.json({
      error: {
        errorSummary: 'Registration validation failed',
        errorCauses: errors
      }
    });
  }

  // Enrich user profile
  const commands = [{
    type: 'com.okta.user.profile.update',
    value: {
      department: deriveDepartmentFromEmail(user.email),
      customAttribute: 'custom-value'
    }
  }];

  res.json({ commands });
});

function deriveDepartmentFromEmail(email) {
  if (email.includes('eng') || email.includes('dev')) return 'Engineering';
  if (email.includes('sales')) return 'Sales';
  if (email.includes('hr')) return 'Human Resources';
  return 'General';
}
```

### Token Inline Hook
```javascript
// Token inline hook for custom claims
app.post('/hooks/token', (req, res) => {
  const { data } = req.body;
  const user = data.identity;
  const tokenType = data.tokenType;

  if (tokenType === 'ACCESS_TOKEN') {
    const commands = [{
      type: 'com.okta.access.patch',
      value: [{
        op: 'add',
        path: '/claims/custom_permissions',
        value: getUserPermissions(user.claims.sub)
      }, {
        op: 'add',
        path: '/claims/department',
        value: user.claims.department
      }, {
        op: 'add',
        path: '/claims/employee_id',
        value: user.claims.employeeNumber
      }]
    }];

    res.json({ commands });
  } else {
    res.json({});
  }
});

function getUserPermissions(userId) {
  // Fetch user permissions from database or external system
  return ['read:profile', 'write:documents', 'admin:users'];
}
```

### Password Import Hook
```javascript
// Password import hook for migration
app.post('/hooks/password-import', (req, res) => {
  const { data } = req.body;
  const { credential, userId } = data;

  // Verify password against legacy system
  const isValid = verifyLegacyPassword(credential.username, credential.password);

  if (isValid) {
    res.json({
      commands: [{
        type: 'com.okta.action.update',
        value: {
          credential: 'VERIFIED'
        }
      }]
    });
  } else {
    res.json({
      error: {
        errorSummary: 'Invalid credentials'
      }
    });
  }
});

function verifyLegacyPassword(username, password) {
  // Implement legacy password verification logic
  return true; // Placeholder
}
```

## Monitoring and Analytics

### System Log Analysis
```python
import asyncio
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

class OktaAnalytics:
    def __init__(self, okta_client):
        self.client = okta_client
    
    async def get_login_analytics(self, days=30):
        """Analyze login patterns"""
        since = datetime.now() - timedelta(days=days)
        
        # Get login events
        filter_expr = 'eventType eq "user.session.start"'
        logs = await self.client.get_system_logs(filter_expr, since, limit=1000)
        
        # Process data
        login_data = []
        for log in logs:
            login_data.append({
                'timestamp': log.published,
                'user': log.actor.displayName,
                'client': log.client.userAgent.rawUserAgent,
                'ip': log.client.ipAddress,
                'outcome': log.outcome.result
            })
        
        df = pd.DataFrame(login_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Generate analytics
        analytics = {
            'total_logins': len(df),
            'unique_users': df['user'].nunique(),
            'success_rate': (df['outcome'] == 'SUCCESS').mean() * 100,
            'daily_logins': df.groupby(df['timestamp'].dt.date).size().to_dict(),
            'top_users': df['user'].value_counts().head(10).to_dict(),
            'failure_reasons': df[df['outcome'] != 'SUCCESS']['outcome'].value_counts().to_dict()
        }
        
        return analytics
    
    async def get_security_analytics(self, days=7):
        """Analyze security events"""
        since = datetime.now() - timedelta(days=days)
        
        # Get security-related events
        security_events = [
            'user.session.start',
            'user.authentication.auth_via_mfa',
            'user.authentication.auth_via_social',
            'policy.lifecycle.activate',
            'user.account.lock'
        ]
        
        all_events = []
        for event_type in security_events:
            filter_expr = f'eventType eq "{event_type}"'
            logs = await self.client.get_system_logs(filter_expr, since, limit=500)
            all_events.extend(logs)
        
        # Analyze suspicious patterns
        suspicious_ips = self.detect_suspicious_ips(all_events)
        failed_logins = self.analyze_failed_logins(all_events)
        mfa_bypass_attempts = self.detect_mfa_bypass(all_events)
        
        return {
            'suspicious_ips': suspicious_ips,
            'failed_logins': failed_logins,
            'mfa_bypass_attempts': mfa_bypass_attempts,
            'total_security_events': len(all_events)
        }
    
    def detect_suspicious_ips(self, events):
        """Detect potentially suspicious IP addresses"""
        ip_activity = {}
        
        for event in events:
            ip = event.client.ipAddress
            if ip not in ip_activity:
                ip_activity[ip] = {'events': 0, 'users': set(), 'countries': set()}
            
            ip_activity[ip]['events'] += 1
            ip_activity[ip]['users'].add(event.actor.displayName)
            
            # Add geolocation if available
            if hasattr(event.client, 'geographicalContext'):
                ip_activity[ip]['countries'].add(event.client.geographicalContext.country)
        
        # Flag IPs with suspicious patterns
        suspicious = []
        for ip, activity in ip_activity.items():
            if (activity['events'] > 100 or  # High activity
                len(activity['users']) > 20 or  # Many different users
                len(activity['countries']) > 3):  # Multiple countries
                suspicious.append({
                    'ip': ip,
                    'events': activity['events'],
                    'unique_users': len(activity['users']),
                    'countries': list(activity['countries'])
                })
        
        return suspicious
    
    async def generate_compliance_report(self, days=30):
        """Generate compliance and audit report"""
        since = datetime.now() - timedelta(days=days)
        
        # Get all administrative events
        admin_filter = 'eventType sw "user.lifecycle" or eventType sw "group" or eventType sw "application"'
        admin_events = await self.client.get_system_logs(admin_filter, since, limit=2000)
        
        report = {
            'period': f"{since.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
            'user_changes': [],
            'group_changes': [],
            'app_changes': [],
            'policy_changes': []
        }
        
        for event in admin_events:
            event_data = {
                'timestamp': event.published,
                'actor': event.actor.displayName,
                'event_type': event.eventType,
                'target': event.target[0].displayName if event.target else 'N/A',
                'outcome': event.outcome.result
            }
            
            if 'user' in event.eventType:
                report['user_changes'].append(event_data)
            elif 'group' in event.eventType:
                report['group_changes'].append(event_data)
            elif 'application' in event.eventType:
                report['app_changes'].append(event_data)
            elif 'policy' in event.eventType:
                report['policy_changes'].append(event_data)
        
        return report

# Usage
analytics = OktaAnalytics(okta_client)

async def run_analytics():
    # Login analytics
    login_stats = await analytics.get_login_analytics(30)
    print(f"Total logins: {login_stats['total_logins']}")
    print(f"Success rate: {login_stats['success_rate']:.2f}%")
    
    # Security analytics
    security_stats = await analytics.get_security_analytics(7)
    print(f"Suspicious IPs: {len(security_stats['suspicious_ips'])}")
    
    # Compliance report
    compliance = await analytics.generate_compliance_report(30)
    print(f"User changes: {len(compliance['user_changes'])}")

asyncio.run(run_analytics())
```

## Best Practices

### Security Configuration
```yaml
# Authentication Policy Best Practices
policies:
  authentication:
    - name: "High Risk Authentication"
      conditions:
        - risk_level: "HIGH"
        - network_zone: "untrusted"
      actions:
        - require_mfa: true
        - require_device_trust: true
        - session_timeout: "1h"
    
    - name: "Standard Authentication"
      conditions:
        - risk_level: "LOW"
        - network_zone: "trusted"
      actions:
        - require_mfa: false
        - session_timeout: "8h"

  password:
    complexity:
      min_length: 12
      require_uppercase: true
      require_lowercase: true
      require_numbers: true
      require_symbols: true
    history: 12
    expiration: 90

  account_lockout:
    max_attempts: 5
    lockout_duration: "30m"
    auto_unlock: true
```

### User Lifecycle Automation
```python
class UserLifecycleManager:
    def __init__(self, okta_client):
        self.okta = okta_client
    
    async def onboard_user(self, user_data):
        """Complete user onboarding process"""
        try:
            # 1. Create user
            user = await self.okta.create_user(user_data)
            
            # 2. Assign to groups based on department
            groups = self.get_department_groups(user_data['department'])
            for group_id in groups:
                await self.okta.add_user_to_group(user.id, group_id)
            
            # 3. Assign applications
            apps = self.get_department_apps(user_data['department'])
            for app_id in apps:
                await self.okta.assign_app_to_user(app_id, user.id)
            
            # 4. Send welcome email
            await self.send_welcome_email(user)
            
            return user
            
        except Exception as e:
            # Rollback on failure
            if 'user' in locals():
                await self.okta.deactivate_user(user.id)
            raise e
    
    async def offboard_user(self, user_id):
        """Complete user offboarding process"""
        # 1. Deactivate user
        await self.okta.deactivate_user(user_id)
        
        # 2. Remove from all groups
        groups = await self.okta.get_user_groups(user_id)
        for group in groups:
            await self.okta.remove_user_from_group(user_id, group.id)
        
        # 3. Remove application assignments
        # Implementation depends on your needs
        
        # 4. Archive user data
        await self.archive_user_data(user_id)

    def get_department_groups(self, department):
        """Map department to group IDs"""
        mapping = {
            'Engineering': ['developers-group', 'engineering-group'],
            'Sales': ['sales-group', 'crm-users-group'],
            'HR': ['hr-group', 'admin-group']
        }
        return mapping.get(department, ['all-users-group'])
```

## Resources

- [Okta Developer Documentation](https://developer.okta.com/)
- [Okta Admin Console Guide](https://help.okta.com/en/prod/okta_help.htm)
- [Okta SDK Documentation](https://github.com/okta/okta-sdk-nodejs)
- [OIDC/OAuth 2.0 Best Practices](https://developer.okta.com/docs/concepts/oauth-openid/)
- [Okta API Reference](https://developer.okta.com/docs/reference/)
- [Security Best Practices](https://help.okta.com/en/prod/Content/Topics/Security/Security.htm)
- [Okta Hooks Documentation](https://developer.okta.com/docs/concepts/inline-hooks/)
- [System Log Events](https://developer.okta.com/docs/reference/api/system-log/)
- [Community Forum](https://devforum.okta.com/)
- [Okta Integration Network](https://www.okta.com/integrations/)