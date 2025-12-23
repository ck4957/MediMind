"""
Kafka Configuration Module
Manages Confluent Kafka connection settings and topic configurations
"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class KafkaConfig:
    """Kafka configuration settings"""
    
    # Confluent Cloud connection
    BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS', 'localhost:9092')
    API_KEY = os.getenv('CONFLUENT_API_KEY')
    API_SECRET = os.getenv('CONFLUENT_API_SECRET')
    
    # Schema Registry
    SCHEMA_REGISTRY_URL = os.getenv('CONFLUENT_SCHEMA_REGISTRY_URL')
    SCHEMA_REGISTRY_API_KEY = os.getenv('CONFLUENT_SCHEMA_REGISTRY_API_KEY')
    SCHEMA_REGISTRY_API_SECRET = os.getenv('CONFLUENT_SCHEMA_REGISTRY_API_SECRET')
    
    # Topics
    TOPIC_IMAGING = os.getenv('TOPIC_IMAGING', 'clinical-imaging-stream')
    TOPIC_LAB_RESULTS = os.getenv('TOPIC_LAB_RESULTS', 'lab-results-stream')
    TOPIC_CLINICAL_NOTES = os.getenv('TOPIC_CLINICAL_NOTES', 'clinical-notes-stream')
    TOPIC_PREDICTIONS = os.getenv('TOPIC_PREDICTIONS', 'risk-predictions-stream')
    TOPIC_ALERTS = os.getenv('TOPIC_ALERTS', 'alerts-stream')
    TOPIC_PATIENT_PROFILES = os.getenv('TOPIC_PATIENT_PROFILES', 'patient-profiles-stream')
    
    @classmethod
    def get_producer_config(cls) -> Dict[str, str]:
        """Get Kafka producer configuration"""
        config = {
            'bootstrap.servers': cls.BOOTSTRAP_SERVERS,
        }
        
        # Add authentication for Confluent Cloud
        if cls.API_KEY and cls.API_SECRET:
            config.update({
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': cls.API_KEY,
                'sasl.password': cls.API_SECRET,
            })
        
        return config
    
    @classmethod
    def get_consumer_config(cls, group_id: str) -> Dict[str, str]:
        """Get Kafka consumer configuration"""
        config = {
            'bootstrap.servers': cls.BOOTSTRAP_SERVERS,
            'group.id': group_id,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True,
        }
        
        # Add authentication for Confluent Cloud
        if cls.API_KEY and cls.API_SECRET:
            config.update({
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': cls.API_KEY,
                'sasl.password': cls.API_SECRET,
            })
        
        return config
    
    @classmethod
    def get_schema_registry_config(cls) -> Dict[str, str]:
        """Get Schema Registry configuration"""
        if not cls.SCHEMA_REGISTRY_URL:
            return {}
        
        config = {
            'url': cls.SCHEMA_REGISTRY_URL,
        }
        
        if cls.SCHEMA_REGISTRY_API_KEY and cls.SCHEMA_REGISTRY_API_SECRET:
            config['basic.auth.user.info'] = f"{cls.SCHEMA_REGISTRY_API_KEY}:{cls.SCHEMA_REGISTRY_API_SECRET}"
        
        return config


# Topic configurations
TOPIC_CONFIGS = {
    'clinical-imaging-stream': {
        'num_partitions': 3,
        'replication_factor': 3,
        'config': {
            'retention.ms': '604800000',  # 7 days
            'compression.type': 'snappy',
        }
    },
    'lab-results-stream': {
        'num_partitions': 3,
        'replication_factor': 3,
        'config': {
            'retention.ms': '604800000',
            'compression.type': 'snappy',
        }
    },
    'clinical-notes-stream': {
        'num_partitions': 3,
        'replication_factor': 3,
        'config': {
            'retention.ms': '604800000',
            'compression.type': 'gzip',
        }
    },
    'risk-predictions-stream': {
        'num_partitions': 3,
        'replication_factor': 3,
        'config': {
            'retention.ms': '2592000000',  # 30 days
            'compression.type': 'snappy',
        }
    },
    'alerts-stream': {
        'num_partitions': 2,
        'replication_factor': 3,
        'config': {
            'retention.ms': '2592000000',
            'compression.type': 'snappy',
        }
    },
    'patient-profiles-stream': {
        'num_partitions': 3,
        'replication_factor': 3,
        'config': {
            'retention.ms': '2592000000',
            'compression.type': 'snappy',
        }
    },
}
