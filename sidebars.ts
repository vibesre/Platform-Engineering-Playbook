import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  gettingStarted: [
    {
      type: 'doc',
      id: 'getting-started/index',
      label: 'Getting Started Overview'
    },
    {
      type: 'doc',
      id: 'intro',
      label: 'Welcome'
    },
    {
      type: 'doc',
      id: 'intro/index',
      label: 'Introduction to Platform Engineering'
    }
  ],

  technicalSkills: [
    {
      type: 'doc',
      id: 'technical/index',
      label: 'Technical Skills Overview'
    },
    {
      type: 'category',
      label: 'Core Fundamentals',
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
      items: [
        'programming/index',
        'algorithms/index'
      ]
    },
    {
      type: 'category',
      label: 'Infrastructure & Architecture',
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
      items: [
        'technical/caching-data-stores',
        'technical/message-queues-event-driven'
      ]
    },
    {
      type: 'category',
      label: 'AI/ML Infrastructure',
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
      items: [
        'technical/linux-deep-dive',
        'technical/cloud-platforms',
        'technical/api-design-protocols',
        'technical/security-compliance',
        'platform-engineering/index',
        'core-skills/index'
      ]
    }
  ],

  interviewPrep: [
    {
      type: 'doc',
      id: 'interview-prep/index',
      label: 'Interview Prep Overview'
    },
    {
      type: 'category',
      label: 'Interview Process',
      items: [
        'interview-process/index',
        'practice/interview-formats',
        'technical/ai-interview-prep'
      ]
    },
    {
      type: 'category',
      label: 'System Design',
      items: [
        'system-design/index'
      ]
    },
    {
      type: 'category',
      label: 'Behavioral',
      items: [
        'behavioral/index'
      ]
    },
    {
      type: 'category',
      label: 'Coding Challenges',
      items: [
        'coding-challenges/index'
      ]
    }
  ],

  careerGuide: [
    {
      type: 'doc',
      id: 'career-guide/index',
      label: 'Career Guide Overview'
    },
    {
      type: 'category',
      label: 'Job Search',
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
      items: [
        'career/index'
      ]
    },
    {
      type: 'category',
      label: 'Compensation & Negotiation',
      items: [
        'compensation/index',
        'get-hired/negotiation'
      ]
    }
  ],

  practiceResources: [
    {
      type: 'doc',
      id: 'practice-resources/index',
      label: 'Practice & Resources Overview'
    },
    {
      type: 'category',
      label: 'Hands-On Practice',
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
      items: [
        'company-specific/index'
      ]
    },
    {
      type: 'category',
      label: 'Additional Resources',
      items: [
        'resources/index'
      ]
    }
  ]
};

export default sidebars;