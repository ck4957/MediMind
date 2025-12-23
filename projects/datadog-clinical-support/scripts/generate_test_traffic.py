"""
Script to generate test traffic for the API
"""

import requests
import time
import random
from datetime import datetime


API_URL = "http://localhost:8000"


SAMPLE_QUERIES = [
    {
        "patient_id_hash": "pt_001_hash",
        "age": 45,
        "gender": "F",
        "clinical_notes": "Routine screening, no symptoms. Family history of breast cancer.",
        "family_history": True,
        "smoking_status": "never"
    },
    {
        "patient_id_hash": "pt_002_hash",
        "age": 62,
        "gender": "M",
        "clinical_notes": "Persistent cough for 3 months. 30 pack-year smoking history. Weight loss noted.",
        "family_history": False,
        "smoking_status": "current"
    },
    {
        "patient_id_hash": "pt_003_hash",
        "age": 38,
        "gender": "F",
        "clinical_notes": "Follow-up visit. No new symptoms. Recent mammogram normal.",
        "family_history": False,
        "smoking_status": "never"
    },
    {
        "patient_id_hash": "pt_004_hash",
        "age": 58,
        "gender": "M",
        "clinical_notes": "Elevated PSA levels. Family history of prostate cancer.",
        "lab_results": {"psa": 6.2},
        "family_history": True,
        "smoking_status": "former"
    },
    {
        "patient_id_hash": "pt_005_hash",
        "age": 71,
        "gender": "F",
        "clinical_notes": "CT scan shows lung nodule. Follow-up required. Former smoker.",
        "family_history": False,
        "smoking_status": "former"
    },
]


def check_health():
    """Check if API is healthy"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def send_assessment_request(query):
    """Send a risk assessment request"""
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/assess-risk",
            json=query,
            timeout=30
        )
        latency = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Assessment completed in {latency:.0f}ms")
            print(f"  Patient: {query['patient_id_hash']}")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            return True
        else:
            print(f"✗ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def generate_traffic(num_requests=100, delay_seconds=1.0):
    """Generate test traffic"""
    print("Cancer Risk Assessment - Traffic Generator")
    print("=" * 60)
    print(f"Target: {API_URL}")
    print(f"Requests: {num_requests}")
    print(f"Delay: {delay_seconds}s")
    print("=" * 60)
    
    # Check health first
    if not check_health():
        print("✗ API is not healthy. Please start the server first.")
        return
    
    print("✓ API is healthy")
    print("\nGenerating traffic...\n")
    
    successful = 0
    failed = 0
    
    for i in range(num_requests):
        query = random.choice(SAMPLE_QUERIES).copy()
        
        # Occasionally add lab results
        if random.random() > 0.5 and 'lab_results' not in query:
            query['lab_results'] = {
                'cea': random.uniform(0, 10),
                'ca_125': random.uniform(0, 50),
            }
        
        print(f"\n[{i+1}/{num_requests}] {datetime.now().strftime('%H:%M:%S')}")
        
        if send_assessment_request(query):
            successful += 1
        else:
            failed += 1
        
        if i < num_requests - 1:
            time.sleep(delay_seconds)
    
    print("\n" + "=" * 60)
    print("Traffic generation complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("=" * 60)
    print("\nCheck Datadog for metrics and traces:")
    print("  - APM: https://app.datadoghq.com/apm/traces")
    print("  - Metrics: https://app.datadoghq.com/metric/explorer")
    print("  - Logs: https://app.datadoghq.com/logs")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate test traffic')
    parser.add_argument('--requests', type=int, default=50, help='Number of requests')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    generate_traffic(args.requests, args.delay)
