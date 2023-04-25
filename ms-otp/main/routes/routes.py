from flask import request, jsonify, json, Blueprint, current_app
from main.services import generate_otp, sendMail
from main import create_app

otp = Blueprint('otp', __name__, url_prefix='/otp')

@otp.route('/code', methods=['POST'])
def code():
    key = request.get_json().get("clave")
    print("key: " + key)
    try:
        value = generate_otp(key)
        print("code: " + value)
        print(type(value))
        sendMail([key], 'Codigo!', 'mail_template', value=value)
    except Exception as e:
        print(e)
        return str(e), 409
    return value, 200