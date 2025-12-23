"""
Conversation prompts for the AI counselor
"""

SYSTEM_PROMPT = """
You are an empathetic AI health counselor specializing in cancer risk assessment. Your role is to:

1. Conduct compassionate conversations with patients about their cancer risk concerns
2. Ask relevant questions to gather necessary health information
3. Provide clear, accurate, and supportive guidance
4. Explain complex medical concepts in accessible language
5. Show empathy and understanding throughout the conversation

Guidelines:
- Use a warm, professional tone
- Ask one question at a time
- Listen carefully to responses
- Provide reassurance when appropriate
- Never diagnose, but help assess risk factors
- Encourage professional medical consultation when needed
- Respect patient emotions and concerns
- Keep responses concise for voice delivery

Remember: You're here to support and guide, not to replace medical professionals.
"""

GREETING_PROMPTS = [
    "Hello, I'm your AI health counselor. I'm here to help assess your cancer risk and answer any questions you might have. This conversation is confidential, and we'll take as much time as you need. How are you feeling today?",
    
    "Good day. I'm an AI counselor trained to help with cancer risk assessment. I'd like to ask you some questions about your health to provide you with personalized guidance. Before we begin, is there anything specific that brought you here today?",
    
    "Welcome. I'm here to have a conversation with you about cancer risk assessment. This is a safe space to discuss your concerns. What would you like to talk about today?",
]

DEMOGRAPHIC_QUESTIONS = {
    'age': [
        "To start, may I ask how old you are?",
        "Could you tell me your age?",
        "What's your age, if you don't mind sharing?",
    ],
    'gender': [
        "And what is your gender?",
        "May I ask your gender?",
        "Could you share your gender?",
    ],
}

RISK_FACTOR_QUESTIONS = {
    'family_history': [
        "Has anyone in your immediate family been diagnosed with cancer? This includes parents, siblings, or children.",
        "I'd like to ask about your family health history. Have any of your close relatives had cancer?",
        "Family history can be an important factor. Has anyone in your immediate family had cancer?",
    ],
    
    'smoking': [
        "Do you smoke, or have you smoked in the past?",
        "I need to ask about smoking. What's your smoking history?",
        "Have you ever been a smoker, or do you currently smoke?",
    ],
    
    'alcohol': [
        "How often do you drink alcohol, if at all?",
        "Could you tell me about your alcohol consumption?",
        "Do you drink alcohol? If so, how frequently?",
    ],
    
    'occupation': [
        "What type of work do you do? Some occupations involve exposure to certain substances.",
        "Can you tell me about your occupation? This helps us understand potential environmental exposures.",
        "What kind of work have you been doing throughout your career?",
    ],
    
    'lifestyle': [
        "How would you describe your diet and exercise habits?",
        "Could you tell me a bit about your lifestyle - diet, exercise, that sort of thing?",
        "I'd like to understand your lifestyle habits. How do you typically eat and exercise?",
    ],
}

SYMPTOM_QUESTIONS = {
    'has_symptoms': [
        "Are you experiencing any health concerns or symptoms that worry you?",
        "Is there a particular symptom or health issue that brought you here?",
        "Have you noticed any changes in your health recently?",
    ],
    
    'symptom_details': [
        "Can you describe what you've been experiencing?",
        "Tell me more about these symptoms. What exactly have you noticed?",
        "Could you provide more details about what you're experiencing?",
    ],
    
    'duration': [
        "How long have you been experiencing this?",
        "When did you first notice these symptoms?",
        "How long has this been going on?",
    ],
    
    'severity': [
        "How severe would you say these symptoms are?",
        "On a scale from mild to severe, how would you describe the symptoms?",
        "Are these symptoms affecting your daily life?",
    ],
}

CLARIFICATION_PROMPTS = [
    "I want to make sure I understand correctly. Could you elaborate on that?",
    "Can you tell me a bit more about that?",
    "I'd like to understand better. Could you provide more details?",
    "That's helpful. Can you explain a bit more?",
]

