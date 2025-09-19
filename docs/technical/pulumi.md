# Pulumi - Infrastructure as Code Using General Programming Languages

## Overview

Pulumi is a modern Infrastructure as Code (IaC) platform that enables developers to use familiar programming languages to define, deploy, and manage cloud infrastructure. Unlike traditional declarative IaC tools, Pulumi leverages the full power of general-purpose programming languages.

## Architecture

### Core Components

1. **Pulumi Engine**
   - State management and resource graph
   - Provider plugin system
   - Deployment orchestration
   - Policy enforcement engine

2. **Language SDKs**
   - TypeScript/JavaScript SDK
   - Python SDK
   - Go SDK
   - .NET SDK
   - Java SDK
   - YAML support

3. **Provider Ecosystem**
   - Cloud providers (AWS, Azure, GCP, etc.)
   - Kubernetes providers
   - Database providers
   - SaaS integrations

4. **State Management**
   - Backend options (local, S3, Azure Blob, Pulumi Service)
   - Concurrent state locking
   - State encryption
   - Import/export capabilities

## Language Support

### TypeScript/JavaScript
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create VPC with typed configuration
const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: "pulumi-vpc",
        Environment: pulumi.getStack(),
    },
});

// Create subnets with loops
const azs = aws.getAvailabilityZones({ state: "available" });
const publicSubnets = azs.then(azs => {
    return azs.names.slice(0, 2).map((az, index) => {
        return new aws.ec2.Subnet(`public-${index}`, {
            vpcId: vpc.id,
            cidrBlock: `10.0.${index}.0/24`,
            availabilityZone: az,
            mapPublicIpOnLaunch: true,
            tags: {
                Name: `public-subnet-${index}`,
                Type: "public",
            },
        });
    });
});
```

### Python
```python
import pulumi
import pulumi_aws as aws
from typing import List

# Configuration class for type safety
class VpcConfig:
    def __init__(self, cidr_block: str, az_count: int = 2):
        self.cidr_block = cidr_block
        self.az_count = az_count

