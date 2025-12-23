# Datadog Challenge: LLM-Powered Clinical Decision Support with Full Observability

## Overview

This project demonstrates a clinical decision support system powered by LLMs (Gemini/Vertex AI) with comprehensive observability using Datadog. The system monitors AI model performance, tracks API latency, detects anomalies, and ensures security in healthcare AI applications.

## Architecture

```
Clinical Query → Gemini/Vertex AI → Risk Assessment → 
Datadog Monitoring → Alerts & Incidents
```

## Key Features

### Monitoring Capabilities

1. **Application Performance Monitoring (APM)**
   - Trace Gemini API calls end-to-end
   - Monitor Vertex AI inference latency
   - Track request-response times
   - Identify bottlenecks in the pipeline

2. **Logs Management**
   - Capture model inputs/outputs (de-identified)
   - Track error patterns
   - Audit trail for compliance
   - Search and filter clinical queries

3. **Custom Metrics**
   - Prediction accuracy over time
   - Model confidence scores
   - Risk level distribution
   - API rate limiting events
   - Token usage tracking

4. **Security Monitoring**
   - Detect anomalous queries
   - Monitor for PHI exposure attempts
   - Track authentication failures
   - Alert on suspicious patterns

5. **Synthetic Monitoring**
   - Test clinical scenarios regularly
   - Validate response accuracy
   - Monitor endpoint availability
   - Track SLA compliance

## Prerequisites

- Datadog account (free trial available)
- Datadog API key and Application key
- Google Cloud Platform project
- Python 3.9+
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Datadog Setup

```bash
# Sign up for Datadog (14-day trial)
# Go to https://www.datadoghq.com/

# Get your API and App keys from:
# https://app.datadoghq.com/organization-settings/api-keys

# Install Datadog Agent (for local development)
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

### 2. Environment Configuration

Create `.env` file:

```env
# Datadog Configuration
DD_API_KEY=your-datadog-api-key
DD_APP_KEY=your-datadog-app-key
DD_SITE=datadoghq.com
DD_SERVICE=cancer-risk-assessment
DD_ENV=production
DD_VERSION=1.0.0

# Google Cloud Configuration
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
GEMINI_API_KEY=your-gemini-api-key
VERTEX_AI_ENDPOINT=your-vertex-ai-endpoint

# Application Configuration
API_PORT=8000
LOG_LEVEL=INFO
ENABLE_TRACING=true
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Datadog Monitors

```bash
# Create detection rules and monitors
python scripts/setup_monitors.py

# Create dashboard
python scripts/create_dashboard.py
```

### 5. Run the Application

```bash
# Start the API server with Datadog tracing
python api/server.py
```

### 6. Generate Test Traffic

```bash
# Generate synthetic clinical queries
python scripts/generate_test_traffic.py
```

## Project Structure

```
datadog-clinical-support/
├── README.md
├── requirements.txt
├── config/
│   ├── datadog_config.py
│   └── monitor_definitions.py
├── api/
│   ├── server.py
│   ├── risk_assessment.py
│   └── middleware.py
├── monitors/
│   ├── high_latency.json
│   ├── low_confidence.json
│   ├── api_errors.json
│   └── security_anomalies.json
├── dashboards/
│   └── clinical_ai_dashboard.json
└── scripts/
    ├── setup_monitors.py
    ├── create_dashboard.py
    └── generate_test_traffic.py
```

## Datadog Integration Points

### APM Traces

The application uses `ddtrace` to automatically instrument:
- FastAPI endpoints
- HTTP requests to Gemini/Vertex AI
- Database queries (if applicable)
- Custom service calls

Example trace spans:
- `cancer_risk_assessment` - Main assessment operation
- `gemini.analyze_clinical_data` - Gemini API call
- `vertex_ai.predict` - Model inference
- `data.extract_features` - Feature engineering

### Custom Metrics

Track business-critical metrics:

```python
# Model performance
statsd.histogram('cancer_risk.prediction.confidence', confidence_score)
statsd.increment('cancer_risk.predictions.total', tags=['risk_level:high'])

# API performance
statsd.histogram('cancer_risk.api.latency', latency_ms, tags=['endpoint:/assess'])
statsd.gauge('cancer_risk.gemini.tokens_used', token_count)

# Errors
statsd.increment('cancer_risk.errors', tags=['type:api_timeout'])
```

### Log Attributes

Structured logging with key attributes:

