import time
import pyotp

print("Generar una clave secreta para el usuario")
# Generar una clave secreta para el usuario
key = "OF3WK4TUPEYTEMY=" #deberiamos usar la clave del perfil del usuario en base32, traida del archivo to_b32.py
totp = pyotp.TOTP(key)

# Generar una contraseña OTP
otp = totp.now()
print("Contraseña OTP: ", otp)

# Acá iría el envio de mail al usuario con el código

input("Presione enter cuando esté listo para ingresar la contraseña OTP:")

user_otp = input("Ingrese la contraseña OTP: ")

# Verificar si el código es correcto
if totp.verify(user_otp, valid_window=300): #valid_window=300 es para que la contraseña sea válida por 5 minutos
    print("Contraseña OTP válida")
else:
    print("Contraseña OTP no válida")
