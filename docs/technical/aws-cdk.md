# AWS CDK - AWS Cloud Development Kit

## Overview

The AWS Cloud Development Kit (CDK) is an open-source software development framework for defining cloud infrastructure using familiar programming languages. CDK synthesizes to CloudFormation templates but provides higher-level abstractions, reusable components, and the full power of programming languages for infrastructure definition.

## Architecture

### Core Components

1. **CDK Core Framework**
   - Construct library hierarchy (L1, L2, L3)
   - Synthesis engine
   - Asset management system
   - Context providers
   - Stack synthesis and deployment

2. **Language Bindings**
   - TypeScript/JavaScript (primary)
   - Python
   - Java
   - C#/.NET
   - Go

3. **Construct Levels**
   - **L1 (CFN Resources)**: Direct CloudFormation resource mappings
   - **L2 (Curated)**: Higher-level abstractions with sensible defaults
   - **L3 (Patterns)**: Complete architectures and solutions

4. **CDK Toolkit (CLI)**
   - Synthesis and deployment
   - Diff and change management
   - Bootstrap environment setup
   - Asset publishing

## Language Support

### TypeScript/JavaScript
```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';

export class ThreeTierWebAppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC with public/private subnets across 3 AZs
    const vpc = new ec2.Vpc(this, 'AppVPC', {
      maxAzs: 3,
      natGateways: 2,
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
          cidrMask: 24,
        },
        {
          name: 'Isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 24,
        },
      ],
    });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, 'AppCluster', {
      vpc,
      containerInsights: true,
    });

    // Aurora Serverless v2 Database
    const database = new rds.DatabaseCluster(this, 'Database', {
      engine: rds.DatabaseClusterEngine.auroraMysql({
        version: rds.AuroraMysqlEngineVersion.VER_3_02_0,
      }),
      serverlessV2ScalingConfiguration: {
        minCapacity: rds.AuroraCapacityUnit.ACU_1,
        maxCapacity: rds.AuroraCapacityUnit.ACU_4,
      },
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      defaultDatabaseName: 'webapp',
      enableDataApi: true,
    });

    // ElastiCache Redis Cluster
    const cacheSubnetGroup = new elasticache.CfnSubnetGroup(this, 'CacheSubnetGroup', {
      description: 'Subnet group for ElastiCache',
      subnetIds: vpc.selectSubnets({
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      }).subnetIds,
    });

    const cacheSecurityGroup = new ec2.SecurityGroup(this, 'CacheSecurityGroup', {
      vpc,
      description: 'Security group for ElastiCache',
    });

    const cache = new elasticache.CfnReplicationGroup(this, 'CacheCluster', {
      replicationGroupDescription: 'Redis cache cluster',
      engine: 'redis',
      cacheNodeType: 'cache.r6g.large',
      numNodeGroups: 1,
      replicasPerNodeGroup: 1,
      automaticFailoverEnabled: true,
      multiAzEnabled: true,
      cacheSubnetGroupName: cacheSubnetGroup.ref,
      securityGroupIds: [cacheSecurityGroup.securityGroupId],
      atRestEncryptionEnabled: true,
      transitEncryptionEnabled: true,
    });

    // Application Load Balanced Fargate Service
    const webService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'WebService', {
      cluster,
      cpu: 512,
      memoryLimitMiB: 1024,
      desiredCount: 3,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry('nginx:latest'),
        environment: {
          DATABASE_HOST: database.clusterEndpoint.hostname,
          DATABASE_NAME: 'webapp',
          CACHE_ENDPOINT: cache.attrPrimaryEndPointAddress,
          CACHE_PORT: cache.attrPrimaryEndPointPort,
        },
        secrets: {
          DATABASE_PASSWORD: ecs.Secret.fromSecretsManager(database.secret!, 'password'),
        },
      },
      publicLoadBalancer: true,
      domainName: 'app.example.com',
      domainZone: route53.HostedZone.fromLookup(this, 'Zone', {
        domainName: 'example.com',
      }),
      certificate: certificatemanager.Certificate.fromCertificateArn(
        this,
        'Cert',
        'arn:aws:acm:region:account:certificate/id'
      ),
    });

    // Auto Scaling
    const scaling = webService.service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10,
    });

    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    scaling.scaleOnRequestCount('RequestScaling', {
      requestsPerTarget: 1000,
      targetGroup: webService.targetGroup,
    });

    // Allow web service to access database and cache
    database.connections.allowFrom(webService.service, ec2.Port.tcp(3306));
    cacheSecurityGroup.addIngressRule(
      webService.service.connections.securityGroups[0],
      ec2.Port.tcp(6379)
    );

    // Outputs
    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      value: webService.loadBalancer.loadBalancerDnsName,
      description: 'Load Balancer DNS Name',
    });

    new cdk.CfnOutput(this, 'ServiceURL', {
      value: `https://${webService.domainName}`,
      description: 'Service URL',
    });
  }
}

// Main app
const app = new cdk.App();
new ThreeTierWebAppStack(app, 'ThreeTierWebApp', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
  tags: {
    Environment: 'production',
    Application: 'webapp',
    ManagedBy: 'cdk',
  },
});
```

### Python
```python
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_logs as logs,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_cloudwatch as cloudwatch,
)
from constructs import Construct
from typing import Dict, List, Optional

