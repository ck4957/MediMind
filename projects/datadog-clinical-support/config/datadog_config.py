"""
Datadog Configuration Module
"""

import os
from dotenv import load_dotenv

load_dotenv()


class DatadogConfig:
    """Datadog configuration settings"""
    
    # Datadog credentials
    DD_API_KEY = os.getenv('DD_API_KEY')
    DD_APP_KEY = os.getenv('DD_APP_KEY')
    DD_SITE = os.getenv('DD_SITE', 'datadoghq.com')
    
    # Service configuration
    DD_SERVICE = os.getenv('DD_SERVICE', 'cancer-risk-assessment')
    DD_ENV = os.getenv('DD_ENV', 'development')
    DD_VERSION = os.getenv('DD_VERSION', '1.0.0')
    
    # Tracing configuration
    ENABLE_TRACING = os.getenv('ENABLE_TRACING', 'true').lower() == 'true'
    TRACE_SAMPLE_RATE = float(os.getenv('TRACE_SAMPLE_RATE', '1.0'))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_tracer_config(cls) -> dict:
        """Get tracer configuration"""
        return {
            'service': cls.DD_SERVICE,
            'env': cls.DD_ENV,
            'version': cls.DD_VERSION,
        }
    
    @classmethod
    def get_statsd_config(cls) -> dict:
        """Get StatsD configuration for metrics"""
        return {
            'host': 'localhost',
            'port': 8125,
            'namespace': 'cancer_risk',
            'constant_tags': [
                f'service:{cls.DD_SERVICE}',
                f'env:{cls.DD_ENV}',
                f'version:{cls.DD_VERSION}',
            ]
        }


class GCPConfig:
    """Google Cloud Platform configuration"""
    
    PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    REGION = os.getenv('GCP_REGION', 'us-central1')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    VERTEX_AI_ENDPOINT = os.getenv('VERTEX_AI_ENDPOINT')


# Metrics configuration
METRICS_CONFIG = {
    'prediction_confidence': {
        'name': 'prediction.confidence',
        'type': 'histogram',
        'description': 'Model prediction confidence score',
    },
    'prediction_count': {
        'name': 'predictions.total',
        'type': 'counter',
        'description': 'Total number of predictions made',
    },
    'api_latency': {
        'name': 'api.latency',
        'type': 'histogram',
        'description': 'API endpoint latency in milliseconds',
    },
    'gemini_tokens': {
        'name': 'gemini.tokens_used',
        'type': 'gauge',
        'description': 'Number of tokens used in Gemini API call',
    },
    'vertex_latency': {
        'name': 'vertex_ai.latency',
        'type': 'histogram',
        'description': 'Vertex AI inference latency',
    },
    'errors': {
        'name': 'errors',
        'type': 'counter',
        'description': 'Error count by type',
    },
}


# Log attributes
LOG_ATTRIBUTES = {
    'required': [
        'timestamp',
        'service',
        'level',
        'request_id',
        'operation',
    ],
    'optional': [
        'patient_id_hash',
        'model',
        'latency_ms',
        'confidence',
        'risk_level',
        'tokens_used',
        'error_type',
        'error_message',
    ]
}
