import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import BlogSidebar from '@theme/BlogSidebar';
import DocSidebarItems from '@theme/DocSidebarItems';
import {ThemeClassNames} from '@docusaurus/theme-common';
import type {Props} from '@theme/BlogLayout';
import type {PropSidebarItem} from '@docusaurus/plugin-content-docs';
// Correct import path for sidebars
import sidebars from '../../../sidebars';

// Map of doc IDs to their proper display labels (matching frontmatter titles)
const docTitles: Record<string, string> = {
  'intro': 'Welcome',
  'technical/index': 'Platform Engineering Technical Skills - Complete Technology Guide',
  'technical/cloud-platforms': 'Cloud Platforms - AWS, Azure, GCP Guide',
  'technical/aws': 'AWS - Amazon Web Services Cloud Platform',
  'technical/azure': 'Azure - Microsoft\'s Enterprise Cloud Platform',
  'technical/gcp': 'GCP - Google\'s Data and AI Cloud Platform',
  'technical/iam': 'IAM - Identity and Access Management',
  'technical/serverless': 'Serverless - Function as a Service (FaaS)',
  'technical/api-gateway': 'API Gateway - Traffic Management and Security',
  'technical/openstack': 'OpenStack - Open Source Cloud Platform',
  'technical/vmware': 'VMware vSphere - Enterprise Virtualization Platform',
  'technical/docker': 'Docker - Container Platform',
  'technical/kubernetes': 'Kubernetes - Container Orchestration Platform',
  'technical/container-registries': 'Container Registries - Docker Hub, Harbor, ECR Guide',
  'technical/helm': 'Helm - Kubernetes Package Manager',
  'technical/kustomize': 'Kustomize - Template-Free Kubernetes Configuration',
  'technical/operators': 'Kubernetes Operators - Application Automation',
  'technical/k3s': 'K3s - Lightweight Kubernetes',
  'technical/podman': 'Podman - Daemonless Container Engine',
  'technical/containerd': 'containerd - Industry-Standard Container Runtime',
  'technical/terraform': 'Terraform - Infrastructure as Code Platform',
  'technical/ansible': 'Ansible - IT Automation and Configuration Management',
  'technical/cloudformation': 'CloudFormation - AWS Native Infrastructure as Code',
  'technical/pulumi': 'Pulumi - Infrastructure as Real Programming Code',
  'technical/crossplane': 'Crossplane - Universal Control Plane',
  'technical/packer': 'Packer - Machine Image Automation',
  'technical/cloud-init': 'Cloud-init - Cloud Instance Initialization',
  'technical/git': 'Git - Distributed Version Control System',
  'technical/jenkins': 'Jenkins - CI/CD Automation Server',
  'technical/github-actions': 'GitHub Actions - Cloud-Native CI/CD Platform',
  'technical/gitlab-ci': 'GitLab CI/CD - Complete DevOps Platform',
  'technical/circleci': 'CircleCI - Cloud CI/CD Platform',
  'technical/spinnaker': 'Spinnaker - Multi-Cloud Continuous Delivery',
  'technical/argocd': 'ArgoCD - GitOps Continuous Delivery for Kubernetes',
  'technical/flux': 'Flux - GitOps Continuous Delivery for Kubernetes',
  'technical/prometheus': 'Prometheus - Cloud-Native Monitoring and Alerting',
  'technical/grafana': 'Grafana - Observability Visualization Platform',
  'technical/elasticsearch': 'Elasticsearch - Distributed Search and Analytics Engine',
  'technical/fluentd': 'Fluentd - Unified Logging Layer',
  'technical/loki': 'Loki - Cost-Effective Log Aggregation Like Prometheus',
  'technical/opentelemetry': 'OpenTelemetry - Observability Framework',
  'technical/jaeger': 'Jaeger - Distributed Tracing for Microservices',
  'technical/datadog': 'Datadog - Unified Observability and Monitoring Platform',
  'technical/splunk': 'Splunk - Enterprise Data Analytics and SIEM Platform',
  'technical/new-relic': 'New Relic - Application Performance Monitoring',
  'technical/influxdb': 'InfluxDB - Time-Series Database',
  'technical/telegraf': 'Telegraf - Metrics Collection Agent',
  'technical/sre-practices-incident-management': 'SRE Practices & Incident Management',
  'technical/tcp-ip': 'TCP/IP - Network Protocol Fundamentals',
  'technical/dns': 'DNS (Domain Name System)',
  'technical/linux-networking': 'Linux Networking - Configuration and Troubleshooting',
  'technical/nginx': 'NGINX - High-Performance Web Server and Reverse Proxy',
  'technical/haproxy': 'HAProxy',
  'technical/envoy': 'Envoy Proxy',
  'technical/traefik': 'Traefik - Cloud-Native Edge Router',
  'technical/istio': 'Istio - Enterprise Service Mesh Platform',
  'technical/consul-connect': 'Consul Connect - Service Mesh by HashiCorp',
  'technical/vault': 'HashiCorp Vault - Secrets Management Platform',
  'technical/container-security': 'Container Security - Best Practices and Scanning',
  'technical/zero-trust': 'Zero Trust - Modern Security Architecture',
  'technical/opa': 'OPA - Open Policy Agent',
  'technical/trivy': 'Trivy - Vulnerability Scanner',
  'technical/falco': 'Falco - Cloud-Native Runtime Security',
  'technical/cert-manager': 'cert-manager - Kubernetes Certificate Management',
  'technical/keycloak': 'Keycloak - Open Source Identity Management',
  'technical/gatekeeper': 'Gatekeeper - Kubernetes Policy Controller',
  'technical/kyverno': 'Kyverno - Kubernetes Native Policy Management',
  'technical/postgresql': 'PostgreSQL - Advanced Open Source Database',
  'technical/mysql': 'MySQL - Relational Database Management System',
  'technical/mongodb': 'MongoDB - Developer-Friendly Document Database',
  'technical/redis': 'Redis - In-Memory Data Store and Cache',
  'technical/dynamodb': 'Amazon DynamoDB - Managed NoSQL Database',
  'technical/cassandra': 'Apache Cassandra - Distributed NoSQL Database',
  'technical/clickhouse': 'ClickHouse - Columnar Database for Analytics',
  'technical/minio': 'MinIO - High-Performance Object Storage',
  'technical/ceph': 'Ceph - Distributed Storage System',
  'technical/etcd': 'etcd - Distributed Key-Value Store',
  'technical/kafka': 'Apache Kafka - Distributed Event Streaming Platform',
  'technical/rabbitmq': 'RabbitMQ - Message Broker for Microservices',
  'technical/nats': 'NATS - Cloud-Native Messaging System',
  'technical/apache-airflow': 'Apache Airflow - Workflow Orchestration Platform',
  'technical/python': 'Python - Programming for Platform Engineering',
  'technical/go': 'Go - Cloud Native Programming Language',
  'technical/bash': 'Bash - System Automation and Scripting',
  'technical/javascript': 'JavaScript - Modern Web Development',
  'technical/yaml': 'YAML - Data Serialization Language',
  'technical/json': 'JSON - JavaScript Object Notation',
  'technical/hcl': 'HCL - HashiCorp Configuration Language',
  'technical/linux-fundamentals': 'Linux Fundamentals - Core Concepts and Commands',
  'technical/linux-performance': 'Linux Performance - Tuning and Optimization',
  'technical/system-administration': 'System Administration - Linux Server Management',
  'technical/linux-security': 'Linux Security - Hardening and Best Practices',
  'technical/platform-engineering': 'Platform Engineering - Internal Developer Platforms',
  'technical/backstage': 'Backstage - Developer Portal Platform',
  'technical/api-design-protocols': 'API Design & Protocols - REST, GraphQL, gRPC Guide',
  'technical/kubecost': 'Kubecost - Kubernetes Cost Monitoring',
  'technical/velero': 'Velero - Kubernetes Backup and Disaster Recovery',
  'technical/tmux': 'tmux - Terminal Multiplexer',
  'technical/vim': 'Vim - Powerful Text Editor',
};

