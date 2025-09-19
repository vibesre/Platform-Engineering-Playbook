import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  // Default sidebar containing all sections
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: true,
      collapsible: true,
      items: [
        {
          type: 'doc',
          id: 'getting-started/index',
          label: 'Getting Started Overview'
        },
        {
          type: 'doc',
          id: 'intro',
          label: 'Welcome'
        }
      ]
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
          label: 'Linux & Systems',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/linux-fundamentals',
            'technical/linux-deep-dive',
            'technical/linux-networking',
            'technical/linux-performance',
            'technical/linux-security',
            'technical/system-administration',
            'technical/bash',
            'technical/bash-scripting',
            'technical/process-management',
            'technical/file-systems',
            'technical/package-management',
            'technical/tmux',
            'technical/vim',
            'technical/vscode'
          ]
        },
        {
          type: 'category',
          label: 'Cloud Platforms',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/cloud-platforms',
            'technical/aws',
            'technical/aws-cdk',
            'technical/aws-messaging',
            'technical/aws-secrets',
            'technical/azure',
            'technical/azure-devops',
            'technical/azure-service-bus',
            'technical/gcp',
            'technical/gcp-pubsub',
            'technical/alibaba-cloud',
            'technical/digitalocean',
            'technical/linode',
            'technical/oracle-cloud',
            'technical/openstack',
            'technical/proxmox',
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
            'technical/docker-compose',
            'technical/podman',
            'technical/containerd',
            'technical/cri-o',
            'technical/kubernetes',
            'technical/kubernetes-mastery',
            'technical/k3s',
            'technical/kind',
            'technical/openshift',
            'technical/rancher',
            'technical/helm',
            'technical/kustomize',
            'technical/operators',
            'technical/serverless-edge-computing'
          ]
        },
        {
          type: 'category',
          label: 'Infrastructure as Code',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/terraform',
            'technical/pulumi',
            'technical/cloudformation',
            'technical/crossplane',
            'technical/ansible',
            'technical/chef',
            'technical/puppet',
            'technical/saltstack',
            'technical/packer',
            'technical/cloud-init',
            'technical/cloud-custodian'
          ]
        },
        {
          type: 'category',
          label: 'CI/CD & DevOps',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/git',
            'technical/git-advanced',
            'technical/github-actions',
            'technical/gitlab-ci',
            'technical/jenkins',
            'technical/circleci',
            'technical/teamcity',
            'technical/tekton',
            'technical/spinnaker',
            'technical/argocd',
            'technical/flux',
            'technical/bazel',
            'technical/gradle',
            'technical/make'
          ]
        },
        {
          type: 'category',
          label: 'Monitoring & Observability',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/prometheus',
            'technical/grafana',
            'technical/victoriametrics',
            'technical/influxdb',
            'technical/telegraf',
            'technical/datadog',
            'technical/new-relic',
            'technical/appdynamics',
            'technical/splunk',
            'technical/elasticsearch',
            'technical/logstash',
            'technical/opensearch',
            'technical/fluent-bit',
            'technical/fluentd',
            'technical/loki',
            'technical/vector',
            'technical/jaeger',
            'technical/zipkin',
            'technical/tempo',
            'technical/opentelemetry',
            'technical/chaos-engineering',
            'technical/sre-practices-incident-management',
            'technical/pagerduty',
            'technical/opsgenie',
            'technical/victorops'
          ]
        },
        {
          type: 'category',
          label: 'Service Mesh & Networking',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/istio',
            'technical/linkerd',
            'technical/service-mesh',
            'technical/envoy',
            'technical/traefik',
            'technical/nginx',
            'technical/haproxy',
            'technical/consul-connect',
            'technical/service-discovery',
            'technical/dns',
            'technical/tcp-ip',
            'technical/http-https',
            'technical/bgp',
            'technical/network-troubleshooting',
            'technical/vpn',
            'technical/cdn'
          ]
        },
        {
          type: 'category',
          label: 'Data & Message Systems',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/caching-data-stores',
            'technical/redis',
            'technical/redis-pubsub',
            'technical/memcached',
            'technical/etcd',
            'technical/message-queues-event-driven',
            'technical/kafka',
            'technical/rabbitmq',
            'technical/pulsar',
            'technical/nats',
            'technical/mqtt',
            'technical/amqp'
          ]
        },
        {
          type: 'category',
          label: 'Databases',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/postgresql',
            'technical/mysql',
            'technical/mariadb',
            'technical/mongodb',
            'technical/cassandra',
            'technical/cockroachdb',
            'technical/couchdb',
            'technical/dynamodb',
            'technical/tidb',
            'technical/timescaledb',
            'technical/clickhouse',
            'technical/yugabyte'
          ]
        },
        {
          type: 'category',
          label: 'Storage & Backup',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/minio',
            'technical/ceph',
            'technical/glusterfs',
            'technical/velero',
            'technical/restic'
          ]
        },
        {
          type: 'category',
          label: 'Security & Secrets',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/security-compliance',
            'technical/vault',
            'technical/sealed-secrets',
            'technical/sops',
            'technical/cert-manager',
            'technical/lets-encrypt',
            'technical/keycloak',
            'technical/okta',
            'technical/oauth2-proxy',
            'technical/ldap',
            'technical/opa',
            'technical/gatekeeper',
            'technical/kyverno',
            'technical/falco',
            'technical/trivy',
            'technical/snyk',
            'technical/owasp-zap',
            'technical/sonarqube',
            'technical/container-security'
          ]
        },
        {
          type: 'category',
          label: 'Programming Languages',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/go',
            'technical/python',
            'technical/rust',
            'technical/javascript',
            'technical/typescript',
            'technical/ruby'
          ]
        },
        {
          type: 'category',
          label: 'APIs & Protocols',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/api-design-protocols',
            'technical/graphql',
            'technical/grpc',
            'technical/json',
            'technical/yaml',
            'technical/toml',
            'technical/hcl'
          ]
        },
        {
          type: 'category',
          label: 'Testing & Quality',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/k6',
            'technical/jmeter',
            'technical/gatling',
            'technical/selenium',
            'technical/postman'
          ]
        },
        {
          type: 'category',
          label: 'Cost & Compliance',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/kubecost',
            'technical/infracost'
          ]
        },
        {
          type: 'category',
          label: 'Documentation & Visualization',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/markdown',
            'technical/drawio',
            'technical/plantuml',
            'technical/confluence'
          ]
        },
        {
          type: 'category',
          label: 'Utilities & Tools',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/jq',
            'technical/yq',
            'technical/regex'
          ]
        },
        {
          type: 'category',
          label: 'AI/ML Infrastructure',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/ai-ml-platform',
            'technical/llm-infrastructure',
            'technical/vector-databases-ai'
          ]
        },
        {
          type: 'category',
          label: 'Interview Preparation',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/ai-interview-prep'
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
            'practice/interview-formats',
            'technical/ai-interview-prep'
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