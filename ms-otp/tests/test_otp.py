import unittest
import pyotp
import redis
import time
from datetime import datetime


class TestOTP(unittest.TestCase):

    def setUp(self):
        # Conectar a Redis
        self.redis_client = redis.Redis(host='redis', port=6379)
        
        # Generar una clave secreta
        self.secret_key = pyotp.random_base32()

    def tearDown(self):
        # Eliminar la clave de la base de datos de Redis
        self.redis_client.delete(self.code)

    def test_generate_otp(self):
        # Generar un código OTP y almacenarlo en Redis
        self.code = generate_otp(self.secret_key)
        
        # Comprobar que el código tiene una longitud de 6 dígitos
        self.assertEqual(len(self.code), 6)
        
        # Comprobar que el código se ha almacenado en Redis
        self.assertEqual(self.redis_client.get(self.code), b'valid')

    def test_validate_otp(self):
        # Generar un código OTP y almacenarlo en Redis
        self.code = generate_otp(self.secret_key)

        # Esperar 1 segundo para que el código expire
        time.sleep(1)

        # Comprobar que el código ya no es válido
        self.assertFalse(validate_otp(self.secret_key, self.code))

    def test_is_code_valid(self):
        # Generar un código OTP y almacenarlo en Redis
        self.code = generate_otp(self.secret_key)

        # Comprobar que el código es válido
        self.assertTrue(is_code_valid(self.code))

        # Esperar 1 segundo para que el código expire
        time.sleep(1)

        # Comprobar que el código ya no es válido
        self.assertFalse(is_code_valid(self.code))


if __name__ == '__main__':
    unittest.main()
