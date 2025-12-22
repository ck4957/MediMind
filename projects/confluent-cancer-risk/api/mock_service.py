import asyncio
import json
import logging
import random
from datetime import datetime
import sys
import os

# Import producers logic to reuse generation code if possible
# Or simplified versions for mock service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from producers.patient_profile_producer import PatientProfileProducer
from producers.imaging_producer import ImagingProducer
from producers.lab_results_producer import LabResultsProducer
from producers.clinical_notes_producer import ClinicalNotesProducer
from config.kafka_config import KafkaConfig

logger = logging.getLogger("mock_service")

class MockDataService:
    def __init__(self):
        self.running = False
        self.patient_profile_gen = PatientProfileProducer()
        self.imaging_gen = ImagingProducer()
        self.lab_gen = LabResultsProducer()
        self.notes_gen = ClinicalNotesProducer()

    async def start(self, message_callback):
        self.running = True
        logger.info("Starting Mock Data Service...")
        
        # Simulate a pool of patients
        patient_ids = [f"PT-{str(i).zfill(5)}" for i in range(1000, 1005)]
        
        while self.running:
            try:
                # Randomly pick a data type to generate
                msg_type = random.choice(['profile', 'imaging', 'lab', 'note'])
                patient_id = random.choice(patient_ids)
                
                payload = {}
                
                if msg_type == 'profile':
                    data = self.patient_profile_gen.generate_patient_profile(patient_id)
                    topic = getattr(KafkaConfig, 'TOPIC_PATIENT_PROFILES', 'patient-profiles-stream')
                elif msg_type == 'imaging':
                    data = self.imaging_gen.generate_imaging_data(patient_id)
                    topic = KafkaConfig.TOPIC_IMAGING
                elif msg_type == 'lab':
                    data = self.lab_gen.generate_lab_results(patient_id)
                    topic = KafkaConfig.TOPIC_LAB_RESULTS
                else:
                    data = self.notes_gen.generate_clinical_note(patient_id)
                    topic = KafkaConfig.TOPIC_CLINICAL_NOTES
                
                payload = json.dumps({
                    "type": topic,
                    "data": data
                })
                
                await message_callback(payload)
                
                # Random delay between 2-5 seconds
                await asyncio.sleep(random.uniform(2.0, 5.0))
                
            except Exception as e:
                logger.error(f"Error in mock generation: {e}")
                await asyncio.sleep(1.0)

    async def stop(self):
        self.running = False