// Transform string items to have explicit labels
function transformSidebarItems(items: any[]): PropSidebarItem[] {
  return items.map(item => {
    if (typeof item === 'string') {
      // Use the proper title from our mapping, or generate one if not found
      const label = docTitles[item] || item.split('/').pop()?.replace(/-/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ') || item;
      return {
        type: 'link',
        label: label,
        href: `/${item}`,
      } as PropSidebarItem;
    }

    if (item.type === 'doc') {
      // Skip the technical/index item as it's redundant in the blog sidebar
      if (item.id === 'technical/index') {
        return null;
      }
      // Convert doc to link with proper label
      const label = item.label || docTitles[item.id] || item.id.split('/').pop()?.replace(/-/g, ' ')
        .split(' ')
        .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ') || item.id;
      return {
        type: 'link',
        label: label,
        href: `/${item.id}`,
      } as PropSidebarItem;
    }

    if (item.type === 'category' && item.items) {
      // Recursively transform category items and filter out nulls
      const transformedCategory = {
        ...item,
        items: transformSidebarItems(item.items).filter(Boolean),
      };

      // If category has a link, convert it to href
      if (item.link && item.link.type === 'doc') {
        transformedCategory.link = {
          type: 'generated-index' as const,
          slug: item.link.id,
        };
      }

      return transformedCategory;
    }

    return item;
  }).filter(Boolean);
}

export default function BlogLayout(props: Props): React.ReactElement {
  const {sidebar, toc, children, ...layoutProps} = props;
  const hasBlogSidebar = sidebar && sidebar.items.length > 0;

  // Get the sidebar items from sidebars.ts and transform them
  const rawSidebarItems = sidebars.tutorialSidebar as any[];
  const sidebarItems = transformSidebarItems(rawSidebarItems);

  return (
    <Layout {...layoutProps} wrapperClassName={clsx(ThemeClassNames.wrapper.blogPages, 'blog-wrapper')}>
      <div className="container margin-vert--lg">
        <div className="row">
          {/* Left Column: Docs Sidebar (Technical Skills List) */}
          <aside className="col col--3">
            <nav
              className={clsx(
                'menu thin-scrollbar',
                ThemeClassNames.docs.docSidebarMenu,
                'menu--responsive'
              )}
              style={{
                position: 'sticky',
                top: 'calc(var(--ifm-navbar-height) + 1rem)',
                height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                overflowY: 'auto'
              }}
            >
              <ul className="menu__list">
                <DocSidebarItems
                  items={sidebarItems}
                  activePath="/blog"
                  level={1}
                />
              </ul>
            </nav>
          </aside>

          {/* Middle Column: Blog Content */}
          <main
            className={clsx(
              'col',
              hasBlogSidebar ? 'col--6' : 'col--9'
            )}
          >
            {children}
          </main>

          {/* Right Column: Blog Sidebar (Recent Posts) - Conditional */}
          {hasBlogSidebar && (
            <aside className="col col--3 blogSidebarContainer">
              <div
                style={{
                  position: 'sticky',
                  top: 'calc(var(--ifm-navbar-height) + 1rem)',
                  maxHeight: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                  overflowY: 'auto',
                  width: '100%'
                }}
              >
                <BlogSidebar sidebar={sidebar} />
              </div>
            </aside>
          )}
        </div>
      </div>
    </Layout>
  );
}