import matplotlib
matplotlib.use('Agg')  # Headless backend for non-GUI (e.g., GitHub Actions)
import matplotlib.pyplot as plt
import random
import os
import sys
from datetime import datetime

# Detect if local/GUI (not CI/headless)
if os.environ.get('CI') or '--headless' in sys.argv:  # Or check for no display
    matplotlib.use('Agg')
else:
    matplotlib.use('TkAgg')  # Interactive for Windows; falls back if tkinter missing

import matplotlib.pyplot as plt
# ... rest of the file unchanged

# Absolute import (works from root or subdir)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add repo root if needed
from detect_anomalies import create_payload_with_anomalies, detect_via_api

def plot_detection(payload, result, save_path='anomaly_demo.png', show_plot=True):
    """
    Plots time-series with anomalies highlighted.
    Expects 'series' from payload and 'expectedValues', 'isAnomaly' from result.
    """
    timestamps = [p['timestamp'] for p in payload['series']]
    actual_values = [p['value'] for p in payload['series']]
    expected_values = result.get('expectedValues', [sum(actual_values)/len(actual_values)] * len(actual_values))  # Mean fallback

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(timestamps)), actual_values, label='Actual Metrics (e.g., CPU %)', color='blue', linewidth=1)
    plt.plot(range(len(timestamps)), expected_values, label='Expected (Learned Pattern)', color='green', linestyle='--', alpha=0.7)
    
    if result.get('isAnomaly', False):
        # Highlight anomalies
        anomaly_status = result.get('anomalyStatus', [1 if random.random() < 0.15 else 0 for _ in payload['series']])
        anomaly_indices = [i for i, status in enumerate(anomaly_status) if status == 1]
        plt.scatter(anomaly_indices, [actual_values[i] for i in anomaly_indices], color='red', s=50, label='Detected Anomalies', zorder=5)
    
    plt.xlabel('Time Points (e.g., Minutes Ago)')
    plt.ylabel('Value')
    plt.title('AIOps Anomaly Detection: Actual vs. Expected (Offline Sim)')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(save_path)
    print(f"📊 Plot saved to {save_path}")
    if show_plot:
        plt.show()

if __name__ == "__main__":
    # Demo run with synthetic data
    payload = create_payload_with_anomalies(50, anomaly_prob=0.15)
    endpoint = os.getenv("ANOMALY_DETECTOR_ENDPOINT")
    api_key = os.getenv("ANOMALY_DETECTOR_KEY")
    
    if endpoint and api_key:
        result = detect_via_api(payload, endpoint, api_key)
    else:
        result = {
            'isAnomaly': True, 
            'expectedValues': [75] * len(payload['series']), 
            'anomalyStatus': [1 if random.random() < 0.15 else 0 for _ in payload['series']]
        }
        print("🧪 Offline mode: Using mock detection results with synthetic anomalies.")
    
    plot_detection(payload, result, show_plot=True)  # Set False for headless
    print("Demo complete! Check the plot window or PNG.")