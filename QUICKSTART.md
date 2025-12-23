# Quick Start Guide - Cancer Risk Assessment Platforms

This guide will help you quickly get started with any of the three hackathon projects.

## 🎯 Choose Your Project

### 30-Second Decision Guide

**Want real-time streaming?** → Choose **Confluent**
**Want monitoring/observability?** → Choose **Datadog**  
**Want voice interaction?** → Choose **ElevenLabs**

## ⚡ Super Quick Setup (Any Project)

### Step 1: Clone & Navigate

```bash
git clone https://github.com/ck4957/MediMind.git
cd MediMind/projects/[confluent-cancer-risk|datadog-clinical-support|elevenlabs-voice-counseling]
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Then edit `.env` with your API keys:
- **All projects need**: `GEMINI_API_KEY` (get from https://makersuite.google.com/)
- **Confluent needs**: `CONFLUENT_API_KEY` (get from https://confluent.cloud)
- **Datadog needs**: `DD_API_KEY` (get from https://datadoghq.com)
- **ElevenLabs needs**: `ELEVENLABS_API_KEY` (get from https://elevenlabs.io)

### Step 3: Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run (project-specific)
# See below for each project
```

---

## 🎪 Project 1: Confluent (5-minute demo)

### Run It Now

```bash
cd projects/confluent-cancer-risk

# Terminal 1: Start imaging producer
python producers/imaging_producer.py

# Terminal 2: Start lab results producer
python producers/lab_results_producer.py

# Terminal 3: Start consumer
python consumers/risk_assessment_consumer.py

# Terminal 4: Dashboard (optional)
streamlit run dashboard/app.py
```

### What You'll See
- Real-time clinical data streaming
- AI processing each message
- Risk assessments appearing live
- Alerts for high-risk cases

### Demo Tips
- Let it run for 2-3 minutes to accumulate data
- Point out the multi-source streaming
- Highlight the AI analysis
- Show the alerting system

---

## 🎪 Project 2: Datadog (3-minute demo)

### Run It Now

```bash
cd projects/datadog-clinical-support

# Start the API (with tracing)
ddtrace-run python api/server.py

# In another terminal: Generate traffic
python scripts/generate_test_traffic.py --requests=20
```

### What You'll See
- API receiving requests
- Real-time processing
- Datadog traces appearing
- Metrics being collected

### Demo Tips
- Open Datadog dashboard in browser
- Show APM traces live
- Point out custom metrics
- Demonstrate alerting rules

---

## 🎪 Project 3: ElevenLabs (2-minute demo)

### Run It Now

```bash
cd projects/elevenlabs-voice-counseling

# Test setup first
python scripts/test_elevenlabs.py

# Start the counselor
python conversation_engine/voice_counselor.py
```

### What You'll See
- Voice conversation starting
- AI asking questions
- Natural language interaction
- Risk assessment results

### Demo Tips
- Have predefined answers ready
- Show empathetic responses
- Highlight voice quality
- Complete full assessment flow

---

## 🐛 Troubleshooting

### Common Issues

**"API key not found"**
```bash
# Check your .env file exists
ls -la .env

# Make sure it has your keys
cat .env | grep API_KEY
```

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Connection refused"**
```bash
# Check if service is running
# Check your internet connection
# Verify API keys are correct
```

### Project-Specific Issues

**Confluent: "Topic not found"**
```bash
# Create topics first
python scripts/create_topics.py
```

**Datadog: "No traces appearing"**
```bash
# Make sure ddtrace is installed
pip install ddtrace

# Use ddtrace-run prefix
ddtrace-run python api/server.py
```

**ElevenLabs: "No audio"**
```bash
# Check audio libraries
pip install sounddevice soundfile

# Test microphone
python scripts/test_microphone.py
```

---

## 📚 Next Steps

After getting started:

1. **Read the full README** for your project
2. **Customize** the configuration
3. **Test** all features
4. **Prepare** your demo script
5. **Practice** the presentation

---

## 🎤 Presentation Tips

### 3-Minute Pitch Structure

**Minute 1: The Problem**
- Cancer risk assessment is complex
- Multiple data sources needed
- Time-sensitive decisions
- Need for accessible technology

**Minute 2: Our Solution**
- Show the technology architecture
- Explain how it works
- Highlight key features
- Emphasize innovation

**Minute 3: Live Demo**
- Run the actual system
- Show real-time results
- Point out differentiators
- End with impact statement

### Key Talking Points

**Confluent Project:**
- "Real-time streaming enables instant risk assessment"
- "Multiple data sources processed simultaneously"
- "Scalable to handle hospital-wide deployments"

**Datadog Project:**
- "Full observability ensures AI reliability"
- "Monitor model performance in real-time"
- "Security monitoring protects patient data"

**ElevenLabs Project:**
- "Natural conversation makes healthcare accessible"
- "Empathetic AI reduces patient anxiety"
- "Voice interface serves diverse populations"

---

## ✅ Pre-Demo Checklist

### 30 Minutes Before

- [ ] Test internet connection
- [ ] Verify all API keys work
- [ ] Run through demo once
- [ ] Prepare backup slides
- [ ] Have code open in IDE
- [ ] Clear terminal history
- [ ] Set comfortable screen brightness

### 5 Minutes Before

- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Open required terminals
- [ ] Have browser tabs ready
- [ ] Test audio/video
- [ ] Take a deep breath 😊

---

## 🏆 Judging Criteria Alignment

### Technical Complexity
- **Confluent**: ⭐⭐⭐⭐⭐ (Streaming architecture)
- **Datadog**: ⭐⭐⭐⭐ (Observability stack)
- **ElevenLabs**: ⭐⭐⭐⭐ (Voice AI integration)

### Innovation
- **Confluent**: ⭐⭐⭐⭐⭐ (Real-time clinical AI)
- **Datadog**: ⭐⭐⭐⭐⭐ (AI monitoring)
- **ElevenLabs**: ⭐⭐⭐⭐⭐ (Conversational health)

### Impact
- **Confluent**: ⭐⭐⭐⭐⭐ (Hospital-scale deployment)
- **Datadog**: ⭐⭐⭐⭐ (Production reliability)
- **ElevenLabs**: ⭐⭐⭐⭐⭐ (Accessibility)

### Completeness
- **All projects**: ⭐⭐⭐⭐⭐ (Fully functional)

---

## 💪 Last-Minute Tips

1. **Keep it simple**: Focus on core features
2. **Tell a story**: Use patient scenarios
3. **Show, don't tell**: Live demo is key
4. **Be enthusiastic**: Passion is contagious
5. **Have fun**: Enjoy the experience!

---

## 🚨 Emergency Backup Plan

If something breaks during demo:

1. **Have screenshots/video ready**
2. **Show code instead of running**
3. **Use sample dialogues**
4. **Explain what would happen**
5. **Stay confident**

Remember: Judges understand demos fail sometimes. Your explanation matters more than perfect execution.

---

## 📞 Need Help?

- Check project README files
- Review code comments
- Test with mock data
- Ask teammates for help
- Trust your preparation

---

**You've got this! Go win that hackathon! 🎉**
