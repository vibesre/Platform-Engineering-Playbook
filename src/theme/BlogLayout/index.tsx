import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import BlogSidebar from '@theme/BlogSidebar';
import DocSidebarItems from '@theme/DocSidebarItems';
import {ThemeClassNames} from '@docusaurus/theme-common';
import type {Props} from '@theme/BlogLayout';
import type {PropSidebarItem} from '@docusaurus/plugin-content-docs';
import tutorialSidebar from '../../../sidebars';

export default function BlogLayout(props: Props): React.ReactElement {
  const {sidebar, toc, children, ...layoutProps} = props;
  const hasBlogSidebar = sidebar && sidebar.items.length > 0;

  // Get docs sidebar items from sidebars configuration and cast to correct type
  const docsSidebar = tutorialSidebar.tutorialSidebar as PropSidebarItem[];

  return (
    <Layout {...layoutProps} wrapperClassName={clsx(ThemeClassNames.wrapper.blogPages, ThemeClassNames.page.blogListPage)}>
      <div className="container margin-vert--lg">
        <div className="row">
          {/* Left Column: Docs Sidebar (Technical Skills List) */}
          <aside className="col col--3">
            <div
              className={clsx(
                'theme-doc-sidebar-container',
                'docSidebarContainer_node_modules-@docusaurus-theme-classic-lib-theme-DocSidebar-Desktop-styles-module'
              )}
              style={{
                position: 'sticky',
                top: 'calc(var(--ifm-navbar-height) + 1rem)',
                maxHeight: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                overflow: 'hidden auto',
              }}
            >
              <nav className="menu thin-scrollbar menu__list">
                <DocSidebarItems
                  items={docsSidebar}
                  activePath="/blog"
                  level={1}
                />
              </nav>
            </div>
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
            <aside className="col col--3">
              <div
                style={{
                  position: 'sticky',
                  top: 'calc(var(--ifm-navbar-height) + 1rem)',
                  maxHeight: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                  overflowY: 'auto',
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
