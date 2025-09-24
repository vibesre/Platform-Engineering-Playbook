import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Default sidebar containing all sections
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Welcome'
    },
    {
      type: 'category',
      label: 'Technical Skills',
      collapsed: true,
      collapsible: true,
      items: [
        {
          type: 'doc',
          id: 'technical/index',
          label: 'Technical Skills Overview'
        },
        {
          type: 'category',
          label: 'Cloud Platforms & Services',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/aws',
            'technical/azure',
            'technical/gcp',
            'technical/iam',
            'technical/serverless',
            'technical/api-gateway',
            'technical/openstack',
            'technical/vmware'
          ]
        },
        {
          type: 'category',
          label: 'Containers & Orchestration',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/docker',
            'technical/kubernetes',
            'technical/container-registries',
            'technical/helm',
            'technical/kustomize',
            'technical/operators',
            'technical/k3s',
            'technical/podman',
            'technical/containerd'
          ]
        },
        {
          type: 'category',
          label: 'Infrastructure as Code',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/terraform',
            'technical/ansible',
            'technical/cloudformation',
            'technical/pulumi',
            'technical/crossplane',
            'technical/packer',
            'technical/cloud-init'
          ]
        },
        {
          type: 'category',
          label: 'CI/CD & GitOps',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/git',
            'technical/jenkins',
            'technical/github-actions',
            'technical/gitlab-ci',
            'technical/circleci',
            'technical/spinnaker',
            'technical/argocd',
            'technical/flux'
          ]
        },
        {
          type: 'category',
          label: 'Observability & Monitoring',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/prometheus',
            'technical/grafana',
            'technical/elasticsearch',
            'technical/fluentd',
            'technical/loki',
            'technical/opentelemetry',
            'technical/jaeger',
            'technical/datadog',
            'technical/splunk',
            'technical/new-relic',
            'technical/influxdb',
            'technical/telegraf',
            'technical/sre-practices-incident-management'
          ]
        },
        {
          type: 'category',
          label: 'Networking & Service Mesh',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/tcp-ip',
            'technical/dns',
            'technical/linux-networking',
            'technical/nginx',
            'technical/haproxy',
            'technical/envoy',
            'technical/traefik',
            'technical/istio',
            'technical/consul-connect'
          ]
        },
        {
          type: 'category',
          label: 'Security & Compliance',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/vault',
            'technical/container-security',
            'technical/zero-trust',
            'technical/opa',
            'technical/trivy',
            'technical/falco',
            'technical/cert-manager',
            'technical/keycloak',
            'technical/gatekeeper',
            'technical/kyverno'
          ]
        },
        {
          type: 'category',
          label: 'Data & Storage',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/postgresql',
            'technical/mysql',
            'technical/mongodb',
            'technical/redis',
            'technical/dynamodb',
            'technical/cassandra',
            'technical/influxdb',
            'technical/clickhouse',
            'technical/minio',
            'technical/ceph',
            'technical/etcd'
          ]
        },
        {
          type: 'category',
          label: 'Messaging & Streaming',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/kafka',
            'technical/rabbitmq',
            'technical/nats',
            'technical/apache-airflow'
          ]
        },
        {
          type: 'category',
          label: 'Programming Languages',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/python',
            'technical/go',
            'technical/bash',
            'technical/javascript',
            'technical/yaml',
            'technical/json',
            'technical/hcl'
          ]
        },
        {
          type: 'category',
          label: 'Linux & Systems',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/linux-fundamentals',
            'technical/linux-performance',
            'technical/system-administration',
            'technical/linux-security'
          ]
        },
        {
          type: 'category',
          label: 'Platform Engineering',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/platform-engineering',
            'technical/backstage',
            'technical/api-design-protocols',
            'technical/kubecost',
            'technical/velero',
            'technical/tmux',
            'technical/vim'
          ]
        }
      ]
    },
    {
      type: 'category',
      label: 'Interview Prep',
      collapsed: true,
      collapsible: true,
      items: [
        {
          type: 'doc',
          id: 'interview-prep/index',
          label: 'Interview Prep Overview'
        },
        {
          type: 'category',
          label: 'Interview Process',
          collapsed: true,
          collapsible: true,
          items: [
            'interview-process/index',
            'practice/interview-formats'
          ]
        },
        {
          type: 'category',
          label: 'System Design',
          collapsed: true,
          collapsible: true,
          items: [
            'system-design/index'
          ]
        },
        {
          type: 'category',
          label: 'Behavioral',
          collapsed: true,
          collapsible: true,
          items: [
            'behavioral/index'
          ]
        },
        {
          type: 'category',
          label: 'Coding Challenges',
          collapsed: true,
          collapsible: true,
          items: [
            'coding-challenges/index'
          ]
        }
      ]
    },
    {
      type: 'category',
      label: 'Career Guide',
      collapsed: true,
      collapsible: true,
      items: [
        {
          type: 'doc',
          id: 'career-guide/index',
          label: 'Career Guide Overview'
        },
        {
          type: 'category',
          label: 'Job Search',
          collapsed: true,
          collapsible: true,
          items: [
            'get-hired/index',
            'get-hired/job-search',
            'get-hired/company-research',
            'resume/index'
          ]
        },
        {
          type: 'category',
          label: 'Career Development',
          collapsed: true,
          collapsible: true,
          items: [
            'career/index'
          ]
        },
        {
          type: 'category',
          label: 'Compensation & Negotiation',
          collapsed: true,
          collapsible: true,
          items: [
            'compensation/index',
            'get-hired/negotiation'
          ]
        }
      ]
    },
    {
      type: 'category',
      label: 'Practice & Resources',
      collapsed: true,
      collapsible: true,
      items: [
        {
          type: 'doc',
          id: 'practice-resources/index',
          label: 'Practice & Resources Overview'
        },
        {
          type: 'category',
          label: 'Hands-On Practice',
          collapsed: true,
          collapsible: true,
          items: [
            'practice/index',
            'practice/hands-on-labs',
            'practice/mock-scenarios',
            'hands-on-labs/index'
          ]
        },
        {
          type: 'category',
          label: 'Company Guides',
          collapsed: true,
          collapsible: true,
          items: [
            'company-specific/index'
          ]
        },
        {
          type: 'category',
          label: 'Additional Resources',
          collapsed: true,
          collapsible: true,
          items: [
            'resources/index'
          ]
        }
      ]
    }
  ]
};

export default sidebars;