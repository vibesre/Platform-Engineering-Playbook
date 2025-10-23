import React from 'react';
import './PodcastSubscribeButtons.css';

export default function PodcastSubscribeButtons() {
  const platforms = [
    {
      name: 'YouTube',
      url: 'https://www.youtube.com/@platform-engineering-playbook',
      icon: '▶️', // YouTube play button
      color: '#FF0000',
    },
    {
      name: 'Apple Podcasts',
      url: 'https://podcasts.apple.com/us/podcast/platform-engineering-playbook-podcast/id1847172390',
      icon: '🎧', // Headphones for Apple
      color: '#9933CC',
    },
    {
      name: 'Spotify',
      url: 'https://open.spotify.com/show/68RowA7SeKgu9a2u1T3LfQ',
      icon: '🎵', // Music note for Spotify
      color: '#1DB954',
    },
    {
      name: 'Amazon Music',
      url: 'https://music.amazon.com/podcasts/62c174ad-d5f6-45a7-bfbe-a5a87601642c/platform-engineering-playbook-podcast',
      icon: '🔊', // Speaker for Amazon
      color: '#FF9900',
    },
  ];

  return (
    <div className="podcast-subscribe-container">
      <div className="podcast-subscribe-header">
        🎧 Subscribe & Listen
      </div>
      <div className="podcast-subscribe-buttons">
        {platforms.map((platform) => (
          <a
            key={platform.name}
            href={platform.url}
            target="_blank"
            rel="noopener noreferrer"
            className="podcast-subscribe-button"
            style={{ '--platform-color': platform.color }}
            title={`Listen on ${platform.name}`}
          >
            <span className="podcast-icon">{platform.icon}</span>
            <span className="podcast-name">{platform.name}</span>
          </a>
        ))}
      </div>
    </div>
  );
}
