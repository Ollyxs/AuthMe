from flask import request, jsonify, Blueprint, current_app, json
from .. import db
from main.models import UserModel
from main.schemas import UserSchema, OtpSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_schema = UserSchema()
otp_schema = OtpSchema()
auth = Blueprint('auth', __name__, url_prefix='/auth')
otp = Blueprint('otp', __name__, url_prefix='/otp')

@auth.route('/login', methods=['POST'])
def login():
    print("entra")
    print(request.get_json())
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    if user.check_password(request.get_json().get("password")):
        access_token = create_access_token(identity=user)
        data = {
            'id': str(user.id),
            'email': user.email,
            'access_token': access_token
        }
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

@otp.route
def code():
    data = {}
    r = request.get(current_app.config["API_URL"]+'/code',
                    headers = {"content-type":"application/json"},
                    data = json.dumps(data))
    print(r.data)
    print(data)
    user = json.loads(r.text)
    user_code = otp_schema.load(request.get_json())
    codigo = user + " " + user_code
    return codigo