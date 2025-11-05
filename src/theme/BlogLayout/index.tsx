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

// Map of doc IDs to their proper display labels
const docTitles: Record<string, string> = {
  'intro': 'Welcome',
  'technical/aws': 'AWS',
  'technical/azure': 'Azure',
  'technical/gcp': 'GCP',
  'technical/iam': 'IAM',
  'technical/serverless': 'Serverless',
  'technical/api-gateway': 'API Gateway',
  'technical/openstack': 'OpenStack',
  'technical/vmware': 'VMware',
  'technical/docker': 'Docker',
  'technical/kubernetes': 'Kubernetes',
  'technical/container-registries': 'Container Registries',
  'technical/helm': 'Helm',
  'technical/kustomize': 'Kustomize',
  'technical/operators': 'Operators',
  'technical/k3s': 'K3s',
  'technical/podman': 'Podman',
  'technical/containerd': 'containerd',
  'technical/terraform': 'Terraform',
  'technical/ansible': 'Ansible',
  'technical/cloudformation': 'CloudFormation',
  'technical/pulumi': 'Pulumi',
  'technical/crossplane': 'Crossplane',
  'technical/packer': 'Packer',
  'technical/cloud-init': 'Cloud-init',
  'technical/git': 'Git',
  'technical/jenkins': 'Jenkins',
  'technical/github-actions': 'GitHub Actions',
  'technical/gitlab-ci': 'GitLab CI',
  'technical/circleci': 'CircleCI',
  'technical/spinnaker': 'Spinnaker',
  'technical/argocd': 'ArgoCD',
  'technical/flux': 'Flux',
  'technical/prometheus': 'Prometheus',
  'technical/grafana': 'Grafana',
  'technical/elasticsearch': 'Elasticsearch',
  'technical/fluentd': 'Fluentd',
  'technical/loki': 'Loki',
  'technical/opentelemetry': 'OpenTelemetry',
  'technical/jaeger': 'Jaeger',
  'technical/datadog': 'Datadog',
  'technical/splunk': 'Splunk',
  'technical/new-relic': 'New Relic',
  'technical/influxdb': 'InfluxDB',
  'technical/telegraf': 'Telegraf',
  'technical/sre-practices-incident-management': 'SRE Practices & Incident Management',
  'technical/tcp-ip': 'TCP/IP',
  'technical/dns': 'DNS',
  'technical/linux-networking': 'Linux Networking',
  'technical/nginx': 'NGINX',
  'technical/haproxy': 'HAProxy',
  'technical/envoy': 'Envoy',
  'technical/traefik': 'Traefik',
  'technical/istio': 'Istio',
  'technical/consul-connect': 'Consul Connect',
  'technical/vault': 'HashiCorp Vault',
  'technical/container-security': 'Container Security',
  'technical/zero-trust': 'Zero Trust',
  'technical/opa': 'Open Policy Agent (OPA)',
  'technical/trivy': 'Trivy',
  'technical/falco': 'Falco',
  'technical/cert-manager': 'cert-manager',
  'technical/keycloak': 'Keycloak',
  'technical/gatekeeper': 'Gatekeeper',
  'technical/kyverno': 'Kyverno',
  'technical/postgresql': 'PostgreSQL',
  'technical/mysql': 'MySQL',
  'technical/mongodb': 'MongoDB',
  'technical/redis': 'Redis',
  'technical/dynamodb': 'DynamoDB',
  'technical/cassandra': 'Cassandra',
  'technical/clickhouse': 'ClickHouse',
  'technical/minio': 'MinIO',
  'technical/ceph': 'Ceph',
  'technical/etcd': 'etcd',
  'technical/kafka': 'Apache Kafka',
  'technical/rabbitmq': 'RabbitMQ',
  'technical/nats': 'NATS',
  'technical/apache-airflow': 'Apache Airflow',
  'technical/python': 'Python',
  'technical/go': 'Go',
  'technical/bash': 'Bash',
  'technical/javascript': 'JavaScript',
  'technical/yaml': 'YAML',
  'technical/json': 'JSON',
  'technical/hcl': 'HCL',
  'technical/linux-fundamentals': 'Linux Fundamentals',
  'technical/linux-performance': 'Linux Performance',
  'technical/system-administration': 'System Administration',
  'technical/linux-security': 'Linux Security',
  'technical/platform-engineering': 'Platform Engineering',
  'technical/backstage': 'Backstage',
  'technical/api-design-protocols': 'API Design & Protocols',
  'technical/kubecost': 'Kubecost',
  'technical/velero': 'Velero',
  'technical/tmux': 'tmux',
  'technical/vim': 'Vim',
  'technical/index': 'Technical Skills Overview',
  'technical/cloud-platforms': 'Cloud Platforms & Services',
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
      // Recursively transform category items
      const transformedCategory = {
        ...item,
        items: transformSidebarItems(item.items),
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
  });
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