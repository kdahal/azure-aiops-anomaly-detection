import unittest
import sys
import os
sys.path.append('../src')

# Mock for detect_anomalies (adjust imports)
class TestAnomalyDetection(unittest.TestCase):
    def test_series_payload(self):
        # Simulate payload creation
        from detect_anomalies import create_payload  # Assume helper func
        payload = create_payload(10)  # e.g., 10 points
        self.assertIn('series', payload)
        self.assertEqual(len(payload['series']), 10)

if __name__ == '__main__':
    unittest.main()
    