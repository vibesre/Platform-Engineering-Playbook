# Oracle Cloud Infrastructure (OCI) Technical Documentation

## Overview

Oracle Cloud Infrastructure (OCI) is a comprehensive cloud platform offering high-performance computing, storage, networking, and database services. Built from the ground up for enterprise workloads, OCI provides a unique architecture with off-box virtualization, bare metal offerings, and deep integration with Oracle's extensive software portfolio.

## Core Services

### Compute Services

#### Compute Instances
```bash
# Create a compute instance using OCI CLI
oci compute instance launch \
  --compartment-id ocid1.compartment.oc1..aaa \
  --availability-domain "AD-1" \
  --shape "VM.Standard.E4.Flex" \
  --shape-config '{"ocpus":2,"memoryInGBs":16}' \
  --image-id ocid1.image.oc1.iad.aaa \
  --subnet-id ocid1.subnet.oc1.iad.aaa \
  --display-name "production-app-server" \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub
```

#### Bare Metal Instances
```python
import oci

# Configure OCI client
config = oci.config.from_file()
compute_client = oci.core.ComputeClient(config)

def launch_bare_metal_instance():
    """Launch a bare metal instance for high-performance workloads"""
    launch_instance_details = oci.core.models.LaunchInstanceDetails(
        compartment_id="ocid1.compartment.oc1..aaa",
        availability_domain="AD-1",
        shape="BM.Standard.E4.128",
        display_name="oracle-db-bare-metal",
        source_details=oci.core.models.InstanceSourceViaImageDetails(
            image_id="ocid1.image.oc1.iad.aaa",
            source_type="image"
        ),
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id="ocid1.subnet.oc1.iad.aaa",
            display_name="primary-vnic",
            assign_public_ip=True
        ),
        metadata={
            "ssh_authorized_keys": open("~/.ssh/id_rsa.pub").read()
        }
    )
    
    response = compute_client.launch_instance(launch_instance_details)
    return response.data
```

#### Container Engine for Kubernetes (OKE)
```yaml
# OKE cluster deployment
apiVersion: containerengine.oracle.com/v1
kind: Cluster
metadata:
  name: production-cluster
spec:
  compartmentId: ocid1.compartment.oc1..aaa
  vcnId: ocid1.vcn.oc1.iad.aaa
  kubernetesVersion: "v1.27.2"
  options:
    serviceLbSubnetIds:
      - ocid1.subnet.oc1.iad.aaa
    addOns:
      isKubernetesDashboardEnabled: true
      isTillerEnabled: false
  nodeShape: VM.Standard.E4.Flex
  nodeShapeConfig:
    ocpus: 4
    memoryInGBs: 32
  nodeSourceDetails:
    imageId: ocid1.image.oc1.iad.aaa
    sourceType: IMAGE
```

### Storage Services

#### Object Storage
```python
import oci
import os

class OCIObjectStorage:
    """Oracle Cloud Object Storage management"""
    
    def __init__(self, config_file="~/.oci/config"):
        self.config = oci.config.from_file(config_file)
        self.object_storage = oci.object_storage.ObjectStorageClient(self.config)
        self.namespace = self.object_storage.get_namespace().data
    
    def create_bucket(self, bucket_name, compartment_id, storage_tier="Standard"):
        """Create an Object Storage bucket"""
        request = oci.object_storage.models.CreateBucketDetails(
            name=bucket_name,
            compartment_id=compartment_id,
            storage_tier=storage_tier,
            public_access_type="NoPublicAccess",
            versioning="Enabled"
        )
        
        response = self.object_storage.create_bucket(
            namespace_name=self.namespace,
            create_bucket_details=request
        )
        return response.data
    
    def upload_file(self, bucket_name, object_name, file_path):
        """Upload file to Object Storage"""
        with open(file_path, 'rb') as f:
            response = self.object_storage.put_object(
                namespace_name=self.namespace,
                bucket_name=bucket_name,
                object_name=object_name,
                put_object_body=f
            )
        return response.headers['etag']
    
    def generate_presigned_url(self, bucket_name, object_name, expiration_hours=24):
        """Generate pre-authenticated request URL"""
        from datetime import datetime, timedelta
        
        par_details = oci.object_storage.models.CreatePreauthenticatedRequestDetails(
            name=f"par-{object_name}",
            object_name=object_name,
            access_type="ObjectRead",
            time_expires=datetime.utcnow() + timedelta(hours=expiration_hours)
        )
        
        response = self.object_storage.create_preauthenticated_request(
            namespace_name=self.namespace,
            bucket_name=bucket_name,
            create_preauthenticated_request_details=par_details
        )
        
        return f"https://objectstorage.{self.config['region']}.oraclecloud.com{response.data.access_uri}"
```

