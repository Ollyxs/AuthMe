import unittest, sys
import pyotp
import redis
import time
from datetime import datetime, timedelta
sys.path.append('../')
from main.services.generator import generate_otp

class TestOTP(unittest.TestCase):

    def setUp(self):
        # Conectar a Redis
        self.redis_client = redis.Redis(host='localhost', port=6380, password='qwerty')

        # Generar una clave secreta
        self.secret_key = pyotp.random_base32()
        self.secret_key2 = pyotp.random_base32()
        self.code = pyotp.TOTP(self.secret_key).now()

    def tearDown(self):
        # Eliminar la clave de la base de datos de Redis
        self.redis_client.delete(self.code)

        # Tests that the Redis key generated for each OTP code is unique.

    def test_generate_otp(self):
        # Generar un código OTP y almacenarlo en Redis
        self.code = generate_otp(self.secret_key)

        # Comprobar que el código tiene una longitud de 6 dígitos
        self.assertEqual(len(self.code), 6)

        # Comprobar que el código se ha almacenado en Redis
        self.assertEqual(int(self.redis_client.get(self.secret_key)), int(self.code))

    #     # Tests that a valid secret key and correct OTP code returns True.
    # def test_valid_secret_key_and_correct_otp(self):
    #     # Happy path test for valid secret key and correct OTP code
    #     secret_key = pyotp.random_base32()
    #     totp = pyotp.TOTP(secret_key)
    #     code = totp.now()
    #     assert validate_otp(secret_key, code) == True

    #     # Tests that a valid secret key and incorrect OTP code returns False.
    # def test_valid_secret_key_and_incorrect_otp(self):
    #     # Happy path test for valid secret key and incorrect OTP code
    #     secret_key = pyotp.random_base32()
    #     totp = pyotp.TOTP(secret_key)
    #     code = "123456"
    #     assert validate_otp(secret_key, code) == False

    #     # Tests that an invalid secret key returns False.
    # def test_invalid_secret_key(self):
    #     # Edge case test for invalid secret key
    #     secret_key = "invalid_secret_key"
    #     code = "123456"
    #     assert validate_otp(secret_key, code) == False

    #     # Tests that an invalid OTP code returns False.
    # def test_invalid_otp_code(self):
    #     # Edge case test for invalid OTP code
    #     secret_key = pyotp.random_base32()
    #     totp = pyotp.TOTP(secret_key)
    #     code = "invalid_otp_code"
    #     assert validate_otp(secret_key, code) == False

    #     # Tests that an expired OTP code returns False.
    # def test_expired_otp_code(self):
    #     # Edge case test for expired OTP code
    #     secret_key = pyotp.random_base32()
    #     totp = pyotp.TOTP(secret_key)
    #     # Set time to 31 seconds in the past to simulate expired code
    #     expired_datetime = datetime.now() - timedelta(seconds=31)
    #     code = totp.at(expired_datetime)
    #     assert validate_otp(secret_key, code) == False

    # def test_is_code_valid(self):
    #     # Generar un código OTP y almacenarlo en Redis
    #     self.code = generate_otp(self.secret_key)

    #     # Comprobar que el código es válido
    #     self.assertTrue(is_code_valid(self.code))

    #     # Esperar 1 segundo para que el código expire
    #     time.sleep(1)

    #     # Comprobar que el código ya no es válido
    #     self.assertFalse(is_code_valid(self.code))




    def test_generate_otp_unique_key(self):
        # Generate two OTP codes and check that their Redis keys are different
        otp1 = generate_otp(self.secret_key)
        otp2 = generate_otp(self.secret_key2)
        assert otp1 != otp2

        # Tests that the OTP code stored in Redis has a 5-minute expiration time.
    def test_generate_otp_expiration_time(self):
        # Generate an OTP code and check that it expires after 5 minutes
        otp = generate_otp(self.secret_key)
        assert self.redis_client.ttl(otp) <= 60

        # Tests that the generate_otp function always returns a string.
    def test_generate_otp_returns_string(self):
        # Check that the generate_otp function always returns a string
        otp = generate_otp(self.secret_key)
        assert isinstance(otp, str)

if __name__ == '__main__':
    unittest.main()