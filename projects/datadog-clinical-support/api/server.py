"""
FastAPI server with Datadog instrumentation
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import time
import uuid
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.datadog_config import DatadogConfig, GCPConfig

# Initialize Datadog tracing if enabled
if DatadogConfig.ENABLE_TRACING:
    try:
        from ddtrace import tracer, patch_all
        patch_all()
        tracer.configure(**DatadogConfig.get_tracer_config())
        print("✓ Datadog tracing enabled")
    except ImportError:
        print("⚠ ddtrace not installed, tracing disabled")

# Initialize StatsD client for metrics
try:
    from datadog import initialize, statsd
    initialize(**DatadogConfig.get_statsd_config())
    print("✓ Datadog metrics enabled")
    METRICS_ENABLED = True
except ImportError:
    print("⚠ datadog not installed, metrics disabled")
    METRICS_ENABLED = False
    statsd = None

# Configure logging
logging.basicConfig(
    level=getattr(logging, DatadogConfig.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import risk assessment module
from risk_assessment import CancerRiskAssessor

# Initialize FastAPI app
app = FastAPI(
    title="Cancer Risk Assessment API",
    description="Clinical decision support with AI and full observability",
    version=DatadogConfig.DD_VERSION,
)

# Initialize risk assessor
risk_assessor = CancerRiskAssessor()


# Request models
class ClinicalQuery(BaseModel):
    """Clinical query for risk assessment"""
    patient_id_hash: str
    age: int
    gender: str
    clinical_notes: str
    lab_results: Optional[Dict[str, Any]] = None
    imaging_results: Optional[Dict[str, Any]] = None
    family_history: Optional[bool] = False
    smoking_status: Optional[str] = "never"


class RiskAssessmentResponse(BaseModel):
    """Risk assessment response"""
    request_id: str
    risk_level: str
    confidence: float
    risk_scores: Dict[str, float]
    explanation: str
    processing_time_ms: float
    timestamp: str


# Middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track all requests with Datadog"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    # Add custom span tags
    if DatadogConfig.ENABLE_TRACING:
        try:
            from ddtrace import tracer
            span = tracer.current_span()
            if span:
                span.set_tag('request_id', request_id)
                span.set_tag('http.url', str(request.url))
        except:
            pass
    
    # Process request
    try:
        response = await call_next(request)
        status_code = response.status_code
        
        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        
        if METRICS_ENABLED:
            statsd.histogram(
                'api.latency',
                latency_ms,
                tags=[
                    f'endpoint:{request.url.path}',
                    f'method:{request.method}',
                    f'status:{status_code}',
                ]
            )
            
            if status_code >= 200 and status_code < 300:
                statsd.increment('api.requests', tags=['status:ok'])
            else:
                statsd.increment('api.requests', tags=['status:error'])
        
        # Log request
        logger.info(
            f"Request completed",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'status_code': status_code,
                'latency_ms': latency_ms,
            }
        )
        
        # Add request ID to response headers
        response.headers['X-Request-ID'] = request_id
        
        return response
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        
        if METRICS_ENABLED:
            statsd.increment('errors', tags=['type:unhandled_exception'])
        
        logger.error(
            f"Request failed: {str(e)}",
            extra={
                'request_id': request_id,
                'error_type': type(e).__name__,
                'error_message': str(e),
                'latency_ms': latency_ms,
            }
        )
        
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": DatadogConfig.DD_SERVICE,
        "version": DatadogConfig.DD_VERSION,
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": DatadogConfig.DD_SERVICE,
        "version": DatadogConfig.DD_VERSION,
        "env": DatadogConfig.DD_ENV,
        "tracing_enabled": DatadogConfig.ENABLE_TRACING,
        "metrics_enabled": METRICS_ENABLED,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/assess-risk", response_model=RiskAssessmentResponse)
async def assess_cancer_risk(query: ClinicalQuery, request: Request):
    """
    Assess cancer risk based on clinical data
    
    This endpoint uses AI models (Gemini and Vertex AI) to analyze clinical data
    and provide a risk assessment with full observability through Datadog.
    """
    start_time = time.time()
    request_id = request.state.request_id
    
    logger.info(
        "Starting risk assessment",
        extra={
            'request_id': request_id,
            'patient_id_hash': query.patient_id_hash,
            'operation': 'risk_assessment',
        }
    )
    
    try:
        # Perform risk assessment (traced automatically by ddtrace)
        result = await risk_assessor.assess_risk(
            age=query.age,
            gender=query.gender,
            clinical_notes=query.clinical_notes,
            lab_results=query.lab_results,
            imaging_results=query.imaging_results,
            family_history=query.family_history,
            smoking_status=query.smoking_status,
        )
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Record metrics
        if METRICS_ENABLED:
            statsd.histogram('prediction.confidence', result['confidence'])
            statsd.increment(
                'predictions.total',
                tags=[f'risk_level:{result["risk_level"]}']
            )
            statsd.histogram('prediction.latency', processing_time_ms)
            
            # Track if this is a high-risk low-confidence case
            if result['risk_level'] in ['high_risk', 'very_high_risk'] and result['confidence'] < 0.7:
                statsd.increment('predictions.low_confidence_high_risk')
        
        # Log result
        logger.info(
            "Risk assessment completed",
            extra={
                'request_id': request_id,
                'patient_id_hash': query.patient_id_hash,
                'risk_level': result['risk_level'],
                'confidence': result['confidence'],
                'latency_ms': processing_time_ms,
                'operation': 'risk_assessment',
            }
        )
        
        return RiskAssessmentResponse(
            request_id=request_id,
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            risk_scores=result['risk_scores'],
            explanation=result['explanation'],
            processing_time_ms=processing_time_ms,
            timestamp=datetime.utcnow().isoformat(),
        )
        
    except Exception as e:
        processing_time_ms = (time.time() - start_time) * 1000
        
        if METRICS_ENABLED:
            statsd.increment('errors', tags=[f'type:{type(e).__name__}'])
        
        logger.error(
            f"Risk assessment failed: {str(e)}",
            extra={
                'request_id': request_id,
                'patient_id_hash': query.patient_id_hash,
                'error_type': type(e).__name__,
                'error_message': str(e),
                'latency_ms': processing_time_ms,
                'operation': 'risk_assessment',
            }
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Risk assessment failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('API_PORT', 8000))
    
    print(f"Starting Cancer Risk Assessment API on port {port}")
    print(f"Service: {DatadogConfig.DD_SERVICE}")
    print(f"Environment: {DatadogConfig.DD_ENV}")
    print(f"Version: {DatadogConfig.DD_VERSION}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level=DatadogConfig.LOG_LEVEL.lower()
    )
