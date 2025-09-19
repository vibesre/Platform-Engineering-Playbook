# LDAP (Lightweight Directory Access Protocol)

LDAP is a directory service protocol used for accessing and maintaining distributed directory information services over an Internet Protocol network.

## Core Concepts

### Directory Structure
- **Directory Information Tree (DIT)**: Hierarchical structure of entries
- **Distinguished Name (DN)**: Unique identifier for each entry
- **Relative Distinguished Name (RDN)**: Component of DN
- **Base DN**: Root of the directory tree
- **Object Classes**: Templates defining entry structure
- **Attributes**: Properties of directory entries

### Common Implementations
- **OpenLDAP**: Open-source LDAP server
- **Active Directory**: Microsoft's directory service
- **Apache Directory Server**: Java-based LDAP server
- **389 Directory Server**: Red Hat's LDAP implementation
- **OpenDJ**: ForgeRock's directory server

## OpenLDAP Installation

### Ubuntu/Debian
```bash
# Install OpenLDAP server
sudo apt update
sudo apt install slapd ldap-utils

# Configure OpenLDAP
sudo dpkg-reconfigure slapd

# Start and enable service
sudo systemctl start slapd
sudo systemctl enable slapd

# Verify installation
sudo systemctl status slapd
ldapsearch -x -LLL -H ldap:/// -b "" -s base
```

### CentOS/RHEL
```bash
# Install OpenLDAP
sudo yum install openldap-servers openldap-clients

# Or with dnf
sudo dnf install openldap-servers openldap-clients

# Start and enable service
sudo systemctl start slapd
sudo systemctl enable slapd

# Configure firewall
sudo firewall-cmd --permanent --add-service=ldap
sudo firewall-cmd --reload
```

### Docker
```yaml
# docker-compose.yml
version: '3.8'
services:
  ldap:
    image: osixia/openldap:1.5.0
    container_name: openldap
    environment:
      LDAP_ORGANISATION: "Company Inc"
      LDAP_DOMAIN: "company.com"
      LDAP_ADMIN_PASSWORD: "admin_password"
      LDAP_CONFIG_PASSWORD: "config_password"
      LDAP_RFC2307BIS_SCHEMA: "true"
      LDAP_REMOVE_CONFIG_AFTER_SETUP: "true"
      LDAP_TLS_VERIFY_CLIENT: "never"
    volumes:
      - ldap_data:/var/lib/ldap
      - ldap_config:/etc/ldap/slapd.d
      - ./certs:/container/service/slapd/assets/certs
    ports:
      - "389:389"
      - "636:636"
    networks:
      - ldap_network

  ldap-admin:
    image: osixia/phpldapadmin:0.9.0
    container_name: ldap-admin
    environment:
      PHPLDAPADMIN_LDAP_HOSTS: ldap
      PHPLDAPADMIN_HTTPS: "false"
    ports:
      - "8080:80"
    depends_on:
      - ldap
    networks:
      - ldap_network

volumes:
  ldap_data:
  ldap_config:

networks:
  ldap_network:
    driver: bridge
```

## LDAP Configuration

### Basic Schema Configuration
```ldif
# base.ldif - Base directory structure
dn: dc=company,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: Company Inc
dc: company

dn: cn=admin,dc=company,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
userPassword: {SSHA}encrypted_password_hash

dn: ou=people,dc=company,dc=com
objectClass: organizationalUnit
ou: people

dn: ou=groups,dc=company,dc=com
objectClass: organizationalUnit
ou: groups

dn: ou=services,dc=company,dc=com
objectClass: organizationalUnit
ou: services
```

### User Entry Examples
```ldif
# users.ldif
dn: uid=jdoe,ou=people,dc=company,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jdoe
sn: Doe
givenName: John
cn: John Doe
displayName: John Doe
uidNumber: 10001
gidNumber: 10001
userPassword: {SSHA}encrypted_password
gecos: John Doe
loginShell: /bin/bash
homeDirectory: /home/jdoe
mail: john.doe@company.com
telephoneNumber: +1-555-0123
departmentNumber: Engineering
employeeNumber: 12345
title: Software Engineer
manager: uid=manager,ou=people,dc=company,dc=com

dn: uid=jsmith,ou=people,dc=company,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jsmith
sn: Smith
givenName: Jane
cn: Jane Smith
displayName: Jane Smith
uidNumber: 10002
gidNumber: 10002
userPassword: {SSHA}encrypted_password
gecos: Jane Smith
loginShell: /bin/bash
homeDirectory: /home/jsmith
mail: jane.smith@company.com
telephoneNumber: +1-555-0124
departmentNumber: Sales
employeeNumber: 12346
title: Sales Manager
```

