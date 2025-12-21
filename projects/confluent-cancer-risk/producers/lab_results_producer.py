"""
Lab Results Producer
Simulates real-time lab results streaming to Kafka
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


class LabResultsProducer:
    """Produces simulated lab results to Kafka"""
    
    def __init__(self):
        self.producer = Producer(KafkaConfig.get_producer_config())
        self.topic = KafkaConfig.TOPIC_LAB_RESULTS
        
    def delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def generate_lab_results(self, patient_id: str) -> dict:
        """Generate synthetic lab results"""
        data = {
            'patient_id': patient_id,
            'lab_id': f'LAB-{random.randint(100000, 999999)}',
            'timestamp': datetime.utcnow().isoformat(),
            'test_type': 'comprehensive_panel',
            'results': {
                # Blood counts
                'wbc_count': random.uniform(4.0, 11.0),  # 10^9/L
                'rbc_count': random.uniform(4.2, 5.9),   # 10^12/L
                'hemoglobin': random.uniform(12.0, 17.0), # g/dL
                'platelet_count': random.uniform(150, 400), # 10^9/L
                
                # Chemistry
                'glucose': random.uniform(70, 140),       # mg/dL
                'creatinine': random.uniform(0.6, 1.2),   # mg/dL
                'alt': random.uniform(7, 56),             # U/L
                'ast': random.uniform(10, 40),            # U/L
                
                # Lipids
                'total_cholesterol': random.uniform(150, 240), # mg/dL
                'hdl': random.uniform(40, 80),            # mg/dL
                'ldl': random.uniform(70, 160),           # mg/dL
                'triglycerides': random.uniform(50, 200), # mg/dL
                
                # Tumor markers
                'cea': random.uniform(0.0, 8.0),          # ng/mL
                'ca_125': random.uniform(0, 50),          # U/mL
                'psa': random.uniform(0.0, 4.0),          # ng/mL (for males)
                'ca_19_9': random.uniform(0, 40),         # U/mL
            },
            'abnormal_flags': [],
            'critical_values': [],
        }
        
        # Flag abnormal values
        if data['results']['cea'] > 5.0:
            data['abnormal_flags'].append('CEA elevated')
        if data['results']['ca_125'] > 35:
            data['abnormal_flags'].append('CA-125 elevated')
        if data['results']['psa'] > 3.0:
            data['abnormal_flags'].append('PSA elevated')
        if data['results']['wbc_count'] > 10.0 or data['results']['wbc_count'] < 4.5:
            data['abnormal_flags'].append('WBC abnormal')
        
        # Flag critical values
        if data['results']['cea'] > 10.0:
            data['critical_values'].append('CEA critically elevated')
        if data['results']['ca_125'] > 100:
            data['critical_values'].append('CA-125 critically elevated')
        
        return data
    
    def produce_message(self, patient_id: str):
        """Produce a single lab results message"""
        data = self.generate_lab_results(patient_id)
        
        self.producer.produce(
            self.topic,
            key=patient_id,
            value=json.dumps(data),
            callback=self.delivery_report
        )
        
        self.producer.poll(0)
    
    def start_streaming(self, num_patients: int = 5, interval_seconds: float = 5.0):
        """Start continuous streaming of lab results"""
        print(f"Starting lab results producer for {num_patients} patients...")
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
    producer = LabResultsProducer()
    producer.start_streaming()