#### Block Volume
```bash
# Create and attach block volume
# Create volume
oci bv volume create \
  --compartment-id ocid1.compartment.oc1..aaa \
  --availability-domain AD-1 \
  --display-name "app-data-volume" \
  --size-in-gbs 500 \
  --vpus-per-gb 20

# Attach to instance
oci compute volume-attachment attach \
  --instance-id ocid1.instance.oc1.iad.aaa \
  --type paravirtualized \
  --volume-id ocid1.volume.oc1.iad.aaa \
  --display-name "app-data-attachment"
```

#### File Storage Service (FSS)
```python
def setup_file_storage(compartment_id, vcn_id, subnet_id):
    """Set up OCI File Storage Service"""
    file_storage_client = oci.file_storage.FileStorageClient(config)
    
    # Create file system
    fs_details = oci.file_storage.models.CreateFileSystemDetails(
        compartment_id=compartment_id,
        availability_domain="AD-1",
        display_name="shared-app-storage"
    )
    
    fs_response = file_storage_client.create_file_system(fs_details)
    file_system_id = fs_response.data.id
    
    # Create mount target
    mt_details = oci.file_storage.models.CreateMountTargetDetails(
        compartment_id=compartment_id,
        availability_domain="AD-1",
        subnet_id=subnet_id,
        display_name="app-mount-target"
    )
    
    mt_response = file_storage_client.create_mount_target(mt_details)
    mount_target_id = mt_response.data.id
    
    # Create export
    export_details = oci.file_storage.models.CreateExportDetails(
        export_set_id=mt_response.data.export_set_id,
        file_system_id=file_system_id,
        path="/shared"
    )
    
    export_response = file_storage_client.create_export(export_details)
    
    return {
        "file_system_id": file_system_id,
        "mount_target_id": mount_target_id,
        "mount_point": f"{mt_response.data.private_ip_ids[0]}:/shared"
    }
```

### Database Services

#### Autonomous Database
```python
class AutonomousDatabase:
    """Manage Oracle Autonomous Database"""
    
    def __init__(self, config):
        self.db_client = oci.database.DatabaseClient(config)
    
    def create_autonomous_database(self, compartment_id, db_name, workload_type="OLTP"):
        """Create an Autonomous Database instance"""
        create_details = oci.database.models.CreateAutonomousDatabaseDetails(
            compartment_id=compartment_id,
            display_name=db_name,
            db_name=db_name,
            admin_password="ComplexPass123!#",
            cpu_core_count=2,
            data_storage_size_in_tbs=1,
            db_workload=workload_type,  # OLTP, DW, AJD, APEX
            is_auto_scaling_enabled=True,
            is_free_tier=False,
            license_model="LICENSE_INCLUDED"
        )
        
        response = self.db_client.create_autonomous_database(create_details)
        return response.data
    
    def scale_autonomous_database(self, db_id, cpu_count, storage_tbs):
        """Scale Autonomous Database resources"""
        update_details = oci.database.models.UpdateAutonomousDatabaseDetails(
            cpu_core_count=cpu_count,
            data_storage_size_in_tbs=storage_tbs
        )
        
        response = self.db_client.update_autonomous_database(
            autonomous_database_id=db_id,
            update_autonomous_database_details=update_details
        )
        return response.data
```

