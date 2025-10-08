import requests
import os
from datetime import datetime, timedelta

def create_payload(num_points=100, base_value=75, granularity="PT1M"):
    """
    Creates a sample time-series payload for anomaly detection.
    Simulates metrics with minor variations (replace with real Azure Monitor data).
    """
    series = []
    for i in range(num_points):
        timestamp = (datetime.now() - timedelta(minutes=i)).isoformat()
        value = base_value + (i % 5)  # Simple pattern with deviations
        series.append({"timestamp": timestamp, "value": value})
    return {
        "series": series,
        "granularity": granularity
    }

def detect_via_api(payload, endpoint, api_key):
    """
    Sends payload to Azure Anomaly Detector API and returns result.
    """
    if not endpoint or not api_key:
        raise ValueError("Set ANOMALY_DETECTOR_ENDPOINT and ANOMALY_DETECTOR_KEY env vars")
    
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    url = f"{endpoint}/anomalydetector/v1.0/timeseries/entire/detect"
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    endpoint = os.getenv("ANOMALY_DETECTOR_ENDPOINT")
    api_key = os.getenv("ANOMALY_DETECTOR_KEY")
    payload = create_payload(100)
    try:
        result = detect_via_api(payload, endpoint, api_key)
        print(f"Expected peak: {result.get('expectedPeak', 'N/A')}")
        if result.get("isAnomaly"):
            print("🚨 Anomaly detected!")
    except Exception as e:
        print(f"Error: {e}")