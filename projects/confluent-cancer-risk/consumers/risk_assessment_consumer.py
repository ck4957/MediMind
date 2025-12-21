"""
Risk Assessment Consumer
Consumes clinical data streams and performs real-time cancer risk assessment
"""

import json
import time
from typing import Dict, Any
from confluent_kafka import Consumer, Producer, KafkaError
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig
from integrations.vertex_ai import VertexAIClient, extract_features_from_streams
from integrations.gemini import GeminiClient


class RiskAssessmentConsumer:
    """
    Consumes clinical data streams and performs risk assessment
    """
    
    def __init__(self):
        # Initialize consumers for different topics
        self.consumer = Consumer(KafkaConfig.get_consumer_config('risk-assessment-group'))
        
        # Initialize producer for predictions
        self.producer = Producer(KafkaConfig.get_producer_config())
        
        # Initialize AI clients
        self.vertex_client = VertexAIClient()
        self.gemini_client = GeminiClient()
        
        # Patient data buffer (stores recent data for each patient)
        self.patient_data_buffer = {}
        
        # Subscribe to all clinical data topics
        self.consumer.subscribe([
            KafkaConfig.TOPIC_IMAGING,
            KafkaConfig.TOPIC_LAB_RESULTS,
            KafkaConfig.TOPIC_CLINICAL_NOTES,
        ])
        
        print("Risk Assessment Consumer initialized")
        print(f"Subscribed to topics: {[KafkaConfig.TOPIC_IMAGING, KafkaConfig.TOPIC_LAB_RESULTS, KafkaConfig.TOPIC_CLINICAL_NOTES]}")
    
    def process_message(self, msg):
        """Process a single message from Kafka"""
        try:
            topic = msg.topic()
            patient_id = msg.key().decode('utf-8')
            data = json.loads(msg.value().decode('utf-8'))
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received from {topic}")
            print(f"Patient ID: {patient_id}")
            
            # Initialize patient buffer if needed
            if patient_id not in self.patient_data_buffer:
                self.patient_data_buffer[patient_id] = {
                    'imaging': None,
                    'lab_results': None,
                    'clinical_notes': None,
                    'last_updated': None,
                }
            
            # Store data in buffer
            if topic == KafkaConfig.TOPIC_IMAGING:
                self.patient_data_buffer[patient_id]['imaging'] = data
                print(f"  Imaging: {data.get('imaging_type')} - {data.get('urgency')}")
            elif topic == KafkaConfig.TOPIC_LAB_RESULTS:
                self.patient_data_buffer[patient_id]['lab_results'] = data
                abnormal = data.get('abnormal_flags', [])
                print(f"  Lab Results: {len(abnormal)} abnormal flags")
            elif topic == KafkaConfig.TOPIC_CLINICAL_NOTES:
                self.patient_data_buffer[patient_id]['clinical_notes'] = data
                print(f"  Clinical Note: {data.get('encounter_type')}")
            
            self.patient_data_buffer[patient_id]['last_updated'] = datetime.now()
            
            # Perform risk assessment if we have sufficient data
            if self._has_sufficient_data(patient_id):
                self.perform_risk_assessment(patient_id)
            else:
                print("  Waiting for more data before assessment...")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            import traceback
            traceback.print_exc()
    
    def _has_sufficient_data(self, patient_id: str) -> bool:
        """Check if we have sufficient data for risk assessment"""
        buffer = self.patient_data_buffer[patient_id]
        # Need at least clinical notes or (lab results + imaging)
        return (
            buffer['clinical_notes'] is not None or
            (buffer['lab_results'] is not None and buffer['imaging'] is not None)
        )
    
    def perform_risk_assessment(self, patient_id: str):
        """Perform complete risk assessment for a patient"""
        print(f"\n{'='*60}")
        print(f"PERFORMING RISK ASSESSMENT FOR {patient_id}")
        print('='*60)
        
        buffer = self.patient_data_buffer[patient_id]
        
        # Step 1: Extract features from streams
        print("\n[1/4] Extracting features from data streams...")
        features = extract_features_from_streams(
            imaging_data=buffer['imaging'],
            lab_data=buffer['lab_results'],
            clinical_notes=buffer['clinical_notes']
        )
        print(f"  Extracted {len(features)} features")
        
        # Step 2: Analyze clinical notes with Gemini
        print("\n[2/4] Analyzing clinical notes with Gemini...")
        clinical_analysis = None
        if buffer['clinical_notes']:
            note_content = buffer['clinical_notes'].get('note', {})
            clinical_analysis = self.gemini_client.analyze_clinical_notes(
                clinical_note=note_content,
                lab_results=buffer['lab_results']
            )
            print(f"  Risk factors: {clinical_analysis.get('risk_factors', [])}")
            print(f"  Concerning findings: {clinical_analysis.get('concerning_findings', [])}")
        
        # Step 3: Get prediction from Vertex AI
        print("\n[3/4] Getting prediction from Vertex AI...")
        prediction = self.vertex_client.predict_cancer_risk(features)
        print(f"  Risk Level: {prediction['risk_level']}")
        print(f"  Confidence: {prediction['confidence']:.2%}")
        
        # Step 4: Generate explanation with Gemini
        print("\n[4/4] Generating explanation...")
        patient_summary = self._create_patient_summary(buffer, features)
        explanation = self.gemini_client.explain_prediction(
            patient_summary=patient_summary,
            risk_level=prediction['risk_level'],
            confidence=prediction['confidence'],
            factors=clinical_analysis.get('risk_factors', []) if clinical_analysis else []
        )
        
        # Prepare final prediction message
        prediction_message = {
            'patient_id': patient_id,
            'timestamp': datetime.utcnow().isoformat(),
            'risk_assessment': {
                'risk_level': prediction['risk_level'],
                'confidence': prediction['confidence'],
                'risk_scores': prediction['risk_scores'],
            },
            'clinical_analysis': clinical_analysis,
            'explanation': explanation,
            'data_sources': {
                'has_imaging': buffer['imaging'] is not None,
                'has_lab_results': buffer['lab_results'] is not None,
                'has_clinical_notes': buffer['clinical_notes'] is not None,
            }
        }
        
        # Publish to predictions stream
        self.publish_prediction(patient_id, prediction_message)
        
        # Check if alert needed
        if self._should_alert(prediction):
            self.publish_alert(patient_id, prediction_message)
        
        print(f"\n{'='*60}")
        print("ASSESSMENT COMPLETE")
        print('='*60)
    
    def _create_patient_summary(self, buffer: Dict, features: Dict) -> str:
        """Create a summary of patient data"""
        summary_parts = []
        
        if features.get('age'):
            summary_parts.append(f"Age: {features['age']}")
        if features.get('gender') is not None:
            gender = 'Male' if features['gender'] == 1 else 'Female'
            summary_parts.append(f"Gender: {gender}")
        if features.get('smoking_history'):
            summary_parts.append(f"Smoking: {features['smoking_history']}")
        if features.get('family_history'):
            summary_parts.append("Family history of cancer: Yes")
        
        return "; ".join(summary_parts)
    
    def _should_alert(self, prediction: Dict) -> bool:
        """Determine if an alert should be sent"""
        risk_level = prediction.get('risk_level', '')
        confidence = prediction.get('confidence', 0)
        
        return (risk_level in ['high_risk', 'very_high_risk'] and confidence > 0.6)
    
    def publish_prediction(self, patient_id: str, prediction: Dict):
        """Publish prediction to predictions stream"""
        try:
            self.producer.produce(
                KafkaConfig.TOPIC_PREDICTIONS,
                key=patient_id,
                value=json.dumps(prediction),
                callback=self.delivery_report
            )
            self.producer.poll(0)
        except Exception as e:
            print(f"Error publishing prediction: {e}")
    
    def publish_alert(self, patient_id: str, prediction: Dict):
        """Publish high-risk alert"""
        try:
            alert = {
                'patient_id': patient_id,
                'timestamp': datetime.utcnow().isoformat(),
                'alert_type': 'high_risk_cancer',
                'risk_level': prediction['risk_assessment']['risk_level'],
                'confidence': prediction['risk_assessment']['confidence'],
                'message': f"High risk cancer assessment for patient {patient_id}",
            }
            
            self.producer.produce(
                KafkaConfig.TOPIC_ALERTS,
                key=patient_id,
                value=json.dumps(alert),
                callback=self.delivery_report
            )
            self.producer.poll(0)
            
            print(f"\n🚨 ALERT SENT for {patient_id}")
            
        except Exception as e:
            print(f"Error publishing alert: {e}")
    
    def delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()}')
    
    def run(self):
        """Main consumer loop"""
        print("\nStarting Risk Assessment Consumer...")
        print("Waiting for messages...\n")
        
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f'Error: {msg.error()}')
                        continue
                
                self.process_message(msg)
                
        except KeyboardInterrupt:
            print("\nShutting down consumer...")
        finally:
            self.consumer.close()
            self.producer.flush()


if __name__ == '__main__':
    consumer = RiskAssessmentConsumer()
    consumer.run()