#### Database Cloud Service (DBCS)
```bash
# Create Database System
oci db system launch \
  --compartment-id ocid1.compartment.oc1..aaa \
  --availability-domain AD-1 \
  --subnet-id ocid1.subnet.oc1.iad.aaa \
  --shape "VM.Standard2.4" \
  --ssh-public-keys file://~/.ssh/id_rsa.pub \
  --display-name "production-oracle-db" \
  --hostname "proddb" \
  --database-edition "ENTERPRISE_EDITION_HIGH_PERFORMANCE" \
  --db-home "{
    \"database\": {
      \"adminPassword\": \"ComplexPass123!#\",
      \"dbName\": \"PRODDB\",
      \"dbWorkload\": \"OLTP\",
      \"characterSet\": \"AL32UTF8\",
      \"ncharacterSet\": \"AL16UTF16\"
    },
    \"displayName\": \"prod-db-home\",
    \"dbVersion\": \"19.0.0.0\"
  }"
```

### Networking

#### Virtual Cloud Network (VCN)
```terraform
# Terraform configuration for OCI VCN
resource "oci_core_vcn" "main_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "production-vcn"
  dns_label      = "prodvcn"
}

resource "oci_core_subnet" "public_subnet" {
  compartment_id      = var.compartment_ocid
  vcn_id              = oci_core_vcn.main_vcn.id
  cidr_block          = "10.0.1.0/24"
  display_name        = "public-subnet"
  dns_label           = "public"
  security_list_ids   = [oci_core_security_list.public_security_list.id]
  route_table_id      = oci_core_route_table.public_route_table.id
  dhcp_options_id     = oci_core_vcn.main_vcn.default_dhcp_options_id
  prohibit_public_ip_on_vnic = false
}

resource "oci_core_subnet" "private_subnet" {
  compartment_id      = var.compartment_ocid
  vcn_id              = oci_core_vcn.main_vcn.id
  cidr_block          = "10.0.2.0/24"
  display_name        = "private-subnet"
  dns_label           = "private"
  security_list_ids   = [oci_core_security_list.private_security_list.id]
  route_table_id      = oci_core_route_table.private_route_table.id
  dhcp_options_id     = oci_core_vcn.main_vcn.default_dhcp_options_id
  prohibit_public_ip_on_vnic = true
}
```

#### Load Balancer
```python
def create_load_balancer(compartment_id, subnet_ids):
    """Create OCI Load Balancer"""
    lb_client = oci.load_balancer.LoadBalancerClient(config)
    
    # Backend set configuration
    backend_set_details = oci.load_balancer.models.BackendSetDetails(
        name="app-backend-set",
        policy="ROUND_ROBIN",
        health_checker=oci.load_balancer.models.HealthCheckerDetails(
            protocol="HTTP",
            url_path="/health",
            port=8080,
            return_code=200,
            interval_in_millis=10000,
            timeout_in_millis=3000,
            retries=3
        ),
        session_persistence_configuration=oci.load_balancer.models.SessionPersistenceConfigurationDetails(
            cookie_name="LB_COOKIE",
            disable_fallback=False
        )
    )
    
    # Listener configuration
    listener_details = oci.load_balancer.models.ListenerDetails(
        name="http-listener",
        default_backend_set_name="app-backend-set",
        port=80,
        protocol="HTTP",
        connection_configuration=oci.load_balancer.models.ConnectionConfiguration(
            idle_timeout_in_seconds=300,
            backend_tcp_proxy_protocol_version=2
        )
    )
    
    # Create load balancer
    create_details = oci.load_balancer.models.CreateLoadBalancerDetails(
        compartment_id=compartment_id,
        display_name="app-load-balancer",
        shape_name="100Mbps",
        subnet_ids=subnet_ids,
        is_private=False,
        backend_sets={"app-backend-set": backend_set_details},
        listeners={"http-listener": listener_details}
    )
    
    response = lb_client.create_load_balancer(create_details)
    return response.data
```

### Security Services

#### Identity and Access Management (IAM)
```python
def setup_iam_policies(compartment_id):
    """Set up IAM policies for OCI resources"""
    identity_client = oci.identity.IdentityClient(config)
    
    # Create a group
    group_details = oci.identity.models.CreateGroupDetails(
        compartment_id=compartment_id,
        name="developers-group",
        description="Group for development team"
    )
    group = identity_client.create_group(group_details).data
    
    # Create policy
    policy_statements = [
        "Allow group developers-group to manage instances in compartment Development",
        "Allow group developers-group to use object-family in compartment Development",
        "Allow group developers-group to manage volume-family in compartment Development",
        "Allow group developers-group to use virtual-network-family in compartment Development"
    ]
    
    policy_details = oci.identity.models.CreatePolicyDetails(
        compartment_id=compartment_id,
        name="developer-policy",
        description="Policies for developers",
        statements=policy_statements
    )
    
    policy = identity_client.create_policy(policy_details).data
    return {"group": group, "policy": policy}
```

