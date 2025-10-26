# Text-to-Speech Setup Guide

This guide explains how to set up real text-to-speech generation for the podcast generator.

## Current Status

The podcast generator is fully functional with:
- ✅ Smart chunking and caching
- ✅ Multi-speaker support
- ✅ Audio processing pipeline
- ⚠️ Placeholder audio (real TTS requires setup)

## Option 1: Google Cloud Text-to-Speech (Recommended)

Google Cloud TTS offers high-quality voices including Journey, Studio, and WaveNet models.

### Setup Steps

1. **Install the Google Cloud TTS library**:
   ```bash
   pip install google-cloud-texttospeech
   ```

2. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing
   - Enable the Text-to-Speech API

3. **Set up Authentication** (Choose one):

   **Option A: API Key (Simplest)**
   - Go to APIs & Services → Credentials
   - Create Credentials → API Key
   - Restrict the key to Text-to-Speech API
   - Set in your `.env` file:
     ```bash
     GOOGLE_CLOUD_API_KEY=your-api-key-here
     # Can also use the same key as GOOGLE_AI_API_KEY if it has access
     ```

   **Option B: Service Account (More secure)**
   - Go to IAM & Admin → Service Accounts
   - Create a new service account
   - Download the JSON key file
   - Set environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
     ```

   **Option C: Application Default Credentials (For development)**
   ```bash
   gcloud auth application-default login
   ```

4. **Test the setup**:
   ```bash
   cd podcast-generator
   python3 scripts/cloud_tts_generator.py
   ```

### Available Voices

High-quality voices for podcasts:
- **Male voices**: en-US-Journey-D, en-US-Studio-M, en-US-Neural2-D
- **Female voices**: en-US-Journey-F, en-US-Studio-O, en-US-Neural2-F

### Costs

- Journey voices: $160 per 1 million characters
- Studio voices: $160 per 1 million characters  
- Neural2 voices: $16 per 1 million characters
- WaveNet voices: $16 per 1 million characters

Example: A 15-minute podcast (~2,250 words, ~11,250 characters) costs:
- Journey/Studio: ~$1.80
- Neural2/WaveNet: ~$0.18

## Option 2: Google AI Studio (Future)

Gemini models will include native TTS capabilities:
- Model: gemini-2.0-flash-exp (with TTS support)
- Voices: Puck, Charon, Kore, Fenrir, Aoede

**Status**: Not yet available in public SDK. Check for updates.

## Option 3: Alternative TTS Services

### Amazon Polly
```python
# Install: pip install boto3
import boto3

polly_client = boto3.Session(region_name='us-west-2').client('polly')
response = polly_client.synthesize_speech(
    VoiceId='Joanna',
    OutputFormat='mp3',
    Text=text
)
```

### OpenAI TTS
```python
# Install: pip install openai
from openai import OpenAI

client = OpenAI()
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="alloy",
    input=text
)
```

### ElevenLabs
```python
# Install: pip install elevenlabs
from elevenlabs import generate, save

audio = generate(
    text=text,
    voice="Rachel",
    model="eleven_monolingual_v1"
)
save(audio, output_path)
```

## Configuration

Update `config.yaml` to specify voice preferences:

```yaml
speakers:
  jordan:
    voice: "en-US-Journey-D"    # Primary voice
    alternatives:                # Fallback voices
      - "en-US-Studio-M"
      - "en-US-Neural2-D"
  alex:
    voice: "en-US-Journey-F"
    alternatives:
      - "en-US-Studio-O"
      - "en-US-Neural2-F"
```

## Troubleshooting

### "Credentials not configured" error
- Ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly
- Verify the service account has Text-to-Speech API permissions
- Check if the API is enabled in your project

### "API not enabled" error
```bash
gcloud services enable texttospeech.googleapis.com
```

### Rate limiting
The system includes automatic rate limiting. Adjust in `config.yaml`:
```yaml
processing:
  rate_limit_delay: 0.5  # Seconds between API calls
```

### Voice not available
The system automatically falls back to alternative voices if the primary isn't available.

## Testing Real TTS

1. **Quick test**:
   ```bash
   python3 scripts/cloud_tts_generator.py
   ```

2. **Generate a podcast**:
   ```bash
   python3 scripts/generate_podcast.py test-episode.md
   ```

3. **Check the output**:
   - Look for "✓ Generated with Google Cloud TTS" in logs
   - Audio files will be real speech, not placeholders

## Best Practices

1. **Voice Consistency**: Use the same voice model series (e.g., all Journey or all Studio)
2. **Chunk Size**: Keep chunks under 5000 characters for API limits
3. **Error Handling**: The system falls back gracefully to placeholder audio
4. **Cost Management**: Use Neural2 voices for drafts, Journey for final production

## Next Steps

After setting up TTS:
1. Generate your first real podcast
2. Experiment with different voices
3. Fine-tune speech parameters (speed, pitch)
4. Set up GitHub Actions with credentials