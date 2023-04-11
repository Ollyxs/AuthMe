from flask import request, jsonify, Blueprint
from .. import db
from main.models import UserModel
from main.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_schema = UserSchema()
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first_or_404()
    if user.validate_pass(request.get_json().get("password")):
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
    print(user)
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