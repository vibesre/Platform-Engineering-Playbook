import React, {useState, useEffect} from 'react';
import {useLocation} from '@docusaurus/router';
import './GitHubButtons.css';

export default function GitHubButtonsSimple() {
  const location = useLocation();
  const [starCount, setStarCount] = useState(null);
  
  useEffect(() => {
    // Fetch star count from GitHub API
    fetch('https://api.github.com/repos/vibesre/Platform-Engineering-Playbook')
      .then(response => response.json())
      .then(data => {
        if (data.stargazers_count) {
          setStarCount(data.stargazers_count);
        }
      })
      .catch(err => {
        console.error('Failed to fetch star count:', err);
      });
  }, []); // Only run once on mount
  
  // Format star count (e.g., 1234 -> 1.2k)
  const formatStarCount = (count) => {
    if (count >= 1000) {
      return (count / 1000).toFixed(1) + 'k';
    }
    return count.toString();
  };
  
  // Construct the edit URL based on current page location
  const getEditUrl = () => {
    let pathname = location.pathname.replace(/\/$/, '');
    
    if (pathname === '' || pathname === '/') {
      return 'https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/docs/intro.md';
    }
    
    if (pathname.startsWith('/blog/')) {
      const blogSlug = pathname.replace('/blog/', '');
      return `https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/blog/${blogSlug}.md`;
    }
    
    let filePath = pathname;
    if (filePath.startsWith('/')) {
      filePath = filePath.substring(1);
    }
    
    if (!filePath.startsWith('docs/')) {
      filePath = 'docs/' + filePath;
    }
    
    if (!filePath.endsWith('.md')) {
      filePath = filePath + '.md';
    }
    
    return `https://github.com/vibesre/Platform-Engineering-Playbook/edit/main/${filePath}`;
  };

  return (
    <div className="github-buttons-container">
      <a href={getEditUrl()} className="github-button-custom" target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 16 16" version="1.1" aria-hidden="true">
          <path fillRule="evenodd" d="M11.013 1.427a1.75 1.75 0 012.474 0l1.086 1.086a1.75 1.75 0 010 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 01-.927-.928l.929-3.25a1.75 1.75 0 01.445-.758l8.61-8.61zm1.414 1.06a.25.25 0 00-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 000-.354l-1.086-1.086zM11.189 6.25L9.75 4.81l-6.286 6.287a.25.25 0 00-.064.108l-.558 1.953 1.953-.558a.249.249 0 00.108-.064l6.286-6.286z"></path>
        </svg>
        Edit on GitHub
      </a>
      <a href="https://github.com/vibesre/Platform-Engineering-Playbook" className="github-button-custom" target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 16 16" version="1.1" aria-hidden="true">
          <path fillRule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"></path>
        </svg>
        Star
        {starCount !== null && (
          <span className="github-star-count">{formatStarCount(starCount)}</span>
        )}
      </a>
    </div>
  );
}