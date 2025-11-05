import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import clsx from 'clsx';
import sidebars from '../../sidebars';

// Type definitions matching Docusaurus sidebar structure
type SidebarItemDoc = {
  type: 'doc';
  id: string;
  label: string;
};

type SidebarItemLink = {
  type: 'link';
  label: string;
  href: string;
};

type SidebarItemCategory = {
  type: 'category';
  label: string;
  collapsed?: boolean;
  collapsible?: boolean;
  link?: {
    type: 'doc';
    id: string;
  };
  items: SidebarItem[];
};

type SidebarItem = string | SidebarItemDoc | SidebarItemLink | SidebarItemCategory;

// Helper function to convert doc ID to URL
function docIdToUrl(docId: string): string {
  // Since docs have routeBasePath: '/', doc IDs map directly to URLs
  return `/${docId}`;
}

// Recursive component to render sidebar items
function SidebarItemComponent({
  item,
  level = 0
}: {
  item: SidebarItem;
  level?: number;
}): React.ReactElement | null {
  // Initialize collapsed state from item config (default to collapsed if not specified)
  const initialCollapsed = typeof item === 'object' && item.type === 'category'
    ? (item.collapsed !== false) // collapsed by default unless explicitly false
    : false;

  const [isExpanded, setIsExpanded] = useState(!initialCollapsed);

  // Handle string items (shorthand for doc items)
  if (typeof item === 'string') {
    const label = item.split('/').pop() || item;
    return (
      <li>
        <Link className="menu__link" to={docIdToUrl(item)}>
          {label}
        </Link>
      </li>
    );
  }

  // Handle doc items
  if (item.type === 'doc') {
    return (
      <li>
        <Link className="menu__link" to={docIdToUrl(item.id)}>
          {item.label}
        </Link>
      </li>
    );
  }

  // Handle link items
  if (item.type === 'link') {
    return (
      <li>
        <Link className="menu__link" to={item.href}>
          {item.label}
        </Link>
      </li>
    );
  }

  // Handle category items
  if (item.type === 'category') {
    const paddingLeft = level > 0 ? `${(level + 1) * 1}rem` : '0.5rem 1rem';

    return (
      <li>
        {item.link ? (
          // Category with link - make label clickable, show expand indicator
          <>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <button
                className={clsx(
                  'menu__link',
                  'menu__link--sublist',
                  isExpanded && 'menu__link--sublist-caret'
                )}
                onClick={() => setIsExpanded(!isExpanded)}
                style={{
                  cursor: 'pointer',
                  background: 'none',
                  border: 'none',
                  width: '100%',
                  textAlign: 'left',
                  padding: paddingLeft
                }}
              >
                {item.label}
              </button>
            </div>
            {isExpanded && item.items && item.items.length > 0 && (
              <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                {/* Add the link target as first item */}
                <li>
                  <Link className="menu__link" to={docIdToUrl(item.link.id)}>
                    {item.label}
                  </Link>
                </li>
                {item.items.map((subItem, idx) => (
                  <SidebarItemComponent key={idx} item={subItem} level={level + 1} />
                ))}
              </ul>
            )}
          </>
        ) : (
          // Category without link - just render as expandable button
          <>
            <button
              className={clsx(
                'menu__link',
                'menu__link--sublist',
                isExpanded && 'menu__link--sublist-caret'
              )}
              onClick={() => setIsExpanded(!isExpanded)}
              style={{
                cursor: 'pointer',
                background: 'none',
                border: 'none',
                width: '100%',
                textAlign: 'left',
                padding: paddingLeft
              }}
            >
              {item.label}
            </button>
            {isExpanded && item.items && item.items.length > 0 && (
              <ul className="menu__list" style={{ paddingLeft: '1rem' }}>
                {item.items.map((subItem, idx) => (
                  <SidebarItemComponent key={idx} item={subItem} level={level + 1} />
                ))}
              </ul>
            )}
          </>
        )}
      </li>
    );
  }

  return null;
}

export default function BlogNavigation(): React.ReactElement {
  // Get the tutorialSidebar from sidebars.ts
  const sidebarItems = sidebars.tutorialSidebar as SidebarItem[];

  return (
    <nav
      className="menu thin-scrollbar"
      style={{
        position: 'sticky',
        top: 'calc(var(--ifm-navbar-height) + 1rem)',
        height: 'calc(100vh - var(--ifm-navbar-height) - 2rem)',
        overflowY: 'auto',
        padding: '1rem 0'
      }}
    >
      <ul className="menu__list">
        {sidebarItems.map((item, idx) => (
          <SidebarItemComponent key={idx} item={item} />
        ))}
      </ul>
    </nav>
  );
}
