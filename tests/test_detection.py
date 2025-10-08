import unittest
import os
import random  # For seeding in anomaly test
from unittest.mock import patch, Mock

from src.detect_anomalies import create_payload, detect_via_api, create_payload_with_anomalies

class TestAnomalyDetection(unittest.TestCase):
    def test_series_payload(self):
        # Test payload creation
        payload = create_payload(num_points=10)
        self.assertIn('series', payload)
        self.assertEqual(len(payload['series']), 10)
        self.assertIn('granularity', payload)
        self.assertEqual(payload['granularity'], 'PT1M')
        # Check timestamps are recent ISOs
        first_ts = payload['series'][0]['timestamp']
        self.assertTrue(first_ts.endswith('Z') or first_ts.count('T') == 1)  # Basic ISO check

    @patch('requests.post')
    def test_detect_via_api_success(self, mock_post):
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'isAnomaly': True, 'expectedPeak': 80.5}
        mock_post.return_value = mock_response

        endpoint = 'https://test-endpoint'
        api_key = 'test-key'
        payload = create_payload(5)

        result = detect_via_api(payload, endpoint, api_key)
        self.assertTrue(result['isAnomaly'])
        self.assertEqual(result['expectedPeak'], 80.5)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_detect_via_api_error(self, mock_post):
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'
        mock_post.return_value = mock_response

        payload = create_payload(5)
        endpoint = 'https://test-endpoint'
        api_key = 'test-key'

        with self.assertRaises(Exception):
            detect_via_api(payload, endpoint, api_key)

    def test_missing_env_vars(self):
        # Test raises ValueError if no endpoint/key (patched to check args)
        payload = create_payload(5)
        with self.assertRaises(ValueError):
            detect_via_api(payload, '', '')  # Directly pass None-like values

    def test_payload_with_anomalies(self):
        # Seed for reproducible test (ensures anomalies)
        random.seed(42)
        payload = create_payload_with_anomalies(20, anomaly_prob=0.2)
        values = [p['value'] for p in payload['series']]
        self.assertEqual(len(values), 20)
        extremes = [v for v in values if v > 90 or v < 60]
        self.assertGreater(len(extremes), 0, "Should have some anomalies")

if __name__ == '__main__':
    unittest.main(verbosity=2)  # Verbose for local runs