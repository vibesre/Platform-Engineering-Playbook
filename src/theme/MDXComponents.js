import React from 'react';
// Import the original mapper
import MDXComponents from '@theme-original/MDXComponents';
import GitHubButtonsSimple from '@site/src/components/GitHubButtonsSimple';

export default {
  // Re-use the default mapping
  ...MDXComponents,
  // Map the "GitHubButtons" tag to our GitHubButtons component
  GitHubButtons: GitHubButtonsSimple,
};