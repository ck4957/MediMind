"""
Patient Profile Producer
Streams baseline patient demographics and risk factors based on Lung Cancer Risk Dataset schema
"""

import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig


class PatientProfileProducer:
    """Produces simulated patient profile/risk factor data to Kafka"""
    
    def __init__(self):
        self.producer = Producer(KafkaConfig.get_producer_config())
        self.topic = KafkaConfig.TOPIC_PATIENT_PROFILES
        
    def delivery_report(self, err, msg):
        """Callback for message delivery reports"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def generate_patient_profile(self, patient_id: str) -> dict:
        """Generate synthetic patient profile matching Lung Cancer Risk dataset features"""
        
        # Risk factors distribution simulation
        age = random.randint(30, 85)
        gender = random.choice(['MALE', 'FEMALE'])
        
        # Smoking probability increases with age
        smoking_prob = 0.2 + (0.4 * (age - 30) / 55)
        is_smoker = random.random() < smoking_prob
        
        if is_smoker:
            smoking_history = random.choice(['CURRENT', 'FORMER'])
            packs_per_day = random.uniform(0.5, 2.5)
            years_smoked = random.randint(5, age - 15)
            pack_years = round(packs_per_day * years_smoked, 1)
        else:
            smoking_history = 'NEVER'
            pack_years = 0.0
            
        data = {
            'patient_id': patient_id,
            'timestamp': datetime.utcnow().isoformat(),
            'demographics': {
                'age': age,
                'gender': gender,
                'occupational_hazards': random.choice([0, 1]) if random.random() > 0.8 else 0,
                'genetic_risk': random.choice([0, 1, 2]) # 0=Low, 1=Med, 2=High
            },
            'lifestyle_factors': {
                'smoking_history': smoking_history,
                'pack_years': pack_years,
                'alcohol_use': random.uniform(0, 10), # scale 0-10
                'obesity': random.choice([True, False]) if random.random() > 0.7 else False,
                'active_smoker': smoking_history == 'CURRENT',
                'passive_smoker': random.choice([True, False]) if random.random() > 0.8 else False
            },
            'clinical_history': {
                'chronic_lung_disease': random.choice([True, False]) if random.random() > 0.85 else False,
                'balanced_diet': random.choice([True, False]),
                'air_pollution_exposure': random.uniform(0, 10), # scale 0-10
                'dust_allergy': random.choice([True, False]) if random.random() > 0.7 else False
            },
            'symptoms': {
                'coughing_of_blood': random.choice([True, False]) if (is_smoker and age > 50) else False,
                'fatigue': random.uniform(0, 10),
                'weight_loss': random.choice([True, False]) if (is_smoker and age > 50) else False,
                'shortness_of_breath': random.uniform(0, 10),
                'wheezing': random.uniform(0, 10),
                'swallowing_difficulty': random.uniform(0, 10),
                'clubbing_of_finger_nails': random.uniform(0, 10),
                'frequent_cold': random.choice([True, False]),
                'dry_cough': random.choice([True, False]),
                'snoring': random.choice([True, False])
            }
        }
        
        return data
    
    def produce_message(self, patient_id: str):
        """Produce a single patient profile message"""
        data = self.generate_patient_profile(patient_id)
        
        self.producer.produce(
            self.topic,
            key=patient_id,
            value=json.dumps(data),
            callback=self.delivery_report
        )
        
        self.producer.poll(0)
    
    def start_streaming(self, num_patients: int = 5, interval_seconds: float = 2.0):
        """Start continuous streaming of patient profiles"""
        print(f"Starting patient profile producer for {num_patients} patients...")
        print(f"Topic: {self.topic}")
        print(f"Interval: {interval_seconds}s")
        print("-" * 50)
        
        patient_ids = [f"PT-{str(i).zfill(5)}" for i in range(1000, 1000 + num_patients)]
        
        try:
            while True:
                # Select a random patient to update (in this context, maybe re-evaluating risk or correcting info)
                # Or just generating profiles for new patients
                patient_id = random.choice(patient_ids)
                self.produce_message(patient_id)
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\nShutting down producer...")
        finally:
            self.producer.flush()


if __name__ == '__main__':
    producer = PatientProfileProducer()
    producer.start_streaming()
