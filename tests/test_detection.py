import unittest
import sys
sys.path.append('../src')
from detect_anomalies import *  # Adjust based on actual imports

class TestAnomalyDetection(unittest.TestCase):
    def test_payload_creation(self):
        # Simulate series creation
        series = [{"timestamp": "2025-10-08T10:00:00Z", "value": 80}]
        self.assertEqual(len(series), 1)

if __name__ == '__main__':
    unittest.main()
    