# Component resource for reusable infrastructure
class NetworkStack(pulumi.ComponentResource):
    def __init__(self, name: str, config: VpcConfig, opts=None):
        super().__init__('custom:network:Stack', name, None, opts)
        
        # Create VPC
        self.vpc = aws.ec2.Vpc(f"{name}-vpc",
            cidr_block=config.cidr_block,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={
                "Name": f"{name}-vpc",
                "ManagedBy": "Pulumi"
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Get availability zones
        azs = aws.get_availability_zones(state="available")
        
        # Create subnets
        self.public_subnets: List[aws.ec2.Subnet] = []
        self.private_subnets: List[aws.ec2.Subnet] = []
        
        for i in range(min(config.az_count, len(azs.names))):
            # Public subnet
            public_subnet = aws.ec2.Subnet(f"{name}-public-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i}.0/24",
                availability_zone=azs.names[i],
                map_public_ip_on_launch=True,
                tags={"Name": f"{name}-public-{i}", "Type": "public"},
                opts=pulumi.ResourceOptions(parent=self)
            )
            self.public_subnets.append(public_subnet)
            
            # Private subnet
            private_subnet = aws.ec2.Subnet(f"{name}-private-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i+100}.0/24",
                availability_zone=azs.names[i],
                tags={"Name": f"{name}-private-{i}", "Type": "private"},
                opts=pulumi.ResourceOptions(parent=self)
            )
            self.private_subnets.append(private_subnet)

# Usage
config = VpcConfig("10.0.0.0/16", az_count=3)
network = NetworkStack("production", config)

# Export outputs
pulumi.export("vpc_id", network.vpc.id)
pulumi.export("public_subnet_ids", [s.id for s in network.public_subnets])
```

### Go
```go
package main

import (
    "fmt"
    "github.com/pulumi/pulumi-aws/sdk/v5/go/aws/ec2"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type NetworkConfig struct {
    VpcCidr    string
    SubnetBits int
    AzCount    int
}

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        config := NetworkConfig{
            VpcCidr:    "10.0.0.0/16",
            SubnetBits: 8,
            AzCount:    2,
        }

        // Create VPC
        vpc, err := ec2.NewVpc(ctx, "main", &ec2.VpcArgs{
            CidrBlock:          pulumi.String(config.VpcCidr),
            EnableDnsHostnames: pulumi.Bool(true),
            EnableDnsSupport:   pulumi.Bool(true),
            Tags: pulumi.StringMap{
                "Name":        pulumi.String("pulumi-vpc"),
                "Environment": pulumi.String(ctx.Stack()),
            },
        })
        if err != nil {
            return err
        }

        // Get AZs
        azs, err := aws.GetAvailabilityZones(ctx, &aws.GetAvailabilityZonesArgs{
            State: pulumi.StringRef("available"),
        })
        if err != nil {
            return err
        }

        // Create subnets
        var publicSubnets []*ec2.Subnet
        var privateSubnets []*ec2.Subnet

        for i := 0; i < config.AzCount && i < len(azs.Names); i++ {
            // Public subnet
            publicSubnet, err := ec2.NewSubnet(ctx, fmt.Sprintf("public-%d", i), &ec2.SubnetArgs{
                VpcId:               vpc.ID(),
                CidrBlock:           pulumi.String(fmt.Sprintf("10.0.%d.0/24", i)),
                AvailabilityZone:    pulumi.String(azs.Names[i]),
                MapPublicIpOnLaunch: pulumi.Bool(true),
                Tags: pulumi.StringMap{
                    "Name": pulumi.String(fmt.Sprintf("public-subnet-%d", i)),
                    "Type": pulumi.String("public"),
                },
            })
            if err != nil {
                return err
            }
            publicSubnets = append(publicSubnets, publicSubnet)

            // Private subnet
            privateSubnet, err := ec2.NewSubnet(ctx, fmt.Sprintf("private-%d", i), &ec2.SubnetArgs{
                VpcId:            vpc.ID(),
                CidrBlock:        pulumi.String(fmt.Sprintf("10.0.%d.0/24", i+100)),
                AvailabilityZone: pulumi.String(azs.Names[i]),
                Tags: pulumi.StringMap{
                    "Name": pulumi.String(fmt.Sprintf("private-subnet-%d", i)),
                    "Type": pulumi.String("private"),
                },
            })
            if err != nil {
                return err
            }
            privateSubnets = append(privateSubnets, privateSubnet)
        }

        // Export outputs
        ctx.Export("vpcId", vpc.ID())
        ctx.Export("publicSubnetCount", pulumi.Int(len(publicSubnets)))
        ctx.Export("privateSubnetCount", pulumi.Int(len(privateSubnets)))

        return nil
    })
}
```

## Practical Examples

### Multi-Cloud Kubernetes Deployment
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as azure from "@pulumi/azure-native";
import * as k8s from "@pulumi/kubernetes";

// AWS EKS Cluster
const eksCluster = new aws.eks.Cluster("production", {
    desiredCapacity: 3,
    minSize: 2,
    maxSize: 5,
    instanceType: "t3.medium",
});

// Azure AKS Cluster
const aksCluster = new azure.containerservice.ManagedCluster("production", {
    resourceGroupName: resourceGroup.name,
    agentPoolProfiles: [{
        name: "agentpool",
        count: 3,
        vmSize: "Standard_DS2_v2",
        mode: "System",
    }],
    dnsPrefix: "aks-prod",
    kubernetesVersion: "1.27.1",
});

// Deploy application to both clusters
[eksCluster, aksCluster].forEach((cluster, index) => {
    const provider = new k8s.Provider(`k8s-provider-${index}`, {
        kubeconfig: cluster.kubeconfig,
    });

    const app = new k8s.apps.v1.Deployment(`app-${index}`, {
        metadata: {
            name: "multi-cloud-app",
        },
        spec: {
            replicas: 3,
            selector: {
                matchLabels: { app: "multi-cloud" },
            },
            template: {
                metadata: {
                    labels: { app: "multi-cloud" },
                },
                spec: {
                    containers: [{
                        name: "app",
                        image: "nginx:latest",
                        ports: [{ containerPort: 80 }],
                    }],
                },
            },
        },
    }, { provider });
});
```

