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

  // Get docs sidebar items from sidebars configuration
  const docsSidebar = tutorialSidebar.tutorialSidebar as PropSidebarItem[];

  return (
    <Layout {...layoutProps} wrapperClassName={ThemeClassNames.wrapper.blogPages}>
      <div className="container margin-vert--lg">
        <div className="row">
          {/* Left Column: Docs Sidebar (Technical Skills List) */}
          <aside className="col col--3 theme-doc-sidebar-container">
            <nav
              className="menu thin-scrollbar menu_node_modules-@docusaurus-theme-classic-lib-theme-DocSidebar-Desktop-Content-styles-module"
              style={{
                position: 'sticky',
                top: 'calc(var(--ifm-navbar-height) + 1rem)',
                height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                overflowY: 'auto',
                padding: '1rem 0'
              }}
            >
              <ul className="menu__list">
                <DocSidebarItems
                  items={docsSidebar}
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
              hasBlogSidebar ? 'col--6' : 'col--7',
              'blog-main-content'
            )}
            style={{
              padding: '0 2rem'
            }}
          >
            {children}
          </main>

          {/* Right Column: Blog Sidebar (Recent Posts) - Conditional */}
          {hasBlogSidebar && (
            <aside
              className="col col--3 blog-sidebar-container"
              style={{
                position: 'sticky',
                top: 'calc(var(--ifm-navbar-height) + 1rem)',
                height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                overflowY: 'auto'
              }}
            >
              <BlogSidebar sidebar={sidebar} />
            </aside>
          )}

          {/* If there's a Table of Contents but no blog sidebar, render TOC on right */}
          {!hasBlogSidebar && toc && (
            <div
              className="col col--2"
              style={{
                position: 'sticky',
                top: 'calc(var(--ifm-navbar-height) + 1rem)',
                height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
                overflowY: 'auto'
              }}
            >
              {toc}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}