#### Web Application Firewall (WAF)
```python
def configure_waf(compartment_id, load_balancer_id):
    """Configure Web Application Firewall"""
    waf_client = oci.waas.WaasClient(config)
    
    # Create WAF policy
    waf_details = oci.waas.models.CreateWaasPolicyDetails(
        compartment_id=compartment_id,
        domain="app.example.com",
        display_name="app-waf-policy",
        origins={
            "primary": oci.waas.models.Origin(
                uri=f"https://{load_balancer_id}.loadbalancer.oci.com",
                http_port=80,
                https_port=443
            )
        },
        waf_config=oci.waas.models.WafConfig(
            access_rules=[
                oci.waas.models.AccessRule(
                    name="block-bad-bots",
                    criteria=[
                        oci.waas.models.AccessRuleCriteria(
                            condition="URL_IS",
                            value="/admin"
                        )
                    ],
                    action="BLOCK",
                    block_action="SET_RESPONSE_CODE",
                    block_response_code=403
                )
            ],
            protection_rules=[
                oci.waas.models.ProtectionRule(
                    key="941000",  # SQL injection protection
                    action="BLOCK",
                    exclusions=[]
                )
            ],
            protection_settings=oci.waas.models.ProtectionSettings(
                block_action="SHOW_ERROR_PAGE",
                block_error_page_code=403,
                block_response_code=403,
                max_argument_count=255,
                max_argument_name_length=400,
                max_total_argument_length=64000
            )
        )
    )
    
    response = waf_client.create_waas_policy(waf_details)
    return response.data
```

### Container and Serverless

#### Functions
```python
import io
import json
import oci

def handler(ctx, data: io.BytesIO=None):
    """OCI Functions handler"""
    try:
        body = json.loads(data.getvalue())
        
        # Process the request
        result = process_data(body)
        
        # Store result in Object Storage
        signer = oci.auth.signers.get_resource_principals_signer()
        object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        
        namespace = object_storage.get_namespace().data
        bucket_name = "results-bucket"
        object_name = f"result-{ctx.GetRequestID()}.json"
        
        object_storage.put_object(
            namespace,
            bucket_name,
            object_name,
            json.dumps(result)
        )
        
        return response.Response(
            ctx, 
            response_data=json.dumps({"status": "success", "object": object_name}),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return response.Response(
            ctx,
            response_data=json.dumps({"error": str(e)}),
            status_code=500
        )
```

#### Container Registry
```bash
# Push image to OCI Container Registry
# Login to registry
docker login ${REGION}.ocir.io -u ${NAMESPACE}/${USERNAME} -p ${AUTH_TOKEN}

# Tag image
docker tag myapp:latest ${REGION}.ocir.io/${NAMESPACE}/myapp:v1.0

# Push image
docker push ${REGION}.ocir.io/${NAMESPACE}/myapp:v1.0

# Create Kubernetes secret for pulling images
kubectl create secret docker-registry ocir-secret \
  --docker-server=${REGION}.ocir.io \
  --docker-username=${NAMESPACE}/${USERNAME} \
  --docker-password=${AUTH_TOKEN}
```

### Analytics and AI

#### Oracle Analytics Cloud
```python
def setup_analytics_cloud(compartment_id, idcs_access_token):
    """Setup Oracle Analytics Cloud instance"""
    analytics_client = oci.analytics.AnalyticsClient(config)
    
    create_details = oci.analytics.models.CreateAnalyticsInstanceDetails(
        compartment_id=compartment_id,
        name="enterprise-analytics",
        description="Enterprise Analytics Platform",
        feature_set="ENTERPRISE_ANALYTICS",
        capacity=oci.analytics.models.Capacity(
            capacity_type="OLPU_COUNT",
            capacity_value=2
        ),
        license_type="LICENSE_INCLUDED",
        idcs_access_token=idcs_access_token,
        network_endpoint_details=oci.analytics.models.PublicEndpointDetails(
            network_endpoint_type="PUBLIC"
        )
    )
    
    response = analytics_client.create_analytics_instance(create_details)
    return response.data
```

