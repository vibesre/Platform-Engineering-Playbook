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
          label: 'Core Fundamentals',
          collapsed: true,
          collapsible: true,
          items: [
            'core-technical/index',
            'core-technical/linux-systems',
            'core-technical/networking',
            'core-technical/cloud-platforms'
          ]
        },
        {
          type: 'category',
          label: 'Programming & Scripting',
          collapsed: true,
          collapsible: true,
          items: [
            'programming/index',
            'algorithms/index'
          ]
        },
        {
          type: 'category',
          label: 'Infrastructure & Architecture',
          collapsed: true,
          collapsible: true,
          items: [
            'platform-infrastructure/index',
            'platform-infrastructure/distributed-systems',
            'technical/kubernetes-mastery',
            'technical/serverless-edge-computing'
          ]
        },
        {
          type: 'category',
          label: 'Reliability & Operations',
          collapsed: true,
          collapsible: true,
          items: [
            'reliability-operations/index',
            'technical/sre-practices-incident-management',
            'technical/chaos-engineering',
            'troubleshooting/index'
          ]
        },
        {
          type: 'category',
          label: 'Data & Messaging',
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
            'technical/vector-databases-ai',
            'career/ai-platform-roadmap'
          ]
        },
        {
          type: 'category',
          label: 'Advanced Topics',
          collapsed: true,
          collapsible: true,
          items: [
            'technical/linux-deep-dive',
            'technical/cloud-platforms',
            'technical/api-design-protocols',
            'technical/security-compliance',
            'platform-engineering/index',
            'core-skills/index'
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