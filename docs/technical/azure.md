# Microsoft Azure

## Overview

Microsoft Azure is a comprehensive cloud computing platform offering over 200 products and cloud services designed to help organizations build, run, and manage applications across multiple clouds, on-premises, and at the edge. With its strong enterprise integration, hybrid cloud capabilities, and extensive compliance certifications, Azure is particularly popular among enterprises already using Microsoft technologies.

### Why Azure?

- **Enterprise Integration**: Seamless integration with Microsoft 365, Active Directory, and enterprise tools
- **Hybrid Cloud Leader**: Azure Arc, Azure Stack for true hybrid deployments
- **Global Reach**: 60+ regions worldwide, more than any other cloud provider
- **AI and ML Services**: Azure OpenAI, Cognitive Services, and Machine Learning
- **Developer Friendly**: Excellent tooling with Visual Studio, VS Code, GitHub integration
- **Compliance**: Most compliance certifications of any cloud provider

## Key Services

### Compute Services

#### Virtual Machines
Scalable on-demand computing resources.

```bash
# Create a resource group
az group create \
  --name myResourceGroup \
  --location eastus

# Create a virtual machine
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_DS2_v2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Open port 80 for web traffic
az vm open-port \
  --resource-group myResourceGroup \
  --name myVM \
  --port 80 \
  --priority 1001

# Connect to VM
ssh azureuser@$(az vm show -d -g myResourceGroup -n myVM --query publicIps -o tsv)
```

#### Azure Kubernetes Service (AKS)
Managed Kubernetes container orchestration service.

```bash
# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --node-vm-size Standard_DS2_v2

# Get credentials
az aks get-credentials \
  --resource-group myResourceGroup \
  --name myAKSCluster

# Deploy application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Scale cluster
az aks scale \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 5
```

#### Azure Functions
Serverless compute service for event-driven applications.

```javascript
// index.js - HTTP Trigger Function
module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const name = (req.query.name || (req.body && req.body.name));
    const responseMessage = name
        ? "Hello, " + name + ". This HTTP triggered function executed successfully."
        : "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.";

    context.res = {
        body: responseMessage
    };
}
```

```json
// function.json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

```bash
# Deploy function
func azure functionapp publish myFunctionApp

# Create Function App
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 16 \
  --functions-version 4 \
  --name myFunctionApp \
  --storage-account mystorageaccount
```

#### App Service
Fully managed platform for building web apps.

```bash
# Create App Service plan
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B2 \
  --is-linux

# Create web app
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name mywebapp \
  --runtime "NODE|16-lts"

# Deploy code
az webapp deployment source config-zip \
  --resource-group myResourceGroup \
  --name mywebapp \
  --src app.zip

# Configure app settings
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name mywebapp \
  --settings NODE_ENV=production DATABASE_URL=$DATABASE_URL
```

### Storage Services

#### Blob Storage
Object storage solution for unstructured data.

```python
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Initialize client
connection_string = "DefaultEndpointsProtocol=https;AccountName=..."
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create container
container_name = "mycontainer"
container_client = blob_service_client.create_container(container_name)

# Upload blob
blob_client = blob_service_client.get_blob_client(
    container=container_name, 
    blob="myblob.txt"
)

