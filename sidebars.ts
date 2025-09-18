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
            'technical/system-administration',
            'technical/bash-scripting',
            'technical/process-management',
            'technical/file-systems'
          ]
        },
        {
          type: 'category',
          label: 'Networking',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/tcp-ip',
            'technical/dns',
            'technical/load-balancing',
            'technical/network-security',
            'technical/tls-ssl',
            'technical/network-troubleshooting'
          ]
        },
        {
          type: 'category',
          label: 'Cloud Platforms',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/aws',
            'technical/gcp',
            'technical/azure',
            'technical/cloud-architecture',
            'technical/cloud-networking',
            'technical/cloud-security'
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
            'technical/container-security',
            'technical/helm',
            'technical/service-mesh',
            'technical/operators'
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
            'technical/pulumi',
            'technical/cloudformation',
            'technical/crossplane'
          ]
        },
        {
          type: 'category',
          label: 'CI/CD & GitOps',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/git',
            'technical/github-actions',
            'technical/jenkins',
            'technical/gitlab-ci',
            'technical/argocd',
            'technical/flux'
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
            'technical/elasticsearch',
            'technical/opentelemetry',
            'technical/datadog',
            'technical/jaeger'
          ]
        },
        {
          type: 'category',
          label: 'Databases & Storage',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/postgresql',
            'technical/mysql',
            'technical/mongodb',
            'technical/redis',
            'technical/cassandra',
            'technical/object-storage'
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
            'technical/javascript',
            'technical/yaml',
            'technical/regex'
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
            'technical/redis-pubsub',
            'technical/nats',
            'technical/aws-messaging'
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