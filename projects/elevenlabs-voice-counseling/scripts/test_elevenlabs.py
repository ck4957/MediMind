"""
Test ElevenLabs API connectivity
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice.speech_synthesis import SpeechSynthesizer


def test_elevenlabs_connection():
    """Test connection to ElevenLabs API"""
    print("Testing ElevenLabs API Connection")
    print("=" * 60)
    
    synthesizer = SpeechSynthesizer()
    
    if synthesizer.mock_mode:
        print("⚠ Running in mock mode (API key not configured)")
        print("\nTo use real ElevenLabs:")
        print("1. Sign up at https://elevenlabs.io")
        print("2. Get your API key")
        print("3. Set ELEVENLABS_API_KEY in .env file")
        return False
    
    print("✓ API key configured")
    print("\nFetching available voices...")
    
    voices = synthesizer.get_available_voices()
    
    if voices:
        print(f"✓ Found {len(voices)} voices")
        print("\nSample voices:")
        for voice in voices[:5]:
            print(f"  - {voice.get('name', 'Unknown')}: {voice.get('voice_id', 'N/A')}")
    else:
        print("✗ Could not fetch voices")
        return False
    
    print("\nTesting speech synthesis...")
    test_text = "Hello, this is a test of the ElevenLabs text to speech system."
    
    audio = synthesizer.synthesize_speech(test_text, play_audio=True)
    
    if audio:
        print(f"✓ Generated {len(audio)} bytes of audio")
        print("✓ Audio should be playing now")
        return True
    else:
        print("✗ Failed to generate audio")
        return False


if __name__ == '__main__':
    success = test_elevenlabs_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ ElevenLabs test completed successfully!")
    else:
        print("⚠ ElevenLabs test completed with warnings")
    print("=" * 60)
