# Crossplane - Kubernetes-Native Infrastructure Management

## Overview

Crossplane is an open-source Kubernetes add-on that enables platform teams to assemble infrastructure from multiple vendors and expose higher-level self-service APIs for application teams to consume. It extends Kubernetes to manage any infrastructure or managed service using the Kubernetes API and enables building cloud-native control planes without writing code.

## Architecture

### Core Components

1. **Crossplane Core**
   - Custom Resource Definitions (CRDs) framework
   - Composition engine
   - Package manager (Configuration and Provider packages)
   - RBAC and policy engine
   - Resource claim and class system

2. **Providers**
   - Cloud provider controllers (AWS, Azure, GCP, Alibaba)
   - Infrastructure providers (Terraform, Ansible, Helm)
   - Managed Kubernetes providers
   - Database and middleware providers

3. **Compositions**
   - Composite Resources (XR)
   - Composite Resource Definitions (XRD)
   - Composition Functions
   - Resource patches and transforms

4. **Control Plane Architecture**
   - Provider pods and controllers
   - Composition controller
   - Package manager controller
   - RBAC manager

## Language Support

### YAML Manifests (Primary)
```yaml
# Provider Configuration
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/crossplane-contrib/provider-aws:v0.39.0
  controllerConfigRef:
    name: aws-config
---
# Provider Config with credentials
apiVersion: aws.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: aws-provider
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-credentials
      key: credentials
  assumeRoleARN: "arn:aws:iam::123456789012:role/CrossplaneRole"
---
# Composite Resource Definition (XRD)
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xpostgresqlinstances.database.platform.io
spec:
  group: database.platform.io
  names:
    kind: XPostgreSQLInstance
    plural: xpostgresqlinstances
  claimNames:
    kind: PostgreSQLInstance
    plural: postgresqlinstances
  connectionSecretKeys:
    - username
    - password
    - endpoint
    - port
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              parameters:
                type: object
                properties:
                  engineVersion:
                    type: string
                    enum: ["13.7", "14.6", "15.1"]
                    default: "14.6"
                  storageGB:
                    type: integer
                    minimum: 20
                    maximum: 1000
                    default: 100
                  instanceSize:
                    type: string
                    enum: ["small", "medium", "large"]
                    default: "small"
                  region:
                    type: string
                    enum: ["us-east-1", "us-west-2", "eu-west-1"]
                  multiAZ:
                    type: boolean
                    default: false
                  backupRetentionDays:
                    type: integer
                    minimum: 1
                    maximum: 35
                    default: 7
                required:
                  - region
---
# Composition implementing the XRD
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xpostgresqlinstances.aws.database.platform.io
  labels:
    provider: aws
    service: rds
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: database.platform.io/v1alpha1
    kind: XPostgreSQLInstance
  
  patchSets:
  - name: common-fields
    patches:
    - fromFieldPath: "metadata.labels"
      toFieldPath: "metadata.labels"
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.region"
  
  resources:
  # VPC and Networking
  - name: vpc
    base:
      apiVersion: ec2.aws.crossplane.io/v1beta1
      kind: VPC
      spec:
        forProvider:
          cidrBlock: 10.0.0.0/16
          enableDnsSupport: true
          enableDnsHostnames: true
    patches:
    - type: PatchSet
      patchSetName: common-fields
    - fromFieldPath: "metadata.name"
      toFieldPath: "metadata.name"
      transforms:
      - type: string
        string:
          fmt: "%s-vpc"
  
  # DB Subnet Group
  - name: db-subnet-group
    base:
      apiVersion: database.aws.crossplane.io/v1beta1
      kind: DBSubnetGroup
      spec:
        forProvider:
          description: "Subnet group for PostgreSQL instance"
          subnetIdSelector:
            matchLabels:
              type: database
    patches:
    - type: PatchSet
      patchSetName: common-fields
    - fromFieldPath: "metadata.name"
      toFieldPath: "metadata.name"
      transforms:
      - type: string
        string:
          fmt: "%s-subnet-group"
  
  # Security Group
  - name: security-group
    base:
      apiVersion: ec2.aws.crossplane.io/v1beta1
      kind: SecurityGroup
      spec:
        forProvider:
          description: "Security group for PostgreSQL instance"
          vpcIdSelector:
            matchControllerRef: true
          ingress:
          - fromPort: 5432
            toPort: 5432
            ipProtocol: tcp
            ipRanges:
            - cidrIp: 10.0.0.0/16
    patches:
    - type: PatchSet
      patchSetName: common-fields
  
  # RDS Instance
  - name: rds-instance
    base:
      apiVersion: database.aws.crossplane.io/v1beta1
      kind: DBInstance
      spec:
        forProvider:
          engine: postgres
          autoGeneratePassword: true
          passwordSecretRef:
            key: password
            namespace: crossplane-system
          masterUsername: postgres
          skipFinalSnapshot: false
          storageEncrypted: true
          deletionProtection: false
          publiclyAccessible: false
          dbSubnetGroupNameSelector:
            matchControllerRef: true
          vpcSecurityGroupIDSelector:
            matchControllerRef: true
        writeConnectionSecretToRef:
          namespace: crossplane-system
    patches:
    - type: PatchSet
      patchSetName: common-fields
    - fromFieldPath: "metadata.name"
      toFieldPath: "metadata.name"
    - fromFieldPath: "spec.parameters.engineVersion"
      toFieldPath: "spec.forProvider.engineVersion"
    - fromFieldPath: "spec.parameters.storageGB"
      toFieldPath: "spec.forProvider.allocatedStorage"
    - fromFieldPath: "spec.parameters.multiAZ"
      toFieldPath: "spec.forProvider.multiAZ"
    - fromFieldPath: "spec.parameters.backupRetentionDays"
      toFieldPath: "spec.forProvider.backupRetentionPeriod"
    - fromFieldPath: "spec.parameters.instanceSize"
      toFieldPath: "spec.forProvider.dbInstanceClass"
      transforms:
      - type: map
        map:
          small: db.t3.micro
          medium: db.t3.medium
          large: db.t3.large
    # Connection secret
    - fromFieldPath: "metadata.uid"
      toFieldPath: "spec.writeConnectionSecretToRef.name"
      transforms:
      - type: string
        string:
          fmt: "%s-postgresql"
    - type: ConnectionDetails
      fromConnectionSecretKey: username
    - type: ConnectionDetails
      fromConnectionSecretKey: password
    - type: ConnectionDetails
      fromConnectionSecretKey: endpoint
    - type: ConnectionDetails
      fromConnectionSecretKey: port
```