class MicroservicesStack(Stack):
    """
    Creates a microservices architecture with service mesh
    """
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # VPC with custom configuration
        self.vpc = ec2.Vpc(
            self, "MicroservicesVPC",
            max_azs=3,
            nat_gateways=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
            ],
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )
        
        # ECS Cluster with capacity providers
        self.cluster = ecs.Cluster(
            self, "ServiceCluster",
            vpc=self.vpc,
            container_insights=True,
            enable_fargate_capacity_providers=True,
        )
        
        # Add EC2 capacity for mixed workloads
        self.cluster.add_capacity(
            "EC2Capacity",
            instance_type=ec2.InstanceType("m5.large"),
            min_capacity=2,
            max_capacity=10,
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            task_drain_time=Duration.seconds(0),
        )
        
        # Service Discovery namespace
        self.namespace = self.cluster.add_default_cloud_map_namespace(
            name="local",
            type=ecs.NamespaceType.DNS_PRIVATE,
        )
        
        # Shared ALB for all services
        self.alb = elbv2.ApplicationLoadBalancer(
            self, "SharedALB",
            vpc=self.vpc,
            internet_facing=True,
            load_balancer_name="microservices-alb",
        )
        
        # Create microservices
        self.services = {}
        service_configs = [
            {
                "name": "user-service",
                "image": "user-service:latest",
                "port": 8080,
                "cpu": 256,
                "memory": 512,
                "path_pattern": "/users/*",
                "priority": 1,
                "env_vars": {
                    "SERVICE_NAME": "user-service",
                    "LOG_LEVEL": "info",
                }
            },
            {
                "name": "order-service",
                "image": "order-service:latest",
                "port": 8081,
                "cpu": 512,
                "memory": 1024,
                "path_pattern": "/orders/*",
                "priority": 2,
                "env_vars": {
                    "SERVICE_NAME": "order-service",
                    "CACHE_ENABLED": "true",
                }
            },
            {
                "name": "payment-service",
                "image": "payment-service:latest",
                "port": 8082,
                "cpu": 512,
                "memory": 1024,
                "path_pattern": "/payments/*",
                "priority": 3,
                "env_vars": {
                    "SERVICE_NAME": "payment-service",
                    "ENCRYPTION_ENABLED": "true",
                }
            },
        ]
        
        for config in service_configs:
            service = self._create_service(config)
            self.services[config["name"]] = service
        
        # API Gateway integration (optional)
        self._setup_api_gateway()
        
        # Outputs
        CfnOutput(
            self, "ALBEndpoint",
            value=f"http://{self.alb.load_balancer_dns_name}",
            description="Application Load Balancer endpoint",
        )
        
        CfnOutput(
            self, "ServiceDiscoveryNamespace",
            value=self.namespace.namespace_name,
            description="Service discovery namespace for internal communication",
        )
    
    def _create_service(self, config: Dict) -> ecs.FargateService:
        """
        Creates a Fargate service with the given configuration
        """
        # Task definition
        task_definition = ecs.FargateTaskDefinition(
            self, f"{config['name']}-task",
            cpu=config["cpu"],
            memory_limit_mib=config["memory"],
            execution_role=self._create_execution_role(config["name"]),
            task_role=self._create_task_role(config["name"]),
        )
        
        # Container definition
        container = task_definition.add_container(
            config["name"],
            image=ecs.ContainerImage.from_registry(config["image"]),
            environment=config["env_vars"],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=config["name"],
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", f"curl -f http://localhost:{config['port']}/health || exit 1"],
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                retries=3,
            ),
        )
        
        container.add_port_mappings(
            ecs.PortMapping(
                container_port=config["port"],
                protocol=ecs.Protocol.TCP,
            )
        )
        
        # Service
        service = ecs.FargateService(
            self, f"{config['name']}-service",
            cluster=self.cluster,
            task_definition=task_definition,
            desired_count=2,
            assign_public_ip=False,
            service_name=config["name"],
            cloud_map_options=ecs.CloudMapOptions(
                name=config["name"],
                cloud_map_namespace=self.namespace,
                dns_record_type=ecs.DnsRecordType.A,
            ),
            circuit_breaker=ecs.DeploymentCircuitBreaker(
                rollback=True,
            ),
            enable_ecs_managed_tags=True,
            propagate_tags=ecs.PropagatedTagSource.SERVICE,
        )
        
        # Target group
        target_group = elbv2.ApplicationTargetGroup(
            self, f"{config['name']}-tg",
            vpc=self.vpc,
            port=config["port"],
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[service],
            health_check=elbv2.HealthCheck(
                path="/health",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(10),
                healthy_threshold_count=2,
                unhealthy_threshold_count=3,
            ),
            deregistration_delay=Duration.seconds(30),
        )
        
        # ALB listener rule
        listener = self.alb.add_listener(
            "HTTPListener",
            port=80,
            open=True,
            default_action=elbv2.ListenerAction.fixed_response(
                status_code=404,
                content_type="text/plain",
                message_body="Not Found",
            ),
        ) if not hasattr(self, '_alb_listener') else self._alb_listener
        
        if not hasattr(self, '_alb_listener'):
            self._alb_listener = listener
        
        listener.add_action(
            f"{config['name']}-rule",
            priority=config["priority"],
            conditions=[
                elbv2.ListenerCondition.path_patterns([config["path_pattern"]])
            ],
            action=elbv2.ListenerAction.forward([target_group]),
        )
        
        # Auto scaling
        scaling = service.auto_scale_task_count(
            min_capacity=2,
            max_capacity=10,
        )
        
        scaling.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )
        
        scaling.scale_on_request_count(
            "RequestScaling",
            requests_per_target=1000,
            target_group=target_group,
        )
        
        # CloudWatch alarms
        cloudwatch.Alarm(
            self, f"{config['name']}-cpu-alarm",
            metric=service.metric_cpu_utilization(),
            threshold=80,
            evaluation_periods=2,
            datapoints_to_alarm=2,
            alarm_description=f"CPU utilization is too high for {config['name']}",
        )
        
        return service
    
    def _create_execution_role(self, service_name: str) -> iam.Role:
        """Creates an execution role for the ECS task"""
        return iam.Role(
            self, f"{service_name}-execution-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )
    
    def _create_task_role(self, service_name: str) -> iam.Role:
        """Creates a task role with service-specific permissions"""
        role = iam.Role(
            self, f"{service_name}-task-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )
        
        # Add service-specific permissions
        if service_name == "payment-service":
            role.add_to_policy(
                iam.PolicyStatement(
                    actions=["kms:Decrypt", "kms:GenerateDataKey"],
                    resources=["*"],
                )
            )
        
        return role
    
    def _setup_api_gateway(self):
        """Sets up API Gateway for external API management"""
        # Implementation depends on specific requirements
        pass


# Custom construct for reusable patterns
class StatefulService(Construct):
    """
    A construct that creates a stateful service with persistent storage
    """
    
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc: ec2.IVpc,
        cluster: ecs.ICluster,
        service_name: str,
        container_image: str,
        storage_size: int = 20,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)
        
        # EFS file system for persistent storage
        self.file_system = efs.FileSystem(
            self, "FileSystem",
            vpc=vpc,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_30_DAYS,
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING,
            encrypted=True,
            enable_automatic_backups=True,
        )
        
        # Access point
        self.access_point = self.file_system.add_access_point(
            "AccessPoint",
            path=f"/{service_name}",
            create_acl=efs.Acl(
                owner_uid="1000",
                owner_gid="1000",
                permissions="755",
            ),
            posix_user=efs.PosixUser(
                uid="1000",
                gid="1000",
            ),
        )
        
        # Task definition with EFS volume
        self.task_definition = ecs.FargateTaskDefinition(
            self, "TaskDef",
            cpu=512,
            memory_limit_mib=1024,
            volumes=[
                ecs.Volume(
                    name="persistent-storage",
                    efs_volume_configuration=ecs.EfsVolumeConfiguration(
                        file_system_id=self.file_system.file_system_id,
                        transit_encryption="ENABLED",
                        authorization_config=ecs.AuthorizationConfig(
                            access_point_id=self.access_point.access_point_id,
                            iam="ENABLED",
                        ),
                    ),
                ),
            ],
        )
        
        # Container with volume mount
        container = self.task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_registry(container_image),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=service_name,
            ),
        )
        
        container.add_mount_points(
            ecs.MountPoint(
                source_volume="persistent-storage",
                container_path="/data",
                read_only=False,
            )
        )
        
        # Service
        self.service = ecs.FargateService(
            self, "Service",
            cluster=cluster,
            task_definition=self.task_definition,
            desired_count=1,  # Stateful services typically run single instance
            service_name=service_name,
            platform_version=ecs.FargatePlatformVersion.VERSION1_4,
        )
        
        # Grant EFS access
        self.file_system.grant_read_write(self.task_definition.task_role)