with open("./data.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# List blobs
container_client = blob_service_client.get_container_client(container_name)
blob_list = container_client.list_blobs()
for blob in blob_list:
    print(blob.name)

# Download blob
with open("./downloaded.txt", "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())
```

```bash
# CLI commands
# Create storage account
az storage account create \
  --name mystorageaccount \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Create container
az storage container create \
  --name mycontainer \
  --account-name mystorageaccount \
  --public-access blob

# Upload file
az storage blob upload \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myblob \
  --file /path/to/file

# Set lifecycle policy
az storage account management-policy create \
  --account-name mystorageaccount \
  --policy @policy.json \
  --resource-group myResourceGroup
```

#### Azure SQL Database
Fully managed relational database service.

```sql
-- Create database
CREATE DATABASE SalesDB
COLLATE SQL_Latin1_General_CP1_CI_AS;

-- Create table
CREATE TABLE Customers (
    CustomerID int IDENTITY(1,1) PRIMARY KEY,
    FirstName nvarchar(50) NOT NULL,
    LastName nvarchar(50) NOT NULL,
    Email nvarchar(100) UNIQUE,
    CreatedDate datetime2 DEFAULT GETDATE()
);

-- Enable Temporal Table (System-Versioned)
ALTER TABLE Customers
ADD 
    ValidFrom datetime2 GENERATED ALWAYS AS ROW START DEFAULT GETDATE(),
    ValidTo datetime2 GENERATED ALWAYS AS ROW END DEFAULT CONVERT(datetime2, '9999-12-31 23:59:59.9999999'),
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo);

ALTER TABLE Customers
SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.CustomersHistory));
```

```python
# Python connection
import pyodbc

server = 'tcp:myserver.database.windows.net,1433'
database = 'SalesDB'
username = 'sqladmin'
password = 'YourPassword'
driver = '{ODBC Driver 17 for SQL Server}'

# Connection string
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect and query
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 10 * FROM Customers")
    for row in cursor:
        print(f"{row.CustomerID}: {row.FirstName} {row.LastName}")
```

#### Cosmos DB
Globally distributed, multi-model database service.

```javascript
// Node.js SDK
const { CosmosClient } = require("@azure/cosmos");

const endpoint = "https://myaccount.documents.azure.com:443/";
const key = "your-account-key";
const client = new CosmosClient({ endpoint, key });

async function createDatabase() {
    const { database } = await client.databases.createIfNotExists({ id: "ToDoList" });
    console.log(`Created database: ${database.id}`);
    
    const { container } = await database.containers.createIfNotExists({
        id: "Items",
        partitionKey: { paths: ["/category"] },
        throughput: 400
    });
    console.log(`Created container: ${container.id}`);
    
    // Create item
    const newItem = {
        id: "1",
        category: "personal",
        name: "Groceries",
        description: "Pick up apples and strawberries",
        isComplete: false
    };
    
    const { resource: createdItem } = await container.items.create(newItem);
    console.log(`Created item with id: ${createdItem.id}`);
    
    // Query items
    const querySpec = {
        query: "SELECT * FROM c WHERE c.category = @category",
        parameters: [{ name: "@category", value: "personal" }]
    };
    
    const { resources: items } = await container.items
        .query(querySpec)
        .fetchAll();
    
    items.forEach(item => {
        console.log(`${item.id}: ${item.name}`);
    });
}
```

### Networking

#### Virtual Network (VNet)
Isolated network infrastructure in Azure.

```bash
# Create VNet
az network vnet create \
  --resource-group myResourceGroup \
  --name myVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name mySubnet \
  --subnet-prefix 10.0.1.0/24

# Create NSG
az network nsg create \
  --resource-group myResourceGroup \
  --name myNSG

# Create NSG rule
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name myNSG \
  --name Allow-SSH \
  --priority 1000 \
  --source-address-prefixes '*' \
  --destination-port-ranges 22 \
  --protocol Tcp \
  --access Allow

# Create VNet peering
az network vnet peering create \
  --resource-group myResourceGroup \
  --name myVNet1-to-myVNet2 \
  --vnet-name myVNet1 \
  --remote-vnet myVNet2 \
  --allow-vnet-access
```

#### Application Gateway
Layer 7 load balancer with WAF capabilities.

```bash
# Create Application Gateway
az network application-gateway create \
  --name myAppGateway \
  --location eastus \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --subnet myAGSubnet \
  --capacity 2 \
  --sku Standard_v2 \
  --http-settings-cookie-based-affinity Disabled \
  --frontend-port 80 \
  --http-settings-port 80 \
  --http-settings-protocol Http \
  --public-ip-address myAGPublicIPAddress \
  --servers 10.0.1.4 10.0.1.5