### Composition Functions (Go)
```go
package main

import (
    "context"
    "fmt"
    
    "github.com/crossplane/crossplane-runtime/pkg/errors"
    "github.com/crossplane/crossplane-runtime/pkg/logging"
    fnv1beta1 "github.com/crossplane/function-sdk-go/proto/v1beta1"
    "github.com/crossplane/function-sdk-go/request"
    "github.com/crossplane/function-sdk-go/response"
    "github.com/crossplane/function-sdk-go/resource"
    "github.com/crossplane/function-sdk-go/resource/composed"
    
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// Function implements a Composition Function that creates cloud resources
// with advanced logic and transformations
type Function struct {
    log logging.Logger
}

// RunFunction is the main entrypoint for the Composition Function
func (f *Function) RunFunction(_ context.Context, req *fnv1beta1.RunFunctionRequest) (*fnv1beta1.RunFunctionResponse, error) {
    log := f.log.WithValues("request-id", req.GetMeta().GetTag())
    log.Info("Running function")
    
    // Parse the request
    input, err := request.GetInput(req)
    if err != nil {
        return nil, errors.Wrap(err, "cannot get Function input from request")
    }
    
    // Get the observed composite resource
    observed, err := request.GetObservedCompositeResource(req)
    if err != nil {
        return nil, errors.Wrap(err, "cannot get observed composite resource")
    }
    
    // Get the desired composite resource
    desired, err := request.GetDesiredCompositeResource(req)
    if err != nil {
        return nil, errors.Wrap(err, "cannot get desired composite resource")
    }
    
    // Get existing composed resources
    observedComposed, err := request.GetObservedComposedResources(req)
    if err != nil {
        return nil, errors.Wrap(err, "cannot get observed composed resources")
    }
    
    // Get desired composed resources
    desiredComposed, err := request.GetDesiredComposedResources(req)
    if err != nil {
        return nil, errors.Wrap(err, "cannot get desired composed resources")
    }
    
    // Extract parameters from composite
    params := &Parameters{}
    if err := observed.Resource.GetValueInto("spec.parameters", params); err != nil {
        return nil, errors.Wrap(err, "cannot get parameters")
    }
    
    // Create response
    rsp := response.To(req, response.DefaultTTL)
    
    // Generate resources based on parameters
    if err := f.generateResources(params, desired, desiredComposed, rsp); err != nil {
        return nil, errors.Wrap(err, "cannot generate resources")
    }
    
    // Update composite resource status
    if err := f.updateStatus(observed, desired, desiredComposed, rsp); err != nil {
        return nil, errors.Wrap(err, "cannot update status")
    }
    
    return rsp, nil
}

func (f *Function) generateResources(params *Parameters, desired resource.Composite, 
    desiredComposed map[resource.Name]resource.DesiredComposed, rsp *response.Response) error {
    
    // Generate VPC if needed
    if params.CreateVPC {
        vpc := f.generateVPC(params)
        if err := rsp.SetDesiredComposedResource(composed.New(vpc)); err != nil {
            return errors.Wrap(err, "cannot set VPC resource")
        }
    }
    
    // Generate subnets based on availability zones
    subnets := f.generateSubnets(params)
    for i, subnet := range subnets {
        if err := rsp.SetDesiredComposedResource(
            composed.New(subnet).WithName(fmt.Sprintf("subnet-%d", i)),
        ); err != nil {
            return errors.Wrapf(err, "cannot set subnet %d", i)
        }
    }
    
    // Generate database cluster with computed configuration
    db := f.generateDatabase(params, len(subnets))
    if err := rsp.SetDesiredComposedResource(composed.New(db)); err != nil {
        return errors.Wrap(err, "cannot set database resource")
    }
    
    // Generate monitoring resources
    if params.EnableMonitoring {
        monitoring := f.generateMonitoring(params)
        for name, resource := range monitoring {
            if err := rsp.SetDesiredComposedResource(
                composed.New(resource).WithName(name),
            ); err != nil {
                return errors.Wrapf(err, "cannot set monitoring resource %s", name)
            }
        }
    }
    
    return nil
}

func (f *Function) generateVPC(params *Parameters) *unstructured.Unstructured {
    vpc := &unstructured.Unstructured{
        Object: map[string]interface{}{
            "apiVersion": "ec2.aws.crossplane.io/v1beta1",
            "kind":       "VPC",
            "metadata": map[string]interface{}{
                "annotations": map[string]interface{}{
                    "crossplane.io/external-name": params.VPCName,
                },
            },
            "spec": map[string]interface{}{
                "forProvider": map[string]interface{}{
                    "region":               params.Region,
                    "cidrBlock":           params.VPCCidr,
                    "enableDnsHostnames":  true,
                    "enableDnsSupport":    true,
                    "instanceTenancy":     "default",
                    "tags": f.generateTags(params, map[string]string{
                        "Type": "VPC",
                    }),
                },
            },
        },
    }
    return vpc
}

func (f *Function) generateSubnets(params *Parameters) []*unstructured.Unstructured {
    var subnets []*unstructured.Unstructured
    
    // Calculate subnet CIDRs
    subnetCidrs := f.calculateSubnetCIDRs(params.VPCCidr, params.SubnetCount)
    
    for i, cidr := range subnetCidrs {
        subnet := &unstructured.Unstructured{
            Object: map[string]interface{}{
                "apiVersion": "ec2.aws.crossplane.io/v1beta1",
                "kind":       "Subnet",
                "spec": map[string]interface{}{
                    "forProvider": map[string]interface{}{
                        "region":            params.Region,
                        "availabilityZone": params.AvailabilityZones[i%len(params.AvailabilityZones)],
                        "cidrBlock":        cidr,
                        "vpcIdSelector": map[string]interface{}{
                            "matchControllerRef": true,
                        },
                        "tags": f.generateTags(params, map[string]string{
                            "Type": "Subnet",
                            "Tier": f.getSubnetTier(i),
                        }),
                    },
                },
            },
        }
        subnets = append(subnets, subnet)
    }
    
    return subnets
}

func (f *Function) generateDatabase(params *Parameters, subnetCount int) *unstructured.Unstructured {
    // Calculate instance type based on workload
    instanceType := f.calculateInstanceType(params)
    
    // Generate database configuration
    db := &unstructured.Unstructured{
        Object: map[string]interface{}{
            "apiVersion": "rds.aws.crossplane.io/v1beta1",
            "kind":       "DBCluster",
            "spec": map[string]interface{}{
                "forProvider": map[string]interface{}{
                    "region":                     params.Region,
                    "engine":                    params.Engine,
                    "engineVersion":             params.EngineVersion,
                    "databaseName":              params.DatabaseName,
                    "masterUsername":            "admin",
                    "autoGeneratePassword":      true,
                    "backupRetentionPeriod":     params.BackupRetention,
                    "preferredBackupWindow":     f.calculateBackupWindow(params.Region),
                    "preferredMaintenanceWindow": f.calculateMaintenanceWindow(params.Region),
                    "storageEncrypted":          true,
                    "enableCloudwatchLogsExports": []string{
                        "postgresql",
                    },
                    "serverlessV2ScalingConfiguration": map[string]interface{}{
                        "maxCapacity": params.MaxCapacity,
                        "minCapacity": params.MinCapacity,
                    },
                    "dbSubnetGroupNameSelector": map[string]interface{}{
                        "matchControllerRef": true,
                    },
                    "vpcSecurityGroupIdSelector": map[string]interface{}{
                        "matchControllerRef": true,
                    },
                },
                "writeConnectionSecretToRef": map[string]interface{}{
                    "namespace": "crossplane-system",
                    "name":      fmt.Sprintf("%s-connection", params.Name),
                },
            },
        },
    }
    
    // Add instances to cluster
    instances := f.generateDBInstances(params, instanceType, subnetCount)
    db.Object["spec"].(map[string]interface{})["forProvider"].(map[string]interface{})["instances"] = instances
    
    return db
}

func (f *Function) generateMonitoring(params *Parameters) map[string]*unstructured.Unstructured {
    monitoring := make(map[string]*unstructured.Unstructured)
    
    // CloudWatch Dashboard
    dashboard := &unstructured.Unstructured{
        Object: map[string]interface{}{
            "apiVersion": "cloudwatch.aws.crossplane.io/v1alpha1",
            "kind":       "Dashboard",
            "spec": map[string]interface{}{
                "forProvider": map[string]interface{}{
                    "region": params.Region,
                    "dashboardBody": f.generateDashboardJSON(params),
                },
            },
        },
    }
    monitoring["dashboard"] = dashboard
    
    // CloudWatch Alarms
    alarms := f.generateAlarms(params)
    for name, alarm := range alarms {
        monitoring[fmt.Sprintf("alarm-%s", name)] = alarm
    }
    
    // SNS Topic for notifications
    topic := &unstructured.Unstructured{
        Object: map[string]interface{}{
            "apiVersion": "sns.aws.crossplane.io/v1beta1",
            "kind":       "Topic",
            "spec": map[string]interface{}{
                "forProvider": map[string]interface{}{
                    "region":      params.Region,
                    "displayName": fmt.Sprintf("%s-alerts", params.Name),
                    "subscriptions": []map[string]interface{}{
                        {
                            "protocol": "email",
                            "endpoint": params.AlertEmail,
                        },
                    },
                },
            },
        },
    }
    monitoring["alert-topic"] = topic
    
    return monitoring
}

// Parameters represents the input parameters for the composition function
type Parameters struct {
    Name              string   `json:"name"`
    Region            string   `json:"region"`
    VPCName           string   `json:"vpcName"`
    VPCCidr           string   `json:"vpcCidr"`
    CreateVPC         bool     `json:"createVPC"`
    SubnetCount       int      `json:"subnetCount"`
    AvailabilityZones []string `json:"availabilityZones"`
    Engine            string   `json:"engine"`
    EngineVersion     string   `json:"engineVersion"`
    DatabaseName      string   `json:"databaseName"`
    InstanceClass     string   `json:"instanceClass"`
    StorageSize       int      `json:"storageSize"`
    MaxCapacity       float64  `json:"maxCapacity"`
    MinCapacity       float64  `json:"minCapacity"`
    BackupRetention   int      `json:"backupRetention"`
    EnableMonitoring  bool     `json:"enableMonitoring"`
    AlertEmail        string   `json:"alertEmail"`
    Tags              map[string]string `json:"tags"`
}
```

