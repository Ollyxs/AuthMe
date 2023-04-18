import pyotp
import redis
from datetime import datetime


redis_client = redis.Redis(host='localhost', port=6380, password='qwerty')
secret_key = datetime.now()


def generate_otp(secret_key):
    #Genera un código OTP
    totp = pyotp.TOTP(secret_key)
    code = totp.now()
    #Inserta el código en Redis y configura el tiempo de expiración
    redis_client.setex(code, 300, 'valid')
    return code

def validate_otp(secret_key, code: str) -> bool:
    #Valida un código OTP dado
    totp = pyotp.TOTP(secret_key)
    return totp.verify(code, datetime.now())

def is_code_valid(code: str) -> bool:
    #Verifica si un código aún es válido
    return redis_client.get(code) is not None
