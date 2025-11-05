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

export default function BlogLayout(props: Props): React.ReactElement {
  const {sidebar, toc, children, ...layoutProps} = props;
  const hasBlogSidebar = sidebar && sidebar.items.length > 0;

  // Get the sidebar items from sidebars.ts and cast to correct type
  const sidebarItems = sidebars.tutorialSidebar as PropSidebarItem[];

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