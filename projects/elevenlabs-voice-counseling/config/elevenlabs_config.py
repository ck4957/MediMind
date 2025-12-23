"""
ElevenLabs Configuration Module
"""

import os
from dotenv import load_dotenv

load_dotenv()


class ElevenLabsConfig:
    """ElevenLabs API configuration"""
    
    # API credentials
    API_KEY = os.getenv('ELEVENLABS_API_KEY')
    API_BASE_URL = 'https://api.elevenlabs.io/v1'
    
    # Voice settings
    VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')  # Default: Rachel
    MODEL_ID = os.getenv('ELEVENLABS_MODEL', 'eleven_multilingual_v2')
    
    # Voice parameters
    VOICE_SETTINGS = {
        'stability': float(os.getenv('VOICE_STABILITY', '0.75')),
        'similarity_boost': float(os.getenv('VOICE_SIMILARITY', '0.80')),
        'style': float(os.getenv('VOICE_STYLE', '0.20')),
        'use_speaker_boost': os.getenv('VOICE_SPEAKER_BOOST', 'true').lower() == 'true',
    }
    
    # Audio settings
    OUTPUT_FORMAT = 'mp3_44100_128'
    SAMPLE_RATE = int(os.getenv('AUDIO_SAMPLE_RATE', '44100'))


class GCPConfig:
    """Google Cloud Platform configuration"""
    
    PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    REGION = os.getenv('GCP_REGION', 'us-central1')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    VERTEX_AI_ENDPOINT = os.getenv('VERTEX_AI_ENDPOINT')


class ConversationConfig:
    """Conversation management settings"""
    
    # Timeouts
    CONVERSATION_TIMEOUT = int(os.getenv('CONVERSATION_TIMEOUT', '300'))  # 5 minutes
    RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', '30'))  # 30 seconds
    
    # Limits
    MAX_TURNS = int(os.getenv('MAX_TURNS', '20'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # Voice activity detection
    VAD_AGGRESSIVENESS = int(os.getenv('VAD_AGGRESSIVENESS', '2'))  # 0-3
    SILENCE_THRESHOLD_MS = int(os.getenv('SILENCE_THRESHOLD_MS', '1000'))
    
    # Audio processing
    CHUNK_SIZE = int(os.getenv('AUDIO_CHUNK_SIZE', '1024'))
    AUDIO_FORMAT = 'int16'


# Available voices with descriptions
AVAILABLE_VOICES = {
    '21m00Tcm4TlvDq8ikWAM': {
        'name': 'Rachel',
        'gender': 'female',
        'description': 'Professional, empathetic, clear',
        'use_case': 'Medical counseling, general support'
    },
    'pNInz6obpgDQGcFmaJgB': {
        'name': 'Adam',
        'gender': 'male',
        'description': 'Professional, trustworthy, calm',
        'use_case': 'Medical counseling, information delivery'
    },
    'EXAVITQu4vr4xnSDxMaL': {
        'name': 'Bella',
        'gender': 'female',
        'description': 'Warm, supportive, friendly',
        'use_case': 'Patient support, reassurance'
    },
    'ErXwobaYiN019PkySvjV': {
        'name': 'Antoni',
        'gender': 'male',
        'description': 'Calm, clear, well-articulated',
        'use_case': 'Complex explanations, instructions'
    },
}


# Conversation states
CONVERSATION_STATES = [
    'GREETING',
    'INITIAL_ASSESSMENT',
    'RISK_FACTOR_COLLECTION',
    'SYMPTOM_EXPLORATION',
    'RISK_ASSESSMENT',
    'RESULTS_COMMUNICATION',
    'FOLLOW_UP',
    'CLOSING',
]


# Required information to collect
REQUIRED_INFORMATION = {
    'demographics': ['age', 'gender'],
    'risk_factors': [
        'family_history',
        'smoking_status',
        'alcohol_consumption',
        'occupation',
    ],
    'symptoms': [
        'has_symptoms',
        'symptom_details',
        'symptom_duration',
    ],
}
