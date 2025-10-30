import React from 'react';
import BlogLayout from '@theme-original/BlogLayout';
import type BlogLayoutType from '@theme/BlogLayout';
import type {WrapperProps} from '@docusaurus/types';
import {ThemeClassNames} from '@docusaurus/theme-common';
import DocSidebarItems from '@theme/DocSidebarItems';
import tutorialSidebar from '../../../sidebars';

type Props = WrapperProps<typeof BlogLayoutType>;

export default function BlogLayoutWrapper(props: Props): JSX.Element {
  const sidebar = tutorialSidebar.tutorialSidebar;

  return (
    <div className={ThemeClassNames.wrapper.docsPages}>
      <div className="container margin-vert--lg">
        <div className="row">
          <aside className="col col--3">
            <nav className="menu thin-scrollbar">
              <DocSidebarItems items={sidebar} activePath="/blog" />
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
