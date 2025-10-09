import matplotlib
import sys
import os
import random
from datetime import datetime

# Detect if local/GUI (not CI/headless)
if os.environ.get('CI') or '--headless' in sys.argv:
    matplotlib.use('Agg')  # Headless for CI/non-GUI
else:
    try:
        matplotlib.use('TkAgg')  # Interactive for Windows (requires tkinter)
    except:
        matplotlib.use('Agg')  # Fallback if TkAgg unavailable

import matplotlib.pyplot as plt
import pandas as pd

# Add repo root to path if needed (for imports from src/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.detect_anomalies import create_payload_with_anomalies, detect_via_api  # Fixed: Added src. prefix

def plot_detection(payload, result, save_path='anomaly_demo.png', show_plot=True):
    """
    Plots time-series with anomalies highlighted.
    Expects 'series' from payload and 'expectedValues', 'isAnomaly' from result.
    Uses consistent datetime x-axis for realism.
    """
    timestamps = [p['timestamp'] for p in payload['series']]
    actual_values = [p['value'] for p in payload['series']]
    expected_values = result.get('expectedValues', [sum(actual_values)/len(actual_values)] * len(actual_values))  # Mean fallback

    # Create DataFrame for consistent plotting with datetimes
    df = pd.DataFrame({
        'time': pd.to_datetime(timestamps),
        'actual': actual_values,
        'expected': expected_values
    })

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # Plot lines separately for precise control (avoids list linestyle issues)
    ax.plot(df['time'], df['actual'], color='blue', linewidth=1, 
            label='Actual Metrics (e.g., CPU %)')
    ax.plot(df['time'], df['expected'], color='green', linestyle='--', alpha=0.7, 
            label='Expected (Learned Pattern)')

    if result.get('isAnomaly', False):
        # Generate or use anomaly status
        anomaly_status = result.get('anomalyStatus', [1 if random.random() < 0.15 else 0 for _ in payload['series']])
        anomaly_indices = [i for i, status in enumerate(anomaly_status) if status == 1]
        
        # Subset for anomalies
        anomaly_df = df.iloc[anomaly_indices]
        ax.scatter(anomaly_df['time'], anomaly_df['actual'], color='red', s=50, 
                   label='Detected Anomalies', zorder=5)

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('AIOps Anomaly Detection: Actual vs. Expected (Offline Sim)')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(save_path)
    print(f"📊 Plot saved to {save_path}")
    if show_plot:
        plt.show(block=False)  # Non-blocking show for inline/Jupyter
    # plt.close()  # Clean up

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