import requests
from flask_retry import retry
from flask import Flask


@retry(max_attempts=3, wait_fixed=2000)
def check_service_health():
    try:
        response = requests.get('http://register/api')
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
    
@otp.route('/check_microservice_health')
def check_microservice():
    if check_service_health():
        return 'El microservicio está en línea'
    else:
        return 'El microservicio está down downnnn'