# Enable WAF
az network application-gateway waf-config set \
  --enabled true \
  --gateway-name myAppGateway \
  --resource-group myResourceGroup \
  --firewall-mode Prevention \
  --rule-set-version 3.0
```

## Infrastructure as Code

### Terraform Example

```hcl
# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = var.location
  
  tags = {
    environment = var.environment
    project     = var.project
  }
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Subnet
resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.prefix}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-aks"

  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size            = "Standard_DS2_v2"
    type               = "VirtualMachineScaleSets"
    availability_zones = ["1", "2", "3"]
    enable_auto_scaling = true
    min_count          = 1
    max_count          = 5
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "calico"
    load_balancer_sku = "standard"
  }

  addon_profile {
    azure_policy {
      enabled = true
    }
    oms_agent {
      enabled                    = true
      log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
    }
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${var.prefix}-law"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "${var.prefix}-appinsights"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
}

# Cosmos DB Account
resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmos"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  geo_location {
    location          = var.failover_location
    failover_priority = 1
  }

  enable_automatic_failover = true
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "${lower(replace(var.prefix, "-", ""))}store"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  
  blob_properties {
    versioning_enabled = true
    
    delete_retention_policy {
      days = 7
    }
    
    container_delete_retention_policy {
      days = 7
    }
  }
}
```

### ARM Template Example

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "webAppName": {
      "type": "string",
      "defaultValue": "[concat('webApp-', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Web app name."
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "Location for all resources."
      }
    },
    "sku": {
      "type": "string",
      "defaultValue": "S1",
      "metadata": {
        "description": "The SKU of App Service Plan."
      }
    }
  },
  "variables": {
    "appServicePlanPortalName": "[concat('AppServicePlan-', parameters('webAppName'))]"
  },
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2020-12-01",
      "name": "[variables('appServicePlanPortalName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "[parameters('sku')]"
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2020-12-01",
      "name": "[parameters('webAppName')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanPortalName'))]"
      ],
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanPortalName'))]",
        "siteConfig": {
          "appSettings": [
            {
              "name": "WEBSITE_NODE_DEFAULT_VERSION",
              "value": "14.16.0"
            }
          ],
          "ftpsState": "FtpsOnly",
          "minTlsVersion": "1.2"
        },
        "httpsOnly": true
      }
    },
    {
      "type": "Microsoft.Insights/components",
      "apiVersion": "2020-02-02",
      "name": "[parameters('webAppName')]",
      "location": "[parameters('location')]",
      "kind": "web",
      "properties": {
        "Application_Type": "web",
        "Request_Source": "rest"
      }
    }
  ],
  "outputs": {
    "webAppUrl": {
      "type": "string",
      "value": "[concat('https://', reference(resourceId('Microsoft.Web/sites', parameters('webAppName'))).hostNames[0])]"
    }
  }
}
```

### Bicep Example

```bicep
// main.bicep
@description('The name of the web app')
param webAppName string = 'webApp-${uniqueString(resourceGroup().id)}'

@description('The location for all resources')
param location string = resourceGroup().location

@description('The SKU of App Service Plan')
@allowed([
  'F1'
  'B1'
  'S1'
  'P1v2'
])
param sku string = 'S1'

var appServicePlanName = 'AppServicePlan-${webAppName}'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: sku
  }
  properties: {
    reserved: true // Linux
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|14-lts'
      appSettings: [
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '14.16.0'
        }
      ]
      ftpsState: 'FtpsOnly'
      minTlsVersion: '1.2'
    }
    httpsOnly: true
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: webAppName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Request_Source: 'rest'
  }
}

// Outputs
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output appInsightsKey string = appInsights.properties.InstrumentationKey
```

## Best Practices

### Cost Optimization

1. **Azure Advisor Recommendations**
   ```bash
   # Get cost recommendations
   az advisor recommendation list \
     --category Cost \
     --query "[?impactedField=='Microsoft.Compute/virtualMachines']"
   ```

2. **Reserved Instances**
   - 1 or 3-year commitments
   - Up to 72% savings
   - Exchange and cancellation options