### Dynamic Infrastructure with Loops
```python
import pulumi
import pulumi_aws as aws
from typing import Dict, List

# Configuration
config = pulumi.Config()
environments = config.require_object("environments")

# Create infrastructure for each environment
for env_name, env_config in environments.items():
    # VPC per environment
    vpc = aws.ec2.Vpc(f"{env_name}-vpc",
        cidr_block=env_config["vpc_cidr"],
        enable_dns_hostnames=True,
        tags={"Environment": env_name}
    )
    
    # Dynamic number of instances
    instances = []
    for i in range(env_config.get("instance_count", 1)):
        instance = aws.ec2.Instance(f"{env_name}-instance-{i}",
            instance_type=env_config.get("instance_type", "t3.micro"),
            ami=aws.ec2.get_ami(
                most_recent=True,
                owners=["amazon"],
                filters=[{
                    "name": "name",
                    "values": ["amzn2-ami-hvm-*-x86_64-gp2"],
                }]
            ).id,
            subnet_id=vpc.id.apply(lambda vpc_id: 
                aws.ec2.get_subnet(filters=[{
                    "name": "vpc-id",
                    "values": [vpc_id]
                }]).id
            ),
            tags={
                "Name": f"{env_name}-instance-{i}",
                "Environment": env_name,
            }
        )
        instances.append(instance)
    
    # Export instance IDs
    pulumi.export(f"{env_name}_instance_ids", [i.id for i in instances])
```

### Policy as Code Integration
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import { PolicyPack, validateResourceOfType } from "@pulumi/policy";

// Define policy pack
new PolicyPack("security-policies", {
    policies: [
        {
            name: "s3-bucket-encryption",
            description: "Ensure all S3 buckets have encryption enabled",
            enforcementLevel: "mandatory",
            validateResource: validateResourceOfType(aws.s3.Bucket, (bucket, args, reportViolation) => {
                if (!bucket.serverSideEncryptionConfiguration) {
                    reportViolation("S3 buckets must have encryption enabled");
                }
            }),
        },
        {
            name: "ec2-instance-size-limit",
            description: "Limit EC2 instance sizes",
            enforcementLevel: "advisory",
            validateResource: validateResourceOfType(aws.ec2.Instance, (instance, args, reportViolation) => {
                const allowedTypes = ["t3.micro", "t3.small", "t3.medium"];
                if (!allowedTypes.includes(instance.instanceType)) {
                    reportViolation(`Instance type ${instance.instanceType} not allowed. Use: ${allowedTypes.join(", ")}`);
                }
            }),
        },
    ],
});

// Infrastructure code with policy compliance
const bucket = new aws.s3.Bucket("secure-bucket", {
    serverSideEncryptionConfiguration: {
        rule: {
            applyServerSideEncryptionByDefault: {
                sseAlgorithm: "AES256",
            },
        },
    },
    versioningConfiguration: {
        status: "Enabled",
    },
});

const instance = new aws.ec2.Instance("web-server", {
    instanceType: "t3.small", // Complies with policy
    ami: "ami-12345678",
});
```

## Best Practices

### 1. Project Structure
```
pulumi-project/
├── Pulumi.yaml              # Project metadata
├── Pulumi.dev.yaml          # Dev stack configuration
├── Pulumi.prod.yaml         # Prod stack configuration
├── index.ts                 # Main entry point
├── src/
│   ├── components/          # Reusable components
│   │   ├── network.ts
│   │   ├── compute.ts
│   │   └── database.ts
│   ├── config/              # Configuration types
│   │   └── types.ts
│   └── utils/               # Helper functions
│       └── tags.ts
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
└── policies/               # Policy packs
    └── security.ts
