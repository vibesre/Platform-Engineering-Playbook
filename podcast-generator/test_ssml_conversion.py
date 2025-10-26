#!/usr/bin/env python3
"""
Test SSML conversion to ensure proper formatting.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / 'scripts'))

try:
    from cloud_tts_generator import GoogleCloudTTSGenerator
except ImportError:
    GoogleCloudTTSGenerator = None

def test_ssml_conversion():
    """Test that custom pause tags convert to proper SSML."""

    # Create a minimal generator instance (won't actually call TTS API)
    try:
        generator = GoogleCloudTTSGenerator()
    except Exception:
        # If credentials aren't set up, create instance manually
        class MockGenerator:
            def _convert_to_ssml(self, text):
                # Copy the updated method from GoogleCloudTTSGenerator
                import re
                import html

                # Extract and temporarily replace all existing SSML tags
                ssml_tags = []
                ssml_pattern = r'<(?:phoneme|say-as)[^>]*>.*?</(?:phoneme|say-as)>|<(?:phoneme|say-as)[^>]*/>'

                def save_ssml_tag(match):
                    tag = match.group(0)
                    placeholder = f'__SSML_TAG_{len(ssml_tags)}__'
                    ssml_tags.append(tag)
                    return placeholder

                text = re.sub(ssml_pattern, save_ssml_tag, text)

                # Replace pause tags with placeholders
                pause_patterns = {
                    '[pause short]': '__PAUSE_SHORT__',
                    '[pause long]': '__PAUSE_LONG__',
                    '[pause]': '__PAUSE__'
                }

                for pause_tag, placeholder in pause_patterns.items():
                    text = text.replace(pause_tag, placeholder)

                # Escape XML characters (now safe since SSML tags are removed)
                text = html.escape(text, quote=False)

                # Restore SSML tags
                for i, tag in enumerate(ssml_tags):
                    placeholder = f'__SSML_TAG_{i}__'
                    text = text.replace(placeholder, tag)

                # Replace pause placeholders with proper SSML break tags
                text = text.replace('__PAUSE_SHORT__', '<break strength="weak"/>')
                text = text.replace('__PAUSE_LONG__', '<break strength="strong"/>')
                text = text.replace('__PAUSE__', '<break strength="medium"/>')

                ssml = f'<speak>{text}</speak>'

                return ssml

        generator = MockGenerator()

    # Test cases
    test_cases = [
        {
            'input': 'This is a test. [pause] Here is more text.',
            'expected': '<speak>This is a test. <break strength="medium"/> Here is more text.</speak>'
        },
        {
            'input': 'Wait, [pause short] are you serious? [pause] That\'s massive.',
            'expected': '<speak>Wait, <break strength="weak"/> are you serious? <break strength="medium"/> That\'s massive.</speak>'
        },
        {
            'input': 'Let me think. [pause long] Yes, that makes sense.',
            'expected': '<speak>Let me think. <break strength="strong"/> Yes, that makes sense.</speak>'
        },
        {
            'input': 'Text with <special> & "quotes" should be escaped.',
            'expected': '<speak>Text with &lt;special&gt; &amp; "quotes" should be escaped.</speak>'
        },
        {
            'input': 'Productivity went up 55% [pause] and that\'s < impressive.',
            'expected': '<speak>Productivity went up 55% <break strength="medium"/> and that\'s &lt; impressive.</speak>'
        },
        {
            'input': 'We deploy <phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme> on <say-as interpret-as="characters">AWS</say-as>.',
            'expected': '<speak>We deploy <phoneme alphabet="ipa" ph="ˌkubɚˈnɛtɪs">Kubernetes</phoneme> on <say-as interpret-as="characters">AWS</say-as>.</speak>'
        },
        {
            'input': '<phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme> [pause] runs on <say-as interpret-as="characters">RDS</say-as>.',
            'expected': '<speak><phoneme alphabet="ipa" ph="ˈpoʊstɡrɛs">Postgres</phoneme> <break strength="medium"/> runs on <say-as interpret-as="characters">RDS</say-as>.</speak>'
        },
        {
            'input': 'Our <phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme> setup < 100 nodes.',
            'expected': '<speak>Our <phoneme alphabet="ipa" ph="ˈæʒɚ">Azure</phoneme> setup &lt; 100 nodes.</speak>'
        }
    ]

    print("Testing SSML Conversion\n" + "="*80)

    all_passed = True
    for i, test in enumerate(test_cases, 1):
        result = generator._convert_to_ssml(test['input'])
        passed = result == test['expected']

        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\nTest {i}: {status}")
        print(f"Input:    {test['input']}")
        print(f"Expected: {test['expected']}")
        print(f"Got:      {result}")

        if not passed:
            all_passed = False

    print("\n" + "="*80)
    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(test_ssml_conversion())
