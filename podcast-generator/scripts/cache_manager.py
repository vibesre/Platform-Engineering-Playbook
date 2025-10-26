#!/usr/bin/env python3
"""
Cache management for podcast chunks.
Handles storing, retrieving, and tracking chunk metadata.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class CacheManager:
    """Manages the cache of generated audio chunks."""
    
    def __init__(self, cache_dir: str = "cache", manifest_file: str = "cache/manifest.json"):
        self.cache_dir = Path(cache_dir)
        self.chunks_dir = self.cache_dir / "chunks"
        self.manifest_file = Path(manifest_file)
        
        # Create directories if they don't exist
        self.cache_dir.mkdir(exist_ok=True)
        self.chunks_dir.mkdir(exist_ok=True)
        
        # Load or create manifest
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """Load the manifest file or create empty one."""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                return json.load(f)
        return {"episodes": {}}
    
    def save_manifest(self):
        """Save the current manifest to disk."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def get_episode_manifest(self, episode_id: str) -> Dict:
        """Get manifest data for a specific episode."""
        if episode_id not in self.manifest["episodes"]:
            self.manifest["episodes"][episode_id] = {
                "chunks": {},
                "last_updated": datetime.now().isoformat(),
                "version": 1
            }
        return self.manifest["episodes"][episode_id]
    
    def is_chunk_cached(self, episode_id: str, chunk_hash: str) -> bool:
        """Check if a chunk with given hash exists in cache."""
        episode_manifest = self.get_episode_manifest(episode_id)
        if chunk_hash in episode_manifest["chunks"]:
            chunk_path = self.get_chunk_path(episode_id, chunk_hash)
            return chunk_path.exists()
        return False
    
    def get_chunk_path(self, episode_id: str, chunk_hash: str) -> Path:
        """Get the file path for a chunk."""
        episode_dir = self.chunks_dir / episode_id
        episode_dir.mkdir(exist_ok=True)
        return episode_dir / f"chunk_{chunk_hash}.mp3"
    
    def register_chunk(self, episode_id: str, chunk_data: Dict):
        """Register a new chunk in the manifest."""
        episode_manifest = self.get_episode_manifest(episode_id)
        chunk_hash = chunk_data["hash"]

        episode_manifest["chunks"][chunk_hash] = {
            "id": chunk_data["id"],
            "speaker": chunk_data["speaker"],
            "text_preview": chunk_data["text"][:50] + "...",
            "word_count": chunk_data["word_count"],
            "duration": chunk_data.get("duration", 0),
            "voice": chunk_data.get("voice", "unknown"),  # Track which voice was used
            "generated_at": datetime.now().isoformat()
        }

        episode_manifest["last_updated"] = datetime.now().isoformat()
        self.save_manifest()
    
    def get_ordered_chunks(self, episode_id: str, chunk_hashes: List[str]) -> List[Path]:
        """Get ordered list of chunk file paths."""
        paths = []
        for chunk_hash in chunk_hashes:
            if self.is_chunk_cached(episode_id, chunk_hash):
                paths.append(self.get_chunk_path(episode_id, chunk_hash))
        return paths
    
    def clean_orphaned_chunks(self, episode_id: str, active_hashes: List[str]):
        """Remove chunks that are no longer needed."""
        episode_manifest = self.get_episode_manifest(episode_id)
        
        # Find orphaned chunks
        orphaned = set(episode_manifest["chunks"].keys()) - set(active_hashes)
        
        for chunk_hash in orphaned:
            # Delete file
            chunk_path = self.get_chunk_path(episode_id, chunk_hash)
            if chunk_path.exists():
                chunk_path.unlink()
            
            # Remove from manifest
            del episode_manifest["chunks"][chunk_hash]
        
        if orphaned:
            episode_manifest["last_updated"] = datetime.now().isoformat()
            self.save_manifest()
            print(f"Cleaned {len(orphaned)} orphaned chunks")
    
    def is_chunk_voice_valid(self, episode_id: str, chunk_hash: str, expected_voice: str) -> bool:
        """
        Check if a cached chunk was generated with the expected voice.

        Args:
            episode_id: Episode identifier
            chunk_hash: Chunk hash
            expected_voice: Expected voice name (e.g., "en-US-Neural2-J")

        Returns:
            True if voice matches or unknown, False if mismatch detected
        """
        episode_manifest = self.get_episode_manifest(episode_id)

        if chunk_hash not in episode_manifest["chunks"]:
            return False

        chunk_metadata = episode_manifest["chunks"][chunk_hash]
        cached_voice = chunk_metadata.get("voice", "unknown")

        # If voice is unknown (old cache), assume valid for now
        if cached_voice == "unknown":
            return True

        # Check if voices match
        return cached_voice == expected_voice

    def get_cache_stats(self, episode_id: str) -> Dict:
        """Get statistics about the cache for an episode."""
        episode_manifest = self.get_episode_manifest(episode_id)

        total_chunks = len(episode_manifest["chunks"])
        total_size = 0

        episode_dir = self.chunks_dir / episode_id
        if episode_dir.exists():
            for chunk_file in episode_dir.glob("chunk_*.mp3"):
                total_size += chunk_file.stat().st_size

        return {
            "total_chunks": total_chunks,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "last_updated": episode_manifest["last_updated"],
            "version": episode_manifest["version"]
        }

    def validate_voice_consistency(self, episode_id: str, voice_mapping: Dict[str, str]) -> Dict:
        """
        Validate that all cached chunks use the expected voices.

        Args:
            episode_id: Episode identifier
            voice_mapping: Dict of speaker -> expected voice name

        Returns:
            Dict with validation results
        """
        episode_manifest = self.get_episode_manifest(episode_id)

        mismatches = []
        unknown_voices = []

        for chunk_hash, chunk_metadata in episode_manifest["chunks"].items():
            speaker = chunk_metadata.get("speaker", "unknown")
            cached_voice = chunk_metadata.get("voice", "unknown")
            expected_voice = voice_mapping.get(speaker)

            if cached_voice == "unknown":
                unknown_voices.append({
                    "chunk_id": chunk_metadata.get("id"),
                    "speaker": speaker,
                    "hash": chunk_hash
                })
            elif expected_voice and cached_voice != expected_voice:
                mismatches.append({
                    "chunk_id": chunk_metadata.get("id"),
                    "speaker": speaker,
                    "expected": expected_voice,
                    "actual": cached_voice,
                    "hash": chunk_hash
                })

        return {
            "total_chunks": len(episode_manifest["chunks"]),
            "mismatches": mismatches,
            "unknown_voices": unknown_voices,
            "is_valid": len(mismatches) == 0
        }


def main():
    """Test the cache manager."""
    cache = CacheManager()
    
    # Test registering a chunk
    test_chunk = {
        "id": 0,
        "hash": "abc123",
        "speaker": "jordan",
        "text": "This is a test chunk for the cache manager demonstration.",
        "word_count": 10,
        "duration": 3.5
    }
    
    cache.register_chunk("test-episode", test_chunk)
    
    # Check if cached
    is_cached = cache.is_chunk_cached("test-episode", "abc123")
    print(f"Chunk cached: {is_cached}")
    
    # Get stats
    stats = cache.get_cache_stats("test-episode")
    print(f"Cache stats: {stats}")


if __name__ == "__main__":
    main()