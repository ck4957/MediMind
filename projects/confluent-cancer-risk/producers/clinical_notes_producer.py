"""
Clinical Notes Producer
Simulates real-time clinical notes streaming to Kafka
"""

import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig


class ClinicalNotesProducer:
    """Produces simulated clinical notes to Kafka"""
    
    def __init__(self):
        self.producer = Producer(KafkaConfig.get_producer_config())
        self.topic = KafkaConfig.TOPIC_CLINICAL_NOTES
        
    def delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def generate_clinical_note(self, patient_id: str) -> dict:
        """Generate synthetic clinical note"""
        note_templates = [
            {
                'chief_complaint': 'Routine cancer screening',
                'history': 'Patient presents for routine annual screening. No new symptoms. Family history of breast cancer (mother diagnosed at age 52). Non-smoker. Exercises regularly.',
                'physical_exam': 'Vital signs stable. No palpable masses. No lymphadenopathy.',
                'assessment': 'Low-moderate risk based on family history. Continue routine surveillance.',
                'plan': 'Schedule mammography. Return in 12 months for follow-up.',
            },
            {
                'chief_complaint': 'Persistent cough and weight loss',
                'history': '55-year-old with 30 pack-year smoking history presents with persistent cough for 3 months and unintentional 15 lb weight loss. Denies fever or hemoptysis.',
                'physical_exam': 'Decreased breath sounds in right upper lobe. Weight 165 lbs (down from 180 lbs).',
                'assessment': 'Concerning for possible lung malignancy given smoking history and symptoms.',
                'plan': 'Order chest CT with contrast. Refer to pulmonology. Consider bronchoscopy.',
            },
            {
                'chief_complaint': 'Abdominal pain and bloating',
                'history': 'Patient reports increasing abdominal discomfort and bloating over past 2 months. Some early satiety. No family history of cancer.',
                'physical_exam': 'Abdomen distended. Mild tenderness in lower quadrants. No rebound.',
                'assessment': 'Differential includes ovarian pathology vs GI issues.',
                'plan': 'Order pelvic ultrasound and CA-125. Follow up in 2 weeks with results.',
            },
            {
                'chief_complaint': 'Follow-up post suspicious imaging',
                'history': 'Patient returns for discussion of recent CT findings showing 2.5cm lung nodule. Mild smoking history. No respiratory symptoms.',
                'physical_exam': 'General condition good. No acute distress.',
                'assessment': 'Lung nodule requiring further workup. PET scan ordered.',
                'plan': 'Schedule PET/CT. Refer to thoracic surgery for consultation. Discuss smoking cessation.',
            },
            {
                'chief_complaint': 'Elevated PSA follow-up',
                'history': 'Patient with PSA of 6.2 on recent screening. No urinary symptoms. Father had prostate cancer at age 68.',
                'physical_exam': 'DRE reveals slightly enlarged prostate, no nodules.',
                'assessment': 'Elevated PSA with family history warrants further investigation.',
                'plan': 'Refer to urology for possible biopsy. Repeat PSA in 6 weeks.',
            },
        ]
        
        selected_note = random.choice(note_templates)
        
        data = {
            'patient_id': patient_id,
            'note_id': f'NOTE-{random.randint(100000, 999999)}',
            'timestamp': datetime.utcnow().isoformat(),
            'encounter_type': random.choice(['outpatient', 'consultation', 'follow-up']),
            'provider_id': f'PROV-{random.randint(100, 999)}',
            'note': selected_note,
            'structured_data': {
                'age': random.randint(35, 75),
                'gender': random.choice(['M', 'F']),
                'smoking_status': random.choice(['never', 'former', 'current']),
                'bmi': round(random.uniform(18.5, 35.0), 1),
                'family_history_cancer': random.choice([True, False]),
            },
        }
        
        return data
    
    def produce_message(self, patient_id: str):
        """Produce a single clinical note message"""
        data = self.generate_clinical_note(patient_id)
        
        self.producer.produce(
            self.topic,
            key=patient_id,
            value=json.dumps(data),
            callback=self.delivery_report
        )
        
        self.producer.poll(0)
    
    def start_streaming(self, num_patients: int = 5, interval_seconds: float = 10.0):
        """Start continuous streaming of clinical notes"""
        print(f"Starting clinical notes producer for {num_patients} patients...")
        print(f"Topic: {self.topic}")
        print(f"Interval: {interval_seconds}s")
        print("-" * 50)
        
        patient_ids = [f"PT-{str(i).zfill(5)}" for i in range(1000, 1000 + num_patients)]
        
        try:
            while True:
                patient_id = random.choice(patient_ids)
                self.produce_message(patient_id)
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\nShutting down producer...")
        finally:
            self.producer.flush()


if __name__ == '__main__':
    producer = ClinicalNotesProducer()
    producer.start_streaming()