3. **Spot VMs**
   ```bash
   # Create Spot VM
   az vm create \
     --resource-group myResourceGroup \
     --name mySpotVM \
     --image UbuntuLTS \
     --priority Spot \
     --max-price 0.05 \
     --eviction-policy Deallocate
   ```

4. **Auto-shutdown for Dev/Test**
   ```bash
   # Configure auto-shutdown
   az vm auto-shutdown \
     --resource-group myResourceGroup \
     --name myVM \
     --time 1800 \
     --timezone "Pacific Standard Time"
   ```

5. **Cost Management + Billing**
   ```python
   from azure.mgmt.costmanagement import CostManagementClient
   from datetime import datetime, timedelta

   # Create budget
   budget = {
       "properties": {
           "category": "Cost",
           "amount": 100.0,
           "timeGrain": "Monthly",
           "timePeriod": {
               "startDate": datetime.utcnow().isoformat(),
               "endDate": (datetime.utcnow() + timedelta(days=365)).isoformat()
           },
           "notifications": {
               "Actual_GreaterThan_80_Percent": {
                   "enabled": True,
                   "operator": "GreaterThan",
                   "threshold": 80,
                   "contactEmails": ["admin@example.com"]
               }
           }
       }
   }
   ```

### Security Best Practices

1. **Azure Active Directory Integration**
   ```bash
   # Enable AAD authentication for AKS
   az aks update \
     --resource-group myResourceGroup \
     --name myAKSCluster \
     --enable-aad \
     --aad-admin-group-object-ids <group-id>

   # Managed Identity for resources
   az vm identity assign \
     --resource-group myResourceGroup \
     --name myVM
   ```

2. **Network Security**
   ```bash
   # Create Private Endpoint
   az network private-endpoint create \
     --name myPrivateEndpoint \
     --resource-group myResourceGroup \
     --vnet-name myVNet \
     --subnet mySubnet \
     --private-connection-resource-id $(az storage account show -g myResourceGroup -n mystorageaccount --query id -o tsv) \
     --connection-name myConnection \
     --group-id blob

   # Enable DDoS Protection
   az network ddos-protection create \
     --resource-group myResourceGroup \
     --name myDdosProtectionPlan
   ```

3. **Azure Key Vault**
   ```python
   from azure.identity import DefaultAzureCredential
   from azure.keyvault.secrets import SecretClient

   credential = DefaultAzureCredential()
   vault_url = "https://myvault.vault.azure.net/"
   client = SecretClient(vault_url=vault_url, credential=credential)

   # Store secret
   secret = client.set_secret("database-password", "StrongPassword123!")

   # Retrieve secret
   retrieved_secret = client.get_secret("database-password")
   print(f"Secret value: {retrieved_secret.value}")

   # Key Vault references in App Service
   # @Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/database-password/)
   ```

4. **Azure Policy**
   ```json
   {
     "properties": {
       "displayName": "Require tag on resources",
       "policyType": "Custom",
       "mode": "Indexed",
       "parameters": {
         "tagName": {
           "type": "String",
           "metadata": {
             "displayName": "Tag Name",
             "description": "Name of the tag, such as 'environment'"
           }
         }
       },
       "policyRule": {
         "if": {
           "field": "[concat('tags[', parameters('tagName'), ']')]",
           "exists": "false"
         },
         "then": {
           "effect": "deny"
         }
       }
     }
   }
   ```

5. **Azure Security Center**
   ```bash
   # Enable Security Center
   az security pricing create \
     --name VirtualMachines \
     --tier Standard

   # Get security recommendations
   az security assessment list \
     --query "[?properties.status.code=='Unhealthy']"
   ```

## Common Architectures

### 1. Multi-Tier Web Application

