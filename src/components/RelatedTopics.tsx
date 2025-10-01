import React from 'react';

interface RelatedTopic {
  title: string;
  url: string;
  description?: string;
}

interface RelatedTopicsProps {
  topics: RelatedTopic[];
}

export default function RelatedTopics({ topics }: RelatedTopicsProps) {
  return (
    <div style={{
      marginTop: '3rem',
      padding: '1.5rem',
      backgroundColor: 'var(--ifm-color-emphasis-100)',
      borderRadius: '8px',
      borderLeft: '4px solid var(--ifm-color-primary)',
    }}>
      <h3 style={{ marginTop: 0 }}>Related Topics</h3>
      <ul style={{ marginBottom: 0 }}>
        {topics.map((topic, idx) => (
          <li key={idx}>
            <a href={topic.url}><strong>{topic.title}</strong></a>
            {topic.description && <span> - {topic.description}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