### Group Entries
```ldif
# groups.ldif
dn: cn=developers,ou=groups,dc=company,dc=com
objectClass: groupOfNames
objectClass: posixGroup
cn: developers
gidNumber: 20001
description: Software Developers
member: uid=jdoe,ou=people,dc=company,dc=com
member: uid=anotherdev,ou=people,dc=company,dc=com

dn: cn=admins,ou=groups,dc=company,dc=com
objectClass: groupOfNames
objectClass: posixGroup
cn: admins
gidNumber: 20002
description: System Administrators
member: uid=admin,ou=people,dc=company,dc=com

dn: cn=sales,ou=groups,dc=company,dc=com
objectClass: groupOfNames
objectClass: posixGroup
cn: sales
gidNumber: 20003
description: Sales Team
member: uid=jsmith,ou=people,dc=company,dc=com
```

## LDAP Operations

### Basic LDAP Commands
```bash
# Add entries to LDAP
ldapadd -x -D "cn=admin,dc=company,dc=com" -W -f base.ldif
ldapadd -x -D "cn=admin,dc=company,dc=com" -W -f users.ldif
ldapadd -x -D "cn=admin,dc=company,dc=com" -W -f groups.ldif

# Search operations
# Search all entries
ldapsearch -x -LLL -H ldap://localhost -b "dc=company,dc=com"

# Search for specific user
ldapsearch -x -LLL -H ldap://localhost -b "ou=people,dc=company,dc=com" "(uid=jdoe)"

# Search for users in specific department
ldapsearch -x -LLL -H ldap://localhost -b "ou=people,dc=company,dc=com" "(departmentNumber=Engineering)"

# Search for groups
ldapsearch -x -LLL -H ldap://localhost -b "ou=groups,dc=company,dc=com" "(objectClass=groupOfNames)"

# Modify user attributes
cat > modify_user.ldif << EOF
dn: uid=jdoe,ou=people,dc=company,dc=com
changetype: modify
replace: telephoneNumber
telephoneNumber: +1-555-9999
-
add: description
description: Senior Software Engineer
EOF

ldapmodify -x -D "cn=admin,dc=company,dc=com" -W -f modify_user.ldif

# Delete user
ldapdelete -x -D "cn=admin,dc=company,dc=com" -W "uid=olduser,ou=people,dc=company,dc=com"

# Change password
ldappasswd -x -D "cn=admin,dc=company,dc=com" -W -S "uid=jdoe,ou=people,dc=company,dc=com"
```

### Advanced Search Filters
```bash
# Complex search filters
# Users with email ending in @company.com
ldapsearch -x -LLL -b "ou=people,dc=company,dc=com" "(mail=*@company.com)"

# Users in Engineering with manager
ldapsearch -x -LLL -b "ou=people,dc=company,dc=com" "(&(departmentNumber=Engineering)(manager=*))"

# Groups with specific members
ldapsearch -x -LLL -b "ou=groups,dc=company,dc=com" "(member=uid=jdoe,ou=people,dc=company,dc=com)"

# Users without phone numbers
ldapsearch -x -LLL -b "ou=people,dc=company,dc=com" "(!(telephoneNumber=*))"

# Users created in the last 30 days (if createTimestamp is available)
ldapsearch -x -LLL -b "ou=people,dc=company,dc=com" "(createTimestamp>=20240101000000Z)"
```

## Python LDAP Integration