```yaml
# Architecture Components:
# - Azure Front Door (Global load balancing)
# - App Service (Web tier)
# - API Management (API tier)
# - Azure SQL Database (Data tier)
# - Redis Cache (Caching layer)

# Bicep template
param location string = resourceGroup().location
param prefix string = 'webapp'

// Front Door
resource frontDoor 'Microsoft.Network/frontDoors@2021-06-01' = {
  name: '${prefix}-fd'
  location: 'global'
  properties: {
    enabledState: 'Enabled'
    frontendEndpoints: [
      {
        name: 'frontend'
        properties: {
          hostName: '${prefix}-fd.azurefd.net'
        }
      }
    ]
    loadBalancingSettings: [
      {
        name: 'loadBalancing'
        properties: {
          sampleSize: 4
          successfulSamplesRequired: 2
        }
      }
    ]
    backendPools: [
      {
        name: 'backend'
        properties: {
          backends: [
            {
              address: webApp.properties.defaultHostName
              backendHostHeader: webApp.properties.defaultHostName
              httpPort: 80
              httpsPort: 443
              priority: 1
              weight: 50
            }
          ]
        }
      }
    ]
  }
}

// App Service
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: '${prefix}-asp'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
  }
  properties: {
    zoneRedundant: true
  }
}

resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: '${prefix}-app'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      alwaysOn: true
      http20Enabled: true
      minTlsVersion: '1.2'
    }
  }
}
```

### 2. Microservices on AKS

```yaml
# kubernetes/deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: microservices
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: microservices
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: myacr.azurecr.io/frontend:v1.0
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_URL
          value: "http://backend-service:8080"
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: microservices
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: frontend
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: microservices
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

```bash
# Setup service mesh with Istio
# Install Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y

# Enable sidecar injection
kubectl label namespace microservices istio-injection=enabled

# Deploy application
kubectl apply -f kubernetes/
```

### 3. Event-Driven Architecture

```python
# Function App - Event processor
import logging
import json
import azure.functions as func
from azure.servicebus import ServiceBusClient
from azure.cosmos import CosmosClient

def main(msg: func.ServiceBusMessage):
    logging.info('Processing ServiceBus message: %s',
                 msg.get_body().decode('utf-8'))
    
    # Parse message
    message_body = json.loads(msg.get_body().decode('utf-8'))
    
    # Process based on event type
    if message_body['eventType'] == 'OrderCreated':
        process_order(message_body)
    elif message_body['eventType'] == 'PaymentReceived':
        process_payment(message_body)
    
def process_order(order_data):
    # Connect to Cosmos DB
    client = CosmosClient(
        url=os.environ['COSMOS_ENDPOINT'],
        credential=os.environ['COSMOS_KEY']
    )
    
    database = client.get_database_client('Orders')
    container = database.get_container_client('OrderItems')
    
    # Store order
    container.create_item(body=order_data)
    
    # Send to next queue
    send_to_queue('payment-queue', {
        'orderId': order_data['orderId'],
        'amount': order_data['totalAmount'],
        'customerId': order_data['customerId']
    })

def send_to_queue(queue_name, message):
    client = ServiceBusClient.from_connection_string(
        os.environ['SERVICE_BUS_CONNECTION']
    )
    
    with client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            message = ServiceBusMessage(json.dumps(message))
            sender.send_messages(message)
```

```json
// function.json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "msg",
      "type": "serviceBusTrigger",
      "direction": "in",
      "queueName": "order-queue",
      "connection": "ServiceBusConnection"
    }
  ]
}
```

### 4. Data Analytics Platform

```python
# Azure Databricks - ETL Pipeline
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta import *

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DataPipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read from Event Hub
df = spark.readStream \
    .format("eventhubs") \
    .options(**ehConf) \
    .load()

# Parse JSON data
parsed_df = df.select(
    col("body").cast("string").alias("data"),
    col("enqueuedTime").alias("timestamp")
).select(
    from_json("data", schema).alias("event"),
    "timestamp"
)

# Transform data
transformed_df = parsed_df.select(
    col("event.userId"),
    col("event.productId"),
    col("event.quantity"),
    col("event.price"),
    col("timestamp"),
    (col("event.quantity") * col("event.price")).alias("total_amount")
)