```

### Java
```java
package com.example.cdk;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;
import software.amazon.awscdk.services.ecs.*;
import software.amazon.awscdk.services.ecs.patterns.*;
import software.amazon.awscdk.services.elasticloadbalancingv2.*;
import software.amazon.awscdk.services.rds.*;
import software.amazon.awscdk.services.logs.*;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awscdk.services.autoscaling.*;

import software.constructs.Construct;

import java.util.*;

public class ContainerizedAppStack extends Stack {
    
    public ContainerizedAppStack(final Construct scope, final String id) {
        this(scope, id, null);
    }
    
    public ContainerizedAppStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);
        
        // VPC Configuration
        Vpc vpc = Vpc.Builder.create(this, "AppVpc")
            .maxAzs(3)
            .natGateways(2)
            .subnetConfiguration(Arrays.asList(
                SubnetConfiguration.builder()
                    .name("Public")
                    .subnetType(SubnetType.PUBLIC)
                    .cidrMask(24)
                    .build(),
                SubnetConfiguration.builder()
                    .name("Private")
                    .subnetType(SubnetType.PRIVATE_WITH_EGRESS)
                    .cidrMask(24)
                    .build(),
                SubnetConfiguration.builder()
                    .name("Isolated")
                    .subnetType(SubnetType.PRIVATE_ISOLATED)
                    .cidrMask(24)
                    .build()
            ))
            .build();
        
        // ECS Cluster
        Cluster cluster = Cluster.Builder.create(this, "EcsCluster")
            .vpc(vpc)
            .containerInsights(true)
            .build();
        
        // Add Auto Scaling Group to cluster
        AutoScalingGroup asg = AutoScalingGroup.Builder.create(this, "ClusterASG")
            .vpc(vpc)
            .instanceType(InstanceType.of(InstanceClass.M5, InstanceSize.LARGE))
            .machineImage(EcsOptimizedImage.amazonLinux2())
            .minCapacity(2)
            .maxCapacity(10)
            .desiredCapacity(4)
            .build();
        
        cluster.addAsgCapacityProvider(
            AsgCapacityProvider.Builder.create(this, "AsgCapacityProvider")
                .autoScalingGroup(asg)
                .enableManagedTerminationProtection(false)
                .build()
        );
        
        // RDS Database
        DatabaseCluster database = DatabaseCluster.Builder.create(this, "Database")
            .engine(DatabaseClusterEngine.auroraMysql(
                AuroraMysqlClusterEngineProps.builder()
                    .version(AuroraMysqlEngineVersion.VER_2_10_1)
                    .build()
            ))
            .instanceProps(InstanceProps.builder()
                .vpc(vpc)
                .vpcSubnets(SubnetSelection.builder()
                    .subnetType(SubnetType.PRIVATE_ISOLATED)
                    .build())
                .instanceType(InstanceType.of(InstanceClass.R5, InstanceSize.LARGE))
                .build())
            .instances(2)
            .defaultDatabaseName("appdb")
            .build();
        
        // Application Load Balancer
        ApplicationLoadBalancer alb = ApplicationLoadBalancer.Builder.create(this, "ALB")
            .vpc(vpc)
            .internetFacing(true)
            .build();
        
        // Create services
        Map<String, ServiceConfig> services = new HashMap<>();
        services.put("api", new ServiceConfig("api-service", 3000, 512, 1024));
        services.put("worker", new ServiceConfig("worker-service", 3001, 1024, 2048));
        
        for (Map.Entry<String, ServiceConfig> entry : services.entrySet()) {
            createService(cluster, vpc, alb, database, entry.getKey(), entry.getValue());
        }
        
        // Outputs
        CfnOutput.Builder.create(this, "ALBUrl")
            .value(String.format("http://%s", alb.getLoadBalancerDnsName()))
            .description("Application Load Balancer URL")
            .build();
    }
    
    private void createService(Cluster cluster, Vpc vpc, ApplicationLoadBalancer alb,
                              DatabaseCluster database, String serviceName, ServiceConfig config) {
        
        // Task Definition
        Ec2TaskDefinition taskDefinition = Ec2TaskDefinition.Builder.create(this, config.getName() + "Task")
            .cpu(String.valueOf(config.getCpu()))
            .memoryMiB(String.valueOf(config.getMemory()))
            .networkMode(NetworkMode.AWS_VPC)
            .build();
        
        // Container Definition
        ContainerDefinition container = taskDefinition.addContainer(config.getName(), ContainerDefinitionOptions.builder()
            .image(ContainerImage.fromRegistry(config.getName() + ":latest"))
            .cpu(config.getCpu())
            .memoryLimitMiB(config.getMemory())
            .environment(Map.of(
                "DB_HOST", database.getClusterEndpoint().getHostname(),
                "DB_NAME", "appdb",
                "SERVICE_NAME", config.getName()
            ))
            .logging(LogDrivers.awsLogs(AwsLogDriverProps.builder()
                .streamPrefix(config.getName())
                .logRetention(RetentionDays.ONE_WEEK)
                .build()))
            .build());
        
        container.addPortMappings(PortMapping.builder()
            .containerPort(config.getPort())
            .protocol(Protocol.TCP)
            .build());
        
        // Security Group
        SecurityGroup serviceSecurityGroup = SecurityGroup.Builder.create(this, config.getName() + "SG")
            .vpc(vpc)
            .description("Security group for " + config.getName())
            .build();
        
        // ECS Service
        Ec2Service service = Ec2Service.Builder.create(this, config.getName() + "Service")
            .cluster(cluster)
            .taskDefinition(taskDefinition)
            .desiredCount(2)
            .securityGroups(List.of(serviceSecurityGroup))
            .vpcSubnets(SubnetSelection.builder()
                .subnetType(SubnetType.PRIVATE_WITH_EGRESS)
                .build())
            .build();
        
        // Target Group
        ApplicationTargetGroup targetGroup = ApplicationTargetGroup.Builder.create(this, config.getName() + "TG")
            .vpc(vpc)
            .port(config.getPort())
            .protocol(ApplicationProtocol.HTTP)
            .targets(List.of(service))
            .healthCheck(HealthCheck.builder()
                .path("/health")
                .interval(Duration.seconds(30))
                .timeout(Duration.seconds(10))
                .healthyThresholdCount(2)
                .unhealthyThresholdCount(3)
                .build())
            .build();
        
        // ALB Listener
        ApplicationListener listener = alb.addListener(config.getName() + "Listener", ApplicationListenerProps.builder()
            .port(config.getPort())
            .protocol(ApplicationProtocol.HTTP)
            .defaultTargetGroups(List.of(targetGroup))
            .build());
        
        // Auto Scaling
        ScalableTaskCount scalableTarget = service.autoScaleTaskCount(EnableScalingProps.builder()
            .minCapacity(2)
            .maxCapacity(10)
            .build());
        
        scalableTarget.scaleOnCpuUtilization(config.getName() + "CpuScaling", CpuUtilizationScalingProps.builder()
            .targetUtilizationPercent(70)
            .scaleInCooldown(Duration.seconds(60))
            .scaleOutCooldown(Duration.seconds(60))
            .build());
        
        // Allow database access
        database.connections.allowFrom(serviceSecurityGroup, Port.tcp(3306));
    }
    
    // Helper class for service configuration
    static class ServiceConfig {
        private final String name;
        private final int port;
        private final int cpu;
        private final int memory;
        
        public ServiceConfig(String name, int port, int cpu, int memory) {
            this.name = name;
            this.port = port;
            this.cpu = cpu;
            this.memory = memory;
        }
        
        // Getters
        public String getName() { return name; }
        public int getPort() { return port; }
        public int getCpu() { return cpu; }
        public int getMemory() { return memory; }
    }
}
```

## Practical Examples

### Serverless API with Step Functions
```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as logs from 'aws-cdk-lib/aws-logs';

