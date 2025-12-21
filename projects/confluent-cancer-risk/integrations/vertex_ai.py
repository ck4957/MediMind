"""
Vertex AI Integration Module
Handles model deployment and inference with Google Cloud Vertex AI
"""

import json
from typing import Dict, List, Any
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.gcp_config import GCPConfig, MODEL_CONFIG


class VertexAIClient:
    """Client for Vertex AI model inference"""
    
    def __init__(self):
        GCPConfig.initialize_vertex_ai()
        self.endpoint = None
        
    def get_or_create_endpoint(self):
        """Get existing endpoint or create new one"""
        if self.endpoint:
            return self.endpoint
            
        if GCPConfig.VERTEX_AI_ENDPOINT:
            self.endpoint = aiplatform.Endpoint(GCPConfig.VERTEX_AI_ENDPOINT)
        else:
            # For demo purposes, we'll use a mock endpoint
            print("WARNING: No Vertex AI endpoint configured. Using mock predictions.")
            self.endpoint = None
        
        return self.endpoint
    
    def predict_cancer_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make cancer risk prediction
        
        Args:
            features: Dictionary of patient features
            
        Returns:
            Dictionary containing risk prediction and confidence scores
        """
        endpoint = self.get_or_create_endpoint()
        
        if endpoint is None:
            # Return mock prediction for demo
            return self._mock_prediction(features)
        
        # Prepare input for model
        instances = [self._prepare_input(features)]
        
        # Make prediction
        response = endpoint.predict(instances=instances)
        
        # Parse response
        predictions = response.predictions
        return self._parse_prediction(predictions[0])
    
    def _prepare_input(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare features for model input"""
        model_input = {}
        
        for feature_name in MODEL_CONFIG['input_features']:
            if feature_name in features:
                model_input[feature_name] = features[feature_name]
            else:
                # Handle missing features with defaults
                model_input[feature_name] = 0.0
        
        return model_input
    
    def _parse_prediction(self, prediction: Any) -> Dict[str, Any]:
        """Parse model prediction output"""
        if isinstance(prediction, dict):
            risk_scores = prediction.get('risk_scores', [0.1, 0.3, 0.4, 0.2])
        else:
            risk_scores = [0.1, 0.3, 0.4, 0.2]
        
        risk_classes = MODEL_CONFIG['output_classes']
        max_score_idx = risk_scores.index(max(risk_scores))
        
        return {
            'risk_level': risk_classes[max_score_idx],
            'confidence': max(risk_scores),
            'risk_scores': {
                risk_classes[i]: risk_scores[i] 
                for i in range(len(risk_classes))
            },
        }
    
    def _mock_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mock prediction for demo purposes
        Based on simple heuristics from features
        """
        import random
        
        # Calculate mock risk score based on features
        risk_score = 0.0
        
        # Age factor
        age = features.get('age', 50)
        if age > 60:
            risk_score += 0.3
        elif age > 50:
            risk_score += 0.2
        else:
            risk_score += 0.1
        
        # Smoking history
        smoking = features.get('smoking_history', 'never')
        if smoking == 'current':
            risk_score += 0.4
        elif smoking == 'former':
            risk_score += 0.2
        
        # Family history
        if features.get('family_history', False):
            risk_score += 0.3
        
        # Tumor markers
        tumor_markers = features.get('tumor_markers', {})
        if tumor_markers:
            elevated_count = sum(1 for v in tumor_markers.values() if v and v > 5.0)
            risk_score += min(0.3, elevated_count * 0.1)
        
        # Add some randomness
        risk_score += random.uniform(-0.1, 0.1)
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Determine risk level
        if risk_score >= MODEL_CONFIG['threshold_high_risk']:
            risk_level = 'high_risk'
        elif risk_score >= MODEL_CONFIG['threshold_moderate_risk']:
            risk_level = 'moderate_risk'
        else:
            risk_level = 'low_risk'
        
        # Create risk scores for all classes
        risk_scores = {
            'low_risk': max(0.0, 0.4 - risk_score),
            'moderate_risk': 0.3 if risk_level == 'moderate_risk' else 0.2,
            'high_risk': risk_score if risk_level == 'high_risk' else 0.2,
            'very_high_risk': max(0.0, risk_score - 0.7) if risk_score > 0.7 else 0.1,
        }
        
        # Normalize scores
        total = sum(risk_scores.values())
        risk_scores = {k: v/total for k, v in risk_scores.items()}
        
        return {
            'risk_level': risk_level,
            'confidence': max(risk_scores.values()),
            'risk_scores': risk_scores,
            'is_mock': True,
        }


def extract_features_from_streams(
    imaging_data: Dict = None,
    lab_data: Dict = None,
    clinical_notes: Dict = None
) -> Dict[str, Any]:
    """
    Extract and combine features from multiple data streams
    
    Args:
        imaging_data: Imaging stream data
        lab_data: Lab results stream data
        clinical_notes: Clinical notes stream data
        
    Returns:
        Combined feature dictionary for model input
    """
    features = {}
    
    # Extract from clinical notes (demographics)
    if clinical_notes:
        structured = clinical_notes.get('note', {}).get('structured_data', {})
        features['age'] = structured.get('age', 50)
        features['gender'] = 1 if structured.get('gender') == 'M' else 0
        features['smoking_history'] = structured.get('smoking_status', 'never')
        features['family_history'] = structured.get('family_history_cancer', False)
        features['bmi'] = structured.get('bmi', 25.0)
    
    # Extract from lab results
    if lab_data:
        results = lab_data.get('results', {})
        features['glucose_level'] = results.get('glucose', 100)
        features['cholesterol'] = results.get('total_cholesterol', 180)
        features['tumor_markers'] = {
            'cea': results.get('cea', 0),
            'ca_125': results.get('ca_125', 0),
            'psa': results.get('psa', 0),
        }
        # Simple blood pressure mock
        features['blood_pressure'] = 120
    
    # Extract from imaging
    if imaging_data:
        findings = imaging_data.get('findings', {})
        features['imaging_features'] = {
            'nodules': findings.get('nodules_detected', False),
            'masses': findings.get('suspicious_masses', False),
            'calcifications': findings.get('calcifications', False),
        }
    
    return features
