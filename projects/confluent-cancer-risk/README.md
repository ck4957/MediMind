# Confluent Challenge: Real-Time Cancer Risk Assessment

## Overview

This project demonstrates real-time cancer risk assessment using streaming clinical data with Confluent Kafka and Google Cloud AI services.

## Architecture

```
Clinical Data Sources → Confluent Kafka → Feature Processing → 
Vertex AI Model → Risk Predictions → Real-time Dashboard
```

## Core Components

### 1. Data Streaming with Confluent Cloud

**Topics Structure:**
- `clinical-imaging-stream`: Incoming imaging metadata
- `lab-results-stream`: Real-time lab values
- `clinical-notes-stream`: De-identified clinical notes
- `risk-predictions-stream`: Model outputs
- `alerts-stream`: High-risk patient notifications

### 2. Google Cloud Integration

- **Vertex AI**: Deploy pre-trained cancer risk model
- **Gemini**: Analyze clinical notes, generate risk summaries
- **Cloud Functions**: Kafka consumers for model inference
- **BigQuery**: Historical data and analytics
- **Cloud Storage**: Image/video processing pipeline

## Prerequisites

- Confluent Cloud account (free trial available)
- Google Cloud Platform project with billing enabled
- Python 3.9+
- Node.js 16+ (for dashboard)

## Setup Instructions

### 1. Confluent Cloud Setup

```bash
# Install Confluent CLI
curl -L --http1.1 https://cnfl.io/cli | sh -s -- -b /usr/local/bin

# Login to Confluent Cloud
confluent login

# Create cluster (or use existing)
confluent kafka cluster create cancer-risk-cluster --cloud gcp --region us-central1
```

### 2. Google Cloud Setup

```bash
# Set project ID
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable bigquery.googleapis.com

# Create service account
gcloud iam service-accounts create cancer-risk-sa \
    --display-name="Cancer Risk Assessment Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:cancer-risk-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

### 3. Environment Configuration

Create `.env` file:

```env
# Confluent Cloud
CONFLUENT_BOOTSTRAP_SERVERS=your-bootstrap-server.confluent.cloud:9092
CONFLUENT_API_KEY=your-api-key
CONFLUENT_API_SECRET=your-api-secret
CONFLUENT_SCHEMA_REGISTRY_URL=https://your-schema-registry.confluent.cloud
CONFLUENT_SCHEMA_REGISTRY_API_KEY=your-sr-api-key
CONFLUENT_SCHEMA_REGISTRY_API_SECRET=your-sr-api-secret

# Google Cloud
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
VERTEX_AI_ENDPOINT=your-vertex-ai-endpoint
GEMINI_API_KEY=your-gemini-api-key

# Kafka Topics
TOPIC_IMAGING=clinical-imaging-stream
TOPIC_LAB_RESULTS=lab-results-stream
TOPIC_CLINICAL_NOTES=clinical-notes-stream
TOPIC_PREDICTIONS=risk-predictions-stream
TOPIC_ALERTS=alerts-stream
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create Kafka Topics

```bash
python scripts/create_topics.py
```

### 6. Deploy Model to Vertex AI

```bash
python scripts/deploy_model.py
```

## Running the Application

### Start Data Producers (Simulate Clinical Data)

```bash
# Terminal 1: Imaging data producer
python producers/imaging_producer.py

# Terminal 2: Lab results producer
python producers/lab_results_producer.py

# Terminal 3: Clinical notes producer
python producers/clinical_notes_producer.py
```

### Start Stream Processors

```bash
# Terminal 4: Risk assessment consumer
python consumers/risk_assessment_consumer.py
```

### Launch Dashboard

```bash
# Terminal 5: Real-time dashboard
streamlit run dashboard/app.py
```

Open browser to http://localhost:8501

## Demo Scenario

**Narrative:**
"A patient arrives for routine screening. As their lab results arrive, imaging is completed, and clinical notes are entered, our system processes each data point in real-time through Kafka streams, updating the cancer risk assessment continuously."

**Live Demo Flow:**

1. Show Confluent dashboard with active topics
2. Inject simulated patient data into streams
3. Watch real-time processing in Cloud Functions logs
4. Display Vertex AI model making predictions
5. Show Gemini analyzing clinical notes
6. Dashboard updates with risk score and explanation
7. High-risk alert triggers automatically

## Project Structure

```
confluent-cancer-risk/
├── README.md
├── requirements.txt
├── config/
│   ├── kafka_config.py
│   └── gcp_config.py
├── producers/
│   ├── imaging_producer.py
│   ├── lab_results_producer.py
│   └── clinical_notes_producer.py
├── consumers/
│   ├── risk_assessment_consumer.py
│   └── alert_consumer.py
├── models/
│   ├── cancer_risk_model.py
│   └── feature_engineering.py
├── integrations/
│   ├── vertex_ai.py
│   └── gemini.py
├── dashboard/
│   ├── app.py
│   └── components/
├── scripts/
│   ├── create_topics.py
│   ├── deploy_model.py
│   └── generate_synthetic_data.py
└── data/
    └── synthetic_patients.json
```

## Key Features

1. **Real-time Processing**: Demonstrates how streaming enables immediate risk assessment
2. **Multimodal AI**: Combines structured (labs), unstructured (notes), and imaging data
3. **Explainable AI**: Gemini provides human-readable explanations
4. **Scalable Architecture**: Kafka handles high-throughput clinical data
5. **Clinical Relevance**: Addresses real healthcare need for timely risk assessment

## Data Sources

- **MIMIC-III Demo**: Small publicly available dataset
- **Synthetic Data Generator**: Create realistic clinical scenarios
- **Kaggle Cancer Datasets**: Pre-processed imaging data

## Monitoring

- Confluent Cloud Console: Monitor topic throughput, consumer lag
- Google Cloud Console: View Vertex AI predictions, function logs
- Dashboard: Real-time metrics and alerts

## Troubleshooting

### Connection Issues

```bash
# Test Kafka connectivity
python scripts/test_connection.py
```

### Model Deployment

```bash
# Check Vertex AI endpoint status
gcloud ai endpoints list --region=us-central1
```

## License

MIT License
