import requests
import unittest
from retrying import retry
import httpretty
from main.auth import login
import sys

class TestMicroservice(unittest.TestCase):
    @retry(wait_fixed=2000, stop_max_attempt_number=5)
    def test_msuser(self):
        response = requests.get('API_URL')
        self.assertEqual(response.status_code, 200, f'Error al acceder al microservicio: {response.status_code}')

    @httpretty.activate
    def test_msuser_with_mock(self):
        httpretty.register_uri(
            httpretty.GET,
            'API_URL',
            responses=[
                httpretty.Response(body='{}', status=200),
            ]
        )

        self.test_msuser()

if __name__ == '__main__':
    unittest.main()
