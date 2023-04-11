from flask_restful import Resource
from flask import request
from .. import db
from main.models import UserModel
from main.schemas import UserSchema
from main.schemas import UserFilters
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

user_schema = UserSchema()


class User(Resource):
    @jwt_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user_schema.dump(user), 201

    @admin_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @jwt_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class Users(Resource):
    @jwt_required
    def get(self):
        users = db.session.query(UserModel)
        user_filtro = UserFilters(users)
        for key, value in request.get_json().items():
            consulta = user_filtro.aplicar_filtro(key, value)
        return user_schema.dump(consulta.all(), many=True)

    @jwt_required
    def post(self):
        user = user_schema.load(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201