#### Data Science Platform
```python
# OCI Data Science notebook session
def create_notebook_session(project_id, compartment_id):
    """Create a Data Science notebook session"""
    data_science = oci.data_science.DataScienceClient(config)
    
    notebook_config = oci.data_science.models.NotebookSessionConfigurationDetails(
        shape="VM.Standard2.8",
        subnet_id="ocid1.subnet.oc1.iad.aaa",
        block_storage_size_in_gbs=100
    )
    
    create_details = oci.data_science.models.CreateNotebookSessionDetails(
        compartment_id=compartment_id,
        project_id=project_id,
        display_name="ml-development",
        notebook_session_configuration_details=notebook_config
    )
    
    response = data_science.create_notebook_session(create_details)
    return response.data
```

## Enterprise Features

### Oracle Maximum Availability Architecture (MAA)
```python
def setup_maa_configuration(primary_db_id, standby_region):
    """Configure Maximum Availability Architecture"""
    db_client = oci.database.DatabaseClient(config)
    
    # Enable automatic backups
    backup_config = oci.database.models.UpdateDatabaseDetails(
        backup_config=oci.database.models.DbBackupConfig(
            auto_backup_enabled=True,
            recovery_window_in_days=30,
            auto_backup_window="SLOT_TWO"
        )
    )
    
    db_client.update_database(primary_db_id, backup_config)
    
    # Create Data Guard association
    data_guard_details = oci.database.models.CreateDataGuardAssociationDetails(
        database_admin_password="ComplexPass123!#",
        protection_mode="MAXIMUM_AVAILABILITY",
        transport_type="ASYNC",
        creation_type="NewDbSystem",
        display_name="standby-db",
        availability_domain="AD-1",
        subnet_id="ocid1.subnet.oc1.{}.aaa".format(standby_region),
        hostname="standbydb",
        is_active_data_guard_enabled=True
    )
    
    response = db_client.create_data_guard_association(
        database_id=primary_db_id,
        create_data_guard_association_details=data_guard_details
    )
    return response.data
```

### Integration with Oracle Applications
```python
class OracleAppsIntegration:
    """Integration with Oracle Cloud Applications"""
    
    def __init__(self, config):
        self.integration_client = oci.integration.IntegrationInstanceClient(config)
    
    def create_integration_instance(self, compartment_id):
        """Create Oracle Integration Cloud instance"""
        create_details = oci.integration.models.CreateIntegrationInstanceDetails(
            compartment_id=compartment_id,
            display_name="enterprise-integration",
            integration_instance_type="ENTERPRISE",
            is_byol=False,
            message_packs=1,
            is_visual_builder_enabled=True,
            is_file_server_enabled=True
        )
        
        response = self.integration_client.create_integration_instance(create_details)
        return response.data
    
    def connect_to_erp_cloud(self, integration_id, erp_url, username, password):
        """Connect to Oracle ERP Cloud"""
        connection_details = {
            "connectionType": "ORACLE_ERP_CLOUD",
            "connectionUrl": erp_url,
            "username": username,
            "password": password,
            "securityPolicy": "OAUTH2"
        }
        
        # Implementation would use Oracle Integration REST API
        return connection_details
```

## Monitoring and Management

