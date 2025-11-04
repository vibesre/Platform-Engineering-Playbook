import React from 'react';
import BlogLayout from '@theme-original/BlogLayout';
import type BlogLayoutType from '@theme/BlogLayout';
import type {WrapperProps} from '@docusaurus/types';
import type {PropSidebarItem} from '@docusaurus/plugin-content-docs';
import {ThemeClassNames} from '@docusaurus/theme-common';
import DocSidebarItems from '@theme/DocSidebarItems';
import tutorialSidebar from '../../../sidebars';

type Props = WrapperProps<typeof BlogLayoutType>;

export default function BlogLayoutWrapper(props: Props): React.ReactElement {
  const sidebar = tutorialSidebar.tutorialSidebar as PropSidebarItem[];

  return (
    <div className={ThemeClassNames.wrapper.docsPages}>
      <div className="container margin-vert--lg">
        <div className="row">
          <aside className="col col--3">
            <nav className="menu thin-scrollbar">
              <DocSidebarItems items={sidebar} activePath="/blog" level={1} />
            </nav>
          </aside>
          <main className="col col--9">
            <BlogLayout {...props} />
          </main>
        </div>
      </div>
    </div>
  );
}
