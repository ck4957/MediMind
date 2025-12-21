# ElevenLabs Challenge: Voice-Interactive Cancer Risk Counseling Assistant

## Overview

This project demonstrates a voice-interactive AI counselor that provides cancer risk assessment through natural conversation. The system uses ElevenLabs for speech-to-text and text-to-speech, Gemini for conversational analysis, and Vertex AI for risk assessment calculations.

## Architecture

```
Voice Input → ElevenLabs Speech-to-Text → 
Gemini (Clinical Analysis) → Vertex AI (Risk Assessment) → 
ElevenLabs Text-to-Speech → Voice Output
```

## Key Features

### 1. Natural Voice Interaction
- Real-time speech recognition
- Natural language understanding
- Empathetic voice responses
- Multi-turn conversation support

### 2. Intelligent Conversation Flow
- Context-aware dialogue management
- Adaptive questioning based on responses
- Clarification requests when needed
- Smooth topic transitions

### 3. Clinical Data Collection
- Voice-driven symptom reporting
- Family history gathering
- Lifestyle factor assessment
- Medical history review

### 4. AI-Powered Risk Assessment
- Real-time risk calculation
- Confidence scoring
- Personalized recommendations
- Clear explanation of findings

### 5. Empathetic Communication
- Supportive tone and pacing
- Appropriate emotional responses
- Clear health communication
- Patient-centered language

## Use Case

"A patient speaks with an AI counselor about their cancer risk concerns. The system asks relevant questions, analyzes responses, calculates risk using ML models, and provides personalized guidance in a natural, empathetic voice."

## Prerequisites

- ElevenLabs API account (free tier available)
- Google Cloud Platform project
- Python 3.9+
- Microphone for voice input
- Speakers/headphones for voice output

## Setup Instructions

### 1. ElevenLabs Setup

```bash
# Sign up for ElevenLabs
# Go to https://elevenlabs.io/

# Get your API key from:
# https://elevenlabs.io/app/settings/api-keys

# Choose a voice ID from:
# https://elevenlabs.io/app/voice-library
```

### 2. Environment Configuration

Create `.env` file:

```env
# ElevenLabs Configuration
ELEVENLABS_API_KEY=your-elevenlabs-api-key
ELEVENLABS_VOICE_ID=your-chosen-voice-id
ELEVENLABS_MODEL=eleven_multilingual_v2

# Google Cloud Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
GEMINI_API_KEY=your-gemini-api-key
VERTEX_AI_ENDPOINT=your-vertex-ai-endpoint

# Application Configuration
CONVERSATION_TIMEOUT=300
MAX_TURNS=20
AUDIO_SAMPLE_RATE=44100
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test Voice Setup

```bash
# Test microphone
python scripts/test_microphone.py

# Test speaker output
python scripts/test_speaker.py

# Test ElevenLabs connection
python scripts/test_elevenlabs.py
```

### 5. Run the Voice Counselor

```bash
# Interactive mode
python conversation_engine/voice_counselor.py

# Demo mode with predefined responses
python scripts/demo_conversation.py
```

## Project Structure

```
elevenlabs-voice-counseling/
├── README.md
├── requirements.txt
├── config/
│   ├── elevenlabs_config.py
│   ├── conversation_config.py
│   └── prompts.py
├── voice/
│   ├── speech_recognition.py
│   ├── speech_synthesis.py
│   └── audio_processing.py
├── conversation_engine/
│   ├── voice_counselor.py
│   ├── dialogue_manager.py
│   └── risk_assessor.py
├── dialogues/
│   ├── sample_conversation_1.txt
│   ├── sample_conversation_2.txt
│   └── sample_conversation_3.txt
└── scripts/
    ├── test_microphone.py
    ├── test_speaker.py
    ├── test_elevenlabs.py
    └── demo_conversation.py
```

## Conversation Flow

### 1. Greeting & Introduction

**Counselor:** "Hello, I'm your AI health counselor. I'm here to help assess your cancer risk and answer any questions you might have. This conversation is confidential, and we'll take as much time as you need. How are you feeling today?"

### 2. Initial Assessment

**Topics covered:**
- Current health concerns
- Reason for assessment
- General health status
- Immediate symptoms

### 3. Risk Factor Collection

**Systematic questions about:**
- Age and gender
- Family history of cancer
- Smoking history
- Alcohol consumption
- Diet and exercise
- Occupational exposures
- Previous medical conditions

### 4. Symptom Exploration

**If symptoms mentioned:**
- Duration and severity
- Changes over time
- Associated symptoms
- Impact on daily life

### 5. Risk Assessment

**AI Processing:**
- Analyze collected information with Gemini
- Calculate risk score with Vertex AI
- Generate personalized recommendations
- Prepare empathetic explanation

### 6. Results Communication

**Counselor delivers:**
- Clear risk level explanation
- Key contributing factors
- Recommended next steps
- Reassurance and support

### 7. Follow-up & Resources

**Provide:**
- Screening recommendations
- Lifestyle modifications
- When to seek medical attention
- Support resources

## Sample Dialogues

### Low Risk Scenario

```
Counselor: "Hello, I'm here to help assess your cancer risk. How can I help you today?"

Patient: "I'm 35 and just want to know if I should be worried about cancer."

Counselor: "That's a very responsible question. Can you tell me about your family history? Has anyone in your immediate family had cancer?"

Patient: "No, not that I know of."

Counselor: "That's good to hear. Do you smoke or have you smoked in the past?"

Patient: "Never smoked."

[Assessment continues...]

