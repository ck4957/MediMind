"""
Google Cloud Platform Configuration Module
Manages GCP service connections and settings
"""

import os
from google.cloud import aiplatform
from dotenv import load_dotenv

load_dotenv()


class GCPConfig:
    """Google Cloud Platform configuration"""
    
    # Project settings
    PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    REGION = os.getenv('GCP_REGION', 'us-central1')
    
    # Vertex AI settings
    VERTEX_AI_ENDPOINT = os.getenv('VERTEX_AI_ENDPOINT')
    MODEL_NAME = os.getenv('MODEL_NAME', 'cancer-risk-model')
    
    # Gemini settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
    
    # BigQuery settings
    BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET', 'cancer_risk_data')
    BIGQUERY_TABLE_PREDICTIONS = os.getenv('BIGQUERY_TABLE_PREDICTIONS', 'predictions')
    
    # Cloud Storage
    STORAGE_BUCKET = os.getenv('STORAGE_BUCKET', f'{PROJECT_ID}-cancer-risk-data')
    
    @classmethod
    def initialize_vertex_ai(cls):
        """Initialize Vertex AI client"""
        aiplatform.init(
            project=cls.PROJECT_ID,
            location=cls.REGION,
        )
    
    @classmethod
    def get_endpoint(cls):
        """Get Vertex AI endpoint"""
        if not cls.VERTEX_AI_ENDPOINT:
            raise ValueError("VERTEX_AI_ENDPOINT not configured")
        return aiplatform.Endpoint(cls.VERTEX_AI_ENDPOINT)


# Model configuration
MODEL_CONFIG = {
    'input_features': [
        'age',
        'gender',
        'smoking_history',
        'family_history',
        'bmi',
        'blood_pressure',
        'cholesterol',
        'glucose_level',
        'tumor_markers',
        'imaging_features',
    ],
    'output_classes': [
        'low_risk',
        'moderate_risk',
        'high_risk',
        'very_high_risk',
    ],
    'threshold_high_risk': 0.7,
    'threshold_moderate_risk': 0.4,
}


# Gemini prompts
GEMINI_PROMPTS = {
    'analyze_clinical_notes': """
You are a medical AI assistant analyzing clinical notes for cancer risk assessment.

Clinical Note:
{clinical_note}

Lab Results:
{lab_results}

Tasks:
1. Extract key risk factors mentioned in the note
2. Identify any concerning symptoms or findings
3. Note any family history of cancer
4. Assess the overall risk level based on the information
5. Provide a concise summary for the risk assessment model

Format your response as JSON with the following structure:
{{
    "risk_factors": ["factor1", "factor2", ...],
    "concerning_findings": ["finding1", "finding2", ...],
    "family_history": true/false,
    "risk_level": "low/moderate/high/very_high",
    "summary": "Brief summary of key findings"
}}
""",
    
    'explain_prediction': """
You are a medical AI assistant explaining cancer risk predictions to patients and healthcare providers.

Patient Data Summary:
{patient_summary}

Model Prediction:
- Risk Level: {risk_level}
- Confidence: {confidence}
- Key Contributing Factors: {factors}

Task:
Provide a clear, empathetic explanation of this risk assessment that:
1. Explains what the risk level means
2. Describes the main factors contributing to this assessment
3. Suggests next steps or recommendations
4. Uses language appropriate for a patient consultation

Keep the explanation concise (3-4 paragraphs) and supportive.
""",
}