export class ServerlessWorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Tables
    const ordersTable = new dynamodb.Table(this, 'OrdersTable', {
      partitionKey: { name: 'orderId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      stream: dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
      pointInTimeRecovery: true,
    });

    const inventoryTable = new dynamodb.Table(this, 'InventoryTable', {
      partitionKey: { name: 'productId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    // Lambda Functions
    const validateOrderFn = new lambda.Function(this, 'ValidateOrder', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'validate.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        ORDERS_TABLE: ordersTable.tableName,
      },
      timeout: cdk.Duration.seconds(30),
      tracing: lambda.Tracing.ACTIVE,
    });

    const checkInventoryFn = new lambda.Function(this, 'CheckInventory', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'inventory.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        INVENTORY_TABLE: inventoryTable.tableName,
      },
      timeout: cdk.Duration.seconds(30),
      tracing: lambda.Tracing.ACTIVE,
    });

    const processPaymentFn = new lambda.Function(this, 'ProcessPayment', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'payment.handler',
      code: lambda.Code.fromAsset('lambda'),
      timeout: cdk.Duration.seconds(60),
      tracing: lambda.Tracing.ACTIVE,
    });

    const shipOrderFn = new lambda.Function(this, 'ShipOrder', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'shipping.handler',
      code: lambda.Code.fromAsset('lambda'),
      timeout: cdk.Duration.seconds(30),
      tracing: lambda.Tracing.ACTIVE,
    });

    // Grant permissions
    ordersTable.grantReadWriteData(validateOrderFn);
    inventoryTable.grantReadWriteData(checkInventoryFn);

    // Step Functions Definition
    const validateOrder = new tasks.LambdaInvoke(this, 'ValidateOrderTask', {
      lambdaFunction: validateOrderFn,
      outputPath: '$.Payload',
    });

    const checkInventory = new tasks.LambdaInvoke(this, 'CheckInventoryTask', {
      lambdaFunction: checkInventoryFn,
      outputPath: '$.Payload',
    });

    const processPayment = new tasks.LambdaInvoke(this, 'ProcessPaymentTask', {
      lambdaFunction: processPaymentFn,
      outputPath: '$.Payload',
      retryOnServiceExceptions: true,
    });

    const shipOrder = new tasks.LambdaInvoke(this, 'ShipOrderTask', {
      lambdaFunction: shipOrderFn,
      outputPath: '$.Payload',
    });

    const notifyCustomer = new tasks.SnsPublish(this, 'NotifyCustomer', {
      topic: sns.Topic.fromTopicArn(this, 'NotificationTopic', 
        'arn:aws:sns:region:account:customer-notifications'),
      message: sfn.TaskInput.fromJsonPathAt('$.message'),
    });

    const orderFailed = new sfn.Fail(this, 'OrderFailed', {
      cause: 'Order processing failed',
      error: 'OrderError',
    });

    // State Machine Definition
    const definition = validateOrder
      .next(checkInventory)
      .next(
        new sfn.Choice(this, 'InventoryAvailable?')
          .when(
            sfn.Condition.stringEquals('$.status', 'AVAILABLE'),
            processPayment
              .next(
                new sfn.Choice(this, 'PaymentSuccessful?')
                  .when(
                    sfn.Condition.stringEquals('$.paymentStatus', 'SUCCESS'),
                    shipOrder.next(notifyCustomer)
                  )
                  .otherwise(orderFailed)
              )
          )
          .otherwise(orderFailed)
      );

    const stateMachine = new sfn.StateMachine(this, 'OrderProcessingWorkflow', {
      definition,
      timeout: cdk.Duration.minutes(30),
      tracingEnabled: true,
      logs: {
        destination: new logs.LogGroup(this, 'StateMachineLogGroup', {
          retention: logs.RetentionDays.ONE_WEEK,
        }),
        level: sfn.LogLevel.ALL,
      },
    });

    // API Gateway
    const api = new apigateway.RestApi(this, 'OrderAPI', {
      restApiName: 'Order Processing API',
      deployOptions: {
        stageName: 'prod',
        tracingEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
      },
    });

    // Lambda for API integration
    const startWorkflowFn = new lambda.Function(this, 'StartWorkflow', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'startWorkflow.handler',
      code: lambda.Code.fromAsset('lambda'),
      environment: {
        STATE_MACHINE_ARN: stateMachine.stateMachineArn,
      },
    });

    stateMachine.grantStartExecution(startWorkflowFn);

    // API Gateway integration
    const ordersResource = api.root.addResource('orders');
    ordersResource.addMethod('POST', 
      new apigateway.LambdaIntegration(startWorkflowFn),
      {
        authorizationType: apigateway.AuthorizationType.IAM,
        requestValidator: new apigateway.RequestValidator(this, 'RequestValidator', {
          restApi: api,
          validateRequestBody: true,
          validateRequestParameters: true,
        }),
      }
    );

    // Outputs
    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: api.url,
      description: 'API Gateway endpoint URL',
    });

    new cdk.CfnOutput(this, 'StateMachineArn', {
      value: stateMachine.stateMachineArn,
      description: 'Step Functions state machine ARN',
    });
  }
}
```

### Multi-Region Active-Active Setup
```typescript
import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';