```

### 2. Component Resources
```typescript
// Reusable component pattern
export class WebApplicationStack extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;
    public readonly database: aws.rds.Instance;

    constructor(name: string, args: WebApplicationArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:app:WebApplication", name, {}, opts);

        // Create ALB
        const alb = new aws.lb.LoadBalancer(`${name}-alb`, {
            loadBalancerType: "application",
            subnets: args.subnetIds,
            securityGroups: [args.securityGroupId],
        }, { parent: this });

        // Create RDS instance
        this.database = new aws.rds.Instance(`${name}-db`, {
            engine: "postgres",
            engineVersion: "14.7",
            instanceClass: args.dbInstanceClass || "db.t3.micro",
            allocatedStorage: args.dbStorage || 20,
            dbName: args.dbName,
            username: args.dbUsername,
            password: args.dbPassword,
            skipFinalSnapshot: true,
        }, { parent: this });

        // Create ECS service
        const service = new awsx.ecs.FargateService(`${name}-service`, {
            cluster: args.cluster.arn,
            taskDefinitionArgs: {
                container: {
                    image: args.dockerImage,
                    memory: 512,
                    environment: [{
                        name: "DATABASE_URL",
                        value: pulumi.interpolate`postgresql://${args.dbUsername}:${args.dbPassword}@${this.database.endpoint}/${args.dbName}`,
                    }],
                },
            },
            desiredCount: args.desiredCount || 2,
            loadBalancers: [{
                targetGroup: alb.defaultTargetGroup,
                containerName: "app",
                containerPort: 80,
            }],
        }, { parent: this });

        this.url = alb.dnsName;
        this.registerOutputs({
            url: this.url,
            databaseEndpoint: this.database.endpoint,
        });
    }
}
```

### 3. Configuration Management
```typescript
// Structured configuration
interface EnvironmentConfig {
    instanceType: aws.ec2.InstanceType;
    instanceCount: number;
    enableMonitoring: boolean;
    tags: Record<string, string>;
}

const config = new pulumi.Config();
const environment = config.require("environment");
const envConfigs: Record<string, EnvironmentConfig> = {
    development: {
        instanceType: "t3.micro",
        instanceCount: 1,
        enableMonitoring: false,
        tags: { Environment: "dev", CostCenter: "engineering" },
    },
    production: {
        instanceType: "t3.large",
        instanceCount: 3,
        enableMonitoring: true,
        tags: { Environment: "prod", CostCenter: "operations", Compliance: "pci" },
    },
};

const currentConfig = envConfigs[environment];
if (!currentConfig) {
    throw new Error(`Unknown environment: ${environment}`);
}
```

### 4. Testing Infrastructure
```typescript
import * as pulumi from "@pulumi/pulumi";
import "jest";

// Unit tests for infrastructure
describe("Infrastructure Tests", () => {
    let infra: typeof import("../index");

    beforeAll(() => {
        // Set up mock runtime
        pulumi.runtime.setMocks({
            newResource: (type, name, inputs) => {
                return {
                    id: `${name}_id`,
                    state: inputs,
                };
            },
            call: (token, args, provider) => {
                return args;
            },
        });

        infra = require("../index");
    });

    test("VPC has correct CIDR", async () => {
        const vpcCidr = await infra.vpc.cidrBlock.promise();
        expect(vpcCidr).toBe("10.0.0.0/16");
    });

    test("Instance count matches configuration", async () => {
        const instances = await infra.instances;
        expect(instances.length).toBe(3);
    });

    test("All resources have required tags", async () => {
        const vpc = await infra.vpc;
        const tags = await vpc.tags.promise();
        expect(tags).toHaveProperty("Environment");
        expect(tags).toHaveProperty("ManagedBy", "Pulumi");
    });
});
```

### 5. State Management
```typescript
// Remote state backend configuration
const stackReference = new pulumi.StackReference("organization/networking/prod");
const vpcId = stackReference.getOutput("vpcId");
const subnetIds = stackReference.getOutput("publicSubnetIds");

// State import example
const existingVpc = aws.ec2.Vpc.get("imported-vpc", "vpc-12345678");

// State encryption
export const secrets = {
    dbPassword: config.requireSecret("dbPassword"),
    apiKey: config.requireSecret("apiKey"),
};
```

## Integration Patterns

### 1. CI/CD Integration
```yaml
# GitHub Actions
name: Pulumi Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Preview changes
        if: github.event_name == 'pull_request'
        uses: pulumi/actions@v4
        with:
          command: preview
          stack-name: dev
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
      
      - name: Deploy infrastructure
        if: github.ref == 'refs/heads/main'
        uses: pulumi/actions@v4
        with:
          command: up
          stack-name: prod
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```

### 2. GitOps Integration
```typescript
// Flux GitOps integration
import * as k8s from "@pulumi/kubernetes";

const flux = new k8s.helm.v3.Chart("flux2", {
    repo: "https://fluxcd-community.github.io/helm-charts",
    chart: "flux2",
    version: "2.10.0",
    namespace: "flux-system",
    values: {
        gitRepository: {
            url: "https://github.com/org/infrastructure",
            branch: "main",
            interval: "1m",
        },
        kustomization: {
            path: "./clusters/production",
            prune: true,
            interval: "10m",
        },
    },
});

