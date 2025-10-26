#!/usr/bin/env python3
"""
Improved chunking for dialogue-based podcast scripts.
Handles alternating speaker format better than the original chunker.
"""

import re
import hashlib
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class DialogueChunk:
    """Represents a dialogue chunk with multiple speakers."""
    id: int
    segments: List[Tuple[str, str]]  # List of (speaker, text) tuples
    hash: str
    word_count: int
    primary_speaker: str  # Speaker with most words in chunk
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'segments': self.segments,
            'hash': self.hash,
            'word_count': self.word_count,
            'primary_speaker': self.primary_speaker
        }
    
    def get_text(self) -> str:
        """Get the full text of the chunk WITHOUT speaker names, WITH pause tags (for TTS)."""
        # Don't include speaker names - the TTS system uses voices to distinguish speakers
        # Add [pause] tags between different speakers for natural conversation flow
        result = []
        last_speaker = None

        for speaker, text in self.segments:
            # Add pause between speaker changes
            if last_speaker and speaker != last_speaker:
                result.append('[pause]')
            result.append(text)
            last_speaker = speaker

        return ' '.join(result)


class DialogueChunker:
    """Improved chunker for dialogue-based scripts - chunks by speaker segments."""

    def __init__(self, target_words: int = 100, max_words: int = 200):
        self.target_words = target_words
        self.max_words = max_words
        # Accept any speaker name (letters, numbers, spaces), validate afterward
        self.speaker_pattern = re.compile(r'^([A-Za-z0-9\s]+):\s*(.+)$', re.MULTILINE)

    def chunk_script(self, script_text: str) -> List[DialogueChunk]:
        """
        Split a dialogue script into chunks based on speaker segments.
        NEVER breaks within a speaker's segment - only chunks at speaker boundaries.

        Args:
            script_text: The full podcast script text

        Returns:
            List of DialogueChunk objects
        """
        # Parse all speaker segments first
        segments = self._parse_dialogue(script_text)

        # Group segments into chunks - ONLY break at speaker boundaries
        chunks = []
        chunk_id = 0
        current_segments = []
        current_word_count = 0

        for speaker, text in segments:
            segment_words = len(text.split())

            # CRITICAL FIX: ALWAYS break at speaker changes to ensure each speaker
            # gets their own voice in the TTS output. The old logic combined speakers
            # into one chunk, causing all dialogue to use the "primary speaker's" voice.
            is_speaker_change = current_segments and speaker != current_segments[-1][0]
            would_exceed_max = current_word_count + segment_words > self.max_words

            if current_segments and is_speaker_change:
                # ALWAYS break on speaker change - this ensures proper voice assignment
                chunk = self._create_chunk(chunk_id, current_segments)
                chunks.append(chunk)
                chunk_id += 1
                current_segments = [(speaker, text)]
                current_word_count = segment_words
            elif current_segments and would_exceed_max:
                # Must break here - adding this would exceed max
                chunk = self._create_chunk(chunk_id, current_segments)
                chunks.append(chunk)
                chunk_id += 1
                current_segments = [(speaker, text)]
                current_word_count = segment_words
            else:
                # Add to current chunk (same speaker continuation)
                current_segments.append((speaker, text))
                current_word_count += segment_words

        # Don't forget the last chunk
        if current_segments:
            chunk = self._create_chunk(chunk_id, current_segments)
            chunks.append(chunk)

        return chunks
    
    def _parse_dialogue(self, script_text: str) -> List[Tuple[str, str]]:
        """Parse script to extract (speaker, text) tuples."""
        segments = []
        
        lines = script_text.strip().split('\n')
        current_speaker = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a speaker line
            match = self.speaker_pattern.match(line)
            if match:
                # Save previous segment if any
                if current_speaker and current_text:
                    segments.append((current_speaker, ' '.join(current_text)))
                
                # Start new segment
                current_speaker = match.group(1)
                first_line = match.group(2).strip()
                current_text = [first_line] if first_line else []
            elif current_speaker:
                # Continuation of current speaker's text
                current_text.append(line)
        
        # Save final segment
        if current_speaker and current_text:
            segments.append((current_speaker, ' '.join(current_text)))
        
        return segments
    
    def _create_chunk(self, chunk_id: int, segments: List[Tuple[str, str]]) -> DialogueChunk:
        """Create a chunk from segments."""
        # Calculate total words and primary speaker
        speaker_words = {}
        total_words = 0

        for speaker, text in segments:
            words = len(text.split())
            total_words += words
            speaker_words[speaker] = speaker_words.get(speaker, 0) + words

        # Find primary speaker (most words)
        primary_speaker = max(speaker_words.items(), key=lambda x: x[1])[0]

        # Normalize speaker names (consistent with cloud_tts_generator.py)
        primary_speaker = self._normalize_speaker_name(primary_speaker)

        # Validate speaker is known
        known_speakers = ["jordan", "alex"]
        if primary_speaker not in known_speakers:
            raise ValueError(
                f"Unknown speaker detected: '{primary_speaker}'. "
                f"Valid speakers: {known_speakers}. "
                f"Check script for typos in speaker names."
            )

        # Create hash from content
        content_str = '|'.join(f"{s}:{t}" for s, t in segments)
        chunk_hash = hashlib.sha256(content_str.encode()).hexdigest()[:16]

        return DialogueChunk(
            id=chunk_id,
            segments=segments,
            hash=chunk_hash,
            word_count=total_words,
            primary_speaker=primary_speaker
        )

    def _normalize_speaker_name(self, speaker: str) -> str:
        """
        Normalize speaker name for consistent processing.

        Args:
            speaker: Raw speaker name

        Returns:
            Normalized speaker name (lowercase, mapped)
        """
        normalized = speaker.lower().strip()

        # Map "Speaker 1" and "Speaker 2" to "jordan" and "alex"
        if normalized == "speaker 1":
            return "jordan"
        elif normalized == "speaker 2":
            return "alex"

        return normalized


def main():
    """Test the dialogue chunker."""
    sample_dialogue = """
Alex: Welcome to the show! Today we're discussing cloud architecture.

Jordan: Thanks for having me. It's great to be here.

Alex: Let's start with the basics. What is cloud computing?

Jordan: Cloud computing is essentially using someone else's computers over the internet. Instead of running your own servers, you rent computing power from providers like AWS or Google.

Alex: That's a great explanation. How has it changed the industry?

Jordan: It's been revolutionary. Companies can now scale instantly without huge upfront investments in hardware.
    """
    
    chunker = DialogueChunker()
    chunks = chunker.chunk_script(sample_dialogue)
    
    print(f"Generated {len(chunks)} chunks:")
    for chunk in chunks:
        print(f"\nChunk {chunk.id} (primary: {chunk.primary_speaker}, {chunk.word_count} words):")
        print(f"Segments: {len(chunk.segments)}")
        print("Text:")
        print(chunk.get_text())
        print("-" * 50)


if __name__ == "__main__":
    main()