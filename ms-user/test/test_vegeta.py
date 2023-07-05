import unittest
import httplib2
import time
import random

class TestVegeta(unittest.TestCase):
    def test_success_response(self):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request("https://ms-user.authme.localhost/auth/healthcheck", "GET")
        self.assertEqual(response.status, 200)

    def test_not_found_response(self):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request("https://ms-user.authme.localhost/auth/goku", "GET")
        self.assertEqual(response.status, 404)

    def test_server_error_response(self):
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request("https://ms-user.authme.localhost/auth/servererror", "GET")
        self.assertTrue(response.status >= 500)

if __name__ == '__main__':
    unittest.main()