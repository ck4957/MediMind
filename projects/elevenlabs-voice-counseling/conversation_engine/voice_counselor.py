"""
Main Voice Counselor Application
Interactive AI counselor for cancer risk assessment
"""

import sys
import os
import random
from typing import Dict, Any, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.elevenlabs_config import ConversationConfig, CONVERSATION_STATES
from config.prompts import (
    SYSTEM_PROMPT, GREETING_PROMPTS, DEMOGRAPHIC_QUESTIONS,
    RISK_FACTOR_QUESTIONS, SYMPTOM_QUESTIONS, RISK_LEVEL_EXPLANATIONS,
    CLOSING_PROMPTS, FAREWELL_MESSAGES, RECOMMENDATIONS
)
from voice.speech_synthesis import SpeechSynthesizer
from voice.speech_recognition import SpeechRecognizer

# Try to import Gemini for conversation
try:
    import google.generativeai as genai
    from config.elevenlabs_config import GCPConfig
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class VoiceCounselor:
    """AI voice counselor for cancer risk assessment"""
    
    def __init__(self):
        self.synthesizer = SpeechSynthesizer()
        self.recognizer = SpeechRecognizer()
        
        # Initialize Gemini if available
        self.gemini_client = None
        if GEMINI_AVAILABLE and GCPConfig.GEMINI_API_KEY:
            genai.configure(api_key=GCPConfig.GEMINI_API_KEY)
            self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
        
        # Conversation state
        self.conversation_state = 'GREETING'
        self.turn_count = 0
        self.collected_info = {}
        self.conversation_history = []
    
    def start_conversation(self):
        """Start a new counseling session"""
        print("=" * 60)
        print("AI Cancer Risk Counselor")
        print("=" * 60)
        print("\nStarting conversation...")
        print("(You can type 'quit' or 'exit' to end the conversation)\n")
        
        # Greeting
        greeting = random.choice(GREETING_PROMPTS)
        self.speak(greeting)
        self.add_to_history('counselor', greeting)
        
        # Main conversation loop
        while self.turn_count < ConversationConfig.MAX_TURNS:
            try:
                # Listen to patient
                patient_response = self.listen()
                
                if not patient_response:
                    self.speak("I didn't catch that. Could you please repeat?")
                    continue
                
                # Check for exit commands
                if patient_response.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                    farewell = random.choice(FAREWELL_MESSAGES)
                    self.speak(farewell)
                    break
                
                self.add_to_history('patient', patient_response)
                self.turn_count += 1
                
                # Process response and generate reply
                counselor_response = self.process_response(patient_response)
                self.speak(counselor_response)
                self.add_to_history('counselor', counselor_response)
                
                # Check if conversation is complete
                if self.conversation_state == 'CLOSING':
                    break
                
            except KeyboardInterrupt:
                print("\n\nConversation interrupted.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                self.speak("I apologize, I encountered an issue. Let's continue our conversation.")
        
        # Wrap up
        self.end_conversation()
    
    def speak(self, text: str):
        """Speak text through TTS"""
        self.synthesizer.synthesize_speech(text, play_audio=True)
    
    def listen(self) -> str:
        """Listen for patient response"""
        return self.recognizer.listen(timeout=ConversationConfig.RESPONSE_TIMEOUT)
    
    def process_response(self, patient_response: str) -> str:
        """
        Process patient response and generate counselor reply
        
        Args:
            patient_response: What the patient said
            
        Returns:
            Counselor's response
        """
        # Extract information from response
        self.extract_information(patient_response)
        
        # Determine next question or statement
        if self.conversation_state == 'GREETING':
            return self.handle_greeting_state(patient_response)
        
        elif self.conversation_state == 'INITIAL_ASSESSMENT':
            return self.handle_initial_assessment(patient_response)
        
        elif self.conversation_state == 'RISK_FACTOR_COLLECTION':
            return self.collect_risk_factors()
        
        elif self.conversation_state == 'SYMPTOM_EXPLORATION':
            return self.explore_symptoms()
        
        elif self.conversation_state == 'RISK_ASSESSMENT':
            return self.perform_assessment()
        
        elif self.conversation_state == 'RESULTS_COMMUNICATION':
            return self.communicate_results()
        
        elif self.conversation_state == 'FOLLOW_UP':
            return self.provide_recommendations()
        
        else:
            return "Let's continue our conversation. What else would you like to discuss?"
    
    def handle_greeting_state(self, response: str) -> str:
        """Handle initial greeting state"""
        self.conversation_state = 'INITIAL_ASSESSMENT'
        
        # Check if patient expressed concern
        concern_keywords = ['worried', 'concerned', 'afraid', 'scared', 'anxious']
        if any(word in response.lower() for word in concern_keywords):
            return "I understand you're concerned. It's very wise to be proactive about your health. Let's start by getting some basic information. How old are you?"
        
        return "Thank you for sharing. To help assess your risk, I need to gather some information. First, may I ask how old you are?"
    
    def handle_initial_assessment(self, response: str) -> str:
        """Handle initial assessment questions"""
        # Check what information we still need
        if 'age' not in self.collected_info:
            self.extract_age(response)
            return "Thank you. And what is your gender?"
        
        if 'gender' not in self.collected_info:
            self.extract_gender(response)
            self.conversation_state = 'RISK_FACTOR_COLLECTION'
            return "Now, I'd like to ask about your family history. Has anyone in your immediate family been diagnosed with cancer?"
        
        return "Could you please provide your age and gender?"
    
    def collect_risk_factors(self) -> str:
        """Collect risk factor information"""
        # Ask about different risk factors
        if 'family_history' not in self.collected_info:
            return random.choice(RISK_FACTOR_QUESTIONS['family_history'])
        
        if 'smoking' not in self.collected_info:
            return random.choice(RISK_FACTOR_QUESTIONS['smoking'])
        
        if 'alcohol' not in self.collected_info:
            return random.choice(RISK_FACTOR_QUESTIONS['alcohol'])
        
        # Check for symptoms
        self.conversation_state = 'SYMPTOM_EXPLORATION'
        return random.choice(SYMPTOM_QUESTIONS['has_symptoms'])
    
    def explore_symptoms(self) -> str:
        """Explore any symptoms the patient has"""
        if 'has_symptoms' not in self.collected_info:
            return random.choice(SYMPTOM_QUESTIONS['has_symptoms'])
        
        if self.collected_info.get('has_symptoms') and 'symptom_details' not in self.collected_info:
            return random.choice(SYMPTOM_QUESTIONS['symptom_details'])
        
        # Move to assessment
        self.conversation_state = 'RISK_ASSESSMENT'
        return "Thank you for sharing all this information. Let me assess your risk based on what you've told me. One moment please."
    
    def perform_assessment(self) -> str:
        """Calculate and return risk assessment"""
        risk_level = self.calculate_risk()
        self.collected_info['risk_level'] = risk_level
        
        self.conversation_state = 'RESULTS_COMMUNICATION'
        
        explanation = RISK_LEVEL_EXPLANATIONS.get(risk_level, RISK_LEVEL_EXPLANATIONS['low'])
        return explanation.strip()
    
    def communicate_results(self) -> str:
        """Communicate assessment results"""
        self.conversation_state = 'FOLLOW_UP'
        return "Would you like me to provide some specific recommendations based on this assessment?"
    
    def provide_recommendations(self) -> str:
        """Provide personalized recommendations"""
        risk_level = self.collected_info.get('risk_level', 'low')
        
        if risk_level == 'urgent':
            recommendations = RECOMMENDATIONS['high_risk']
        elif risk_level == 'high':
            recommendations = RECOMMENDATIONS['high_risk']
        elif risk_level == 'moderate':
            recommendations = RECOMMENDATIONS['moderate_risk']
        else:
            recommendations = RECOMMENDATIONS['low_risk']
        
        # Format recommendations
        rec_text = "Here are my recommendations:\n\n"
        for i, rec in enumerate(recommendations[:3], 1):
            rec_text += f"{i}. {rec}\n"
        
        self.conversation_state = 'CLOSING'
        return rec_text + "\n" + random.choice(CLOSING_PROMPTS)
    
    def extract_information(self, text: str):
        """Extract relevant information from patient response"""
        text_lower = text.lower()
        
        # Extract age
        if 'age' not in self.collected_info:
            self.extract_age(text)
        
        # Extract gender
        if 'gender' not in self.collected_info:
            self.extract_gender(text)
        
        # Extract family history
        if 'family_history' not in self.collected_info:
            if any(word in text_lower for word in ['yes', 'mother', 'father', 'sister', 'brother', 'parent']):
                self.collected_info['family_history'] = True
            elif any(word in text_lower for word in ['no', 'not', 'never', 'none']):
                self.collected_info['family_history'] = False
        
        # Extract smoking status
        if 'smoking' not in self.collected_info:
            if 'current' in text_lower or 'still smoke' in text_lower:
                self.collected_info['smoking'] = 'current'
            elif 'former' in text_lower or 'used to' in text_lower or 'quit' in text_lower:
                self.collected_info['smoking'] = 'former'
            elif 'never' in text_lower or "don't smoke" in text_lower:
                self.collected_info['smoking'] = 'never'
        
        # Extract symptoms
        if 'has_symptoms' not in self.collected_info:
            symptom_keywords = ['pain', 'cough', 'weight loss', 'fatigue', 'lump', 'bleeding']
            if any(word in text_lower for word in symptom_keywords):
                self.collected_info['has_symptoms'] = True
                self.collected_info['symptom_details'] = text
            elif any(word in text_lower for word in ['no', 'not', 'none', "don't have"]):
                self.collected_info['has_symptoms'] = False
    
    def extract_age(self, text: str):
        """Extract age from text"""
        import re
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            age = int(numbers[0])
            if 18 <= age <= 120:
                self.collected_info['age'] = age
    
    def extract_gender(self, text: str):
        """Extract gender from text"""
        text_lower = text.lower()
        if 'male' in text_lower and 'female' not in text_lower:
            self.collected_info['gender'] = 'male'
        elif 'female' in text_lower:
            self.collected_info['gender'] = 'female'
        elif any(word in text_lower for word in ['man', 'boy']):
            self.collected_info['gender'] = 'male'
        elif any(word in text_lower for word in ['woman', 'girl']):
            self.collected_info['gender'] = 'female'
    
    def calculate_risk(self) -> str:
        """Calculate risk level based on collected information"""
        risk_score = 0.0
        
        # Age factor
        age = self.collected_info.get('age', 40)
        if age > 65:
            risk_score += 0.3
        elif age > 50:
            risk_score += 0.2
        
        # Family history
        if self.collected_info.get('family_history'):
            risk_score += 0.3
        
        # Smoking
        smoking = self.collected_info.get('smoking')
        if smoking == 'current':
            risk_score += 0.4
        elif smoking == 'former':
            risk_score += 0.2
        
        # Symptoms
        if self.collected_info.get('has_symptoms'):
            risk_score += 0.3
        
        # Determine level
        if risk_score >= 0.8:
            return 'urgent'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'moderate'
        else:
            return 'low'
    
    def add_to_history(self, speaker: str, text: str):
        """Add to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'speaker': speaker,
            'text': text,
        })
    
    def end_conversation(self):
        """End the counseling session"""
        print("\n" + "=" * 60)
        print("Conversation Summary")
        print("=" * 60)
        print(f"Total turns: {self.turn_count}")
        print(f"\nCollected Information:")
        for key, value in self.collected_info.items():
            print(f"  {key}: {value}")
        print("=" * 60)
        print("\nThank you for using the AI Cancer Risk Counselor.")
        print("Remember: This is an assessment tool, not medical advice.")
        print("Please consult with healthcare professionals for proper evaluation.")
        print("=" * 60)


if __name__ == '__main__':
    counselor = VoiceCounselor()
    counselor.start_conversation()