### Python Composition Functions
```python
"""
Crossplane Composition Function in Python
"""
import json
import ipaddress
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

import function_sdk as sdk
from function_sdk.proto.v1beta1 import run_function_pb2 as fnv1beta1
from function_sdk.proto.v1beta1 import run_function_pb2_grpc as fnv1beta1_grpc

@dataclass
class NetworkParameters:
    """Parameters for network configuration"""
    vpc_cidr: str = "10.0.0.0/16"
    availability_zones: List[str] = field(default_factory=list)
    public_subnet_count: int = 0
    private_subnet_count: int = 0
    enable_nat_gateway: bool = True
    enable_vpc_flow_logs: bool = True
    
@dataclass
class ComputeParameters:
    """Parameters for compute resources"""
    cluster_name: str = ""
    node_groups: List[Dict[str, Any]] = field(default_factory=list)
    enable_cluster_autoscaler: bool = True
    enable_metrics_server: bool = True
    kubernetes_version: str = "1.27"

class CrossplaneFunction(sdk.Function):
    """
    Crossplane function that generates cloud resources with advanced logic
    """
    
    def run_function(self, req: fnv1beta1.RunFunctionRequest) -> fnv1beta1.RunFunctionResponse:
        """Main function entrypoint"""
        
        # Get the observed composite resource
        observed = sdk.get_observed_composite_resource(req)
        
        # Extract parameters
        network_params = self._extract_network_params(observed)
        compute_params = self._extract_compute_params(observed)
        
        # Generate resources
        resources = []
        
        # Generate network resources
        vpc = self._generate_vpc(network_params)
        resources.append(vpc)
        
        subnets = self._generate_subnets(network_params, vpc)
        resources.extend(subnets)
        
        if network_params.enable_nat_gateway:
            nat_gateways = self._generate_nat_gateways(network_params, subnets)
            resources.extend(nat_gateways)
        
        # Generate compute resources
        if compute_params.cluster_name:
            cluster = self._generate_eks_cluster(compute_params, vpc, subnets)
            resources.append(cluster)
            
            node_groups = self._generate_node_groups(compute_params, cluster, subnets)
            resources.extend(node_groups)
        
        # Create response
        rsp = sdk.Response()
        
        # Add all resources to response
        for resource in resources:
            rsp.set_desired_composed_resource(resource)
        
        # Update composite status
        self._update_composite_status(rsp, resources)
        
        return rsp.to_proto()
    
    def _extract_network_params(self, observed: sdk.ObservedComposite) -> NetworkParameters:
        """Extract network parameters from composite"""
        params = NetworkParameters()
        
        spec = observed.resource.get("spec", {}).get("parameters", {})
        network = spec.get("network", {})
        
        params.vpc_cidr = network.get("vpcCidr", params.vpc_cidr)
        params.availability_zones = network.get("availabilityZones", ["us-west-2a", "us-west-2b"])
        params.public_subnet_count = network.get("publicSubnetCount", 2)
        params.private_subnet_count = network.get("privateSubnetCount", 2)
        params.enable_nat_gateway = network.get("enableNatGateway", True)
        params.enable_vpc_flow_logs = network.get("enableVpcFlowLogs", True)
        
        return params
    
    def _generate_vpc(self, params: NetworkParameters) -> Dict[str, Any]:
        """Generate VPC resource"""
        return {
            "apiVersion": "ec2.aws.crossplane.io/v1beta1",
            "kind": "VPC",
            "metadata": {
                "name": "platform-vpc",
                "annotations": {
                    "crossplane.io/external-name": "platform-vpc"
                }
            },
            "spec": {
                "forProvider": {
                    "region": "us-west-2",
                    "cidrBlock": params.vpc_cidr,
                    "enableDnsHostnames": True,
                    "enableDnsSupport": True,
                    "tags": [
                        {"key": "Name", "value": "platform-vpc"},
                        {"key": "ManagedBy", "value": "crossplane"},
                    ]
                }
            }
        }
    
    def _generate_subnets(self, params: NetworkParameters, 
                         vpc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate subnet resources"""
        subnets = []
        
        # Calculate subnet CIDRs
        vpc_network = ipaddress.ip_network(params.vpc_cidr)
        subnet_prefix = vpc_network.prefixlen + 4  # /20 subnets from /16 VPC
        subnet_iter = vpc_network.subnets(new_prefix=subnet_prefix)
        
        # Public subnets
        for i in range(params.public_subnet_count):
            az = params.availability_zones[i % len(params.availability_zones)]
            subnet_cidr = str(next(subnet_iter))
            
            subnet = {
                "apiVersion": "ec2.aws.crossplane.io/v1beta1",
                "kind": "Subnet",
                "metadata": {
                    "name": f"public-subnet-{i+1}",
                    "labels": {
                        "type": "public",
                        "zone": az
                    }
                },
                "spec": {
                    "forProvider": {
                        "region": "us-west-2",
                        "availabilityZone": az,
                        "cidrBlock": subnet_cidr,
                        "mapPublicIpOnLaunch": True,
                        "vpcIdSelector": {
                            "matchLabels": {
                                "crossplane.io/claim-name": vpc["metadata"]["name"]
                            }
                        },
                        "tags": [
                            {"key": "Name", "value": f"public-subnet-{i+1}"},
                            {"key": "Type", "value": "public"},
                            {"key": "kubernetes.io/role/elb", "value": "1"}
                        ]
                    }
                }
            }
            subnets.append(subnet)
        
        # Private subnets
        for i in range(params.private_subnet_count):
            az = params.availability_zones[i % len(params.availability_zones)]
            subnet_cidr = str(next(subnet_iter))
            
            subnet = {
                "apiVersion": "ec2.aws.crossplane.io/v1beta1",
                "kind": "Subnet",
                "metadata": {
                    "name": f"private-subnet-{i+1}",
                    "labels": {
                        "type": "private",
                        "zone": az
                    }
                },
                "spec": {
                    "forProvider": {
                        "region": "us-west-2",
                        "availabilityZone": az,
                        "cidrBlock": subnet_cidr,
                        "vpcIdSelector": {
                            "matchLabels": {
                                "crossplane.io/claim-name": vpc["metadata"]["name"]
                            }
                        },
                        "tags": [
                            {"key": "Name", "value": f"private-subnet-{i+1}"},
                            {"key": "Type", "value": "private"},
                            {"key": "kubernetes.io/role/internal-elb", "value": "1"}
                        ]
                    }
                }
            }
            subnets.append(subnet)
        
        return subnets
    
    def _generate_eks_cluster(self, params: ComputeParameters, 
                             vpc: Dict[str, Any], 
                             subnets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate EKS cluster resource"""
        
        # Filter private subnets for EKS
        private_subnet_ids = [
            s["metadata"]["name"] 
            for s in subnets 
            if s["metadata"]["labels"]["type"] == "private"
        ]
        
        cluster = {
            "apiVersion": "eks.aws.crossplane.io/v1beta1",
            "kind": "Cluster",
            "metadata": {
                "name": params.cluster_name,
                "annotations": {
                    "crossplane.io/external-name": params.cluster_name
                }
            },
            "spec": {
                "forProvider": {
                    "region": "us-west-2",
                    "version": params.kubernetes_version,
                    "roleArnSelector": {
                        "matchLabels": {
                            "role": "eks-cluster"
                        }
                    },
                    "resourcesVpcConfig": {
                        "endpointPrivateAccess": True,
                        "endpointPublicAccess": True,
                        "publicAccessCidrs": ["0.0.0.0/0"],
                        "subnetIdSelector": {
                            "matchLabels": {
                                "type": "private"
                            }
                        }
                    },
                    "logging": {
                        "clusterLogging": [
                            {
                                "enabled": True,
                                "types": ["api", "audit", "authenticator", 
                                         "controllerManager", "scheduler"]
                            }
                        ]
                    },
                    "tags": {
                        "Name": params.cluster_name,
                        "ManagedBy": "crossplane"
                    }
                }
            }
        }
        
        return cluster
    
    def _generate_node_groups(self, params: ComputeParameters,
                             cluster: Dict[str, Any],
                             subnets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate EKS node group resources"""
        node_groups = []
        
        for ng_config in params.node_groups:
            node_group = {
                "apiVersion": "eks.aws.crossplane.io/v1alpha1",
                "kind": "NodeGroup",
                "metadata": {
                    "name": ng_config["name"]
                },
                "spec": {
                    "forProvider": {
                        "region": "us-west-2",
                        "clusterNameSelector": {
                            "matchLabels": {
                                "crossplane.io/claim-name": cluster["metadata"]["name"]
                            }
                        },
                        "nodeRole": {
                            "matchLabels": {
                                "role": "eks-node"
                            }
                        },
                        "subnetSelector": {
                            "matchLabels": {
                                "type": "private"
                            }
                        },
                        "scalingConfig": {
                            "desiredSize": ng_config.get("desiredSize", 2),
                            "maxSize": ng_config.get("maxSize", 10),
                            "minSize": ng_config.get("minSize", 1)
                        },
                        "instanceTypes": ng_config.get("instanceTypes", ["m5.large"]),
                        "amiType": ng_config.get("amiType", "AL2_x86_64"),
                        "diskSize": ng_config.get("diskSize", 100),
                        "labels": ng_config.get("labels", {}),
                        "tags": {
                            "Name": ng_config["name"],
                            "NodeGroup": ng_config["name"]
                        }
                    }
                }
            }
            
            node_groups.append(node_group)
        
        return node_groups

def main():
    """Main entrypoint"""
    fn = CrossplaneFunction()
    sdk.serve(fn)

if __name__ == "__main__":
    main()
```

