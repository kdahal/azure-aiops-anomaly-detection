import requests
from datetime import datetime, timedelta
import os
# Add after imports
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

# Fetch metrics (e.g., VM CPU)
credential = DefaultAzureCredential()
client = LogsQueryClient(credential)
query = "Heartbeat | where TimeGenerated > ago(1h) | summarize avg(Heartbeat) by bin(TimeGenerated, 1m)"
response = client.query_workspace(
    workspace_id="your-log-analytics-id",  # From IaC output
    query=query,
    timespan=timespan
)
# Process response into payload for Anomaly Detector

endpoint = os.getenv("ANOMALY_DETECTOR_ENDPOINT")
api_key = os.getenv("ANOMALY_DETECTOR_KEY")

if not endpoint or not api_key:
    print("Set ANOMALY_DETECTOR_ENDPOINT and ANOMALY_DETECTOR_KEY env vars")
    exit(1)

headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

# Simulated time-series (replace with real metrics from Azure Monitor)
payload = {
    "series": [{"timestamp": (datetime.now() - timedelta(minutes=i)).isoformat(), "value": 75 + (i % 5)} for i in range(100)],
    "granularity": "PT1M"
}

response = requests.post(f"{endpoint}/anomalydetector/v1.0/timeseries/entire/detect", headers=headers, json=payload)
if response.status_code == 200:
    result = response.json()
    print(f"Expected peak: {result.get('expectedPeak', 'N/A')}")
    if result.get("isAnomaly"):
        print("🚨 Anomaly detected!")
else:
    print(f"Error: {response.status_code}")
