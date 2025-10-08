import unittest
import sys
import os
sys.path.append('../src')  # For local/CI path

from detect_anomalies import create_payload, detect_via_api
from unittest.mock import patch, Mock

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
        # Test raises ValueError if no endpoint/key
        with patch.dict(os.environ, {'ANOMALY_DETECTOR_ENDPOINT': '', 'ANOMALY_DETECTOR_KEY': ''}):
            payload = create_payload(5)
            with self.assertRaises(ValueError):
                detect_via_api(payload, None, None)  # But actually checks env in func

if __name__ == '__main__':
    unittest.main()