### Installation and Basic Usage
```python
import ldap
import ldap.modlist as modlist
from ldap.controls import SimplePagedResultsControl
import hashlib
import base64
import os
from typing import List, Dict, Optional

class LDAPClient:
    def __init__(self, server_uri: str, bind_dn: str, bind_password: str):
        self.server_uri = server_uri
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.connection = None
        
    def connect(self):
        """Establish LDAP connection"""
        try:
            self.connection = ldap.initialize(self.server_uri)
            self.connection.protocol_version = ldap.VERSION3
            self.connection.set_option(ldap.OPT_REFERRALS, 0)
            
            # Bind to LDAP server
            self.connection.simple_bind_s(self.bind_dn, self.bind_password)
            print(f"Connected to LDAP server: {self.server_uri}")
            
        except ldap.INVALID_CREDENTIALS:
            print("Invalid credentials")
            raise
        except ldap.SERVER_DOWN:
            print("LDAP server is down")
            raise
        except Exception as e:
            print(f"LDAP connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close LDAP connection"""
        if self.connection:
            self.connection.unbind_s()
            self.connection = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    def search(self, base_dn: str, search_filter: str = "(objectClass=*)", 
               attributes: Optional[List[str]] = None, scope: int = ldap.SCOPE_SUBTREE) -> List[Dict]:
        """Search LDAP directory"""
        try:
            result_id = self.connection.search(base_dn, scope, search_filter, attributes)
            results = []
            
            while True:
                result_type, result_data = self.connection.result(result_id, 0)
                if result_type == ldap.RES_SEARCH_ENTRY:
                    dn, attrs = result_data[0]
                    # Convert bytes to strings
                    converted_attrs = {}
                    for key, values in attrs.items():
                        converted_attrs[key] = [v.decode('utf-8') if isinstance(v, bytes) else v for v in values]
                    
                    results.append({
                        'dn': dn,
                        'attributes': converted_attrs
                    })
                elif result_type == ldap.RES_SEARCH_RESULT:
                    break
            
            return results
            
        except ldap.NO_SUCH_OBJECT:
            print(f"Base DN not found: {base_dn}")
            return []
        except Exception as e:
            print(f"Search failed: {e}")
            raise
    
    def add_entry(self, dn: str, attributes: Dict):
        """Add new LDAP entry"""
        try:
            # Convert string values to bytes and create modlist
            ldif = modlist.addModlist(attributes)
            self.connection.add_s(dn, ldif)
            print(f"Entry added: {dn}")
            
        except ldap.ALREADY_EXISTS:
            print(f"Entry already exists: {dn}")
            raise
        except Exception as e:
            print(f"Add entry failed: {e}")
            raise
    
    def modify_entry(self, dn: str, modifications: List):
        """Modify existing LDAP entry"""
        try:
            self.connection.modify_s(dn, modifications)
            print(f"Entry modified: {dn}")
            
        except ldap.NO_SUCH_OBJECT:
            print(f"Entry not found: {dn}")
            raise
        except Exception as e:
            print(f"Modify entry failed: {e}")
            raise
    
    def delete_entry(self, dn: str):
        """Delete LDAP entry"""
        try:
            self.connection.delete_s(dn)
            print(f"Entry deleted: {dn}")
            
        except ldap.NO_SUCH_OBJECT:
            print(f"Entry not found: {dn}")
            raise
        except Exception as e:
            print(f"Delete entry failed: {e}")
            raise
    
    def create_user(self, uid: str, user_data: Dict, base_dn: str = "ou=people,dc=company,dc=com"):
        """Create a new user"""
        dn = f"uid={uid},{base_dn}"
        
        # Generate SSHA password hash
        password_hash = self.generate_ssha_password(user_data['password'])
        
        attributes = {
            'objectClass': ['inetOrgPerson', 'posixAccount', 'shadowAccount'],
            'uid': [uid],
            'cn': [user_data['cn']],
            'sn': [user_data['sn']],
            'givenName': [user_data.get('givenName', '')],
            'displayName': [user_data.get('displayName', user_data['cn'])],
            'mail': [user_data['mail']],
            'userPassword': [password_hash],
            'uidNumber': [str(user_data['uidNumber'])],
            'gidNumber': [str(user_data['gidNumber'])],
            'homeDirectory': [user_data.get('homeDirectory', f'/home/{uid}')],
            'loginShell': [user_data.get('loginShell', '/bin/bash')],
            'gecos': [user_data.get('gecos', user_data['cn'])]
        }
        
        # Add optional attributes
        optional_attrs = ['telephoneNumber', 'departmentNumber', 'employeeNumber', 'title', 'manager']
        for attr in optional_attrs:
            if attr in user_data:
                attributes[attr] = [user_data[attr]]
        
        self.add_entry(dn, attributes)
        return dn
    
    def create_group(self, cn: str, group_data: Dict, base_dn: str = "ou=groups,dc=company,dc=com"):
        """Create a new group"""
        dn = f"cn={cn},{base_dn}"
        
        attributes = {
            'objectClass': ['groupOfNames', 'posixGroup'],
            'cn': [cn],
            'gidNumber': [str(group_data['gidNumber'])],
            'description': [group_data.get('description', '')],
            'member': group_data.get('members', [''])  # GroupOfNames requires at least one member
        }
        
        self.add_entry(dn, attributes)
        return dn
    
    def add_user_to_group(self, user_dn: str, group_dn: str):
        """Add user to group"""
        modifications = [(ldap.MOD_ADD, 'member', [user_dn.encode('utf-8')])]
        self.modify_entry(group_dn, modifications)
    
    def remove_user_from_group(self, user_dn: str, group_dn: str):
        """Remove user from group"""
        modifications = [(ldap.MOD_DELETE, 'member', [user_dn.encode('utf-8')])]
        self.modify_entry(group_dn, modifications)
    
    def authenticate_user(self, user_dn: str, password: str) -> bool:
        """Authenticate user credentials"""
        try:
            # Create a separate connection for authentication
            auth_conn = ldap.initialize(self.server_uri)
            auth_conn.protocol_version = ldap.VERSION3
            auth_conn.simple_bind_s(user_dn, password)
            auth_conn.unbind_s()
            return True
        except ldap.INVALID_CREDENTIALS:
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def change_password(self, user_dn: str, new_password: str):
        """Change user password"""
        password_hash = self.generate_ssha_password(new_password)
        modifications = [(ldap.MOD_REPLACE, 'userPassword', [password_hash.encode('utf-8')])]
        self.modify_entry(user_dn, modifications)
    
    def generate_ssha_password(self, password: str) -> str:
        """Generate SSHA password hash"""
        salt = os.urandom(4)
        sha_hash = hashlib.sha1(password.encode('utf-8') + salt).digest()
        ssha_hash = base64.b64encode(sha_hash + salt).decode('utf-8')
        return f"{{SSHA}}{ssha_hash}"
    
    def get_user_groups(self, user_dn: str) -> List[str]:
        """Get groups that user belongs to"""
        search_filter = f"(member={user_dn})"
        results = self.search("ou=groups,dc=company,dc=com", search_filter, ['cn'])
        return [result['attributes']['cn'][0] for result in results]
    
    def get_group_members(self, group_dn: str) -> List[str]:
        """Get members of a group"""
        results = self.search(group_dn, "(objectClass=groupOfNames)", ['member'])
        if results:
            return results[0]['attributes'].get('member', [])
        return []

# Usage example
def main():
    ldap_client = LDAPClient(
        server_uri="ldap://localhost:389",
        bind_dn="cn=admin,dc=company,dc=com",
        bind_password="admin_password"
    )
    
    with ldap_client:
        # Create a user
        user_data = {
            'cn': 'Alice Johnson',
            'sn': 'Johnson',
            'givenName': 'Alice',
            'mail': 'alice.johnson@company.com',
            'password': 'temporary_password',
            'uidNumber': 10003,
            'gidNumber': 10003,
            'departmentNumber': 'Marketing',
            'title': 'Marketing Manager'
        }
        
        user_dn = ldap_client.create_user('ajohnson', user_data)
        
        # Create a group
        group_data = {
            'gidNumber': 20004,
            'description': 'Marketing Team',
            'members': [user_dn]
        }
        
        group_dn = ldap_client.create_group('marketing', group_data)
        
        # Search for users
        users = ldap_client.search(
            "ou=people,dc=company,dc=com",
            "(departmentNumber=Marketing)",
            ['cn', 'mail', 'title']
        )
        
        print("Marketing users:")
        for user in users:
            attrs = user['attributes']
            print(f"  {attrs['cn'][0]} - {attrs['mail'][0]} - {attrs['title'][0]}")
        
        # Authenticate user
        is_valid = ldap_client.authenticate_user(user_dn, 'temporary_password')
        print(f"Authentication successful: {is_valid}")

if __name__ == "__main__":
    main()
```

