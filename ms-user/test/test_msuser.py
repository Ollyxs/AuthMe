import requests
import unittest
from retrying import retry

class TestMicroservice(unittest.TestCase):
    @retry(wait_fixed=2000, stop_max_attempt_number=5)
    def test_msuser(self):
        response = requests.get('http://localhost:5000/api/v1/health')
        self.assertEqual(response.status_code, 200, f'Error al acceder al microservicio: {response.status_code}')

if __name__ == '__main__':
    unittest.main()