### Monitoring Service
```python
def setup_comprehensive_monitoring(compartment_id):
    """Setup OCI Monitoring with custom metrics"""
    monitoring_client = oci.monitoring.MonitoringClient(config)
    
    # Create alarm for high CPU usage
    alarm_details = oci.monitoring.models.CreateAlarmDetails(
        display_name="high-cpu-alarm",
        compartment_id=compartment_id,
        metric_compartment_id=compartment_id,
        namespace="oci_computeagent",
        query="CpuUtilization[1m]{resourceType=\"instance\"}.mean() > 80",
        severity="CRITICAL",
        body="Instance CPU utilization is above 80%",
        destinations=["ocid1.onstopic.oc1.iad.aaa"],
        is_enabled=True,
        repeat_notification_duration="PT4H"
    )
    
    response = monitoring_client.create_alarm(alarm_details)
    return response.data

# Post custom metrics
def post_custom_metric(compartment_id, metric_name, value):
    """Post custom metrics to OCI Monitoring"""
    monitoring_client = oci.monitoring.MonitoringClient(config)
    
    metric_data = oci.monitoring.models.MetricDataDetails(
        namespace="custom_app",
        compartment_id=compartment_id,
        name=metric_name,
        dimensions={"environment": "production", "app": "web"},
        datapoints=[
            oci.monitoring.models.Datapoint(
                timestamp=datetime.utcnow(),
                value=value
            )
        ]
    )
    
    post_details = oci.monitoring.models.PostMetricDataDetails(
        metric_data=[metric_data]
    )
    
    response = monitoring_client.post_metric_data(post_details)
    return response.data
```

### Logging Service
```python
def configure_logging(compartment_id):
    """Configure OCI Logging service"""
    logging_client = oci.logging.LoggingManagementClient(config)
    
    # Create log group
    log_group_details = oci.logging.models.CreateLogGroupDetails(
        compartment_id=compartment_id,
        display_name="application-logs",
        description="Centralized application logging"
    )
    
    log_group = logging_client.create_log_group(log_group_details).data
    
    # Create custom log
    log_details = oci.logging.models.CreateLogDetails(
        display_name="app-custom-log",
        log_group_id=log_group.id,
        log_type="CUSTOM",
        is_enabled=True,
        retention_duration=30
    )
    
    log = logging_client.create_log(log_group.id, log_details).data
    
    # Configure service log
    service_log_details = oci.logging.models.CreateLogDetails(
        display_name="vcn-flow-logs",
        log_group_id=log_group.id,
        log_type="SERVICE",
        is_enabled=True,
        configuration=oci.logging.models.Configuration(
            source=oci.logging.models.OciService(
                source_type="OCISERVICE",
                service="flowlogs",
                resource="ocid1.subnet.oc1.iad.aaa",
                category="all"
            )
        )
    )
    
    service_log = logging_client.create_log(log_group.id, service_log_details).data
    
    return {"log_group": log_group, "custom_log": log, "service_log": service_log}
```

## Cost Management

### Cost Analysis and Budgets
```python
def setup_cost_management(compartment_id):
    """Setup cost tracking and budgets"""
    budget_client = oci.budget.BudgetClient(config)
    
    # Create budget
    budget_details = oci.budget.models.CreateBudgetDetails(
        compartment_id=compartment_id,
        target_compartment_id=compartment_id,
        display_name="monthly-compute-budget",
        description="Monthly budget for compute resources",
        amount=5000,
        reset_period="MONTHLY",
        budget_processing_period_start_offset=1,
        processing_period_type="MONTH",
        targets=["COMPARTMENT"],
        alert_rule_details=[
            oci.budget.models.CreateAlertRuleDetails(
                threshold=80,
                threshold_type="PERCENTAGE",
                type="ACTUAL",
                display_name="80-percent-alert",
                recipients="platform-team@example.com",
                message="Budget has reached 80% threshold"
            ),
            oci.budget.models.CreateAlertRuleDetails(
                threshold=100,
                threshold_type="PERCENTAGE",
                type="FORECAST",
                display_name="forecast-exceed-alert",
                recipients="platform-team@example.com",
                message="Forecasted to exceed budget"
            )
        ]
    )
    
    response = budget_client.create_budget(budget_details)
    return response.data
```

