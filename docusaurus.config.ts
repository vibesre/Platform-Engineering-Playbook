import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Platform Engineering Playbook',
  tagline: 'Your comprehensive guide to Platform Engineering, SRE, and DevOps interviews',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://platformengineeringplaybook.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'vibesre', // Usually your GitHub org/user name.
  projectName: 'Platform-Engineering-Playbook', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
    localeConfigs: {
      en: {
        htmlLang: 'en-US',
        label: 'English',
      },
    },
  },

  // SEO metadata
  headTags: [
    // Preconnect to external domains for performance
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.googleapis.com',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'dns-prefetch',
        href: 'https://www.google-analytics.com',
      },
    },
    // Meta tags for SEO
    {
      tagName: 'meta',
      attributes: {
        name: 'keywords',
        content: 'platform engineering, SRE, DevOps, kubernetes, terraform, docker, AWS, interview preparation, site reliability engineering, DevOps engineer, cloud platforms, container orchestration',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'author',
        content: 'Platform Engineering Playbook',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'robots',
        content: 'index, follow',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        property: 'og:type',
        content: 'website',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'twitter:card',
        content: 'summary_large_image',
      },
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl:
            'https://github.com/vibesre/Platform-Engineering-Playbook/tree/main/',
          showLastUpdateTime: false,
          showLastUpdateAuthor: false,
          breadcrumbs: true,
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/vibesre/Platform-Engineering-Playbook/tree/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
          blogSidebarTitle: 'Recent Posts',
          blogSidebarCount: 'ALL',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'G-JYN3ZYTSNR',
          anonymizeIP: true,
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/tags/**', '/blog/tags/**', '/blog/archive'],
          filename: 'sitemap.xml',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/social-card.jpg',
    navbar: {
      title: 'Platform Engineering Playbook',
      logo: {
        alt: 'Platform Engineering Logo',
        src: 'img/logo_square.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          to: '/blog',
          position: 'left',
          label: 'Blog',
        },
        {
          href: 'https://github.com/vibesre/Platform-Engineering-Playbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Welcome',
              to: '/',
            },
            {
              label: 'Technical Skills',
              to: '/technical-skills',
            },
          ],
        },
        {
          title: 'Prepare',
          items: [
            {
              label: 'Interview Prep',
              to: '/interview-prep',
            },
            {
              label: 'Career Guide',
              to: '/career-guide',
            },
            {
              label: 'Practice Labs',
              to: '/practice-resources',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/vibesre/Platform-Engineering-Playbook',
            },
            {
              label: 'Contribute',
              href: 'https://github.com/vibesre/Platform-Engineering-Playbook/pulls',
            },
            {
              label: 'Report Issues',
              href: 'https://github.com/vibesre/Platform-Engineering-Playbook/issues',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Platform Engineering Playbook. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
