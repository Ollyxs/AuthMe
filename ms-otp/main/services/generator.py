import os
import pyotp
import redis
import base64
from dotenv import load_dotenv
from datetime import datetime
from main import create_app

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = create_app.redis()
secret_key = str(datetime.now())


def generate_otp(secret_key):
    #Codificar la secret key en Base32
    secret_key = base64.b32encode(secret_key.encode('ascii'))
    #Genera un código OTP
    totp = pyotp.TOTP(secret_key)
    code = totp.now()
    #Inserta el código en Redis y configura el tiempo de expiración
    redis_client.setex('valid', 300, code)
    return code

def validate_otp(secret_key, code: str) -> bool:
    #Valida un código OTP dado
    totp = pyotp.TOTP(secret_key)
    return totp.verify(code, datetime.now())

def is_code_valid(code: str) -> bool:
    #Verifica si un código aún es válido
    return redis_client.get(code) is not None

print(generate_otp(secret_key))