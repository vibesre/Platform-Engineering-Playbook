#!/usr/bin/env python3
"""
Logging utilities for podcast generation.

Provides simple JSON lines logging to track:
- Generation sessions
- Per-chunk TTS calls
- Errors and retries
- Cost estimates
- Cache statistics

Log format: One JSON object per line (newline-delimited JSON)
Log file: podcast-generator/logs/generation.log
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Log file location
LOG_FILE = Path(__file__).parent.parent / "logs" / "generation.log"


def log_event(event_type: str, data: Dict[str, Any]):
    """
    Append event to log file in JSON lines format.

    Args:
        event_type: Type of event (generation_start, chunk_tts, etc.)
        data: Event-specific data to log
    """
    # Ensure logs directory exists
    LOG_FILE.parent.mkdir(exist_ok=True)

    # Build log entry with timestamp
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        **data
    }

    # Append to log file (one JSON object per line)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def log_generation_start(episode_id: str, script_path: str, force: bool):
    """Log the start of a generation session."""
    log_event("generation_start", {
        "episode_id": episode_id,
        "script_path": str(script_path),
        "force_regenerate": force
    })


def log_chunk_tts(
    chunk_id: int,
    speaker: str,
    status: str,
    character_count: Optional[int] = None,
    word_count: Optional[int] = None,
    voice: Optional[str] = None,
    duration_seconds: Optional[float] = None,
    generation_time_seconds: Optional[float] = None,
    estimated_cost_usd: Optional[float] = None,
    cached: bool = False,
    attempt: int = 1,
    error: Optional[str] = None
):
    """
    Log a TTS generation attempt for a chunk.

    Args:
        chunk_id: Chunk number (1-indexed)
        speaker: Speaker name
        status: "success", "failed", or "cached"
        character_count: Number of characters sent to TTS API
        word_count: Number of words in chunk
        voice: TTS voice name used
        duration_seconds: Audio duration produced
        generation_time_seconds: Time to generate
        estimated_cost_usd: Estimated cost for this chunk
        cached: Whether chunk was loaded from cache
        attempt: Retry attempt number (1 = first attempt)
        error: Error message if failed
    """
    data = {
        "chunk_id": chunk_id,
        "speaker": speaker,
        "status": status,
        "cached": cached,
        "attempt": attempt
    }

    # Add optional fields if provided
    if character_count is not None:
        data["character_count"] = character_count
    if word_count is not None:
        data["word_count"] = word_count
    if voice is not None:
        data["voice"] = voice
    if duration_seconds is not None:
        data["duration_seconds"] = round(duration_seconds, 2)
    if generation_time_seconds is not None:
        data["generation_time_seconds"] = round(generation_time_seconds, 2)
    if estimated_cost_usd is not None:
        data["estimated_cost_usd"] = round(estimated_cost_usd, 6)
    if error is not None:
        data["error"] = str(error)

    log_event("chunk_tts", data)


def log_generation_complete(
    episode_id: str,
    total_chunks: int,
    successful_chunks: int,
    failed_chunks: int,
    cached_chunks: int,
    total_characters: int,
    total_duration_seconds: float,
    estimated_total_cost_usd: float,
    generation_time_seconds: float,
    validation_passed: bool,
    output_file: Optional[str] = None
):
    """Log the completion of a generation session."""
    log_event("generation_complete", {
        "episode_id": episode_id,
        "total_chunks": total_chunks,
        "successful_chunks": successful_chunks,
        "failed_chunks": failed_chunks,
        "cached_chunks": cached_chunks,
        "total_characters": total_characters,
        "total_duration_seconds": round(total_duration_seconds, 2),
        "estimated_total_cost_usd": round(estimated_total_cost_usd, 6),
        "generation_time_seconds": round(generation_time_seconds, 2),
        "validation_passed": validation_passed,
        "output_file": str(output_file) if output_file else None
    })


def log_error(episode_id: str, error_type: str, error_message: str, context: Optional[Dict] = None):
    """Log an error that occurred during generation."""
    data = {
        "episode_id": episode_id,
        "error_type": error_type,
        "error_message": str(error_message)
    }

    if context:
        data["context"] = context

    log_event("error", data)


def log_warning(episode_id: str, warning_message: str, context: Optional[Dict] = None):
    """Log a warning during generation."""
    data = {
        "episode_id": episode_id,
        "warning_message": str(warning_message)
    }

    if context:
        data["context"] = context

    log_event("warning", data)


def get_recent_logs(n: int = 100) -> list:
    """
    Get the most recent N log entries.

    Args:
        n: Number of recent entries to retrieve

    Returns:
        List of log entry dicts (most recent last)
    """
    if not LOG_FILE.exists():
        return []

    entries = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # Skip malformed lines

    return entries[-n:] if len(entries) > n else entries


def get_session_logs(episode_id: str) -> list:
    """
    Get all log entries for a specific episode generation session.

    Args:
        episode_id: Episode identifier

    Returns:
        List of log entry dicts for this episode
    """
    if not LOG_FILE.exists():
        return []

    entries = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("episode_id") == episode_id:
                    entries.append(entry)
            except json.JSONDecodeError:
                continue

    return entries


if __name__ == "__main__":
    # Test the logging system
    print("Testing logging system...")

    # Test generation start
    log_generation_start("test-episode", "/path/to/script.txt", force=True)

    # Test successful chunk
    log_chunk_tts(
        chunk_id=1,
        speaker="jordan",
        status="success",
        character_count=312,
        word_count=56,
        voice="en-US-Chirp3-HD-Kore",
        duration_seconds=22.4,
        generation_time_seconds=3.2,
        estimated_cost_usd=0.00468,
        cached=False
    )

    # Test failed chunk (first attempt)
    log_chunk_tts(
        chunk_id=2,
        speaker="alex",
        status="failed",
        attempt=1,
        error="Connection timeout"
    )

    # Test retry success
    log_chunk_tts(
        chunk_id=2,
        speaker="alex",
        status="success",
        character_count=280,
        word_count=45,
        voice="en-US-Chirp3-HD-Algieba",
        duration_seconds=18.0,
        generation_time_seconds=2.8,
        estimated_cost_usd=0.00420,
        cached=False,
        attempt=2
    )

    # Test generation complete
    log_generation_complete(
        episode_id="test-episode",
        total_chunks=108,
        successful_chunks=108,
        failed_chunks=0,
        cached_chunks=0,
        total_characters=23456,
        total_duration_seconds=1378.1,
        estimated_total_cost_usd=0.35184,
        generation_time_seconds=345.6,
        validation_passed=True,
        output_file="/path/to/output.mp3"
    )

    print(f"\n✓ Test logs written to: {LOG_FILE}")
    print(f"\nRecent logs:")
    for entry in get_recent_logs(5):
        print(f"  {entry['timestamp']} - {entry['event']}: {entry.get('episode_id', 'N/A')}")