## Practical Examples

### Multi-Cloud Database Platform
```yaml
# Configuration Package for multi-cloud database platform
apiVersion: meta.pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: platform-ref-multi-cloud
spec:
  package: xpkg.upbound.io/platform-ref-multi-cloud:v0.1.0
  revisionActivationPolicy: Automatic
  revisionHistoryLimit: 1
---
# Multi-cloud PostgreSQL XRD
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xpostgresqldatabases.platform.io
spec:
  group: platform.io
  names:
    kind: XPostgreSQLDatabase
    plural: xpostgresqldatabases
  claimNames:
    kind: PostgreSQLDatabase
    plural: postgresqldatabases
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              parameters:
                type: object
                properties:
                  provider:
                    type: string
                    enum: ["aws", "azure", "gcp"]
                  region:
                    type: string
                  version:
                    type: string
                    default: "14"
                  size:
                    type: string
                    enum: ["small", "medium", "large", "xlarge"]
                  highAvailability:
                    type: boolean
                    default: false
                  backup:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      retentionDays:
                        type: integer
                        default: 7
                  monitoring:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      alertEmail:
                        type: string
                required: ["provider", "region", "size"]
---
# AWS Implementation
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xpostgresqldatabases.aws.platform.io
  labels:
    provider: aws
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XPostgreSQLDatabase
  
  functions:
  - name: patch-and-transform
    type: Container
    container:
      image: xpkg.upbound.io/crossplane-contrib/function-patch-and-transform:v0.1.4
      
  resources:
  # RDS Instance
  - name: rds-instance
    base:
      apiVersion: database.aws.crossplane.io/v1beta1
      kind: DBInstance
      spec:
        forProvider:
          engine: postgres
          autoGeneratePassword: true
          masterUsername: postgres
          publiclyAccessible: false
          storageEncrypted: true
          deletionProtection: true
          enablePerformanceInsights: true
          performanceInsightsRetentionPeriod: 7
    patches:
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.region"
    - fromFieldPath: "spec.parameters.version"
      toFieldPath: "spec.forProvider.engineVersion"
      transforms:
      - type: string
        string:
          fmt: "%s.0"
    - fromFieldPath: "spec.parameters.size"
      toFieldPath: "spec.forProvider.dbInstanceClass"
      transforms:
      - type: map
        map:
          small: db.t3.micro
          medium: db.t3.medium
          large: db.r6g.large
          xlarge: db.r6g.xlarge
    - fromFieldPath: "spec.parameters.highAvailability"
      toFieldPath: "spec.forProvider.multiAZ"
    - fromFieldPath: "spec.parameters.backup.retentionDays"
      toFieldPath: "spec.forProvider.backupRetentionPeriod"
    
  # CloudWatch Alarms
  - name: cpu-alarm
    base:
      apiVersion: cloudwatch.aws.crossplane.io/v1alpha1
      kind: Alarm
      spec:
        forProvider:
          alarmDescription: "RDS CPU utilization"
          metricName: CPUUtilization
          namespace: AWS/RDS
          statistic: Average
          period: 300
          evaluationPeriods: 2
          threshold: 80
          comparisonOperator: GreaterThanThreshold
    patches:
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.region"
    - fromFieldPath: "spec.parameters.monitoring.enabled"
      toFieldPath: "spec.forProvider.actionsEnabled"
    
  # Parameter Group
  - name: parameter-group
    base:
      apiVersion: database.aws.crossplane.io/v1beta1
      kind: DBParameterGroup
      spec:
        forProvider:
          dbParameterGroupFamily: postgres14
          description: "Custom parameter group for PostgreSQL"
          parameters:
          - parameterName: shared_preload_libraries
            parameterValue: pg_stat_statements
          - parameterName: log_statement
            parameterValue: all
          - parameterName: log_min_duration_statement
            parameterValue: "1000"
    patches:
    - fromFieldPath: "spec.parameters.version"
      toFieldPath: "spec.forProvider.dbParameterGroupFamily"
      transforms:
      - type: string
        string:
          fmt: "postgres%s"
---
# Azure Implementation
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xpostgresqldatabases.azure.platform.io
  labels:
    provider: azure
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XPostgreSQLDatabase
    
  resources:
  # Azure Database for PostgreSQL
  - name: azure-postgresql
    base:
      apiVersion: database.azure.upbound.io/v1beta1
      kind: PostgreSQLServer
      spec:
        forProvider:
          skuName: B_Gen5_1
          version: "11"
          storageMb: 5120
          administratorLogin: psqladmin
          autoGeneratePassword: true
          publicNetworkAccessEnabled: false
          sslEnforcementEnabled: true
          sslMinimalTlsVersionEnforced: "TLS1_2"
          geoRedundantBackupEnabled: false
    patches:
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.location"
    - fromFieldPath: "spec.parameters.version"
      toFieldPath: "spec.forProvider.version"
    - fromFieldPath: "spec.parameters.size"
      toFieldPath: "spec.forProvider.skuName"
      transforms:
      - type: map
        map:
          small: B_Gen5_1
          medium: GP_Gen5_2
          large: GP_Gen5_4
          xlarge: GP_Gen5_8
    - fromFieldPath: "spec.parameters.highAvailability"
      toFieldPath: "spec.forProvider.geoRedundantBackupEnabled"
    
  # Firewall Rules
  - name: firewall-rule
    base:
      apiVersion: database.azure.upbound.io/v1beta1
      kind: PostgreSQLFirewallRule
      spec:
        forProvider:
          serverNameSelector:
            matchControllerRef: true
          startIpAddress: 0.0.0.0
          endIpAddress: 0.0.0.0
    patches:
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.location"
---
# GCP Implementation
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xpostgresqldatabases.gcp.platform.io
  labels:
    provider: gcp
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XPostgreSQLDatabase
    
  resources:
  # Cloud SQL Instance
  - name: cloudsql-instance
    base:
      apiVersion: database.gcp.upbound.io/v1beta1
      kind: DatabaseInstance
      spec:
        forProvider:
          databaseVersion: POSTGRES_14
          deletionProtection: true
          settings:
          - tier: db-f1-micro
            diskSize: 10
            diskType: PD_SSD
            ipConfiguration:
            - ipv4Enabled: false
              privateNetwork: projects/PROJECT_ID/global/networks/default
            backupConfiguration:
            - enabled: true
              startTime: "03:00"
            databaseFlags:
            - name: max_connections
              value: "100"
    patches:
    - fromFieldPath: "spec.parameters.region"
      toFieldPath: "spec.forProvider.region"
    - fromFieldPath: "spec.parameters.version"
      toFieldPath: "spec.forProvider.databaseVersion"
      transforms:
      - type: string
        string:
          fmt: "POSTGRES_%s"
    - fromFieldPath: "spec.parameters.size"
      toFieldPath: "spec.forProvider.settings[0].tier"
      transforms:
      - type: map
        map:
          small: db-f1-micro
          medium: db-g1-small
          large: db-n1-standard-1
          xlarge: db-n1-standard-2
```

