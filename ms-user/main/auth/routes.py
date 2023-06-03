from flask import request, jsonify, Blueprint, current_app, json
from .. import db
from main.models import UserModel
from main.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests
from retrying import retry
import random
from datetime import datetime
import time


user_schema = UserSchema()
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    if user.check_password(request.get_json().get("password")):
        access_token = create_access_token(identity=user)
        data = {
            'id': str(user.id),
            'email': user.email,
            'access_token': access_token
        }
        data_otp = {"clave": user.email}
        r = make_request(
             "POST",
             current_app.config['API_URL'] + 'otp/code',
             headers={"content-type": "application/json"},
             data=json.dumps(data_otp), 
             verify=False
         )
        return data, 200
    else:
        return 'Incorrect password', 401
    


@auth.route('/register', methods=['POST'])
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def register():
    user = user_schema.load(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    if exists:
        return 'Duplicated mail', 409
    else:
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e), 409
        return user_schema.dump(user), 201

@auth.route('/validate', methods=['POST'])
@retry(stop_max_attempt_number=6, wait_exponential_multiplier=1000, wait_exponential_max=10000)
@jwt_required()
def validate():
    iduser = get_jwt_identity()
    user = db.session.query(UserModel).get_or_404(iduser)
    clave = str(user.email)
    code = request.get_json().get("code")
    redis = current_app.config['REDIS']
    byte_val = redis.get(clave)
    code_otp = byte_val.decode('utf-8')

    if code_otp is None:
        return "Clave no encontrada en Redis", 404

    if code is None:
        return "Codigo no proporcionado", 400

    if code == code_otp:
        return "Codigo valido", 201
    else:
        return "Código invalido", 404

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def make_request(method, url, headers=None, data=None, verify=None):
    print("Intentando conectar...")
    if method == "POST":
        response = requests.post(url, headers=headers, data=data, verify=verify)
    else:
        raise ValueError("Invalid method")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    return response


@auth.route("/health-check-users")
def health_check():
    try:
        response = make_request("http://localhost:5000/api/v1/health")
        return jsonify({"status": "UP", "response": response.json()})
    except Exception as e:
        return jsonify({"status": "DOWN", "error ": str(e)})

@auth.route('/vegeta', methods=['GET'])
def vegeta():
    random.seed(datetime.now)
    time.sleep(random.randint(0, 20))
    value = random.randint(0, 149)
    if value in range(0, 49):
        return "Success:", 200
    elif value in range(50, 99):
        return "Not Found:", 404
    elif value in range(100, 149):
        return "Server Error:", 500