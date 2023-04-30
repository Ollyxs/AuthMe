from flask import request, jsonify, json, Blueprint, current_app
from main.services import generate_otp, sendMail
from main import create_app
from flask_retry import retry

otp = Blueprint('otp', __name__, url_prefix='/otp')

@otp.route('/code', methods=['POST'])
def code():
    key = request.get_json().get("clave")
    try:
        value = generate_otp(key)
        sendMail([key], 'Codigo!', 'mail_template', value=value)
    except Exception as e:
        return str(e), 409
    return value, 200
