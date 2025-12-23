"""
Gemini Integration Module
Handles clinical text analysis using Google Gemini
"""

import json
import os
from typing import Dict, Any
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.gcp_config import GCPConfig, GEMINI_PROMPTS

# Try to import Google Generative AI, fall back to mock if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("WARNING: google-generativeai not installed. Using mock responses.")


class GeminiClient:
    """Client for Gemini clinical text analysis"""
    
    def __init__(self):
        self.model = None
        if GEMINI_AVAILABLE and GCPConfig.GEMINI_API_KEY:
            genai.configure(api_key=GCPConfig.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(GCPConfig.GEMINI_MODEL)
        else:
            print("WARNING: Gemini not configured. Using mock responses.")
    
    def analyze_clinical_notes(
        self,
        clinical_note: str,
        lab_results: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze clinical notes for cancer risk factors
        
        Args:
            clinical_note: Clinical note text
            lab_results: Optional lab results data
            
        Returns:
            Dictionary with extracted risk factors and analysis
        """
        if self.model:
            return self._gemini_analysis(clinical_note, lab_results)
        else:
            return self._mock_analysis(clinical_note, lab_results)
    
    def explain_prediction(
        self,
        patient_summary: str,
        risk_level: str,
        confidence: float,
        factors: list
    ) -> str:
        """
        Generate human-readable explanation of risk prediction
        
        Args:
            patient_summary: Summary of patient data
            risk_level: Predicted risk level
            confidence: Model confidence score
            factors: List of contributing factors
            
        Returns:
            Explanation text
        """
        if self.model:
            return self._gemini_explanation(patient_summary, risk_level, confidence, factors)
        else:
            return self._mock_explanation(patient_summary, risk_level, confidence, factors)
    
    def _gemini_analysis(
        self,
        clinical_note: str,
        lab_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use Gemini to analyze clinical notes"""
        prompt = GEMINI_PROMPTS['analyze_clinical_notes'].format(
            clinical_note=json.dumps(clinical_note, indent=2),
            lab_results=json.dumps(lab_results or {}, indent=2)
        )
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            text = response.text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            else:
                json_str = text.strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return self._mock_analysis(clinical_note, lab_results)
    
    def _gemini_explanation(
        self,
        patient_summary: str,
        risk_level: str,
        confidence: float,
        factors: list
    ) -> str:
        """Use Gemini to generate explanation"""
        prompt = GEMINI_PROMPTS['explain_prediction'].format(
            patient_summary=patient_summary,
            risk_level=risk_level,
            confidence=f"{confidence:.2%}",
            factors=", ".join(factors)
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return self._mock_explanation(patient_summary, risk_level, confidence, factors)
    
    def _mock_analysis(
        self,
        clinical_note: str,
        lab_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate mock analysis for demo"""
        # Simple keyword-based analysis
        note_text = str(clinical_note).lower()
        
        risk_factors = []
        concerning_findings = []
        
        # Check for risk factors in text
        if 'smoking' in note_text or 'smoker' in note_text:
            risk_factors.append('Smoking history')
        if 'family history' in note_text:
            risk_factors.append('Family history of cancer')
        if 'weight loss' in note_text:
            concerning_findings.append('Unintentional weight loss')
        if 'nodule' in note_text or 'mass' in note_text:
            concerning_findings.append('Suspicious imaging findings')
        if 'elevated' in note_text:
            concerning_findings.append('Abnormal lab values')
        
        # Check lab results
        if lab_results:
            results = lab_results.get('results', {})
            if results.get('cea', 0) > 5.0:
                concerning_findings.append('Elevated CEA tumor marker')
            if results.get('ca_125', 0) > 35:
                concerning_findings.append('Elevated CA-125 tumor marker')
        
        # Determine risk level
        if len(concerning_findings) >= 2:
            risk_level = 'high'
        elif len(concerning_findings) >= 1 or len(risk_factors) >= 2:
            risk_level = 'moderate'
        else:
            risk_level = 'low'
        
        return {
            'risk_factors': risk_factors if risk_factors else ['No significant risk factors identified'],
            'concerning_findings': concerning_findings if concerning_findings else ['No concerning findings'],
            'family_history': 'family history' in note_text,
            'risk_level': risk_level,
            'summary': f'Assessment suggests {risk_level} risk based on available clinical data.',
            'is_mock': True,
        }
    
    def _mock_explanation(
        self,
        patient_summary: str,
        risk_level: str,
        confidence: float,
        factors: list
    ) -> str:
        """Generate mock explanation for demo"""
        explanations = {
            'low_risk': (
                "Based on the comprehensive assessment, this patient shows a low risk profile "
                "for cancer. The analysis considered multiple factors including clinical history, "
                "laboratory results, and imaging findings. "
                "\n\n"
                f"Key factors in this assessment include: {', '.join(factors)}. "
                "\n\n"
                "Recommended next steps include continuing routine surveillance with "
                "age-appropriate screening tests. The patient should maintain healthy lifestyle "
                "habits and report any new symptoms promptly. "
                "\n\n"
                f"This assessment was made with {confidence:.0%} confidence based on the available data."
            ),
            'moderate_risk': (
                "The assessment indicates a moderate risk level that warrants careful monitoring. "
                "While not immediately alarming, certain factors require attention and follow-up. "
                "\n\n"
                f"Contributing factors include: {', '.join(factors)}. "
                "\n\n"
                "Recommended actions include scheduling follow-up appointments within 3-6 months, "
                "considering additional diagnostic tests, and discussing lifestyle modifications "
                "that may help reduce risk factors. "
                "\n\n"
                f"This assessment was made with {confidence:.0%} confidence. Close monitoring is advised."
            ),
            'high_risk': (
                "This assessment indicates a high risk profile requiring prompt medical attention. "
                "Multiple concerning factors have been identified that need immediate evaluation. "
                "\n\n"
                f"Critical factors include: {', '.join(factors)}. "
                "\n\n"
                "Immediate next steps should include consultation with an oncologist, comprehensive "
                "diagnostic workup including imaging and biopsies as appropriate, and discussion of "
                "treatment options. Time-sensitive follow-up is essential. "
                "\n\n"
                f"This assessment was made with {confidence:.0%} confidence. Urgent follow-up is strongly recommended."
            ),
        }
        
        return explanations.get(risk_level, explanations['moderate_risk'])
