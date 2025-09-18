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
            'technical/linux-deep-dive'
          ]
        },
        {
          type: 'category',
          label: 'Cloud Platforms',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/aws',
            'technical/cloud-platforms'
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
            'technical/kubernetes-mastery',
            'technical/serverless-edge-computing'
          ]
        },
        {
          type: 'category',
          label: 'Infrastructure as Code',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/terraform'
          ]
        },
        {
          type: 'category',
          label: 'Monitoring & Observability',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/chaos-engineering',
            'technical/sre-practices-incident-management'
          ]
        },
        {
          type: 'category',
          label: 'APIs & Integration',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/api-design-protocols'
          ]
        },
        {
          type: 'category',
          label: 'Data & Storage',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/caching-data-stores',
            'technical/message-queues-event-driven'
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
          label: 'Security & Compliance',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/security-compliance'
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