### Advanced User Management
```python
class UserManager:
    def __init__(self, ldap_client: LDAPClient):
        self.ldap = ldap_client
        self.base_user_dn = "ou=people,dc=company,dc=com"
        self.base_group_dn = "ou=groups,dc=company,dc=com"
    
    def bulk_create_users(self, users_data: List[Dict]):
        """Create multiple users in bulk"""
        results = []
        
        for user_data in users_data:
            try:
                user_dn = self.ldap.create_user(user_data['uid'], user_data)
                results.append({'success': True, 'dn': user_dn, 'uid': user_data['uid']})
            except Exception as e:
                results.append({'success': False, 'error': str(e), 'uid': user_data['uid']})
        
        return results
    
    def sync_user_groups(self, uid: str, target_groups: List[str]):
        """Synchronize user's group memberships"""
        user_dn = f"uid={uid},{self.base_user_dn}"
        
        # Get current groups
        current_groups = self.ldap.get_user_groups(user_dn)
        current_group_dns = [f"cn={group},{self.base_group_dn}" for group in current_groups]
        target_group_dns = [f"cn={group},{self.base_group_dn}" for group in target_groups]
        
        # Groups to add
        groups_to_add = set(target_group_dns) - set(current_group_dns)
        for group_dn in groups_to_add:
            try:
                self.ldap.add_user_to_group(user_dn, group_dn)
            except Exception as e:
                print(f"Failed to add user to group {group_dn}: {e}")
        
        # Groups to remove
        groups_to_remove = set(current_group_dns) - set(target_group_dns)
        for group_dn in groups_to_remove:
            try:
                self.ldap.remove_user_from_group(user_dn, group_dn)
            except Exception as e:
                print(f"Failed to remove user from group {group_dn}: {e}")
    
    def get_users_by_department(self, department: str) -> List[Dict]:
        """Get all users in a specific department"""
        search_filter = f"(departmentNumber={department})"
        return self.ldap.search(
            self.base_user_dn,
            search_filter,
            ['uid', 'cn', 'mail', 'title', 'telephoneNumber']
        )
    
    def update_user_profile(self, uid: str, updates: Dict):
        """Update user profile attributes"""
        user_dn = f"uid={uid},{self.base_user_dn}"
        
        modifications = []
        for attr, value in updates.items():
            if value:
                modifications.append((ldap.MOD_REPLACE, attr, [value.encode('utf-8')]))
            else:
                modifications.append((ldap.MOD_DELETE, attr, None))
        
        if modifications:
            self.ldap.modify_entry(user_dn, modifications)
    
    def disable_user(self, uid: str):
        """Disable user account"""
        user_dn = f"uid={uid},{self.base_user_dn}"
        
        # Set account as disabled (implementation depends on schema)
        modifications = [
            (ldap.MOD_REPLACE, 'loginShell', ['/bin/false'.encode('utf-8')]),
            (ldap.MOD_ADD, 'description', ['Account disabled'.encode('utf-8')])
        ]
        
        self.ldap.modify_entry(user_dn, modifications)
    
    def generate_user_report(self) -> Dict:
        """Generate user statistics report"""
        all_users = self.ldap.search(self.base_user_dn, "(objectClass=inetOrgPerson)")
        
        report = {
            'total_users': len(all_users),
            'departments': {},
            'users_without_email': 0,
            'users_without_phone': 0
        }
        
        for user in all_users:
            attrs = user['attributes']
            
            # Department statistics
            dept = attrs.get('departmentNumber', ['Unknown'])[0]
            if dept not in report['departments']:
                report['departments'][dept] = 0
            report['departments'][dept] += 1
            
            # Missing information
            if not attrs.get('mail'):
                report['users_without_email'] += 1
            if not attrs.get('telephoneNumber'):
                report['users_without_phone'] += 1
        
        return report
```

