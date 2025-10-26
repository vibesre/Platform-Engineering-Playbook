#!/bin/bash
# Podcast Generator Setup Script

echo "🎙️  Podcast Generator Setup"
echo "=========================="
echo ""

# Check OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    INSTALL_CMD="brew install"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    INSTALL_CMD="sudo apt-get install -y"
else
    OS="Unknown"
fi

echo "Detected OS: $OS"
echo ""

# Create directories
echo "Creating directory structure..."
mkdir -p cache/chunks output
echo "✓ Directories created"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
    echo "✓ Python dependencies installed"
else
    echo "✗ pip3 not found. Please install Python 3 first."
    exit 1
fi
echo ""

# Check/Install ffmpeg
echo "Checking ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found."
    if [[ "$OS" == "macOS" ]] || [[ "$OS" == "Linux" ]]; then
        read -p "Would you like to install ffmpeg? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            $INSTALL_CMD ffmpeg
        else
            echo "⚠️  Please install ffmpeg manually"
        fi
    else
        echo "⚠️  Please install ffmpeg manually from https://ffmpeg.org"
    fi
else
    echo "✓ ffmpeg is already installed"
fi
echo ""

# API Key setup
echo "Google AI Studio API Key Setup"
echo "------------------------------"
if [ -z "$GOOGLE_AI_API_KEY" ]; then
    echo "GOOGLE_AI_API_KEY is not set."
    echo ""
    echo "To get an API key:"
    echo "1. Visit https://makersuite.google.com/app/apikey"
    echo "2. Click 'Create API Key'"
    echo "3. Copy the key"
    echo ""
    read -p "Enter your Google AI API key (or press Enter to skip): " api_key
    if [ -n "$api_key" ]; then
        echo ""
        echo "Add this to your shell profile (.bashrc, .zshrc, etc.):"
        echo "export GOOGLE_AI_API_KEY='$api_key'"
        echo ""
        echo "Or set it temporarily for this session:"
        echo "export GOOGLE_AI_API_KEY='$api_key'"
    fi
else
    echo "✓ GOOGLE_AI_API_KEY is already set"
fi
echo ""

# Run test
echo "Running setup test..."
echo ""
python3 test_setup.py

echo ""
echo "Setup complete! Next steps:"
echo "1. Set your GOOGLE_AI_API_KEY environment variable"
echo "2. Install ffmpeg if not already installed"
echo "3. Run: python3 scripts/generate_podcast.py sample-episode.md"