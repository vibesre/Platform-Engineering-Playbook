#!/usr/bin/env python3
"""
Text chunking logic for podcast scripts.
Splits text into semantic chunks suitable for TTS generation.
"""

import re
import hashlib
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a single audio chunk."""
    id: int
    speaker: str
    text: str
    hash: str
    word_count: int
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'speaker': self.speaker,
            'text': self.text,
            'hash': self.hash,
            'word_count': self.word_count
        }


class PodcastChunker:
    """Handles chunking of podcast scripts into manageable segments."""
    
    def __init__(self, min_words: int = 80, max_words: int = 150):
        self.min_words = min_words
        self.max_words = max_words
        self.speaker_pattern = re.compile(r'^(Speaker \d+|Jordan|Alex):\s*(.+)', re.MULTILINE)
    
    def chunk_script(self, script_text: str) -> List[Chunk]:
        """
        Split a podcast script into chunks.
        
        Args:
            script_text: The full podcast script text
            
        Returns:
            List of Chunk objects
        """
        chunks = []
        chunk_id = 0
        
        # Parse the script to identify speakers and their lines
        segments = self._parse_speakers(script_text)
        
        # Process each segment and create chunks
        for speaker, lines in segments:
            # Group lines into chunks based on word count
            current_chunk_text = []
            current_word_count = 0
            
            for line in lines:
                line_word_count = len(line.split())
                
                # Check if adding this line would exceed max words
                if current_word_count > 0 and current_word_count + line_word_count > self.max_words:
                    # Create chunk with current accumulated text
                    chunk_text = ' '.join(current_chunk_text)
                    chunks.append(self._create_chunk(chunk_id, speaker, chunk_text))
                    chunk_id += 1
                    
                    # Start new chunk
                    current_chunk_text = [line]
                    current_word_count = line_word_count
                else:
                    current_chunk_text.append(line)
                    current_word_count += line_word_count
            
            # Create chunk with remaining text
            if current_chunk_text:
                chunk_text = ' '.join(current_chunk_text)
                # Only create chunk if it meets minimum words or is the last bit
                if current_word_count >= self.min_words or not chunks:
                    chunks.append(self._create_chunk(chunk_id, speaker, chunk_text))
                    chunk_id += 1
                else:
                    # Append to previous chunk if too small
                    if chunks:
                        prev_chunk = chunks[-1]
                        new_text = f"{prev_chunk.text} {chunk_text}"
                        chunks[-1] = self._create_chunk(
                            prev_chunk.id, 
                            prev_chunk.speaker, 
                            new_text
                        )
        
        return chunks
    
    def _parse_speakers(self, script_text: str) -> List[Tuple[str, List[str]]]:
        """Parse script to extract speaker segments."""
        segments = []
        current_speaker = None
        current_lines = []
        
        lines = script_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts with a speaker identifier
            match = self.speaker_pattern.match(line)
            if match:
                # Save previous speaker's lines
                if current_speaker and current_lines:
                    segments.append((current_speaker, current_lines))
                
                # Start new speaker segment
                current_speaker = match.group(1)
                first_line = match.group(2).strip()
                if first_line:
                    current_lines = [first_line]
                else:
                    current_lines = []
            else:
                # Continue with current speaker
                if current_speaker:
                    current_lines.append(line)
        
        # Save final speaker's lines
        if current_speaker and current_lines:
            segments.append((current_speaker, current_lines))
        
        return segments
    
    def _create_chunk(self, chunk_id: int, speaker: str, text: str) -> Chunk:
        """Create a chunk with calculated hash."""
        # Normalize speaker names
        if speaker == "Speaker 1":
            speaker = "jordan"
        elif speaker == "Speaker 2":
            speaker = "alex"
        else:
            speaker = speaker.lower()
        
        text = text.strip()
        chunk_hash = hashlib.sha256(f"{speaker}:{text}".encode()).hexdigest()[:16]
        word_count = len(text.split())
        
        return Chunk(
            id=chunk_id,
            speaker=speaker,
            text=text,
            hash=chunk_hash,
            word_count=word_count
        )


def main():
    """Test the chunker with a sample script."""
    sample_script = """
Speaker 1: Welcome to The Platform Engineering Playbook! I'm Jordan.

Speaker 2: And I'm Alex. Today we're diving into the world of container orchestration, specifically looking at Kubernetes and its alternatives.

Speaker 1: Kubernetes has become the de facto standard for container orchestration, but it's not the only game in town. We'll explore why it dominates, what problems it solves, and when you might want to consider alternatives.

Speaker 2: That's right. While Kubernetes is incredibly powerful, it's also complex. For teams just starting their container journey or those with simpler needs, there are other options worth considering. We'll look at Docker Swarm, Nomad, and even some newer players in the space.
    """
    
    chunker = PodcastChunker()
    chunks = chunker.chunk_script(sample_script)
    
    print("Generated chunks:")
    for chunk in chunks:
        print(f"\nChunk {chunk.id} ({chunk.speaker}, {chunk.word_count} words):")
        print(f"Hash: {chunk.hash}")
        print(f"Text: {chunk.text[:100]}...")


if __name__ == "__main__":
    main()