## LDAP Authentication in Applications

### Flask Integration
```python
from flask import Flask, request, session, redirect, url_for, jsonify
from functools import wraps
import ldap

app = Flask(__name__)
app.secret_key = 'your-secret-key'

class LDAPAuth:
    def __init__(self, server_uri, base_dn):
        self.server_uri = server_uri
        self.base_dn = base_dn
    
    def authenticate(self, username, password):
        """Authenticate user against LDAP"""
        try:
            # Search for user
            conn = ldap.initialize(self.server_uri)
            conn.protocol_version = ldap.VERSION3
            
            # Search for user DN
            search_filter = f"(uid={username})"
            result = conn.search_s(
                f"ou=people,{self.base_dn}",
                ldap.SCOPE_SUBTREE,
                search_filter,
                ['dn', 'cn', 'mail', 'departmentNumber']
            )
            
            if not result:
                return None
            
            user_dn, user_attrs = result[0]
            
            # Try to bind with user credentials
            user_conn = ldap.initialize(self.server_uri)
            user_conn.protocol_version = ldap.VERSION3
            user_conn.simple_bind_s(user_dn, password)
            user_conn.unbind_s()
            
            # Convert bytes to strings
            converted_attrs = {}
            for key, values in user_attrs.items():
                converted_attrs[key] = [v.decode('utf-8') if isinstance(v, bytes) else v for v in values]
            
            return {
                'dn': user_dn,
                'username': username,
                'name': converted_attrs.get('cn', [''])[0],
                'email': converted_attrs.get('mail', [''])[0],
                'department': converted_attrs.get('departmentNumber', [''])[0]
            }
            
        except ldap.INVALID_CREDENTIALS:
            return None
        except Exception as e:
            print(f"LDAP authentication error: {e}")
            return None
        finally:
            try:
                conn.unbind_s()
            except:
                pass
    
    def get_user_groups(self, user_dn):
        """Get groups for authenticated user"""
        try:
            conn = ldap.initialize(self.server_uri)
            conn.protocol_version = ldap.VERSION3
            
            search_filter = f"(member={user_dn})"
            result = conn.search_s(
                f"ou=groups,{self.base_dn}",
                ldap.SCOPE_SUBTREE,
                search_filter,
                ['cn']
            )
            
            groups = []
            for group_dn, group_attrs in result:
                groups.append(group_attrs['cn'][0].decode('utf-8'))
            
            return groups
            
        except Exception as e:
            print(f"Error getting user groups: {e}")
            return []
        finally:
            try:
                conn.unbind_s()
            except:
                pass

ldap_auth = LDAPAuth('ldap://localhost:389', 'dc=company,dc=com')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        
        user_groups = session.get('groups', [])
        if 'admins' not in user_groups:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = ldap_auth.authenticate(username, password)
        if user:
            session['user'] = user
            session['groups'] = ldap_auth.get_user_groups(user['dn'])
            return jsonify({'success': True, 'user': user})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Please provide username and password'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/profile')
@login_required
def profile():
    return jsonify({
        'user': session['user'],
        'groups': session['groups']
    })

@app.route('/admin')
@admin_required
def admin():
    return jsonify({'message': 'Admin area'})

if __name__ == '__main__':
    app.run(debug=True)
```

