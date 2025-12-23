"""
Speech recognition using local audio input
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.elevenlabs_config import ConversationConfig

try:
    import sounddevice as sd
    import numpy as np
    import webrtcvad
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: Audio libraries not installed. Using text input.")


class SpeechRecognizer:
    """Speech recognition with voice activity detection"""
    
    def __init__(self):
        self.sample_rate = ConversationConfig.AUDIO_FORMAT
        self.chunk_size = ConversationConfig.CHUNK_SIZE
        self.vad_aggressiveness = ConversationConfig.VAD_AGGRESSIVENESS
        
        if AUDIO_AVAILABLE:
            try:
                self.vad = webrtcvad.Vad(self.vad_aggressiveness)
                self.audio_enabled = True
            except:
                self.audio_enabled = False
                print("Voice activity detection not available")
        else:
            self.audio_enabled = False
    
    def listen(self, timeout: int = 30) -> str:
        """
        Listen for speech input
        
        Args:
            timeout: Maximum time to wait for input (seconds)
            
        Returns:
            Transcribed text from speech
        """
        if not self.audio_enabled:
            # Fallback to text input
            return self._text_input(timeout)
        
        try:
            print("\n🎤 Listening... (speak now)")
            
            # Record audio with voice activity detection
            audio_frames = self._record_with_vad(timeout)
            
            if not audio_frames:
                print("No speech detected. Please try again.")
                return ""
            
            # In a real implementation, send audio to speech-to-text service
            # For demo, fallback to text input
            print("Audio captured. Converting to text...")
            return self._text_input(5)
            
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return self._text_input(timeout)
    
    def _record_with_vad(self, max_duration: int = 30) -> list:
        """
        Record audio with voice activity detection
        
        Args:
            max_duration: Maximum recording duration in seconds
            
        Returns:
            List of audio frames containing speech
        """
        if not AUDIO_AVAILABLE:
            return []
        
        frames = []
        silence_frames = 0
        max_silence_frames = int(ConversationConfig.SILENCE_THRESHOLD_MS / 30)  # 30ms frames
        
        def audio_callback(indata, frame_count, time_info, status):
            if status:
                print(status)
            
            # Convert to bytes for VAD
            audio_bytes = (indata * 32767).astype(np.int16).tobytes()
            
            # Check if speech is present
            is_speech = False
            try:
                is_speech = self.vad.is_speech(audio_bytes, self.sample_rate)
            except:
                pass
            
            if is_speech:
                frames.append(indata.copy())
                nonlocal silence_frames
                silence_frames = 0
            else:
                silence_frames += 1
        
        try:
            with sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
            ):
                # Record until silence or max duration
                import time
                start_time = time.time()
                while time.time() - start_time < max_duration:
                    if silence_frames > max_silence_frames and len(frames) > 0:
                        break
                    time.sleep(0.1)
            
            return frames
            
        except Exception as e:
            print(f"Error recording audio: {e}")
            return []
    
    def _text_input(self, timeout: int) -> str:
        """Fallback to text input"""
        try:
            print("\n[Type your response]: ", end='', flush=True)
            response = input()
            return response.strip()
        except:
            return ""
    
    def test_microphone(self):
        """Test microphone functionality"""
        if not AUDIO_AVAILABLE:
            print("Audio libraries not available")
            return False
        
        try:
            print("Testing microphone...")
            print("Speak for 3 seconds...")
            
            duration = 3  # seconds
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            
            # Check if audio was captured
            if np.abs(recording).max() > 0.01:
                print("✓ Microphone is working")
                return True
            else:
                print("✗ No audio detected. Check microphone connection.")
                return False
                
        except Exception as e:
            print(f"✗ Microphone test failed: {e}")
            return False


if __name__ == '__main__':
    # Test speech recognition
    recognizer = SpeechRecognizer()
    
    print("Testing speech recognition...")
    recognizer.test_microphone()
    
    print("\nTrying to capture speech...")
    text = recognizer.listen(timeout=10)
    print(f"Captured: {text}")