### GitOps Platform Configuration
```yaml
# ArgoCD Application for Crossplane
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: crossplane-system
  namespace: argocd
spec:
  project: infrastructure
  source:
    repoURL: https://github.com/company/infrastructure
    path: crossplane/system
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: crossplane-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
---
# Crossplane Provider Configuration via GitOps
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: crossplane-providers
  namespace: argocd
spec:
  project: infrastructure
  source:
    repoURL: https://github.com/company/infrastructure
    path: crossplane/providers
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: false
      selfHeal: true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
---
# Platform APIs via GitOps
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: platform-apis
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: https://github.com/company/platform-apis
    path: apis
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
# Tenant Resources
apiVersion: v1
kind: Namespace
metadata:
  name: team-alpha
  labels:
    team: alpha
    environment: production
---
# RBAC for tenant
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: crossplane-user
  namespace: team-alpha
rules:
- apiGroups: ["platform.io"]
  resources: ["postgresqldatabases", "redisclusters", "messagingqueues"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
---
# NetworkPolicy for tenant isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: team-alpha
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: team-alpha
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: team-alpha
  - to:
    - namespaceSelector:
        matchLabels:
          name: crossplane-system
    ports:
    - protocol: TCP
      port: 443
```

### Self-Service Developer Platform
```yaml
# Developer Portal Backend
apiVersion: v1
kind: ConfigMap
metadata:
  name: backstage-app-config
  namespace: backstage
data:
  app-config.yaml: |
    app:
      title: Internal Developer Platform
      baseUrl: https://portal.company.com
    
    backend:
      baseUrl: https://portal.company.com
      
    catalog:
      import:
        entityFilename: catalog-info.yaml
        pullRequestBranchName: backstage-integration
      rules:
        - allow: [Component, System, API, Resource, Location]
      locations:
        - type: url
          target: https://github.com/company/platform-apis/blob/main/catalog-info.yaml
    
    integrations:
      github:
        - host: github.com
          token: ${GITHUB_TOKEN}
    
    proxy:
      '/crossplane':
        target: 'http://crossplane-api.crossplane-system:8080'
        headers:
          Authorization: Bearer ${CROSSPLANE_TOKEN}
    
    crossplane:
      providers:
        - name: aws
          regions: ['us-east-1', 'us-west-2', 'eu-west-1']
        - name: azure
          regions: ['eastus', 'westus', 'westeurope']
        - name: gcp
          regions: ['us-central1', 'europe-west1']
---
# Backstage Template for Database
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: postgresql-database
  title: PostgreSQL Database
  description: Create a PostgreSQL database instance
  tags:
    - database
    - postgresql
    - crossplane
spec:
  owner: platform-team
  type: resource
  parameters:
    - title: Basic Information
      required:
        - name
        - owner
      properties:
        name:
          title: Name
          type: string
          description: Unique name for this database
          pattern: '^[a-z0-9-]+$'
        owner:
          title: Owner
          type: string
          description: Owner of this database
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: Group
    
    - title: Database Configuration
      required:
        - provider
        - region
        - size
      properties:
        provider:
          title: Cloud Provider
          type: string
          enum:
            - aws
            - azure
            - gcp
          enumNames:
            - Amazon Web Services
            - Microsoft Azure
            - Google Cloud Platform
        region:
          title: Region
          type: string
          description: Deployment region
          enum: []
          enumNames: []
        size:
          title: Instance Size
          type: string
          default: small
          enum:
            - small
            - medium
            - large
            - xlarge
          enumNames:
            - Small (1-2 vCPU, 2-4GB RAM)
            - Medium (2-4 vCPU, 4-8GB RAM)
            - Large (4-8 vCPU, 16-32GB RAM)
            - Extra Large (8+ vCPU, 32+ GB RAM)
        version:
          title: PostgreSQL Version
          type: string
          default: "14"
          enum: ["12", "13", "14", "15"]
        highAvailability:
          title: High Availability
          type: boolean
          default: false
        backup:
          title: Backup Configuration
          type: object
          properties:
            enabled:
              title: Enable Backups
              type: boolean
              default: true
            retentionDays:
              title: Retention Days
              type: integer
              default: 7
              minimum: 1
              maximum: 35
    
    - title: Monitoring
      properties:
        monitoring:
          title: Monitoring Configuration
          type: object
          properties:
            enabled:
              title: Enable Monitoring
              type: boolean
              default: true
            alertEmail:
              title: Alert Email
              type: string
              format: email
  
  steps:
    - id: fetch
      name: Fetch Base
      action: fetch:template
      input:
        url: ./content
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          provider: ${{ parameters.provider }}
          region: ${{ parameters.region }}
          size: ${{ parameters.size }}
          version: ${{ parameters.version }}
          highAvailability: ${{ parameters.highAvailability }}
          backup: ${{ parameters.backup }}
          monitoring: ${{ parameters.monitoring }}
    
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        description: |
          Create PostgreSQL database ${{ parameters.name }}
        repoUrl: github.com?owner=company&repo=infrastructure-requests
        branchName: create-db-${{ parameters.name }}
        title: 'feat: create PostgreSQL database ${{ parameters.name }}'
        gitCommitMessage: 'feat: create PostgreSQL database ${{ parameters.name }}'
    
    - id: create-claim
      name: Create Crossplane Claim
      action: http:backstage:request
      input:
        method: POST
        path: /proxy/crossplane/claims
        headers:
          Content-Type: application/json
        body:
          apiVersion: platform.io/v1alpha1
          kind: PostgreSQLDatabase
          metadata:
            name: ${{ parameters.name }}
            namespace: ${{ parameters.owner }}
            labels:
              backstage.io/entity-ref: ${{ parameters.name }}
          spec:
            parameters:
              provider: ${{ parameters.provider }}
              region: ${{ parameters.region }}
              size: ${{ parameters.size }}
              version: ${{ parameters.version }}
              highAvailability: ${{ parameters.highAvailability }}
              backup: ${{ parameters.backup }}
              monitoring: ${{ parameters.monitoring }}
    
    - id: register
      name: Register in Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'
  
  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Pull Request
        url: ${{ steps.publish.output.pullRequestUrl }}
      - title: Database Status
        url: https://portal.company.com/catalog/default/resource/${{ parameters.name }}
```