```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "service": "cancer-risk-assessment",
  "level": "INFO",
  "request_id": "req-12345",
  "patient_id_hash": "abc123...",
  "operation": "risk_assessment",
  "model": "gemini-1.5-pro",
  "latency_ms": 245,
  "confidence": 0.85,
  "risk_level": "moderate",
  "tokens_used": 1250
}
```

## Detection Rules

### 1. High Latency Alert

**Trigger:** Risk assessment takes > 2 seconds

**Action:** Create incident, notify on-call

```yaml
Name: High Latency on Cancer Risk Assessment
Metric: cancer_risk.api.latency
Condition: avg(last_5m) > 2000
Priority: High
```

### 2. Low Confidence Alert

**Trigger:** Model confidence < 0.7 for high-risk predictions

**Action:** Flag for manual review

```yaml
Name: Low Confidence High Risk Prediction
Metric: cancer_risk.prediction.confidence
Condition: avg(last_15m) < 0.7 where risk_level:high
Priority: Medium
```

### 3. Unusual Query Patterns

**Trigger:** Spike in queries or suspicious content

**Action:** Security team notification

```yaml
Name: Suspicious Query Pattern Detected
Metric: cancer_risk.queries.rate
Condition: change(avg(last_5m), last_15m) > 200%
Priority: High
```

### 4. API Rate Limiting

**Trigger:** Approaching or exceeding API limits

**Action:** Auto-scaling notification

```yaml
Name: API Rate Limit Warning
Metric: cancer_risk.api.rate_limit_errors
Condition: sum(last_5m) > 10
Priority: Medium
```

### 5. Model Accuracy Degradation

**Trigger:** Prediction accuracy drops below threshold

**Action:** Model retraining notification

```yaml
Name: Model Accuracy Degradation
Metric: cancer_risk.model.accuracy
Condition: avg(last_1h) < 0.8
Priority: Critical
```

## Dashboard

The Clinical AI Observability Dashboard includes:

### Performance Overview
- Request rate and latency trends
- Error rate over time
- Top endpoints by traffic
- 95th percentile latency

### Model Metrics
- Prediction confidence distribution
- Risk level breakdown
- Token usage per request
- Model version tracking

### Security & Compliance
- Failed authentication attempts
- Anomalous query detection
- Data access patterns
- Audit log summary

### Infrastructure
- CPU and memory usage
- API gateway health
- Database connection pool
- Cache hit rate

## Monitoring Best Practices

### 1. Set Up Alerts Thoughtfully
- Avoid alert fatigue with meaningful thresholds
- Use different priorities for different severity
- Include runbook links in alert descriptions

### 2. Tag Everything
```python
tags = [
    f'service:{service_name}',
    f'env:{environment}',
    f'version:{version}',
    f'risk_level:{risk_level}',
    f'model:{model_name}',
]
```

### 3. Use Distributed Tracing
- Connect frontend requests to backend operations
- Track external API calls
- Identify slow dependencies

### 4. Monitor Business Metrics
- Track clinical outcomes, not just technical metrics
- Monitor patient safety indicators
- Track system utilization

### 5. Implement SLOs
```yaml
SLO: 99.5% of requests < 2s latency
SLO: 99.9% availability
SLO: 95% model confidence for high-risk cases
```

## Demo Scenario

**Narrative:**
"Healthcare providers submit clinical queries through our AI-powered decision support system. Datadog monitors every aspect: API performance, model accuracy, security threats, and system health, ensuring reliable and safe AI-assisted clinical decisions."

**Live Demo Flow:**

1. Show Datadog dashboard with live metrics
2. Submit clinical query through API
3. Watch real-time trace in APM
4. Show custom metrics updating
5. Trigger an alert condition (e.g., slow response)
6. Demonstrate incident creation
7. Show security monitoring detecting anomaly
8. Review logs for the entire flow

## Testing

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Load Testing
```bash
python scripts/load_test.py --requests=1000 --concurrent=10
```

## Troubleshooting

### Traces Not Appearing

```bash
# Check Datadog Agent status
sudo datadog-agent status

# Verify APM configuration
ddtrace-run python api/server.py
```

### Metrics Not Showing

```python
# Test StatsD connection
from datadog import statsd
statsd.increment('test.metric')
```

### Dashboard Empty

- Verify API and App keys
- Check service name matches
- Ensure agent is running

## Cost Optimization

- Set appropriate log retention periods
- Use sampling for high-volume traces
- Archive old metrics
- Optimize custom metrics

## Compliance & Security

- De-identify all patient data before logging
- Encrypt sensitive metrics
- Implement role-based access control
- Regular security audits
- HIPAA compliance considerations

## License

MIT License