// Export GitOps sync status
export const gitOpsSyncStatus = flux.getResourceProperty(
    "v1/Service",
    "flux-system/webhook-receiver",
    "status"
);
```

### 3. Monitoring Integration
```python
import pulumi
import pulumi_datadog as datadog
import pulumi_aws as aws

# Create Datadog monitors for infrastructure
def create_monitors(resource_name: str, instance: aws.ec2.Instance):
    # CPU monitor
    cpu_monitor = datadog.Monitor(f"{resource_name}-cpu",
        name=f"{resource_name} CPU Usage",
        type="metric alert",
        query=f"avg(last_5m):avg:aws.ec2.cpu{{instance_id:{instance.id}}} > 90",
        message="CPU usage is too high on {{host.name}}",
        tags=["infrastructure:pulumi", f"instance:{resource_name}"],
        options=datadog.MonitorOptionsArgs(
            thresholds=datadog.MonitorOptionsThresholdsArgs(
                critical=90,
                warning=80,
            ),
            notify_no_data=True,
            no_data_timeframe=10,
        )
    )
    
    # Disk space monitor
    disk_monitor = datadog.Monitor(f"{resource_name}-disk",
        name=f"{resource_name} Disk Space",
        type="metric alert",
        query=f"avg(last_5m):avg:system.disk.used{{instance_id:{instance.id}}} / avg:system.disk.total{{instance_id:{instance.id}}} > 0.9",
        message="Disk space is running low on {{host.name}}",
        tags=["infrastructure:pulumi", f"instance:{resource_name}"],
    )
    
    return [cpu_monitor, disk_monitor]

# Apply monitoring to all instances
for instance in instances:
    monitors = create_monitors(instance._name, instance)
```

### 4. Secret Management
```typescript
// AWS Secrets Manager integration
const dbSecret = new aws.secretsmanager.Secret("db-credentials", {
    description: "Database credentials for production",
});

const dbSecretVersion = new aws.secretsmanager.SecretVersion("db-credentials-version", {
    secretId: dbSecret.id,
    secretString: JSON.stringify({
        username: "admin",
        password: config.requireSecret("dbPassword"),
        engine: "postgres",
        host: database.endpoint,
        port: 5432,
        dbname: "production",
    }),
});

// Use secrets in applications
const app = new aws.ecs.TaskDefinition("app-task", {
    family: "app",
    containerDefinitions: JSON.stringify([{
        name: "app",
        image: "myapp:latest",
        secrets: [{
            name: "DB_CONNECTION",
            valueFrom: dbSecret.arn,
        }],
    }]),
});
```

### 5. Cost Management
```python
import pulumi
from pulumi_aws import ec2, s3

# Cost tags applied to all resources
def apply_cost_tags(args):
    """Apply standard cost allocation tags"""
    base_tags = {
        "CostCenter": pulumi.get_project(),
        "Environment": pulumi.get_stack(),
        "ManagedBy": "Pulumi",
        "Owner": config.get("owner") or "platform-team",
    }
    return {**base_tags, **(args or {})}

# Transform to apply tags to all resources
pulumi.runtime.register_stack_transformation(
    lambda args:
        pulumi.ResourceTransformationResult(
            props=args.props | {"tags": apply_cost_tags(args.props.get("tags"))},
            opts=args.opts,
        )
        if "tags" in args.props else None
)

# Budget alerts
budget = aws.budgets.Budget("monthly-budget",
    budget_type="COST",
    time_unit="MONTHLY",
    limit_amount="1000",
    limit_unit="USD",
    notification=[{
        "comparison_operator": "GREATER_THAN",
        "threshold": 80,
        "threshold_type": "PERCENTAGE",
        "notification_type": "ACTUAL",
        "subscriber_email_addresses": ["platform-team@company.com"],
    }],
)
```

## Advanced Features

### 1. Dynamic Providers
```typescript
// Custom dynamic provider for external resources
const customProvider = {
    async create(inputs: any) {
        // Call external API to create resource
        const response = await fetch("https://api.external.com/resources", {
            method: "POST",
            body: JSON.stringify(inputs),
        });
        const data = await response.json();
        return { id: data.id, outs: data };
    },
    async update(id: string, olds: any, news: any) {
        // Update external resource
        const response = await fetch(`https://api.external.com/resources/${id}`, {
            method: "PUT",
            body: JSON.stringify(news),
        });
        const data = await response.json();
        return { outs: data };
    },
    async delete(id: string, props: any) {
        // Delete external resource
        await fetch(`https://api.external.com/resources/${id}`, {
            method: "DELETE",
        });
    },
};

