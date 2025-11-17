import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import DocSidebarItems from '@theme/DocSidebarItems';
import {ThemeClassNames} from '@docusaurus/theme-common';
import type {Props} from '@theme/BlogLayout';
import type {PropSidebarItem} from '@docusaurus/plugin-content-docs';
import sidebars from '../../../sidebars';

// Map of doc IDs to their proper display labels (matching frontmatter titles)
const docTitles: Record<string, string> = {
  'intro': 'Welcome',
  'technical/index': 'Platform Engineering Technical Skills',
  'technical/cloud-platforms': 'Cloud Platforms',
  'technical/aws': 'AWS',
  'technical/azure': 'Azure',
  'technical/gcp': 'GCP',
  'technical/kubernetes': 'Kubernetes',
  'technical/docker': 'Docker',
  'technical/terraform': 'Terraform',
  'technical/ansible': 'Ansible',
  // Add more as needed...
};

// Transform string items to have explicit labels
function transformSidebarItems(items: any[]): PropSidebarItem[] {
  return items.map(item => {
    if (typeof item === 'string') {
      const label = docTitles[item] || item.split('/').pop()?.replace(/-/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ') || item;

      // Map special paths to their correct URLs
      let href = `/${item}`;
      if (item === 'intro') {
        href = '/';
      } else if (item === 'technical/index') {
        href = '/technical-skills';
      }

      return {
        type: 'link',
        label: label,
        href: href,
      } as PropSidebarItem;
    }

    if (item.type === 'doc') {
      if (item.id === 'technical/index') {
        return null;
      }
      const label = item.label || docTitles[item.id] || item.id.split('/').pop()?.replace(/-/g, ' ')
        .split(' ')
        .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ') || item.id;

      // Map special paths to their correct URLs
      let href = `/${item.id}`;
      if (item.id === 'intro') {
        href = '/';
      } else if (item.id === 'technical/index') {
        href = '/technical-skills';
      }

      return {
        type: 'link',
        label: label,
        href: href,
      } as PropSidebarItem;
    }

    if (item.type === 'category' && item.items) {
      const transformedCategory = {
        ...item,
        items: transformSidebarItems(item.items).filter(Boolean),
      };

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

  const rawSidebarItems = sidebars.tutorialSidebar as any[];
  const sidebarItems = transformSidebarItems(rawSidebarItems);

  return (
    <Layout {...layoutProps}>
      <div className="container margin-vert--lg">
        <div className="row">
          {/* Left Sidebar - Hidden on mobile, visible on desktop */}
          <aside className={clsx('col col--3', 'blogSidebarHidden')}>
            <nav
              className={clsx(
                'menu thin-scrollbar',
                ThemeClassNames.docs.docSidebarMenu
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

          {/* Main Content */}
          <main className={clsx('col', 'col--9', 'blogMainContent')}>
            {children}
          </main>
        </div>
      </div>
    </Layout>
  );
}