// Base stack for regional resources
export class RegionalStack extends cdk.Stack {
  public readonly albDnsName: string;
  public readonly healthCheckId: string;

  constructor(scope: Construct, id: string, props: cdk.StackProps & { isPrimary: boolean }) {
    super(scope, id, props);

    // Regional infrastructure (VPC, ALB, ECS, RDS, etc.)
    const infrastructure = new RegionalInfrastructure(this, 'Infra', {
      isPrimary: props.isPrimary,
    });

    this.albDnsName = infrastructure.alb.loadBalancerDnsName;

    // Route 53 health check
    const healthCheck = new route53.CfnHealthCheck(this, 'HealthCheck', {
      type: 'HTTPS',
      resourcePath: '/health',
      fullyQualifiedDomainName: this.albDnsName,
      port: 443,
      requestInterval: 30,
      failureThreshold: 3,
    });

    this.healthCheckId = healthCheck.ref;
  }
}

// Global stack for multi-region coordination
export class GlobalStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: cdk.StackProps & {
    primaryRegion: string;
    secondaryRegion: string;
    domainName: string;
  }) {
    super(scope, id, props);

    // Deploy regional stacks
    const primaryStack = new RegionalStack(scope, 'PrimaryRegion', {
      env: { region: props.primaryRegion },
      isPrimary: true,
    });

    const secondaryStack = new RegionalStack(scope, 'SecondaryRegion', {
      env: { region: props.secondaryRegion },
      isPrimary: false,
    });

    // Hosted Zone
    const hostedZone = route53.HostedZone.fromLookup(this, 'HostedZone', {
      domainName: props.domainName,
    });

    // Route 53 failover records
    new route53.ARecord(this, 'PrimaryRecord', {
      zone: hostedZone,
      recordName: 'app',
      target: route53.RecordTarget.fromAlias(
        new targets.LoadBalancerTarget(primaryStack.alb)
      ),
      setIdentifier: 'Primary',
      weight: 100,
      healthCheckId: primaryStack.healthCheckId,
    });

    new route53.ARecord(this, 'SecondaryRecord', {
      zone: hostedZone,
      recordName: 'app',
      target: route53.RecordTarget.fromAlias(
        new targets.LoadBalancerTarget(secondaryStack.alb)
      ),
      setIdentifier: 'Secondary',
      weight: 0,
      healthCheckId: secondaryStack.healthCheckId,
    });

    // Global S3 bucket for static assets
    const staticBucket = new s3.Bucket(this, 'StaticAssets', {
      bucketName: `${props.domainName}-static-assets`,
      replication: [{
        role: replicationRole,
        rules: [{
          id: 'ReplicateAll',
          status: 'Enabled',
          priority: 1,
          destination: {
            bucket: s3.Bucket.fromBucketArn(
              this, 
              'ReplicaBucket',
              `arn:aws:s3:::${props.domainName}-static-assets-replica`
            ),
          },
        }],
      }],
    });

    // CloudFront distribution
    const distribution = new cloudfront.Distribution(this, 'CDN', {
      defaultBehavior: {
        origin: new origins.S3Origin(staticBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
      },
      additionalBehaviors: {
        '/api/*': {
          origin: new origins.HttpOrigin(primaryStack.albDnsName, {
            protocolPolicy: cloudfront.OriginProtocolPolicy.HTTPS_ONLY,
          }),
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
          originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER,
        },
      },
      domainNames: [props.domainName],
      certificate: acm.Certificate.fromCertificateArn(
        this,
        'Certificate',
        'arn:aws:acm:us-east-1:account:certificate/id'
      ),
      priceClass: cloudfront.PriceClass.PRICE_CLASS_ALL,
    });

    // Route 53 alias for CloudFront
    new route53.ARecord(this, 'CloudFrontAlias', {
      zone: hostedZone,
      recordName: props.domainName,
      target: route53.RecordTarget.fromAlias(
        new targets.CloudFrontTarget(distribution)
      ),
    });
  }
}
```

### Custom Constructs Library
```typescript
// lib/constructs/secure-bucket.ts
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export interface SecureBucketProps {
  bucketName?: string;
  versioned?: boolean;
  lifecycleRules?: s3.LifecycleRule[];
  replicationRole?: iam.IRole;
  replicationDestination?: string;
}

export class SecureBucket extends Construct {
  public readonly bucket: s3.Bucket;
  public readonly key: kms.Key;

  constructor(scope: Construct, id: string, props: SecureBucketProps = {}) {
    super(scope, id);

    // Create KMS key for encryption
    this.key = new kms.Key(this, 'Key', {
      enableKeyRotation: true,
      description: `Encryption key for ${id} bucket`,
    });

    // Create bucket with security best practices
    this.bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: props.bucketName,
      encryption: s3.BucketEncryption.KMS,
      encryptionKey: this.key,
      versioned: props.versioned ?? true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      lifecycleRules: props.lifecycleRules ?? [
        {
          id: 'DeleteOldVersions',
          noncurrentVersionExpiration: cdk.Duration.days(90),
          abortIncompleteMultipartUploadAfter: cdk.Duration.days(7),
        },
      ],
      serverAccessLogsPrefix: 'access-logs/',
      inventories: [
        {
          frequency: s3.InventoryFrequency.WEEKLY,
          includeObjectVersions: s3.InventoryObjectVersion.ALL,
          destination: {
            bucket: this.bucket,
            prefix: 'inventory',
          },
        },
      ],
    });

    // Add bucket policy
    this.bucket.addToResourcePolicy(
      new iam.PolicyStatement({
        sid: 'DenyInsecureTransport',
        effect: iam.Effect.DENY,
        principals: [new iam.AnyPrincipal()],
        actions: ['s3:*'],
        resources: [
          this.bucket.bucketArn,
          `${this.bucket.bucketArn}/*`,
        ],
        conditions: {
          Bool: {
            'aws:SecureTransport': 'false',
          },
        },
      })
    );

    // Add replication if specified
    if (props.replicationRole && props.replicationDestination) {
      const cfnBucket = this.bucket.node.defaultChild as s3.CfnBucket;
      cfnBucket.replicationConfiguration = {
        role: props.replicationRole.roleArn,
        rules: [
          {
            id: 'ReplicateAll',
            status: 'Enabled',
            priority: 1,
            filter: {},
            destination: {
              bucket: props.replicationDestination,
              replicationTime: {
                status: 'Enabled',
                time: { minutes: 15 },
              },
              metrics: {
                status: 'Enabled',
                eventThreshold: { minutes: 15 },
              },
            },
            deleteMarkerReplication: { status: 'Enabled' },
          },
        ],
      };
    }
  }

  public grantRead(grantee: iam.IGrantable): iam.Grant {
    this.key.grantDecrypt(grantee);
    return this.bucket.grantRead(grantee);
  }

  public grantReadWrite(grantee: iam.IGrantable): iam.Grant {
    this.key.grantEncryptDecrypt(grantee);
    return this.bucket.grantReadWrite(grantee);
  }
}