### Node.js Integration
```javascript
const express = require('express');
const ldap = require('ldapjs');
const session = require('express-session');

const app = express();
app.use(express.json());
app.use(session({
  secret: 'your-session-secret',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 3600000 } // 1 hour
}));

class LDAPAuth {
  constructor(serverUrl, baseDN) {
    this.serverUrl = serverUrl;
    this.baseDN = baseDN;
  }

  async authenticate(username, password) {
    return new Promise((resolve, reject) => {
      const client = ldap.createClient({
        url: this.serverUrl,
        timeout: 5000
      });

      // First, search for the user
      const searchOptions = {
        filter: `(uid=${username})`,
        scope: 'sub',
        attributes: ['dn', 'cn', 'mail', 'departmentNumber']
      };

      client.search(`ou=people,${this.baseDN}`, searchOptions, (err, res) => {
        if (err) {
          client.unbind();
          return reject(err);
        }

        let userEntry = null;

        res.on('searchEntry', (entry) => {
          userEntry = entry.object;
        });

        res.on('error', (err) => {
          client.unbind();
          reject(err);
        });

        res.on('end', (result) => {
          if (!userEntry) {
            client.unbind();
            return resolve(null);
          }

          // Try to bind with user credentials
          const userClient = ldap.createClient({
            url: this.serverUrl,
            timeout: 5000
          });

          userClient.bind(userEntry.dn, password, (bindErr) => {
            userClient.unbind();
            client.unbind();

            if (bindErr) {
              return resolve(null);
            }

            resolve({
              dn: userEntry.dn,
              username: username,
              name: userEntry.cn,
              email: userEntry.mail,
              department: userEntry.departmentNumber
            });
          });
        });
      });
    });
  }

  async getUserGroups(userDN) {
    return new Promise((resolve, reject) => {
      const client = ldap.createClient({
        url: this.serverUrl,
        timeout: 5000
      });

      const searchOptions = {
        filter: `(member=${userDN})`,
        scope: 'sub',
        attributes: ['cn']
      };

      const groups = [];

      client.search(`ou=groups,${this.baseDN}`, searchOptions, (err, res) => {
        if (err) {
          client.unbind();
          return reject(err);
        }

        res.on('searchEntry', (entry) => {
          groups.push(entry.object.cn);
        });

        res.on('error', (err) => {
          client.unbind();
          reject(err);
        });

        res.on('end', () => {
          client.unbind();
          resolve(groups);
        });
      });
    });
  }
}

const ldapAuth = new LDAPAuth('ldap://localhost:389', 'dc=company,dc=com');

// Middleware
function requireAuth(req, res, next) {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  next();
}

function requireAdmin(req, res, next) {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  if (!req.session.groups || !req.session.groups.includes('admins')) {
    return res.status(403).json({ error: 'Admin access required' });
  }
  
  next();
}

// Routes
app.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    const user = await ldapAuth.authenticate(username, password);
    if (user) {
      const groups = await ldapAuth.getUserGroups(user.dn);
      
      req.session.user = user;
      req.session.groups = groups;
      
      res.json({ success: true, user, groups });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: 'Logout failed' });
    }
    res.json({ success: true });
  });
});

app.get('/profile', requireAuth, (req, res) => {
  res.json({
    user: req.session.user,
    groups: req.session.groups
  });
});

app.get('/admin', requireAdmin, (req, res) => {
  res.json({ message: 'Admin area' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

## Security and SSL Configuration

### TLS/SSL Setup
```bash
# Generate certificates for LDAP over SSL
sudo openssl req -new -x509 -nodes -out /etc/ssl/certs/ldap-server.crt \
  -keyout /etc/ssl/private/ldap-server.key -days 365 \
  -subj "/C=US/ST=State/L=City/O=Company/CN=ldap.company.com"

