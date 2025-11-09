import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import BlogLayout from '@theme/BlogLayout';
import type {Props} from '@theme/BlogListPage';
import Heading from '@theme/Heading';

function BlogListPageMetadata(props: Props): React.ReactElement {
  const {metadata} = props;
  return (
    <PageMetadata title={metadata.blogTitle} description={metadata.blogDescription} />
  );
}

function BlogListPageContent(props: Props): React.ReactElement {
  const {metadata, items} = props;

  return (
    <BlogLayout>
      <Heading as="h1">Blog</Heading>
      <p style={{marginBottom: '2rem', color: 'var(--ifm-color-emphasis-700)'}}>
        In-depth analysis, decision frameworks, and real-world insights for senior platform engineers.
      </p>

      <div style={{marginTop: '2rem'}}>
        {items.map(({content: BlogPostContent}) => {
          const {metadata: postMetadata, frontMatter} = BlogPostContent;
          const {permalink, title, date, description} = postMetadata;
          // Format date manually since formattedDate may not be available
          const formattedDate = new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          });

          return (
            <div key={permalink} style={{marginBottom: '2rem', paddingBottom: '1.5rem', borderBottom: '1px solid var(--ifm-color-emphasis-200)'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '0.5rem'}}>
                <Heading as="h2" style={{margin: 0, fontSize: '1.5rem'}}>
                  <a href={permalink} style={{color: 'var(--ifm-color-primary)', textDecoration: 'none'}}>
                    {title}
                  </a>
                </Heading>
                <time dateTime={date} style={{color: 'var(--ifm-color-emphasis-600)', fontSize: '0.9rem', whiteSpace: 'nowrap', marginLeft: '1rem'}}>
                  {formattedDate}
                </time>
              </div>
              {description && (
                <p style={{margin: 0, color: 'var(--ifm-color-emphasis-700)'}}>{description}</p>
              )}
            </div>
          );
        })}
      </div>
    </BlogLayout>
  );
}

export default function BlogListPage(props: Props): React.ReactElement {
  return (
    <HtmlClassNameProvider
      className={clsx(
        ThemeClassNames.wrapper.blogPages,
        ThemeClassNames.page.blogListPage,
      )}>
      <BlogListPageMetadata {...props} />
      <BlogListPageContent {...props} />
    </HtmlClassNameProvider>
  );
}
