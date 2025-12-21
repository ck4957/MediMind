"""
Cancer Risk Assessment Module with AI Integration
"""

import time
import random
from typing import Dict, Any, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.datadog_config import DatadogConfig, METRICS_ENABLED

# Try to import Datadog tracing
try:
    from ddtrace import tracer
    TRACING_ENABLED = True
except ImportError:
    TRACING_ENABLED = False
    tracer = None

# Try to import StatsD
try:
    from datadog import statsd
except ImportError:
    statsd = None


class CancerRiskAssessor:
    """
    Cancer risk assessment using AI models
    Instrumented with Datadog observability
    """
    
    def __init__(self):
        self.gemini_available = False
        self.vertex_available = False
        
        # Try to import AI clients
        try:
            import google.generativeai as genai
            from config.datadog_config import GCPConfig
            
            if GCPConfig.GEMINI_API_KEY:
                genai.configure(api_key=GCPConfig.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
                self.gemini_available = True
        except:
            self.gemini_client = None
    
    async def assess_risk(
        self,
        age: int,
        gender: str,
        clinical_notes: str,
        lab_results: Optional[Dict] = None,
        imaging_results: Optional[Dict] = None,
        family_history: bool = False,
        smoking_status: str = "never",
    ) -> Dict[str, Any]:
        """
        Perform comprehensive cancer risk assessment
        
        Returns risk level, confidence, and explanation
        """
        
        # Step 1: Analyze clinical notes with Gemini
        with self._trace_operation('gemini.analyze_clinical_notes'):
            clinical_analysis = await self._analyze_with_gemini(
                clinical_notes,
                lab_results
            )
        
        # Step 2: Calculate risk score
        with self._trace_operation('calculate_risk_score'):
            risk_score = self._calculate_risk_score(
                age=age,
                gender=gender,
                clinical_analysis=clinical_analysis,
                lab_results=lab_results,
                imaging_results=imaging_results,
                family_history=family_history,
                smoking_status=smoking_status,
            )
        
        # Step 3: Determine risk level
        risk_level, confidence = self._determine_risk_level(risk_score)
        
        # Step 4: Generate explanation
        with self._trace_operation('generate_explanation'):
            explanation = await self._generate_explanation(
                risk_level=risk_level,
                confidence=confidence,
                factors={
                    'age': age,
                    'gender': gender,
                    'family_history': family_history,
                    'smoking': smoking_status,
                    'clinical_findings': clinical_analysis,
                }
            )
        
        # Calculate risk scores for all levels
        risk_scores = self._calculate_all_risk_scores(risk_score)
        
        return {
            'risk_level': risk_level,
            'confidence': confidence,
            'risk_scores': risk_scores,
            'explanation': explanation,
        }
    
    async def _analyze_with_gemini(
        self,
        clinical_notes: str,
        lab_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Analyze clinical data with Gemini"""
        start_time = time.time()
        
        try:
            if self.gemini_available and self.gemini_client:
                prompt = self._create_analysis_prompt(clinical_notes, lab_results)
                response = self.gemini_client.generate_content(prompt)
                
                latency_ms = (time.time() - start_time) * 1000
                
                # Track Gemini API metrics
                if METRICS_ENABLED and statsd:
                    statsd.histogram('gemini.latency', latency_ms)
                    statsd.gauge('gemini.tokens_used', len(prompt.split()))
                    statsd.increment('gemini.requests', tags=['status:success'])
                
                # Simple parsing of response
                analysis = self._parse_gemini_response(response.text)
                return analysis
            else:
                # Fallback to mock analysis
                return self._mock_clinical_analysis(clinical_notes, lab_results)
                
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            if METRICS_ENABLED and statsd:
                statsd.histogram('gemini.latency', latency_ms)
                statsd.increment('gemini.errors', tags=[f'error:{type(e).__name__}'])
            
            # Fallback to mock
            return self._mock_clinical_analysis(clinical_notes, lab_results)
    
    def _create_analysis_prompt(self, clinical_notes: str, lab_results: Optional[Dict]) -> str:
        """Create prompt for Gemini analysis"""
        prompt = f"""
Analyze the following clinical data for cancer risk factors:

Clinical Notes:
{clinical_notes}

Lab Results:
{lab_results if lab_results else 'Not provided'}

Please identify:
1. Key risk factors
2. Concerning findings
3. Overall risk impression (low/moderate/high)

Provide a brief, clinical analysis.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response"""
        # Simple parsing - in production, use structured output
        risk_factors = []
        if 'smoking' in response_text.lower():
            risk_factors.append('smoking_history')
        if 'family' in response_text.lower():
            risk_factors.append('family_history')
        if 'elevated' in response_text.lower() or 'abnormal' in response_text.lower():
            risk_factors.append('abnormal_labs')
        
        return {
            'risk_factors': risk_factors,
            'concerning_findings': [],
            'summary': response_text[:200],
        }
    
    def _mock_clinical_analysis(
        self,
        clinical_notes: str,
        lab_results: Optional[Dict]
    ) -> Dict[str, Any]:
        """Mock clinical analysis for demo"""
        notes_lower = clinical_notes.lower()
        
        risk_factors = []
        if 'smoking' in notes_lower or 'smoker' in notes_lower:
            risk_factors.append('smoking_history')
        if 'family' in notes_lower:
            risk_factors.append('family_history')
        if 'weight loss' in notes_lower:
            risk_factors.append('weight_loss')
        
        return {
            'risk_factors': risk_factors,
            'concerning_findings': [],
            'summary': 'Clinical analysis based on provided notes',
        }
    
    def _calculate_risk_score(
        self,
        age: int,
        gender: str,
        clinical_analysis: Dict,
        lab_results: Optional[Dict],
        imaging_results: Optional[Dict],
        family_history: bool,
        smoking_status: str,
    ) -> float:
        """Calculate overall risk score"""
        score = 0.0
        
        # Age factor
        if age > 65:
            score += 0.3
        elif age > 50:
            score += 0.2
        else:
            score += 0.1
        
        # Smoking
        if smoking_status == 'current':
            score += 0.4
        elif smoking_status == 'former':
            score += 0.2
        
        # Family history
        if family_history:
            score += 0.3
        
        # Clinical findings
        risk_factors = clinical_analysis.get('risk_factors', [])
        score += min(0.3, len(risk_factors) * 0.1)
        
        # Lab results
        if lab_results:
            # Check for elevated tumor markers (mock logic)
            elevated_markers = sum(
                1 for v in lab_results.values()
                if isinstance(v, (int, float)) and v > 100
            )
            score += min(0.2, elevated_markers * 0.1)
        
        # Random variation
        score += random.uniform(-0.05, 0.05)
        
        return max(0.0, min(1.0, score))
    
    def _determine_risk_level(self, risk_score: float) -> tuple:
        """Determine risk level and confidence"""
        if risk_score >= 0.75:
            return 'very_high_risk', min(0.95, risk_score + 0.1)
        elif risk_score >= 0.55:
            return 'high_risk', min(0.90, risk_score + 0.05)
        elif risk_score >= 0.35:
            return 'moderate_risk', min(0.85, risk_score + 0.15)
        else:
            return 'low_risk', min(0.90, 0.8)
    
    def _calculate_all_risk_scores(self, overall_score: float) -> Dict[str, float]:
        """Calculate scores for all risk levels"""
        if overall_score >= 0.75:
            return {
                'low_risk': 0.05,
                'moderate_risk': 0.15,
                'high_risk': 0.30,
                'very_high_risk': 0.50,
            }
        elif overall_score >= 0.55:
            return {
                'low_risk': 0.10,
                'moderate_risk': 0.20,
                'high_risk': 0.60,
                'very_high_risk': 0.10,
            }
        elif overall_score >= 0.35:
            return {
                'low_risk': 0.15,
                'moderate_risk': 0.60,
                'high_risk': 0.20,
                'very_high_risk': 0.05,
            }
        else:
            return {
                'low_risk': 0.70,
                'moderate_risk': 0.20,
                'high_risk': 0.08,
                'very_high_risk': 0.02,
            }
    
    async def _generate_explanation(
        self,
        risk_level: str,
        confidence: float,
        factors: Dict
    ) -> str:
        """Generate human-readable explanation"""
        explanations = {
            'low_risk': f"Based on the assessment, the patient shows a low cancer risk profile (confidence: {confidence:.0%}). Key factors reviewed include age, lifestyle, and clinical findings.",
            'moderate_risk': f"The assessment indicates a moderate cancer risk requiring monitoring (confidence: {confidence:.0%}). Several factors contribute to this assessment including patient history and clinical findings.",
            'high_risk': f"The assessment indicates a high cancer risk requiring prompt evaluation (confidence: {confidence:.0%}). Multiple concerning factors were identified that warrant immediate follow-up.",
            'very_high_risk': f"The assessment indicates a very high cancer risk requiring urgent medical attention (confidence: {confidence:.0%}). Critical factors have been identified requiring immediate oncology consultation.",
        }
        
        return explanations.get(risk_level, "Risk assessment completed.")
    
    def _trace_operation(self, operation_name: str):
        """Context manager for tracing operations"""
        class TraceContext:
            def __init__(self, name, tracer_obj):
                self.name = name
                self.tracer = tracer_obj
                self.span = None
                
            def __enter__(self):
                if TRACING_ENABLED and self.tracer:
                    self.span = self.tracer.trace(self.name)
                return self
            
            def __exit__(self, *args):
                if self.span:
                    self.span.finish()
        
        return TraceContext(operation_name, tracer if TRACING_ENABLED else None)
