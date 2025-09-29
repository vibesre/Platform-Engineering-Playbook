import React, {useEffect, useRef} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useLocation} from '@docusaurus/router';

function GitHubButtonsInner() {
  const location = useLocation();
  const containerRef = useRef(null);
  
  // Construct the edit URL based on current page location
  const getEditUrl = () => {
    // Get the pathname without trailing slash
    let pathname = location.pathname.replace(/\/$/, '');
    
    // Handle special cases
    if (pathname === '' || pathname === '/') {
      return 'https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/docs/intro.md';
    }
    
    // For blog posts
    if (pathname.startsWith('/blog/')) {
      const blogSlug = pathname.replace('/blog/', '');
      return `https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/blog/${blogSlug}.md`;
    }
    
    // For docs pages
    let filePath = pathname;
    if (filePath.startsWith('/')) {
      filePath = filePath.substring(1);
    }
    
    // Add docs prefix if not present
    if (!filePath.startsWith('docs/')) {
      filePath = 'docs/' + filePath;
    }
    
    // Add .md extension if not present
    if (!filePath.endsWith('.md')) {
      filePath = filePath + '.md';
    }
    
    return `https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/${filePath}`;
  };

  useEffect(() => {
    let script = null;
    
    // Function to initialize buttons
    const initializeButtons = () => {
      if (typeof window !== 'undefined') {
        // Remove existing script if any
        const existingScript = document.getElementById('github-buttons-script');
        if (existingScript) {
          existingScript.remove();
        }
        
        // Create new script
        script = document.createElement('script');
        script.id = 'github-buttons-script';
        script.src = 'https://buttons.github.io/buttons.js';
        script.async = true;
        
        // Add script to container instead of document head
        if (containerRef.current) {
          containerRef.current.appendChild(script);
        }
      }
    };
    
    // Initialize on mount and route change
    initializeButtons();
    
    // Cleanup
    return () => {
      if (script && script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, [location.pathname]); // Re-run when pathname changes
  
  // Force re-render by using key
  return (
    <div key={location.pathname} ref={containerRef} style={{marginBottom: '20px', marginTop: '-10px', minHeight: '28px'}}>
      <a className="github-button" 
         href={getEditUrl()}
         data-icon="octicon-pencil" 
         data-size="large"
         aria-label="Edit this page on GitHub">
        Edit
      </a>
      {' '}
      <a className="github-button" 
         href="https://github.com/vibesre/Platform-Engineering-Playbook" 
         data-icon="octicon-star" 
         data-size="large" 
         data-show-count="true"
         aria-label="Star vibesre/Platform-Engineering-Playbook on GitHub">
        Star
      </a>
    </div>
  );
}

export default function GitHubButtons() {
  return (
    <BrowserOnly fallback={<div style={{height: '28px'}}></div>}>
      {() => <GitHubButtonsInner />}
    </BrowserOnly>
  );
}