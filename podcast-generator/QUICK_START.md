# Quick Start - API Key Setup

The easiest way to get real text-to-speech working!

## Step 1: Enable Text-to-Speech API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (or create a new one)
3. Go to "APIs & Services" → "Enable APIs and Services"
4. Search for "Cloud Text-to-Speech API"
5. Click "Enable"

## Step 2: Use Your Existing API Key

If your Google AI API key already has access:
- Your `.env` file is already set up!
- The system will automatically try to use it

If not, create a new API key:
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the key
4. (Optional) Click "Restrict Key" and limit to Text-to-Speech API

## Step 3: Install Dependencies

```bash
pip install google-cloud-texttospeech
```

## Step 4: Test It!

```bash
python3 scripts/generate_podcast.py test-episode.md
```

You should see:
```
✓ Generated with Google Cloud TTS
```

## Troubleshooting

### "API not enabled" error
The Text-to-Speech API needs to be enabled in your Google Cloud project.

### "Permission denied" error  
Your API key might need Text-to-Speech permissions. Create a new key specifically for this API.

### Still using placeholder audio?
Check that `google-cloud-texttospeech` is installed:
```bash
pip list | grep google-cloud-texttospeech
```

## That's It!

You now have real text-to-speech generation! The system will:
- Use Google Cloud TTS for high-quality voices
- Cache generated audio to save API calls
- Fall back to placeholder audio if there's an issue