import pyotp
import redis
from datetime import datetime


redis_client = redis.Redis(host='redis', port=6379)


def generate_otp(secret_key: str) -> str:
    """Genera un código OTP y lo almacena en Redis durante 5 minutos."""

    totp = pyotp.TOTP(secret_key)
    code = totp.now()

    # Insertar el código en Redis y configurar el tiempo de expiración
    redis_client.setex(code, 300, 'valid')

    return code


def validate_otp(secret_key: str, code: str) -> bool:
    """Valida un código OTP dado."""

    totp = pyotp.TOTP(secret_key)
    return totp.verify(code, datetime.now())


def is_code_valid(code: str) -> bool:
    """Verifica si un código aún es válido."""

    return redis_client.get(code) is not None
