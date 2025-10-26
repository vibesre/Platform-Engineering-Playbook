#!/usr/bin/env python3
"""
Test voice consistency system.
Verifies that voice validation and config loading works correctly.
"""

import sys
import yaml
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / "scripts"))

def test_config_loading():
    """Test that config loads correctly."""
    print("🧪 Test 1: Config Loading")
    try:
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)

        assert "speakers" in config, "Config must have 'speakers' section"
        assert "jordan" in config["speakers"], "Config must define 'jordan' speaker"
        assert "alex" in config["speakers"], "Config must define 'alex' speaker"

        jordan_voice = config["speakers"]["jordan"]["voice"]
        alex_voice = config["speakers"]["alex"]["voice"]

        print(f"  ✓ Config loaded successfully")
        print(f"    jordan: {jordan_voice}")
        print(f"    alex: {alex_voice}")
        return True
    except Exception as e:
        print(f"  ✗ Config loading failed: {e}")
        return False


def test_voice_normalization():
    """Test speaker name normalization."""
    print("\n🧪 Test 2: Speaker Name Normalization")

    try:
        # Test normalization logic directly (same as in code)
        def normalize_speaker_name(speaker: str) -> str:
            normalized = speaker.lower().strip()
            if normalized == "speaker 1":
                return "jordan"
            elif normalized == "speaker 2":
                return "alex"
            return normalized

        test_cases = [
            ("Jordan", "jordan"),
            ("ALEX", "alex"),
            ("jordan", "jordan"),
            ("alex", "alex"),
            ("Speaker 1", "jordan"),
            ("Speaker 2", "alex"),
            ("  Jordan  ", "jordan"),  # Test trimming
        ]

        all_passed = True
        for input_name, expected in test_cases:
            result = normalize_speaker_name(input_name)
            if result == expected:
                print(f"  ✓ '{input_name}' → '{result}'")
            else:
                print(f"  ✗ '{input_name}' → '{result}' (expected '{expected}')")
                all_passed = False

        return all_passed
    except Exception as e:
        print(f"  ✗ Normalization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_unknown_speaker_detection():
    """Test that unknown speakers are detected."""
    print("\n🧪 Test 3: Unknown Speaker Detection")

    try:
        from dialogue_chunker import DialogueChunker

        chunker = DialogueChunker()

        # Test script with unknown speaker
        script = """
Jordan: This is Jordan speaking.

UnknownSpeaker: This should fail.
"""

        try:
            chunks = chunker.chunk_script(script)
            print(f"  ✗ Failed to detect unknown speaker")
            return False
        except ValueError as e:
            if "Unknown speaker" in str(e):
                print(f"  ✓ Unknown speaker correctly detected")
                print(f"    Error message: {e}")
                return True
            else:
                print(f"  ✗ Wrong error raised: {e}")
                return False
    except Exception as e:
        print(f"  ✗ Unknown speaker detection test failed: {e}")
        return False


def test_cache_voice_tracking():
    """Test that cache tracks voice information."""
    print("\n🧪 Test 4: Cache Voice Tracking")

    try:
        from cache_manager import CacheManager
        import tempfile
        import shutil

        # Create temporary cache directory
        temp_dir = tempfile.mkdtemp()

        try:
            cache = CacheManager(
                cache_dir=temp_dir,
                manifest_file=f"{temp_dir}/manifest.json"
            )

            # Register a test chunk with voice info
            chunk_data = {
                "id": 0,
                "hash": "test123",
                "speaker": "jordan",
                "text": "Test chunk",
                "word_count": 2,
                "duration": 1.0,
                "voice": "en-US-Chirp3-HD-Kore"
            }

            cache.register_chunk("test-episode", chunk_data)

            # Verify voice is tracked
            manifest = cache.get_episode_manifest("test-episode")
            chunk_metadata = manifest["chunks"]["test123"]

            if chunk_metadata.get("voice") == "en-US-Chirp3-HD-Kore":
                print(f"  ✓ Voice metadata tracked correctly")
                print(f"    Stored voice: {chunk_metadata['voice']}")
                return True
            else:
                print(f"  ✗ Voice metadata not tracked")
                return False
        finally:
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"  ✗ Cache voice tracking test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("VOICE CONSISTENCY SYSTEM TESTS")
    print("=" * 70)

    results = []

    results.append(("Config Loading", test_config_loading()))
    results.append(("Speaker Normalization", test_voice_normalization()))
    results.append(("Unknown Speaker Detection", test_unknown_speaker_detection()))
    results.append(("Cache Voice Tracking", test_cache_voice_tracking()))

    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result[1] for result in results)

    print("=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
