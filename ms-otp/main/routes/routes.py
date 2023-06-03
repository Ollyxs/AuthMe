from flask import request, jsonify, json, Blueprint, current_app
from main.services import generate_otp, sendMail
from main import create_app
import requests
from retrying import retry


otp = Blueprint('otp', __name__, url_prefix='/otp')
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
@otp.route('/code', methods=['POST'])
def code():
    key = request.get_json().get("clave")
    try:
        value = generate_otp(key)
        sendMail([key], 'Codigo!', 'mail_template', value=value)
    except Exception as e:
        return str(e), 409
    return value, 200

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def make_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    return response

@otp.route("/health-check-otp")
def health_check():
    try:
        response = make_request("https://example.com/microservice/health")
        return jsonify({"status": "UP", "response": response.json()})
    except Exception as e:
        return jsonify({"status": "DOWN", "error": str(e)})
