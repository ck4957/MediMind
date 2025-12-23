"""
Real-Time Cancer Risk Assessment Dashboard
Built with Streamlit
"""

import streamlit as st
import json
import time
from datetime import datetime
from confluent_kafka import Consumer, KafkaError
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KafkaConfig

# Page config
st.set_page_config(
    page_title="Cancer Risk Assessment Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'consumer_running' not in st.session_state:
    st.session_state.consumer_running = False


def initialize_consumer():
    """Initialize Kafka consumer for predictions"""
    consumer = Consumer(KafkaConfig.get_consumer_config('dashboard-group'))
    consumer.subscribe([
        KafkaConfig.TOPIC_PREDICTIONS,
        KafkaConfig.TOPIC_ALERTS,
    ])
    return consumer


def fetch_messages(consumer, timeout=1.0):
    """Fetch new messages from Kafka"""
    new_predictions = []
    new_alerts = []
    
    msg = consumer.poll(timeout=timeout)
    
    if msg and not msg.error():
        topic = msg.topic()
        data = json.loads(msg.value().decode('utf-8'))
        
        if topic == KafkaConfig.TOPIC_PREDICTIONS:
            new_predictions.append(data)
        elif topic == KafkaConfig.TOPIC_ALERTS:
            new_alerts.append(data)
    
    return new_predictions, new_alerts


# Dashboard UI
st.title("🏥 Real-Time Cancer Risk Assessment Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("System Status")
    st.success("🟢 System Online")
    
    st.markdown("### Connected Topics")
    st.write(f"📊 {KafkaConfig.TOPIC_PREDICTIONS}")
    st.write(f"🚨 {KafkaConfig.TOPIC_ALERTS}")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This dashboard displays real-time cancer risk assessments 
    processed through Confluent Kafka streams, with predictions 
    from Vertex AI and analysis from Gemini.
    """)
    
    if st.button("Clear History"):
        st.session_state.predictions = []
        st.session_state.alerts = []
        st.rerun()

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Assessments",
        value=len(st.session_state.predictions)
    )

with col2:
    high_risk_count = sum(
        1 for p in st.session_state.predictions 
        if p.get('risk_assessment', {}).get('risk_level') in ['high_risk', 'very_high_risk']
    )
    st.metric(
        label="High Risk Cases",
        value=high_risk_count,
        delta=None if high_risk_count == 0 else "⚠️"
    )

with col3:
    st.metric(
        label="Active Alerts",
        value=len(st.session_state.alerts)
    )

st.markdown("---")

# Try to fetch new messages
try:
    consumer = initialize_consumer()
    new_preds, new_alerts = fetch_messages(consumer)
    
    if new_preds:
        st.session_state.predictions.extend(new_preds)
    if new_alerts:
        st.session_state.alerts.extend(new_alerts)
    
except Exception as e:
    st.warning(f"Consumer not connected: {e}")

# Alerts section
if st.session_state.alerts:
    st.header("🚨 Active Alerts")
    for alert in reversed(st.session_state.alerts[-5:]):  # Show last 5
        with st.expander(
            f"⚠️ {alert.get('patient_id')} - {alert.get('risk_level', 'Unknown')} "
            f"({alert.get('timestamp', '')[:19]})",
            expanded=True
        ):
            st.error(alert.get('message', 'No message'))
            st.write(f"**Confidence:** {alert.get('confidence', 0):.1%}")

st.markdown("---")

# Recent predictions
st.header("📊 Recent Risk Assessments")

if st.session_state.predictions:
    # Show last 10 predictions
    for pred in reversed(st.session_state.predictions[-10:]):
        patient_id = pred.get('patient_id')
        risk_assessment = pred.get('risk_assessment', {})
        risk_level = risk_assessment.get('risk_level', 'Unknown')
        confidence = risk_assessment.get('confidence', 0)
        timestamp = pred.get('timestamp', '')[:19]
        
        # Color coding
        if risk_level in ['high_risk', 'very_high_risk']:
            status_color = "🔴"
        elif risk_level == 'moderate_risk':
            status_color = "🟡"
        else:
            status_color = "🟢"
        
        with st.expander(
            f"{status_color} {patient_id} - {risk_level.replace('_', ' ').title()} "
            f"(Confidence: {confidence:.1%}) - {timestamp}"
        ):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown("**Risk Scores:**")
                risk_scores = risk_assessment.get('risk_scores', {})
                for level, score in risk_scores.items():
                    st.progress(score, text=f"{level.replace('_', ' ').title()}: {score:.1%}")
            
            with col2:
                st.markdown("**Data Sources:**")
                data_sources = pred.get('data_sources', {})
                st.write(f"- Imaging: {'✅' if data_sources.get('has_imaging') else '❌'}")
                st.write(f"- Lab Results: {'✅' if data_sources.get('has_lab_results') else '❌'}")
                st.write(f"- Clinical Notes: {'✅' if data_sources.get('has_clinical_notes') else '❌'}")
            
            # Clinical analysis
            clinical_analysis = pred.get('clinical_analysis')
            if clinical_analysis:
                st.markdown("**Clinical Analysis:**")
                if clinical_analysis.get('risk_factors'):
                    st.write("Risk Factors:", ", ".join(clinical_analysis['risk_factors']))
                if clinical_analysis.get('concerning_findings'):
                    st.write("Concerning Findings:", ", ".join(clinical_analysis['concerning_findings']))
            
            # Explanation
            explanation = pred.get('explanation', '')
            if explanation:
                st.markdown("**Explanation:**")
                st.write(explanation[:500] + "..." if len(explanation) > 500 else explanation)
else:
    st.info("No predictions yet. Start the producers and consumer to see real-time data.")

# Auto-refresh
time.sleep(2)
st.rerun()
