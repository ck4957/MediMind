"""
Imaging Data Producer
Simulates real-time clinical imaging metadata streaming to Kafka
"""

import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig


class ImagingProducer:
    """Produces simulated imaging data to Kafka"""
    
    def __init__(self):
        self.producer = Producer(KafkaConfig.get_producer_config())
        self.topic = KafkaConfig.TOPIC_IMAGING
        
    def delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def generate_imaging_data(self, patient_id: str) -> dict:
        """Generate synthetic imaging metadata"""
        imaging_types = ['CT', 'MRI', 'PET', 'Mammography', 'Ultrasound']
        body_parts = ['chest', 'abdomen', 'pelvis', 'brain', 'breast']
        
        data = {
            'patient_id': patient_id,
            'imaging_id': f'IMG-{random.randint(100000, 999999)}',
            'timestamp': datetime.utcnow().isoformat(),
            'imaging_type': random.choice(imaging_types),
            'body_part': random.choice(body_parts),
            'findings': {
                'nodules_detected': random.choice([True, False]),
                'nodule_size_mm': random.uniform(2.0, 25.0) if random.random() > 0.5 else None,
                'suspicious_masses': random.choice([True, False]),
                'calcifications': random.choice([True, False]),
                'lymph_node_enlargement': random.choice([True, False]),
            },
            'radiologist_notes': self._generate_radiologist_notes(),
            'urgency': random.choice(['routine', 'urgent', 'critical']),
            'quality_score': random.uniform(0.8, 1.0),
        }
        
        return data
    
    def _generate_radiologist_notes(self) -> str:
        """Generate synthetic radiologist notes"""
        notes = [
            "No significant abnormalities detected. Follow-up recommended in 12 months.",
            "Small nodule observed in upper lobe. Recommend follow-up CT in 3 months.",
            "Multiple calcifications noted. Benign appearance. Routine follow-up.",
            "Suspicious mass detected. Recommend biopsy for further evaluation.",
            "Enlarged lymph nodes observed. Clinical correlation recommended.",
            "Ground-glass opacities present. Cannot rule out early malignancy.",
        ]
        return random.choice(notes)
    
    def produce_message(self, patient_id: str):
        """Produce a single imaging message"""
        data = self.generate_imaging_data(patient_id)
        
        self.producer.produce(
            self.topic,
            key=patient_id,
            value=json.dumps(data),
            callback=self.delivery_report
        )
        
        self.producer.poll(0)
    
    def start_streaming(self, num_patients: int = 5, interval_seconds: float = 3.0):
        """Start continuous streaming of imaging data"""
        print(f"Starting imaging data producer for {num_patients} patients...")
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
            # Wait for any outstanding messages to be delivered
            self.producer.flush()


if __name__ == '__main__':
    producer = ImagingProducer()
    producer.start_streaming()
