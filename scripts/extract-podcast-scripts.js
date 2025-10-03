#!/usr/bin/env node
/**
 * Extract raw podcast scripts and metadata from existing markdown files.
 * Outputs:
 * - docs/podcasts/scripts/{slug}.txt - Raw dialogue in "Speaker 1: text" format
 * - docs/podcasts/metadata/{slug}.json - Episode metadata
 */

const fs = require('fs');
const path = require('path');

const PODCASTS_DIR = path.join(__dirname, '..', 'docs', 'podcasts');
const SCRIPTS_DIR = path.join(PODCASTS_DIR, 'scripts');
const METADATA_DIR = path.join(PODCASTS_DIR, 'metadata');

// Speaker name mappings
const SPEAKER_MAPPING = {
  'Alex': 'Speaker 2',
  'Jordan': 'Speaker 1'
};

function extractDialogue(content) {
  const lines = content.split('\n');
  const dialogue = [];

  for (const line of lines) {
    const trimmed = line.trim();

    // Match speaker dialogue: **Speaker:** text or Speaker: text
    const match = trimmed.match(/^\*?\*?(Alex|Jordan):\*?\*?\s*(.+)$/);
    if (match) {
      const speaker = match[1];
      const text = match[2].trim();
      const speakerNum = SPEAKER_MAPPING[speaker];
      dialogue.push(`${speakerNum}: ${text}`);
    }
  }

  return dialogue.join('\n');
}

function extractMetadata(content, filename) {
  const slug = path.basename(filename, '.md');

  // Extract title (first # heading)
  const titleMatch = content.match(/^#\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1] : '';

  // Extract subtitle (## Episode: ...)
  const subtitleMatch = content.match(/^##\s+Episode:\s+(.+)$/m);
  const subtitle = subtitleMatch ? subtitleMatch[1] : '';

  // Extract duration
  const durationMatch = content.match(/\*\*Duration:\*\*\s*(.+)/);
  const duration = durationMatch ? durationMatch[1].trim() : '';

  // Extract related guide link
  const guideMatch = content.match(/>\s*📚\s*\*\*Read the full guide\*\*:\s*\[([^\]]+)\]\(([^)]+)\)/);
  const relatedGuide = guideMatch ? {
    title: guideMatch[1],
    url: guideMatch[2]
  } : null;

  return {
    id: slug,
    title: title,
    subtitle: subtitle,
    duration: duration,
    datePublished: new Date().toISOString().split('T')[0],
    relatedGuide: relatedGuide,
    speakers: {
      "Speaker 1": { "name": "Jordan", "role": "Host" },
      "Speaker 2": { "name": "Alex", "role": "Co-host" }
    },
    seo: {
      description: subtitle.substring(0, 160),
      keywords: [],
      schema: "PodcastEpisode"
    }
  };
}

function processPodcast(filepath) {
  console.log(`Processing: ${filepath}`);

  const content = fs.readFileSync(filepath, 'utf8');
  const filename = path.basename(filepath);
  const slug = filename.replace('.md', '');

  // Extract dialogue
  const dialogue = extractDialogue(content);
  const scriptPath = path.join(SCRIPTS_DIR, `${slug}.txt`);
  fs.writeFileSync(scriptPath, dialogue, 'utf8');
  console.log(`  ✓ Wrote script: ${scriptPath}`);

  // Extract metadata
  const metadata = extractMetadata(content, filename);
  const metadataPath = path.join(METADATA_DIR, `${slug}.json`);
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2), 'utf8');
  console.log(`  ✓ Wrote metadata: ${metadataPath}`);

  // Stats
  const dialogueLines = dialogue.split('\n').length;
  console.log(`  📊 ${dialogueLines} dialogue lines extracted\n`);
}

function main() {
  console.log('🎙️  Extracting podcast scripts and metadata...\n');

  // Get all podcast markdown files (exclude index pages)
  const podcastFiles = fs.readdirSync(PODCASTS_DIR)
    .filter(f => f.endsWith('-episode.md'))
    .map(f => path.join(PODCASTS_DIR, f));

  console.log(`Found ${podcastFiles.length} podcast files\n`);

  // Process each podcast
  podcastFiles.forEach(processPodcast);

  console.log('✅ Extraction complete!');
  console.log(`\nOutput:`);
  console.log(`  Scripts: ${SCRIPTS_DIR}`);
  console.log(`  Metadata: ${METADATA_DIR}`);
}

main();
