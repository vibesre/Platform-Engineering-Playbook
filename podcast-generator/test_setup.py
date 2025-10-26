#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify podcast generator setup.
"""

import os
import sys
import subprocess
from pathlib import Path

# Try to load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed yet


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Python 3.8+ recommended")
        return False
    return True


def check_dependencies():
    """Check Python dependencies."""
    print("\nChecking Python dependencies...")
    try:
        import yaml
        print("✓ PyYAML installed")
    except ImportError:
        print("✗ PyYAML not installed")
        return False
    
    try:
        import google.generativeai
        print("✓ google-generativeai installed")
    except ImportError:
        print("✗ google-generativeai not installed")
        return False
    
    try:
        import pydub
        print("✓ pydub installed")
    except ImportError:
        print("✗ pydub not installed")
        return False
    
    return True


def check_ffmpeg():
    """Check ffmpeg installation."""
    print("\nChecking ffmpeg...")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        version_line = result.stdout.split('\n')[0]
        print(f"✓ {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg not installed")
        print("  Install with: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)")
        return False


def check_api_key():
    """Check Google AI API key."""
    print("\nChecking API key...")
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if api_key:
        print(f"✓ GOOGLE_AI_API_KEY set ({len(api_key)} characters)")
        return True
    else:
        print("✗ GOOGLE_AI_API_KEY not set")
        print("  Options:")
        print("  1. Create .env file with: GOOGLE_AI_API_KEY=your-key-here")
        print("  2. Set environment: export GOOGLE_AI_API_KEY='your-key-here'")
        return False


def check_directory_structure():
    """Check directory structure."""
    print("\nChecking directory structure...")
    required_dirs = [
        Path("scripts"),
        Path("cache"),
        Path("cache/chunks"),
        Path("output")
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✓ {dir_path}/ exists")
        else:
            print(f"✗ {dir_path}/ missing")
            all_exist = False
    
    return all_exist


def check_scripts():
    """Check required scripts."""
    print("\nChecking scripts...")
    scripts = [
        "generate_podcast.py",
        "chunker.py",
        "cache_manager.py",
        "tts_generator.py",
        "audio_stitcher.py"
    ]
    
    all_exist = True
    for script in scripts:
        script_path = Path("scripts") / script
        if script_path.exists():
            print(f"✓ {script}")
        else:
            print(f"✗ {script} missing")
            all_exist = False
    
    return all_exist


def test_chunker():
    """Test the chunker module."""
    print("\nTesting chunker...")
    try:
        sys.path.append(str(Path(__file__).parent / "scripts"))
        from chunker import PodcastChunker
        
        chunker = PodcastChunker()
        test_text = "Speaker 1: Hello world. This is a test."
        chunks = chunker.chunk_script(test_text)
        
        if chunks:
            print(f"✓ Chunker works ({len(chunks)} chunks created)")
            return True
        else:
            print("✗ Chunker failed to create chunks")
            return False
    except Exception as e:
        print(f"✗ Chunker error: {e}")
        return False


def main():
    """Run all checks."""
    print("🎙️  Podcast Generator Setup Test\n")
    
    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("ffmpeg", check_ffmpeg),
        ("API key", check_api_key),
        ("Directory structure", check_directory_structure),
        ("Scripts", check_scripts),
        ("Chunker", test_chunker)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {name} check failed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\nYou're ready to generate podcasts!")
        print("Try: python scripts/generate_podcast.py sample-episode.md")
    else:
        print(f"⚠️  Some checks failed ({passed}/{total})")
        print("\nPlease fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()