// lib/constructs/monitored-function.ts
export interface MonitoredFunctionProps extends lambda.FunctionProps {
  alarmEmail?: string;
  errorRateThreshold?: number;
  durationThreshold?: number;
}

export class MonitoredFunction extends Construct {
  public readonly function: lambda.Function;
  public readonly errorAlarm: cloudwatch.Alarm;
  public readonly durationAlarm: cloudwatch.Alarm;
  public readonly dashboard: cloudwatch.Dashboard;

  constructor(scope: Construct, id: string, props: MonitoredFunctionProps) {
    super(scope, id);

    // Create function
    this.function = new lambda.Function(this, 'Function', props);

    // Error rate alarm
    this.errorAlarm = new cloudwatch.Alarm(this, 'ErrorAlarm', {
      metric: this.function.metricErrors({
        period: cdk.Duration.minutes(5),
      }),
      threshold: props.errorRateThreshold ?? 1,
      evaluationPeriods: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
      alarmDescription: `Error rate alarm for ${this.function.functionName}`,
    });

    // Duration alarm
    this.durationAlarm = new cloudwatch.Alarm(this, 'DurationAlarm', {
      metric: this.function.metricDuration({
        period: cdk.Duration.minutes(5),
        statistic: 'Average',
      }),
      threshold: props.durationThreshold ?? (this.function.timeout?.toMilliseconds() ?? 3000) * 0.8,
      evaluationPeriods: 2,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
      alarmDescription: `Duration alarm for ${this.function.functionName}`,
    });

    // Create dashboard
    this.dashboard = new cloudwatch.Dashboard(this, 'Dashboard', {
      dashboardName: `${this.function.functionName}-dashboard`,
    });

    this.dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'Invocations',
        left: [this.function.metricInvocations()],
        right: [this.function.metricErrors()],
      }),
      new cloudwatch.GraphWidget({
        title: 'Duration',
        left: [
          this.function.metricDuration({ statistic: 'Average' }),
          this.function.metricDuration({ statistic: 'p99' }),
        ],
      }),
      new cloudwatch.GraphWidget({
        title: 'Concurrent Executions',
        left: [this.function.metricConcurrentExecutions()],
      }),
    );

    // SNS topic for alarms
    if (props.alarmEmail) {
      const topic = new sns.Topic(this, 'AlarmTopic');
      topic.addSubscription(new sns_subscriptions.EmailSubscription(props.alarmEmail));
      this.errorAlarm.addAlarmAction(new cloudwatch_actions.SnsAction(topic));
      this.durationAlarm.addAlarmAction(new cloudwatch_actions.SnsAction(topic));
    }
  }
}
```

## Best Practices

### 1. Project Structure
```
cdk-app/
├── bin/
│   └── app.ts                 # App entry point
├── lib/
│   ├── stacks/               # Stack definitions
│   │   ├── network-stack.ts
│   │   ├── compute-stack.ts
│   │   └── database-stack.ts
│   ├── constructs/           # Reusable constructs
│   │   ├── secure-bucket.ts
│   │   └── monitored-lambda.ts
│   └── patterns/             # L3 constructs/patterns
│       └── web-service.ts
├── test/                     # Unit tests
│   ├── stacks/
│   └── constructs/
├── lambda/                   # Lambda function code
├── config/                   # Environment configs
│   ├── dev.json
│   └── prod.json
├── cdk.json                  # CDK configuration
├── jest.config.js           # Jest configuration
├── package.json
└── tsconfig.json
```

### 2. Environment Management
```typescript
// config/environment.ts
export interface EnvironmentConfig {
  account: string;
  region: string;
  vpcCidr: string;
  instanceTypes: {
    web: string;
    app: string;
    database: string;
  };
  scaling: {
    minCapacity: number;
    maxCapacity: number;
  };
  monitoring: {
    enableDetailedMonitoring: boolean;
    logRetention: number;
  };
}

// config/environments.ts
export const environments: Record<string, EnvironmentConfig> = {
  dev: {
    account: '123456789012',
    region: 'us-east-1',
    vpcCidr: '10.0.0.0/16',
    instanceTypes: {
      web: 't3.micro',
      app: 't3.small',
      database: 't3.medium',
    },
    scaling: {
      minCapacity: 1,
      maxCapacity: 3,
    },
    monitoring: {
      enableDetailedMonitoring: false,
      logRetention: 3,
    },
  },
  prod: {
    account: '987654321098',
    region: 'us-east-1',
    vpcCidr: '10.1.0.0/16',
    instanceTypes: {
      web: 'm5.large',
      app: 'm5.xlarge',
      database: 'r5.2xlarge',
    },
    scaling: {
      minCapacity: 3,
      maxCapacity: 20,
    },
    monitoring: {
      enableDetailedMonitoring: true,
      logRetention: 30,
    },
  },
};

// bin/app.ts
const app = new cdk.App();
const envName = app.node.tryGetContext('environment') || 'dev';
const config = environments[envName];

new ApplicationStack(app, `AppStack-${envName}`, {
  env: {
    account: config.account,
    region: config.region,
  },
  config,
});
```

### 3. Testing
```typescript
// test/constructs/secure-bucket.test.ts
import { Template, Match } from 'aws-cdk-lib/assertions';
import * as cdk from 'aws-cdk-lib';
import { SecureBucket } from '../../lib/constructs/secure-bucket';