# Write to Delta Lake
transformed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/delta/checkpoints/sales") \
    .trigger(processingTime="10 seconds") \
    .table("sales_data")

# Create aggregated view
sales_summary = spark.sql("""
    SELECT 
        date_trunc('hour', timestamp) as hour,
        productId,
        SUM(quantity) as total_quantity,
        SUM(total_amount) as revenue,
        COUNT(DISTINCT userId) as unique_customers
    FROM sales_data
    GROUP BY hour, productId
""")

# Write to Synapse for reporting
sales_summary.write \
    .format("com.databricks.spark.sqldw") \
    .option("url", synapse_jdbc_url) \
    .option("tempDir", temp_dir) \
    .option("forwardSparkAzureStorageCredentials", "true") \
    .option("dbTable", "sales_summary") \
    .mode("overwrite") \
    .save()
```

## Monitoring and Management

### Azure Monitor

```python
# Custom metrics
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import metrics

# Configure Azure Monitor
configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

# Create meter
meter = metrics.get_meter(__name__)

# Create counter
order_counter = meter.create_counter(
    name="orders_processed",
    description="Number of orders processed",
    unit="1"
)

# Create histogram
response_time = meter.create_histogram(
    name="response_time",
    description="Response time in milliseconds",
    unit="ms"
)

# Use in application
def process_order(order):
    start_time = time.time()
    
    # Process order logic
    # ...
    
    # Record metrics
    order_counter.add(1, {"status": "success", "region": "eastus"})
    response_time.record((time.time() - start_time) * 1000)
```

### Log Analytics Queries

```kusto
// Top 10 slowest requests
requests
| where timestamp > ago(1h)
| summarize avg_duration = avg(duration), count = count() by name
| top 10 by avg_duration desc

// Failed requests by result code
requests
| where timestamp > ago(24h)
| where success == false
| summarize count() by resultCode, bin(timestamp, 1h)
| render timechart

// Container CPU usage
ContainerInventory
| where TimeGenerated > ago(30m)
| where Name contains "myapp"
| summarize avg_cpu = avg(CPUUsageMillicores) by Name, bin(TimeGenerated, 5m)
| render timechart
```

### Azure Automation

```powershell
# Runbook to start/stop VMs
param(
    [Parameter(Mandatory=$true)]
    [String]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("Start","Stop")]
    [String]$Action
)

# Authenticate
$connection = Get-AutomationConnection -Name AzureRunAsConnection
Connect-AzAccount -ServicePrincipal `
    -Tenant $connection.TenantID `
    -ApplicationId $connection.ApplicationID `
    -CertificateThumbprint $connection.CertificateThumbprint

# Get all VMs in resource group
$vms = Get-AzVM -ResourceGroupName $ResourceGroupName

foreach ($vm in $vms) {
    if ($Action -eq "Start") {
        Write-Output "Starting VM: $($vm.Name)"
        Start-AzVM -ResourceGroupName $ResourceGroupName -Name $vm.Name -NoWait
    }
    else {
        Write-Output "Stopping VM: $($vm.Name)"
        Stop-AzVM -ResourceGroupName $ResourceGroupName -Name $vm.Name -Force -NoWait
    }
}
```

## Interview Preparation

### Common Azure Interview Questions

1. **What is the difference between Azure Resource Manager (ARM) and Classic deployment?**
   - ARM provides resource grouping, RBAC, tags, templates
   - Classic is legacy, limited features, being deprecated

2. **Explain Azure availability zones and sets**
   - Availability Sets: Protect from hardware failures within a datacenter
   - Availability Zones: Protect from datacenter failures

3. **How does Azure Traffic Manager work?**
   - DNS-based traffic load balancer
   - Routes based on: Priority, Weighted, Performance, Geographic
   - Health probes for endpoint monitoring

4. **What are the different redundancy options in Azure Storage?**
   - LRS: 3 copies in single region
   - ZRS: 3 copies across availability zones
   - GRS: 6 copies (3 primary, 3 secondary region)
   - RA-GRS: GRS with read access to secondary