# Set permissions
sudo chown openldap:openldap /etc/ssl/private/ldap-server.key
sudo chmod 600 /etc/ssl/private/ldap-server.key
```

### LDAP Configuration for TLS
```ldif
# tls.ldif
dn: cn=config
changetype: modify
add: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/ldap-server.crt
-
add: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/ldap-server.key
-
add: olcTLSProtocolMin
olcTLSProtocolMin: 3.3
-
add: olcTLSCipherSuite
olcTLSCipherSuite: HIGH:MEDIUM:+TLSv1.2:!SSLv2:!SSLv3

# Apply configuration
sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f tls.ldif
```

### Access Control Lists (ACLs)
```ldif
# acl.ldif
dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange
  by dn="cn=admin,dc=company,dc=com" write
  by anonymous auth
  by self write
  by * none
olcAccess: {1}to dn.base=""
  by * read
olcAccess: {2}to *
  by dn="cn=admin,dc=company,dc=com" write
  by users read
  by * none

sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f acl.ldif
```

## Monitoring and Maintenance

### Health Checks
```bash
#!/bin/bash
# ldap-health-check.sh

LDAP_SERVER="ldap://localhost:389"
BASE_DN="dc=company,dc=com"
BIND_DN="cn=admin,dc=company,dc=com"
BIND_PW="admin_password"

echo "LDAP Health Check - $(date)"
echo "================================"

# Test LDAP connection
echo -n "Testing LDAP connection... "
if ldapsearch -x -H "$LDAP_SERVER" -b "" -s base > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAILED"
    exit 1
fi