## Best Practices

### 1. Composition Design
```yaml
# Well-structured composition with clear separation of concerns
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xapplication.platform.io
  labels:
    platform.io/maturity: stable
    platform.io/version: v1.2.0
spec:
  # Composition metadata
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XApplication
  
  # Environment configuration
  environment:
    environmentConfigs:
    - type: Reference
      ref:
        name: aws-environment
    - type: Selector
      selector:
        matchLabels:
          - key: region
            type: FromCompositeFieldPath
            valueFromFieldPath: spec.parameters.region
  
  # Patch sets for reusability
  patchSets:
  - name: common-parameters
    patches:
    - type: FromCompositeFieldPath
      fromFieldPath: metadata.labels
      toFieldPath: metadata.labels
      policy:
        mergeOptions:
          keepMapValues: true
    - type: FromCompositeFieldPath
      fromFieldPath: spec.parameters.region
      toFieldPath: spec.forProvider.region
    - type: FromCompositeFieldPath
      fromFieldPath: metadata.annotations[crossplane.io/external-name]
      toFieldPath: metadata.annotations[crossplane.io/external-name]
  
  - name: connection-details
    patches:
    - type: FromConnectionSecretKey
      fromConnectionSecretKey: endpoint
      toConnectionSecretKey: endpoint
    - type: FromConnectionSecretKey
      fromConnectionSecretKey: username
      toConnectionSecretKey: username
    - type: FromConnectionSecretKey
      fromConnectionSecretKey: password
      toConnectionSecretKey: password
  
  # Function pipeline
  functions:
  - name: validate-inputs
    type: Container
    container:
      image: xpkg.upbound.io/platform/function-validate:v0.1.0
      timeout: 30s
  
  - name: auto-ready
    type: Container
    container:
      image: xpkg.upbound.io/crossplane-contrib/function-auto-ready:v0.2.0
  
  resources:
  # Resources with proper dependencies and references
  - name: network
    readinessChecks:
    - type: MatchString
      fieldPath: status.atProvider.state
      matchString: available
    patches:
    - type: PatchSet
      patchSetName: common-parameters
```

### 2. Testing Infrastructure
```yaml
# Kuttl test for Crossplane compositions
apiVersion: kuttl.dev/v1beta1
kind: TestSuite
metadata:
  name: crossplane-platform-tests
testDirs:
- tests/e2e
timeout: 300
parallel: 3
---
# tests/e2e/01-database/00-install.yaml
apiVersion: platform.io/v1alpha1
kind: PostgreSQLDatabase
metadata:
  name: test-database
  namespace: default
spec:
  parameters:
    provider: aws
    region: us-east-1
    size: small
    version: "14"
---
# tests/e2e/01-database/01-assert.yaml
apiVersion: database.aws.crossplane.io/v1beta1
kind: DBInstance
metadata:
  labels:
    crossplane.io/claim-name: test-database
    crossplane.io/claim-namespace: default
spec:
  forProvider:
    region: us-east-1
    engine: postgres
    engineVersion: "14.0"
    dbInstanceClass: db.t3.micro
status:
  conditions:
  - type: Ready
    status: "True"
---
# Unit tests for composition functions
package main

import (
    "testing"
    
    "github.com/crossplane/function-sdk-go/resource"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestGenerateVPC(t *testing.T) {
    tests := []struct {
        name     string
        params   Parameters
        expected map[string]interface{}
    }{
        {
            name: "standard VPC",
            params: Parameters{
                Region:  "us-west-2",
                VPCCidr: "10.0.0.0/16",
                VPCName: "test-vpc",
            },
            expected: map[string]interface{}{
                "apiVersion": "ec2.aws.crossplane.io/v1beta1",
                "kind":       "VPC",
                "spec": map[string]interface{}{
                    "forProvider": map[string]interface{}{
                        "region":    "us-west-2",
                        "cidrBlock": "10.0.0.0/16",
                    },
                },
            },
        },
    }
    
    fn := &Function{}
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := fn.generateVPC(tt.params)
            assert.Equal(t, tt.expected["apiVersion"], result.Object["apiVersion"])
            assert.Equal(t, tt.expected["kind"], result.Object["kind"])
        })
    }
}
```

