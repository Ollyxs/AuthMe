import unittest
from your_module import auth  # Importa tu módulo o archivo que contiene la función vegeta

class VegetaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = auth.test_client()

    def test_success(self):
        response = self.app.get('/vegeta')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Success:")

    def test_not_found(self):
        response = self.app.get('/vegeta')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8'), "Not Found:")

    def test_server_error(self):
        response = self.app.get('/vegeta')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data.decode('utf-8'), "Server Error:")