# Test authentication
echo -n "Testing admin authentication... "
if ldapsearch -x -H "$LDAP_SERVER" -D "$BIND_DN" -w "$BIND_PW" -b "$BASE_DN" -s base > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAILED"
    exit 1
fi

# Count entries
USER_COUNT=$(ldapsearch -x -H "$LDAP_SERVER" -D "$BIND_DN" -w "$BIND_PW" \
    -b "ou=people,$BASE_DN" "(objectClass=inetOrgPerson)" dn | grep -c "^dn:")
GROUP_COUNT=$(ldapsearch -x -H "$LDAP_SERVER" -D "$BIND_DN" -w "$BIND_PW" \
    -b "ou=groups,$BASE_DN" "(objectClass=groupOfNames)" dn | grep -c "^dn:")

echo "Users: $USER_COUNT"
echo "Groups: $GROUP_COUNT"

# Check disk usage
LDAP_DATA_DIR="/var/lib/ldap"
if [ -d "$LDAP_DATA_DIR" ]; then
    DISK_USAGE=$(du -sh "$LDAP_DATA_DIR" | cut -f1)
    echo "Data directory size: $DISK_USAGE"
fi

echo "Health check completed successfully"
```

### Backup and Recovery
```bash
#!/bin/bash
# ldap-backup.sh

BACKUP_DIR="/opt/ldap-backups"
DATE=$(date +%Y%m%d_%H%M%S)
LDAP_DATA="/var/lib/ldap"
LDAP_CONFIG="/etc/ldap/slapd.d"

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Stop slapd
systemctl stop slapd

# Backup LDAP data
echo "Backing up LDAP data..."
tar -czf "$BACKUP_DIR/$DATE/ldap-data.tar.gz" -C "$(dirname $LDAP_DATA)" "$(basename $LDAP_DATA)"

# Backup LDAP configuration
echo "Backing up LDAP configuration..."
tar -czf "$BACKUP_DIR/$DATE/ldap-config.tar.gz" -C "$(dirname $LDAP_CONFIG)" "$(basename $LDAP_CONFIG)"

# Export LDIF
echo "Exporting LDIF..."
slapcat -n 1 > "$BACKUP_DIR/$DATE/data.ldif"
slapcat -n 0 > "$BACKUP_DIR/$DATE/config.ldif"

# Start slapd
systemctl start slapd

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "20*" -type d -mtime +30 -exec rm -rf {} +

echo "Backup completed: $BACKUP_DIR/$DATE"
```

## Best Practices

### Directory Design
```
Recommended Directory Structure:
dc=company,dc=com
├── ou=people
│   ├── uid=user1
│   ├── uid=user2
│   └── ou=disabled
├── ou=groups
│   ├── cn=developers
│   ├── cn=admins
│   └── cn=sales
├── ou=services
│   ├── cn=app1
│   └── cn=app2
└── ou=policies
    ├── cn=password-policy
    └── cn=lockout-policy
```

### Performance Optimization
```ldif
# Database tuning
dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcDbMaxSize
olcDbMaxSize: 1073741824
-
replace: olcDbIndex
olcDbIndex: objectClass eq
olcDbIndex: uid eq
olcDbIndex: cn eq,sub
olcDbIndex: mail eq
olcDbIndex: member eq
olcDbIndex: memberUid eq
```

## Resources

- [OpenLDAP Administrator's Guide](https://www.openldap.org/doc/admin24/)
- [LDAP Protocol RFC 4511](https://tools.ietf.org/html/rfc4511)
- [LDAP Schema Reference](https://ldapwiki.com/wiki/ObjectClass)
- [Python LDAP Documentation](https://python-ldap.readthedocs.io/)
- [LDAP Best Practices](https://ldapwiki.com/wiki/Best%20Practices)
- [OpenLDAP FAQ](https://www.openldap.org/faq/)
- [LDAP Security Guidelines](https://tools.ietf.org/html/rfc4513)
- [Directory Service Patterns](https://ldapwiki.com/wiki/Directory%20Service%20Patterns)
- [LDAP Performance Tuning](https://www.openldap.org/doc/admin24/tuning.html)
- [Active Directory LDAP Reference](https://docs.microsoft.com/en-us/windows/win32/adsi/ldap-adspath)