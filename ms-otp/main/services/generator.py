import os
import pyotp
import redis
import base64
from dotenv import load_dotenv
from datetime import datetime
from main import get_redis

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = get_redis()
secret_key = str(datetime.now())


def generate_otp(secret_key):
    #Codificar la secret key en Base32
    secret_key_b32 = base64.b32encode(secret_key.encode('ascii'))
    #Genera un código OTP
    totp = pyotp.TOTP(secret_key_b32)
    code = totp.now()
    #Inserta el código en Redis y configura el tiempo de expiración
    redis_client.setex(secret_key, 60, code)
    return code

# TODO Funcione para usar a futuro
# ? Esto debería estar en el otro microservico?
# def is_code_valid(secret_key: str) -> bool:
#     #Verifica si un código aún es válido
#     return redis_client.get(secret_key) is not None

# def validate_otp(secret_key: str) -> bool:
#     #Valida un código OTP dado
#     if is_code_valid(secret_key):
#         secret_key_b32 = base64.b32encode(secret_key.encode('ascii'))
#         totp = pyotp.TOTP(secret_key_b32)
#         return totp.verify(secret_key)
#     else:
#         return False


# print(generate_otp(secret_key, redis_client))