5. **Explain Azure Service Bus vs Event Hub**
   - Service Bus: Enterprise messaging, FIFO, transactions
   - Event Hub: Big data streaming, millions of events/sec

### Hands-On Scenarios

1. **Design a highly available web application**
   - Use Traffic Manager for global routing
   - Deploy to multiple regions
   - Use Application Gateway with WAF
   - Implement auto-scaling

2. **Implement a disaster recovery solution**
   - Use Azure Site Recovery
   - Geo-redundant storage
   - Automated failover procedures
   - Regular DR testing

3. **Build a secure API platform**
   - API Management for gateway
   - OAuth 2.0/OpenID Connect
   - Rate limiting and quotas
   - Backend pool health monitoring

### Architecture Design Questions

**Q: Design a global e-commerce platform on Azure**

```
Architecture:
1. Azure Front Door (Global LB, CDN, WAF)
2. Regional deployments:
   - App Service (Web tier)
   - AKS (Microservices)
   - Cosmos DB (Multi-region)
   - Redis Cache
3. Event-driven processing:
   - Event Hub (Ingestion)
   - Functions (Processing)
   - Service Bus (Messaging)
4. Analytics:
   - Synapse Analytics
   - Power BI
   
Considerations:
- Multi-region active-active
- Cosmos DB global distribution
- CDN for static content
- Auto-scaling based on traffic
```

## Resources

### Official Documentation
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure Architecture Center](https://docs.microsoft.com/azure/architecture/)
- [Azure Well-Architected Framework](https://docs.microsoft.com/azure/architecture/framework/)
- [Azure Best Practices](https://docs.microsoft.com/azure/cloud-adoption-framework/)

### Learning Resources
- [Microsoft Learn](https://docs.microsoft.com/learn/)
- [Azure Free Account](https://azure.microsoft.com/free/)
- [Azure Certifications](https://docs.microsoft.com/learn/certifications/)
- [Cloud Skills Challenge](https://www.microsoft.com/cloudskillschallenge)

### Tools and SDKs
- [Azure CLI](https://docs.microsoft.com/cli/azure/)
- [Azure PowerShell](https://docs.microsoft.com/powershell/azure/)
- [Azure Cloud Shell](https://shell.azure.com/)
- [Visual Studio Code Azure Extensions](https://code.visualstudio.com/docs/azure/extensions)

### Community Resources
- [Azure Updates](https://azure.microsoft.com/updates/)
- [Azure Blog](https://azure.microsoft.com/blog/)
- [Tech Community](https://techcommunity.microsoft.com/t5/azure/ct-p/Azure)
- [Stack Overflow - azure](https://stackoverflow.com/questions/tagged/azure)

### Sample Architectures
- [Azure Reference Architectures](https://docs.microsoft.com/azure/architecture/reference-architectures/)
- [Azure Solution Ideas](https://docs.microsoft.com/azure/architecture/solution-ideas/)
- [Azure Quickstart Templates](https://azure.microsoft.com/resources/templates/)

### Cost Management
- [Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Azure Cost Management](https://azure.microsoft.com/services/cost-management/)
- [Total Cost of Ownership Calculator](https://azure.microsoft.com/pricing/tco/calculator/)

### Migration Resources
- [Azure Migrate](https://azure.microsoft.com/services/azure-migrate/)
- [Cloud Adoption Framework](https://docs.microsoft.com/azure/cloud-adoption-framework/)
- [Migration Guide](https://docs.microsoft.com/azure/cloud-adoption-framework/migrate/)

### Security Resources
- [Azure Security Center](https://docs.microsoft.com/azure/security-center/)
- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/fundamentals/best-practices-and-patterns)
- [Azure Security Benchmark](https://docs.microsoft.com/azure/security/benchmarks/overview)

### YouTube Channels
- [Microsoft Azure](https://www.youtube.com/c/MicrosoftAzure)
- [Azure Academy](https://www.youtube.com/c/AzureAcademy)
- [John Savill's Technical Training](https://www.youtube.com/c/NTFAQGuy)