describe('SecureBucket', () => {
  let app: cdk.App;
  let stack: cdk.Stack;

  beforeEach(() => {
    app = new cdk.App();
    stack = new cdk.Stack(app, 'TestStack');
  });

  test('creates bucket with encryption', () => {
    // Arrange & Act
    new SecureBucket(stack, 'TestBucket');

    // Assert
    const template = Template.fromStack(stack);
    
    template.hasResourceProperties('AWS::S3::Bucket', {
      BucketEncryption: {
        ServerSideEncryptionConfiguration: [
          {
            ServerSideEncryptionByDefault: {
              SSEAlgorithm: 'aws:kms',
            },
          },
        ],
      },
      PublicAccessBlockConfiguration: {
        BlockPublicAcls: true,
        BlockPublicPolicy: true,
        IgnorePublicAcls: true,
        RestrictPublicBuckets: true,
      },
    });

    template.hasResourceProperties('AWS::KMS::Key', {
      EnableKeyRotation: true,
    });
  });

  test('adds lifecycle rules', () => {
    // Arrange & Act
    new SecureBucket(stack, 'TestBucket', {
      lifecycleRules: [
        {
          id: 'CustomRule',
          expiration: cdk.Duration.days(30),
        },
      ],
    });

    // Assert
    const template = Template.fromStack(stack);
    
    template.hasResourceProperties('AWS::S3::Bucket', {
      LifecycleConfiguration: {
        Rules: Match.arrayWith([
          Match.objectLike({
            Id: 'CustomRule',
            ExpirationInDays: 30,
            Status: 'Enabled',
          }),
        ]),
      },
    });
  });

  test('snapshot test', () => {
    // Arrange & Act
    new SecureBucket(stack, 'TestBucket');

    // Assert
    const template = Template.fromStack(stack);
    expect(template.toJSON()).toMatchSnapshot();
  });
});
```

### 4. Aspect-Based Validation
```typescript
// lib/aspects/security-aspect.ts
export class SecurityAspect implements cdk.IAspect {
  public visit(node: IConstruct): void {
    // Ensure S3 buckets have encryption
    if (node instanceof s3.Bucket) {
      if (!node.encryptionKey) {
        Annotations.of(node).addError('Bucket must have encryption enabled');
      }
    }

    // Ensure databases have backup enabled
    if (node instanceof rds.DatabaseInstance) {
      const cfnDb = node.node.defaultChild as rds.CfnDBInstance;
      if (cfnDb.backupRetentionPeriod === undefined || cfnDb.backupRetentionPeriod < 7) {
        Annotations.of(node).addWarning('Database should have at least 7 days backup retention');
      }
    }

    // Ensure Lambda functions have reserved concurrent executions
    if (node instanceof lambda.Function) {
      if (!node.reservedConcurrentExecutions) {
        Annotations.of(node).addInfo('Consider setting reserved concurrent executions');
      }
    }
  }
}

// Apply to app
const app = new cdk.App();
Aspects.of(app).add(new SecurityAspect());
```

### 5. Cost Optimization
```typescript
// lib/aspects/cost-optimization-aspect.ts
export class CostOptimizationAspect implements cdk.IAspect {
  public visit(node: IConstruct): void {
    // Use Graviton instances where possible
    if (node instanceof ec2.Instance) {
      const instanceType = node.instanceType;
      if (!instanceType.toString().includes('g')) {
        Annotations.of(node).addInfo(
          'Consider using Graviton-based instances for better cost-performance'
        );
      }
    }

    // Enable S3 Intelligent-Tiering
    if (node instanceof s3.Bucket) {
      const cfnBucket = node.node.defaultChild as s3.CfnBucket;
      if (!cfnBucket.lifecycleConfiguration?.rules?.some(
        rule => rule.transitions?.some(t => t.storageClass === 'INTELLIGENT_TIERING')
      )) {
        Annotations.of(node).addInfo(
          'Consider enabling S3 Intelligent-Tiering for cost optimization'
        );
      }
    }

    // Use Aurora Serverless for variable workloads
    if (node instanceof rds.DatabaseCluster) {
      if (!node.serverlessV2ScalingConfiguration) {
        Annotations.of(node).addInfo(
          'Consider Aurora Serverless v2 for variable workloads'
        );
      }
    }
  }
}
```

## Integration Patterns

### 1. CDK Pipelines
```typescript
import * as pipelines from 'aws-cdk-lib/pipelines';
import * as codecommit from 'aws-cdk-lib/aws-codecommit';

export class PipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Source repository
    const repo = codecommit.Repository.fromRepositoryName(
      this,
      'Repo',
      'my-cdk-app'
    );

    // CDK Pipeline
    const pipeline = new pipelines.CodePipeline(this, 'Pipeline', {
      pipelineName: 'MyAppPipeline',
      synth: new pipelines.ShellStep('Synth', {
        input: pipelines.CodePipelineSource.codeCommit(repo, 'main'),
        commands: [
          'npm ci',
          'npm run build',
          'npx cdk synth',
        ],
      }),
      
      // Docker build for Lambda functions
      dockerEnabledForSynth: true,
      dockerEnabledForSelfMutation: true,
    });

    // Add stages
    pipeline.addStage(new ApplicationStage(this, 'Dev', {
      env: { account: '123456789012', region: 'us-east-1' },
    }), {
      pre: [
        new pipelines.ShellStep('RunTests', {
          commands: [
            'npm ci',
            'npm test',
          ],
        }),
      ],
    });

    pipeline.addStage(new ApplicationStage(this, 'Prod', {
      env: { account: '987654321098', region: 'us-east-1' },
    }), {
      pre: [
        new pipelines.ManualApprovalStep('PromoteToProd'),
      ],
      post: [
        new pipelines.ShellStep('IntegrationTests', {
          commands: [
            'npm run integration-test',
          ],
        }),
      ],
    });
  }
}
```

### 2. GitOps with CDK8s
```typescript
import * as cdk8s from 'cdk8s';
import * as kplus from 'cdk8s-plus-24';

export class KubernetesChart extends cdk8s.Chart {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // Namespace
    const namespace = new kplus.Namespace(this, 'AppNamespace', {
      metadata: { name: 'my-app' },
    });

    // Deployment
    const deployment = new kplus.Deployment(this, 'Deployment', {
      metadata: {
        namespace: namespace.name,
      },
      replicas: 3,
      containers: [
        {
          image: 'my-app:latest',
          port: 8080,
          resources: {
            requests: {
              cpu: kplus.Cpu.millis(100),
              memory: kplus.Size.mebibytes(128),
            },
            limits: {
              cpu: kplus.Cpu.millis(200),
              memory: kplus.Size.mebibytes(256),
            },
          },
        },
      ],
    });

