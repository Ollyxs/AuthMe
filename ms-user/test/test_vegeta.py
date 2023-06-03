import unittest
from httplib2 import Authentication
import datetime

class TestVegeta(unittest.TestCase):
    def test_success_response(self):
        response = auth.test_client().get('/auth/vegeta')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Success:')

    def test_not_found_response(self):
        response = auth.test_client().get('/auth/vegeta')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'Not Found:')

    def test_server_error_response(self):
        response = auth.test_client().get('/auth/vegeta')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, b'Server Error:')

    
    def test_random_seed(self):
        with unittest.mock.patch('random.seed') as mock_seed:
            auth.test_client().get('/auth/vegeta')
            mock_seed.assert_called_once_with(datetime.now)

    def test_time_sleep(self):
        with unittest.mock.patch('time.sleep') as mock_sleep:
            auth.test_client().get('/auth/vegeta')
            mock_sleep.assert_called_once_with(unittest.mock.ANY)

    def test_random_randint(self):
        with unittest.mock.patch('random.randint') as mock_randint:
            auth.test_client().get('/auth/vegeta')
            mock_randint.assert_called_with(0, 149)