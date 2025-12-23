"""
Speech synthesis using ElevenLabs Text-to-Speech
"""

import requests
import sys
import os
from typing import Optional
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.elevenlabs_config import ElevenLabsConfig

try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: sounddevice/soundfile not installed. Audio playback disabled.")


class SpeechSynthesizer:
    """Text-to-speech using ElevenLabs"""
    
    def __init__(self):
        self.api_key = ElevenLabsConfig.API_KEY
        self.voice_id = ElevenLabsConfig.VOICE_ID
        self.model_id = ElevenLabsConfig.MODEL_ID
        self.voice_settings = ElevenLabsConfig.VOICE_SETTINGS
        self.base_url = ElevenLabsConfig.API_BASE_URL
        
        if not self.api_key:
            print("Warning: ELEVENLABS_API_KEY not set. Using mock TTS.")
            self.mock_mode = True
        else:
            self.mock_mode = False
    
    def synthesize_speech(self, text: str, play_audio: bool = True) -> Optional[bytes]:
        """
        Convert text to speech and optionally play it
        
        Args:
            text: Text to convert to speech
            play_audio: Whether to play the audio immediately
            
        Returns:
            Audio data in bytes (MP3 format)
        """
        if self.mock_mode:
            print(f"\n[COUNSELOR SPEAKS]: {text}\n")
            return None
        
        try:
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": self.model_id,
                "voice_settings": self.voice_settings
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                audio_data = response.content
                
                if play_audio and AUDIO_AVAILABLE:
                    self._play_audio(audio_data)
                
                return audio_data
            else:
                print(f"Error from ElevenLabs: {response.status_code}")
                print(f"Response: {response.text}")
                # Fallback to mock
                print(f"\n[COUNSELOR SPEAKS]: {text}\n")
                return None
                
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
            # Fallback to text display
            print(f"\n[COUNSELOR SPEAKS]: {text}\n")
            return None
    
    def _play_audio(self, audio_data: bytes):
        """Play audio data through speakers"""
        try:
            # Convert MP3 bytes to audio
            audio_buffer = io.BytesIO(audio_data)
            data, samplerate = sf.read(audio_buffer)
            
            # Play audio
            sd.play(data, samplerate)
            sd.wait()  # Wait until playback is finished
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def save_audio(self, audio_data: bytes, filename: str):
        """Save audio data to file"""
        try:
            with open(filename, 'wb') as f:
                f.write(audio_data)
            print(f"Audio saved to {filename}")
        except Exception as e:
            print(f"Error saving audio: {e}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if self.mock_mode:
            return []
        
        try:
            url = f"{self.base_url}/voices"
            headers = {"xi-api-key": self.api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('voices', [])
            else:
                return []
                
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """Change the voice being used"""
        self.voice_id = voice_id
    
    def adjust_voice_settings(
        self,
        stability: Optional[float] = None,
        similarity_boost: Optional[float] = None,
        style: Optional[float] = None,
    ):
        """Adjust voice parameters"""
        if stability is not None:
            self.voice_settings['stability'] = stability
        if similarity_boost is not None:
            self.voice_settings['similarity_boost'] = similarity_boost
        if style is not None:
            self.voice_settings['style'] = style


if __name__ == '__main__':
    # Test speech synthesis
    synthesizer = SpeechSynthesizer()
    
    test_text = "Hello, I'm your AI health counselor. I'm here to help assess your cancer risk and answer any questions you might have."
    
    print("Testing speech synthesis...")
    audio = synthesizer.synthesize_speech(test_text, play_audio=True)
    
    if audio:
        print(f"Generated {len(audio)} bytes of audio")