### Resource Optimization
```python
def analyze_resource_utilization(compartment_id):
    """Analyze and optimize resource utilization"""
    # Query metrics for underutilized resources
    monitoring_client = oci.monitoring.MonitoringClient(config)
    
    # Find instances with low CPU utilization
    low_cpu_query = """
    CpuUtilization[1h]{resourceType="instance"}.mean() < 10
    """
    
    search_details = oci.monitoring.models.SummarizeMetricsDataDetails(
        namespace="oci_computeagent",
        query=low_cpu_query,
        start_time=datetime.utcnow() - timedelta(days=7),
        end_time=datetime.utcnow()
    )
    
    response = monitoring_client.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=search_details
    )
    
    recommendations = []
    for metric in response.data:
        if metric.mean < 10:
            recommendations.append({
                "resource_id": metric.dimensions.get("resourceId"),
                "current_shape": metric.dimensions.get("shape"),
                "recommendation": "Consider downsizing or terminating",
                "potential_savings": calculate_savings(metric.dimensions.get("shape"))
            })
    
    return recommendations
```

## Disaster Recovery

### Cross-Region Replication
```python
def setup_disaster_recovery(primary_region, dr_region):
    """Configure cross-region disaster recovery"""
    
    # Set up cross-region object storage replication
    def configure_storage_replication(bucket_name):
        os_client_primary = oci.object_storage.ObjectStorageClient(
            config={'region': primary_region}
        )
        
        replication_details = oci.object_storage.models.CreateReplicationPolicyDetails(
            name="dr-replication",
            destination_region_name=dr_region,
            destination_bucket_name=f"{bucket_name}-dr"
        )
        
        response = os_client_primary.create_replication_policy(
            namespace_name=namespace,
            bucket_name=bucket_name,
            create_replication_policy_details=replication_details
        )
        return response.data
    
    # Set up cross-region block volume backup
    def configure_volume_backup(volume_id):
        blockstorage_client = oci.core.BlockstorageClient(config)
        
        backup_policy_details = oci.core.models.CreateVolumeBackupPolicyDetails(
            compartment_id=compartment_id,
            display_name="cross-region-backup",
            schedules=[
                oci.core.models.VolumeBackupSchedule(
                    backup_type="FULL",
                    period="ONE_DAY",
                    retention_seconds=2592000,  # 30 days
                    time_zone="UTC",
                    hour_of_day=2
                )
            ],
            destination_region=dr_region
        )
        
        response = blockstorage_client.create_volume_backup_policy(
            backup_policy_details
        )
        return response.data
```

## Migration Tools

### Database Migration Service
```python
def migrate_database_to_oci(source_db_config, target_adb_id):
    """Migrate database to OCI using Database Migration Service"""
    migration_client = oci.database_migration.DatabaseMigrationClient(config)
    
    # Create migration
    migration_details = oci.database_migration.models.CreateMigrationDetails(
        compartment_id=compartment_id,
        display_name="prod-db-migration",
        type="ONLINE",
        source_database_connection_id=create_source_connection(source_db_config),
        target_database_connection_id=target_adb_id,
        data_transfer_medium_details=oci.database_migration.models.ObjectStoreBucket(
            bucket_name="migration-bucket",
            namespace_name=namespace
        ),
        include_objects=[
            oci.database_migration.models.DatabaseObject(
                schema="APP_SCHEMA",
                object_name="%",
                is_password_reset_required=False
            )
        ]
    )
    
    response = migration_client.create_migration(migration_details)
    migration_id = response.data.id
    
    # Start migration
    migration_client.start_migration(migration_id)
    
    return migration_id
```

## Best Practices Summary

1. **Architecture**: Use compartments for resource isolation and implement proper IAM policies
2. **High Availability**: Deploy across multiple availability domains and use fault domains
3. **Security**: Enable Cloud Guard, use WAF, and implement defense in depth
4. **Performance**: Use appropriate shapes, enable auto-scaling, and optimize network paths
5. **Cost**: Set up budgets, use reserved capacity, and regularly review resource utilization
6. **Backup**: Implement comprehensive backup strategies with cross-region replication
7. **Monitoring**: Use OCI Monitoring, Logging, and Application Performance Monitoring
8. **Database**: Leverage Autonomous Database for reduced management overhead

## Common Pitfalls to Avoid

1. Not properly sizing compute shapes for workload requirements
2. Ignoring compartment design leading to poor resource organization
3. Overlooking network security with overly permissive security lists
4. Not implementing proper backup and disaster recovery strategies
5. Underestimating egress costs for data transfer
6. Not leveraging Oracle-specific optimizations for Oracle workloads
7. Poor IAM policy design leading to security vulnerabilities