### 3. Security and RBAC
```yaml
# Provider security configuration
apiVersion: v1
kind: ServiceAccount
metadata:
  name: provider-aws
  namespace: crossplane-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/crossplane-provider-aws
---
# IRSA configuration for AWS provider
apiVersion: aws.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: aws-provider
spec:
  credentials:
    source: IRSA
---
# Fine-grained RBAC for platform users
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: platform-user
rules:
# Read access to all platform APIs
- apiGroups: ["platform.io"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
# Create/update/delete for claims only
- apiGroups: ["platform.io"]
  resources: ["postgresqldatabases", "applications", "clusters"]
  verbs: ["create", "update", "patch", "delete"]
# No access to compositions or XRs
- apiGroups: ["apiextensions.crossplane.io"]
  resources: ["compositions", "compositeresourcedefinitions"]
  verbs: []
---
# Network policies for provider isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: provider-isolation
  namespace: crossplane-system
spec:
  podSelector:
    matchLabels:
      pkg.crossplane.io/provider: aws
  policyTypes:
  - Egress
  egress:
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
  # Allow AWS API access
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
    ports:
    - protocol: TCP
      port: 443
```

### 4. Monitoring and Observability
```yaml
# Prometheus monitoring for Crossplane
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: crossplane
  namespace: crossplane-system
spec:
  selector:
    matchLabels:
      app: crossplane
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
---
# Grafana dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: crossplane-dashboard
  namespace: monitoring
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Crossplane Platform Overview",
        "panels": [
          {
            "title": "Managed Resources by Type",
            "targets": [
              {
                "expr": "sum by (group, kind) (crossplane_managed_resource_exists)"
              }
            ]
          },
          {
            "title": "Resource Sync Errors",
            "targets": [
              {
                "expr": "sum by (group, kind) (rate(crossplane_managed_resource_sync_error_total[5m]))"
              }
            ]
          },
          {
            "title": "Composition Function Execution Time",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, crossplane_composition_function_duration_seconds)"
              }
            ]
          }
        ]
      }
    }
---
# Alerts for platform health
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: crossplane-alerts
  namespace: crossplane-system
spec:
  groups:
  - name: crossplane.rules
    interval: 30s
    rules:
    - alert: CrossplaneManagedResourceError
      expr: |
        sum by (namespace, kind, name) (
          crossplane_managed_resource_exists{condition_type="Ready", condition_status!="True"}
        ) > 0
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Managed resource {{ $labels.kind }}/{{ $labels.name }} is not ready"
    
    - alert: CrossplaneProviderUnhealthy
      expr: |
        up{job="crossplane-providers"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Crossplane provider {{ $labels.instance }} is down"
```

### 5. Cost Optimization
```yaml
# Composition with cost optimization features
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xworkloads.cost-optimized.platform.io
spec:
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XWorkload
  
  resources:
  # Spot instance configuration
  - name: compute-spot
    base:
      apiVersion: ec2.aws.crossplane.io/v1beta1
      kind: LaunchTemplate
      spec:
        forProvider:
          launchTemplateData:
            instanceMarketOptions:
              marketType: spot
              spotOptions:
                maxPrice: "0.05"
                spotInstanceType: one-time
                instanceInterruptionBehavior: terminate
    patches:
    - fromFieldPath: "spec.parameters.spotEnabled"
      toFieldPath: "spec.forProvider.launchTemplateData.instanceMarketOptions.marketType"
      transforms:
      - type: map
        map:
          true: spot
          false: ""
  
  # Autoscaling with cost awareness
  - name: autoscaling
    base:
      apiVersion: autoscaling.aws.crossplane.io/v1alpha1
      kind: AutoScalingGroup
      spec:
        forProvider:
          mixedInstancesPolicy:
            instancesDistribution:
              onDemandPercentageAboveBaseCapacity: 20
              spotAllocationStrategy: capacity-optimized
            launchTemplate:
              overrides:
              - instanceType: t3.medium
                weightedCapacity: 1
              - instanceType: t3a.medium
                weightedCapacity: 1
              - instanceType: t4g.medium
                weightedCapacity: 0.8
  
  # Scheduled scaling for non-production
  - name: scheduled-scaling
    base:
      apiVersion: autoscaling.aws.crossplane.io/v1alpha1
      kind: ScheduledAction
      spec:
        forProvider:
          schedule: "0 19 * * MON-FRI"
          minSize: 0
          maxSize: 0
    patches:
    - fromFieldPath: "spec.parameters.environment"
      toFieldPath: "spec.forProvider.schedule"
      transforms:
      - type: map
        map:
          production: ""
          development: "0 19 * * MON-FRI"
          staging: "0 19 * * MON-FRI"
```

## Integration Patterns

### 1. CI/CD Integration
```yaml
# GitHub Actions workflow
name: Crossplane Validation
on:
  pull_request:
    paths:
    - 'apis/**'
    - 'compositions/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Crossplane CLI
      run: |
        curl -sL https://raw.githubusercontent.com/crossplane/crossplane/release-1.13/install.sh | sh
        sudo mv crossplane /usr/local/bin
    
    - name: Validate XRDs
      run: |
        for xrd in apis/*.yaml; do
          echo "Validating $xrd"
          crossplane beta validate $xrd
        done
    
    - name: Validate Compositions
      run: |
        for comp in compositions/*.yaml; do
          echo "Validating $comp"
          crossplane beta validate $comp
        done
    
    - name: Render Compositions
      run: |
        for comp in compositions/*.yaml; do
          echo "Rendering $comp"
          crossplane beta render $comp examples/claim.yaml
        done
    
    - name: Run Composition Tests
      run: |
        go test ./functions/... -v
    
    - name: Build Function Images
      run: |
        for fn in functions/*; do
          if [ -d "$fn" ]; then
            echo "Building $fn"
            docker build -t ghcr.io/${{ github.repository }}/$fn:${{ github.sha }} $fn
          fi
        done

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy security scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'config'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### 2. Terraform Provider Integration
```yaml
# Use Terraform Provider in Crossplane
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.9.0
---
# Terraform Workspace
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: example-terraform
spec:
  forProvider:
    source: Inline
    module: |
      resource "random_id" "example" {
        byte_length = 4
      }
      
      module "vpc" {
        source  = "terraform-aws-modules/vpc/aws"
        version = "5.0.0"
        
        name = "crossplane-vpc-${random_id.example.hex}"
        cidr = var.vpc_cidr
        
        azs             = var.availability_zones
        private_subnets = var.private_subnets
        public_subnets  = var.public_subnets
        
        enable_nat_gateway = true
        enable_vpn_gateway = true
        
        tags = var.tags
      }
      
      output "vpc_id" {
        value = module.vpc.vpc_id
      }
      
      output "private_subnet_ids" {
        value = module.vpc.private_subnets
      }
    vars:
    - key: vpc_cidr
      value: "10.0.0.0/16"
    - key: availability_zones
      value: '["us-west-2a", "us-west-2b", "us-west-2c"]'
    - key: private_subnets
      value: '["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]'
    - key: public_subnets
      value: '["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]'
  writeConnectionSecretToRef:
    namespace: crossplane-system
    name: terraform-vpc-outputs