Counselor: "Based on our conversation, you appear to have a low cancer risk profile. Your lack of smoking, absence of family history, and young age are all positive factors. I recommend continuing with age-appropriate screening tests and maintaining a healthy lifestyle."
```

### High Risk Scenario

```
Counselor: "Hello, how can I help you today?"

Patient: "I've been having this persistent cough for about three months now, and I've lost some weight without trying."

Counselor: "I understand your concern. Those are symptoms we should definitely discuss. Can you tell me about your smoking history?"

Patient: "Yes, I've been smoking for about 30 years, about a pack a day."

Counselor: "Thank you for sharing that. Have you noticed any other symptoms along with the cough?"

[Assessment continues...]

Counselor: "Based on what you've told me, including the persistent cough, unexplained weight loss, and significant smoking history, I recommend you schedule an appointment with your doctor as soon as possible. While I can't diagnose, these symptoms combined with your risk factors warrant prompt medical evaluation. Would you like help understanding what to expect at your doctor's visit?"
```

## Voice Configuration

### Voice Selection Tips

For medical counseling, choose voices that are:
- Calm and reassuring
- Clear and easy to understand
- Professional but warm
- Age-appropriate
- Culturally appropriate

### Recommended ElevenLabs Voices

- **Rachel** - Professional, empathetic female voice
- **Adam** - Professional, trustworthy male voice
- **Bella** - Warm, supportive female voice
- **Antoni** - Calm, clear male voice

### Voice Settings

```python
voice_settings = {
    'stability': 0.75,          # Higher = more consistent
    'similarity_boost': 0.80,    # Higher = closer to voice sample
    'style': 0.20,              # Expressiveness
    'use_speaker_boost': True
}
```

## Advanced Features

### 1. Emotion Detection

```python
# Detect patient anxiety from voice patterns
if emotion_detector.is_anxious(audio_features):
    counselor.adjust_tone('reassuring')
    counselor.slow_down()
```

### 2. Interruption Handling

```python
# Allow patient to interrupt
if voice_activity_detector.is_speaking():
    counselor.pause()
    counselor.listen()
```

### 3. Multi-Language Support

```python
# Detect and respond in patient's language
detected_language = language_detector.detect(speech)
counselor.set_language(detected_language)
```

### 4. Session Recording (with consent)

```python
# Record conversation for medical records
if patient.consents_to_recording():
    session_recorder.start()
```

## Technical Details

### Speech-to-Text Pipeline

1. Capture audio from microphone
2. Send to ElevenLabs Speech-to-Text API
3. Receive transcription
4. Process with Gemini for intent understanding
5. Update conversation context

### Text-to-Speech Pipeline

1. Generate response with Gemini
2. Optimize for spoken delivery
3. Send to ElevenLabs Text-to-Speech API
4. Receive audio stream
5. Play through speakers

### Latency Optimization

- Stream audio for real-time playback
- Pre-generate common responses
- Use voice activity detection
- Implement response chunking

## Demo Scenarios

### Scenario 1: Routine Screening

**Patient Profile:** 45-year-old female, no symptoms
**Focus:** Family history, preventive screening
**Outcome:** Low risk, routine surveillance recommended

### Scenario 2: Symptomatic Patient

**Patient Profile:** 62-year-old male with persistent cough
**Focus:** Symptom details, smoking history
**Outcome:** High risk, urgent medical evaluation needed

### Scenario 3: Worried Well

**Patient Profile:** 30-year-old anxious about cancer
**Focus:** Education, reassurance, risk factors
**Outcome:** Very low risk, lifestyle recommendations

## Privacy & Security

### Data Protection

- No voice recordings stored without consent
- All data encrypted in transit
- PHI de-identification
- HIPAA-compliant architecture

### User Consent

```
Before starting:
"This conversation will help assess your cancer risk. 
Your responses will be analyzed by AI but not stored 
unless you provide consent. Do you agree to continue?"
```

## Troubleshooting

### Audio Issues

```bash
# Check microphone
python scripts/test_microphone.py

# Adjust audio settings
export AUDIO_DEVICE_ID=0  # Change device ID
```

### API Issues

```bash
# Test ElevenLabs connection
curl -X GET "https://api.elevenlabs.io/v1/voices" \
     -H "xi-api-key: YOUR_API_KEY"
```

### Latency Issues

- Enable audio streaming
- Use voice activity detection
- Pre-cache common responses
- Optimize network connection

## Testing

### Unit Tests

```bash
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### Voice Quality Tests

```bash
python tests/test_voice_quality.py
```

## Performance Metrics

- **Response Time:** <2 seconds from question to answer
- **Speech Recognition Accuracy:** >95%
- **Voice Quality:** Natural, professional
- **Conversation Completion Rate:** >90%

## Future Enhancements

1. **Multi-modal input:** Accept images, documents
2. **Video counseling:** Add visual avatar
3. **Real-time translation:** Support multiple languages
4. **Emotion AI:** Adapt to patient emotional state
5. **Integration:** Connect with EHR systems

## Cost Estimation

**ElevenLabs Usage:**
- Speech-to-Text: ~$0.01 per minute
- Text-to-Speech: ~$0.30 per 1000 characters
- Average 10-minute conversation: ~$1-2

**Tips for cost optimization:**
- Use voice activity detection
- Cache common responses
- Implement usage limits
- Choose appropriate quality settings

## License

MIT License

## Disclaimer

This AI counselor is for informational purposes only and does not replace professional medical advice. Users should consult qualified healthcare providers for diagnosis and treatment.