    // Service
    const service = new kplus.Service(this, 'Service', {
      metadata: {
        namespace: namespace.name,
      },
      selector: deployment,
      ports: [{ port: 80, targetPort: 8080 }],
    });

    // HPA
    new kplus.HorizontalPodAutoscaler(this, 'HPA', {
      metadata: {
        namespace: namespace.name,
      },
      target: deployment,
      minReplicas: 3,
      maxReplicas: 10,
      metrics: [
        kplus.Metric.resourceCpu(kplus.MetricTarget.averageUtilization(70)),
      ],
    });
  }
}

// Synthesize to YAML
const app = new cdk8s.App();
new KubernetesChart(app, 'my-app');
app.synth();
```

### 3. Multi-Account Organization
```typescript
export class OrganizationStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Control Tower Landing Zone
    const landingZone = new controltower.CfnLandingZone(this, 'LandingZone', {
      version: '3.0',
      manifest: {
        governedRegions: ['us-east-1', 'eu-west-1'],
        organizationStructure: {
          security: {
            name: 'Security',
            organizationalUnits: [
              {
                name: 'Production',
                accounts: [
                  {
                    name: 'LogArchive',
                    email: 'log-archive@company.com',
                  },
                  {
                    name: 'Audit',
                    email: 'audit@company.com',
                  },
                ],
              },
            ],
          },
          production: {
            name: 'Production',
            accounts: [
              {
                name: 'ProdApp',
                email: 'prod-app@company.com',
              },
            ],
          },
        },
      },
    });

    // StackSets for baseline configuration
    new cloudformation.CfnStackSet(this, 'SecurityBaseline', {
      stackSetName: 'SecurityBaseline',
      capabilities: ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
      permissionModel: 'SERVICE_MANAGED',
      autoDeployment: {
        enabled: true,
        retainStacksOnAccountRemoval: false,
      },
      managedExecution: {
        active: true,
      },
      templateBody: this.securityBaselineTemplate(),
      parameters: [
        {
          parameterKey: 'SecurityAccountId',
          parameterValue: '123456789012',
        },
      ],
      operationPreferences: {
        regionConcurrencyType: 'PARALLEL',
        maxConcurrentPercentage: 100,
      },
    });
  }

  private securityBaselineTemplate(): string {
    // Return CloudFormation template for security baseline
    return JSON.stringify({
      AWSTemplateFormatVersion: '2010-09-09',
      Description: 'Security baseline for all accounts',
      Resources: {
        // CloudTrail, GuardDuty, Security Hub, etc.
      },
    });
  }
}
```

## Troubleshooting

### Common Issues

1. **Synthesis Errors**
```typescript
// Error: Cannot find module
// Solution: Check tsconfig paths
{
  "compilerOptions": {
    "paths": {
      "@lib/*": ["lib/*"],
      "@constructs/*": ["lib/constructs/*"]
    }
  }
}

// Error: Construct tree validation failed
// Solution: Use Aspects for debugging
Aspects.of(stack).add({
  visit(node: IConstruct) {
    console.log(`${node.node.path}: ${node.constructor.name}`);
  }
});
```

2. **Deployment Failures**
```bash
# Check CloudFormation events
cdk deploy --require-approval never --verbose

# Use hotswapping for faster iterations
cdk deploy --hotswap

# Rollback failed stack
cdk destroy --force
aws cloudformation delete-stack --stack-name MyStack --retain-resources Resource1,Resource2
```

3. **Context and Environment Issues**
```typescript
// Handle missing context gracefully
const vpcId = this.node.tryGetContext('vpcId');
if (!vpcId) {
  throw new Error('VPC ID must be provided via -c vpcId=xxx');
}

// Use context for environment-specific values
const config = this.node.tryGetContext(props.env?.account || 'default');
```

### Debug Techniques

1. **Local Testing with SAM**
```bash
# Generate SAM template
cdk synth --no-staging > template.yaml

# Local testing
sam local start-api
sam local invoke FunctionName --event event.json
```

2. **CDK Diff**
```bash
# See what will change
cdk diff

# Diff specific stacks
cdk diff Stack1 Stack2

# Diff with context
cdk diff -c environment=prod
```

3. **Asset Debugging**
```typescript
// Debug asset bundling
const fn = new lambda.Function(this, 'Function', {
  code: lambda.Code.fromAsset('lambda', {
    bundling: {
      image: lambda.Runtime.NODEJS_18_X.bundlingImage,
      command: [
        'bash', '-c', [
          'cp -r /asset-input/* /asset-output/',
          'cd /asset-output',
          'npm ci --production',
          'echo "Bundling complete"',
        ].join(' && '),
      ],
      environment: {
        NODE_ENV: 'production',
      },
      volumesFrom: [],
      securityOpt: [],
      network: 'host',
    },
  }),
});
```

## Performance Optimization

### 1. Synthesis Performance
```typescript
// Use lazy evaluation
const expensiveValue = Lazy.string({
  produce: () => {
    // Expensive computation
    return computeExpensiveValue();
  },
});

// Cache context lookups
export class CachedVpcLookup {
  private static cache = new Map<string, ec2.IVpc>();
  
  static getVpc(scope: Construct, vpcId: string): ec2.IVpc {
    if (!this.cache.has(vpcId)) {
      this.cache.set(vpcId, ec2.Vpc.fromLookup(scope, `Vpc-${vpcId}`, { vpcId }));
    }
    return this.cache.get(vpcId)!;
  }
}
```

### 2. Deployment Performance
```json
// cdk.json optimizations
{
  "context": {
    "@aws-cdk/core:newStyleStackSynthesis": true,
    "@aws-cdk/aws-apigateway:usagePlanKeyOrderInsensitiveId": true,
    "@aws-cdk/core:stackRelativeExports": true,
    "@aws-cdk/aws-rds:lowercaseDbIdentifier": true,
    "@aws-cdk/aws-lambda:recognizeVersionProps": true,
    "@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021": true
  },
  "requireApproval": "never",
  "toolkitStackName": "CDKToolkit",
  "toolkitBucketName": "cdk-toolkit-bucket"
}
```

## Conclusion

AWS CDK represents a significant evolution in Infrastructure as Code, bringing software engineering best practices to cloud infrastructure. Its construct-based model, strong typing, and native AWS integration make it an excellent choice for teams looking to leverage programming languages for infrastructure.

Key advantages include:
- Type safety and IDE support catch errors early
- Reusable constructs promote consistency
- Higher-level abstractions reduce boilerplate
- Native integration with AWS services
- Active community and AWS support

Whether building serverless applications, containerized workloads, or traditional infrastructure, CDK provides the tools and patterns needed for modern cloud development.