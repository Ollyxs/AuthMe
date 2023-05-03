from flask import request, jsonify, Blueprint, current_app, json
from .. import db
from main.models import UserModel
from main.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests

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
        r = requests.post('http://ms-otp-ms-otp-1/otp/code',
                    headers = {"content-type":"application/json"},
                    data = json.dumps(data_otp),
                    verify=False)
        return data, 200
    else:
        return 'Incorrect password', 401

@auth.route('/register', methods=['POST'])
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