const externalResource = new pulumi.dynamic.Resource("external", {
    configuration: {
        apiKey: config.requireSecret("externalApiKey"),
        region: "us-east-1",
    },
}, { provider: customProvider });
```

### 2. Stack Transformations
```typescript
// Global resource transformations
pulumi.runtime.registerStackTransformation((args) => {
    // Add naming convention
    if (args.name && !args.name.startsWith(pulumi.getProject())) {
        args.name = `${pulumi.getProject()}-${args.name}`;
    }

    // Add default tags
    if (args.type.startsWith("aws:") && args.props.tags) {
        args.props.tags = {
            ...args.props.tags,
            Project: pulumi.getProject(),
            Stack: pulumi.getStack(),
            PulumiManaged: "true",
        };
    }

    // Enforce encryption
    if (args.type === "aws:s3/bucket:Bucket") {
        args.props.serverSideEncryptionConfiguration = {
            rule: {
                applyServerSideEncryptionByDefault: {
                    sseAlgorithm: "AES256",
                },
            },
        };
    }

    return { props: args.props, opts: args.opts };
});
```

### 3. Resource Aliases
```typescript
// Handle resource renaming without recreation
const database = new aws.rds.Instance("prod-db", {
    // RDS configuration
}, {
    aliases: [{ name: "production-database" }], // Old name
    protect: true, // Prevent accidental deletion
});
```

### 4. Import Existing Resources
```typescript
// Import existing AWS resources
const existingBucket = new aws.s3.Bucket("existing", {
    bucket: "my-existing-bucket-name",
}, {
    import: "my-existing-bucket-name",
});

// Bulk import with automation
const existingInstances = await aws.ec2.getInstances({
    filters: [{
        name: "tag:ManagedBy",
        values: ["Terraform"], // Migrating from Terraform
    }],
});

existingInstances.ids.forEach((id, index) => {
    new aws.ec2.Instance(`imported-${index}`, {
        // Match existing instance configuration
    }, {
        import: id,
    });
});
```

## Troubleshooting

### Common Issues

1. **State Lock Conflicts**
```bash
# Force unlock (use with caution)
pulumi cancel --yes

# Check who has the lock
pulumi stack export | jq '.deployment.locks'
```

2. **Resource Creation Failures**
```typescript
// Add retries for flaky resources
const instance = new aws.ec2.Instance("web", {
    // configuration
}, {
    customTimeouts: {
        create: "10m",
        update: "10m",
        delete: "20m",
    },
    retryOnFailure: true,
});
```

3. **Dependency Issues**
```typescript
// Explicit dependencies
const securityGroup = new aws.ec2.SecurityGroup("web-sg", {
    vpcId: vpc.id,
});

const instance = new aws.ec2.Instance("web", {
    securityGroups: [securityGroup.id],
}, {
    dependsOn: [securityGroup, vpc], // Explicit ordering
});
```

### Debug Logging
```bash
# Verbose logging
export PULUMI_DEBUG=true
pulumi up --debug --logtostderr

# Log specific providers
export TF_LOG=DEBUG  # For Terraform-based providers

# Trace HTTP calls
export PULUMI_HTTP_DEBUG=true
```

## Conclusion

Pulumi represents a paradigm shift in Infrastructure as Code, bringing the full power of programming languages to infrastructure management. Its ability to use loops, conditionals, functions, and type safety makes it particularly powerful for complex, dynamic infrastructure scenarios.

Key advantages include:
- Familiar programming languages reduce learning curve
- Strong typing catches errors at compile time
- Reusable components promote DRY principles
- Rich ecosystem integrates with existing tools
- Policy as Code ensures compliance

Whether you're building cloud-native applications, managing hybrid cloud infrastructure, or migrating from other IaC tools, Pulumi provides the flexibility and power needed for modern infrastructure management.