```

### 3. Service Mesh Integration
```yaml
# Crossplane with Istio service mesh
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xmicroservice.istio.platform.io
spec:
  compositeTypeRef:
    apiVersion: platform.io/v1alpha1
    kind: XMicroservice
    
  resources:
  # Namespace with Istio injection
  - name: namespace
    base:
      apiVersion: v1
      kind: Namespace
      metadata:
        labels:
          istio-injection: enabled
    patches:
    - fromFieldPath: "metadata.name"
      toFieldPath: "metadata.name"
      transforms:
      - type: string
        string:
          fmt: "%s-namespace"
  
  # Virtual Service
  - name: virtual-service
    base:
      apiVersion: networking.istio.io/v1beta1
      kind: VirtualService
      spec:
        hosts:
        - "*"
        gateways:
        - istio-system/main-gateway
        http:
        - match:
          - uri:
              prefix: "/"
          route:
          - destination:
              host: service
              port:
                number: 80
            weight: 100
    patches:
    - fromFieldPath: "spec.parameters.routing.path"
      toFieldPath: "spec.http[0].match[0].uri.prefix"
    - fromFieldPath: "metadata.name"
      toFieldPath: "spec.http[0].route[0].destination.host"
      transforms:
      - type: string
        string:
          fmt: "%s-service"
  
  # Destination Rule with circuit breaking
  - name: destination-rule
    base:
      apiVersion: networking.istio.io/v1beta1
      kind: DestinationRule
      spec:
        trafficPolicy:
          connectionPool:
            tcp:
              maxConnections: 100
            http:
              http1MaxPendingRequests: 100
              http2MaxRequests: 100
          outlierDetection:
            consecutiveErrors: 5
            interval: 30s
            baseEjectionTime: 30s
            maxEjectionPercent: 50
    patches:
    - fromFieldPath: "metadata.name"
      toFieldPath: "spec.host"
      transforms:
      - type: string
        string:
          fmt: "%s-service"
  
  # Service Entry for external dependencies
  - name: service-entry
    base:
      apiVersion: networking.istio.io/v1beta1
      kind: ServiceEntry
      spec:
        location: MESH_EXTERNAL
        ports:
        - number: 443
          name: https
          protocol: HTTPS
        resolution: DNS
    patches:
    - fromFieldPath: "spec.parameters.externalDependencies"
      toFieldPath: "spec.hosts"
```

### 4. Policy Engine Integration
```yaml
# OPA Gatekeeper integration
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8scrossplanerequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sCrossplaneRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8scrossplanerequiredlabels
        
        violation[{"msg": msg}] {
          input.review.kind.group == "platform.io"
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
---
# Constraint to enforce labels
apiVersion: templates.gatekeeper.sh/v1beta1
kind: K8sCrossplaneRequiredLabels
metadata:
  name: must-have-team
spec:
  match:
    kinds:
    - apiGroups: ["platform.io"]
      kinds: ["PostgreSQLDatabase", "Application", "Cluster"]
  parameters:
    labels: ["team", "environment", "cost-center"]
```

## Troubleshooting

### Common Issues

1. **Provider Not Ready**
```bash
# Check provider status
kubectl get providers.pkg.crossplane.io
kubectl describe provider.pkg.crossplane.io provider-aws

# Check provider pods
kubectl get pods -n crossplane-system -l pkg.crossplane.io/provider=provider-aws
kubectl logs -n crossplane-system -l pkg.crossplane.io/provider=provider-aws

# Common fixes
# 1. Check IRSA/Workload Identity configuration
# 2. Verify provider credentials
# 3. Check resource quotas
```

2. **Composition Not Working**
```bash
# Debug composition
kubectl describe composition xpostgresqldatabases.aws.platform.io

# Check XR status
kubectl get xpostgresqldatabase -o wide
kubectl describe xpostgresqldatabase my-database

# View composed resources
kubectl get managed -l crossplane.io/claim-name=my-database

# Common issues:
# - Patch paths incorrect
# - Required fields missing
# - Provider config not found
```

3. **Resource Sync Errors**
```bash
# Check events
kubectl get events --sort-by='.lastTimestamp' | grep my-resource

# Enable debug logging
kubectl edit deployment crossplane -n crossplane-system
# Add --debug to args

# Check provider logs with debug
kubectl logs -n crossplane-system -l pkg.crossplane.io/provider=provider-aws -f
```

### Debug Techniques

1. **Composition Rendering**
```bash
# Render composition locally
crossplane beta render composition.yaml claim.yaml

# Trace composition patches
crossplane beta trace claim.yaml -o wide
```

2. **Connection Secrets**
```bash
# Check if connection secret was created
kubectl get secrets -n crossplane-system -l crossplane.io/claim-name=my-database

# Decode connection details
kubectl get secret my-database-connection -n crossplane-system -o jsonpath='{.data.username}' | base64 -d
```

3. **RBAC Issues**
```bash
# Test RBAC
kubectl auth can-i create postgresqldatabases.platform.io --as=developer

# View provider service account permissions
kubectl get clusterrolebinding -o wide | grep provider
```

## Performance Optimization

### 1. Provider Configuration
```yaml
# Optimize provider performance
apiVersion: pkg.crossplane.io/v1alpha1
kind: ControllerConfig
metadata:
  name: provider-aws-config
spec:
  replicas: 3
  args:
  - --max-reconcile-rate=100
  - --poll-interval=30s
  - --sync-period=30m
  resources:
    requests:
      cpu: 1
      memory: 2Gi
    limits:
      cpu: 2
      memory: 4Gi
  envFrom:
  - configMapRef:
      name: provider-config
```

### 2. Composition Optimization
```yaml
# Use readiness checks efficiently
resources:
- name: database
  readinessChecks:
  - type: MatchString
    fieldPath: status.atProvider.dbInstanceStatus
    matchString: available
  - type: None  # Skip for faster provisioning when safe
```

## Conclusion

Crossplane revolutionizes infrastructure management by bringing Kubernetes-native patterns to cloud resources. Its composition model, combined with strong typing and policy enforcement, enables platform teams to build powerful self-service infrastructure platforms.

Key advantages include:
- True Kubernetes-native experience
- Multi-cloud abstraction without lowest common denominator
- Powerful composition and transformation engine
- Strong GitOps integration
- Extensible through providers and functions

Whether building internal developer platforms, managing multi-cloud infrastructure, or enabling self-service infrastructure, Crossplane provides the foundation for modern cloud-native infrastructure management.