import React, { useEffect, useState } from 'react';
import DialogueBlock from './DialogueBlock';
import GitHubButtons from './GitHubButtons';
import styles from './PodcastEpisode.module.css';

interface EpisodeMetadata {
  id: string;
  title: string;
  subtitle: string;
  duration: string;
  datePublished: string;
  relatedGuide?: {
    title: string;
    url: string;
  };
  speakers: {
    [key: string]: {
      name: string;
      role: string;
    };
  };
  seo: {
    description: string;
    keywords: string[];
    schema: string;
  };
}

interface DialogueLine {
  speaker: string;
  text: string;
}

interface PodcastEpisodeProps {
  episodeId: string;
}

export default function PodcastEpisode({ episodeId }: PodcastEpisodeProps): JSX.Element {
  const [metadata, setMetadata] = useState<EpisodeMetadata | null>(null);
  const [dialogue, setDialogue] = useState<DialogueLine[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadEpisode() {
      try {
        // episodeId may have format "00001-episode-name" or "episode-name"
        // Always use the full episodeId for file loading
        const fileId = episodeId;

        // Load metadata
        const metadataRes = await fetch(`/podcasts/metadata/${fileId}.json`);
        if (!metadataRes.ok) throw new Error('Failed to load metadata');
        const meta = await metadataRes.json();
        setMetadata(meta);

        // Load script
        const scriptRes = await fetch(`/podcasts/scripts/${fileId}.txt`);
        if (!scriptRes.ok) throw new Error('Failed to load script');
        const script = await scriptRes.text();

        // Parse dialogue
        const lines = script.split('\n').filter(line => line.trim());
        const parsed = lines.map(line => {
          const match = line.match(/^(Speaker \d+):\s*(.+)$/);
          if (match) {
            return { speaker: match[1], text: match[2] };
          }
          return null;
        }).filter(Boolean) as DialogueLine[];

        setDialogue(parsed);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }

    loadEpisode();
  }, [episodeId]);

  if (loading) {
    return <div className={styles.loading}>Loading podcast...</div>;
  }

  if (error) {
    return <div className={styles.error}>Error loading podcast: {error}</div>;
  }

  if (!metadata) {
    return <div className={styles.error}>No metadata found</div>;
  }

  return (
    <div className={styles.episode}>
      {/* Header */}
      <header className={styles.header}>
        <h1>{metadata.title}</h1>
        <GitHubButtons />
        <h2 className={styles.subtitle}>Episode: {metadata.subtitle}</h2>

        <div className={styles.meta}>
          <span><strong>Duration:</strong> {metadata.duration}</span>
          <span><strong>Speakers:</strong> {Object.values(metadata.speakers).map(s => s.name).join(' and ')}</span>
          <span><strong>Target Audience:</strong> Senior platform engineers, SREs, DevOps engineers with 5+ years experience</span>
        </div>

        {metadata.relatedGuide && (
          <div className={styles.relatedGuide}>
            📚 <strong>Read the full guide</strong>:{' '}
            <a href={metadata.relatedGuide.url}>{metadata.relatedGuide.title}</a>
            {' '}- Complete implementation guide with ROI data, tool comparisons, and rollout strategy.
          </div>
        )}
      </header>

      {/* TODO: Audio player component */}
      {/* <PodcastPlayer episodeId={episodeId} /> */}

      {/* Dialogue */}
      <div className={styles.dialogue}>
        <h3>Episode Transcript</h3>
        {dialogue.map((line, index) => {
          const speakerInfo = metadata.speakers[line.speaker];
          return (
            <DialogueBlock
              key={index}
              speaker={line.speaker}
              speakerName={speakerInfo?.name || line.speaker}
              text={line.text}
            />
          );
        })}
      </div>

      {/* SEO Schema */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'PodcastEpisode',
            name: metadata.title,
            description: metadata.seo.description,
            datePublished: metadata.datePublished,
            duration: metadata.duration,
            keywords: metadata.seo.keywords.join(', ')
          })
        }}
      />
    </div>
  );
}