EMPATHY_RESPONSES = {
    'concern': [
        "I understand this is concerning for you. Let's work through this together.",
        "It's completely natural to have these concerns. I'm here to help.",
        "I can hear that this is worrying you. Let's see what we can understand about your situation.",
    ],
    
    'fear': [
        "I understand you're feeling anxious about this. That's a very normal reaction.",
        "It's okay to feel worried. Let's look at the facts together.",
        "Fear about health is natural. Let me help you understand your situation better.",
    ],
    
    'relief': [
        "I'm glad we could discuss this together.",
        "It's good that you're taking this proactive approach to your health.",
        "I hope this conversation has been helpful for you.",
    ],
}

RISK_LEVEL_EXPLANATIONS = {
    'low': """
Based on our conversation, you appear to have a low cancer risk profile. The factors we discussed suggest that your risk is below average. This is positive news.

Key points:
- Your risk factors are minimal
- Continue with age-appropriate screening
- Maintain healthy lifestyle habits
- Stay alert to any new symptoms

Remember, low risk doesn't mean no risk, so regular check-ups are still important.
""",
    
    'moderate': """
Based on our discussion, you have a moderate cancer risk level. This means some factors in your history or lifestyle may slightly increase your risk, but it's manageable.

Key points:
- Several risk factors have been identified
- More frequent monitoring may be beneficial
- Lifestyle modifications could help reduce risk
- Discuss with your doctor about appropriate screening

This is not a cause for alarm, but it does mean staying vigilant is important.
""",
    
    'high': """
Based on what you've shared, you have some significant risk factors that warrant closer medical attention. I want to be clear: this is a risk assessment, not a diagnosis.

Important next steps:
- Schedule an appointment with your healthcare provider soon
- Discuss appropriate screening tests
- Be proactive about any concerning symptoms
- Consider lifestyle modifications to reduce risk

While this assessment indicates higher risk, many risk factors can be managed, and early detection makes a significant difference.
""",
    
    'urgent': """
Based on our conversation, particularly the symptoms you've described and your risk factors, I strongly recommend you schedule a medical appointment as soon as possible - ideally within the next few days.

Why this is important:
- The combination of symptoms and risk factors needs professional evaluation
- Early assessment by a doctor is crucial
- Several concerning factors have been identified

Please don't delay in seeing a healthcare provider. While I can't diagnose, the information you've shared warrants prompt medical attention.
""",
}

CLOSING_PROMPTS = [
    "Thank you for sharing your health information with me today. Is there anything else you'd like to discuss or any questions you have?",
    
    "I appreciate your openness during our conversation. Before we end, do you have any other concerns you'd like to address?",
    
    "We've covered a lot today. Is there anything else on your mind that you'd like to talk about?",
]

FAREWELL_MESSAGES = [
    "Thank you for speaking with me today. Please remember to follow up with your healthcare provider. Take care of yourself.",
    
    "I hope this conversation has been helpful. Remember, your healthcare provider is your best resource for personalized medical advice. Wishing you good health.",
    
    "It was good speaking with you. Please don't hesitate to seek medical attention if you have concerns. Take care.",
]

# Follow-up recommendations
RECOMMENDATIONS = {
    'low_risk': [
        "Continue with age-appropriate cancer screening tests",
        "Maintain a healthy diet rich in fruits and vegetables",
        "Exercise regularly - at least 150 minutes per week",
        "Avoid tobacco and limit alcohol consumption",
        "Protect your skin from excessive sun exposure",
        "Schedule regular check-ups with your primary care physician",
    ],
    
    'moderate_risk': [
        "Discuss earlier or more frequent screening with your doctor",
        "Consider genetic counseling if family history is significant",
        "Make lifestyle modifications to reduce controllable risk factors",
        "Keep detailed records of your health history",
        "Be vigilant about any new or changing symptoms",
        "Schedule regular medical check-ups",
    ],
    
    'high_risk': [
        "Schedule an appointment with your healthcare provider promptly",
        "Discuss intensive screening programs",
        "Consider referral to a specialist",
        "Explore risk reduction strategies with your doctor",
        "Stop smoking immediately if you currently smoke",
        "Document any symptoms or changes carefully",
    ],
}
