import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import pymysql
from retrying import retry
import requests
import re
from datetime import timedelta


api = Api()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    redis = get_redis()
    app.config['REDIS'] = redis

    U = os.getenv('MYSQL_USER')
    # U = U.replace('\\', '')
    PW = os.getenv('MYSQL_PASSWORD')
    # PW = PW.replace('\\', '')
    D = os.getenv('MYSQL_DATABASE')
    # D = D.replace('\\', '')
    H = os.getenv('MYSQL_HOST')
    # H = H.replace('\\', '')
    P = os.getenv('MYSQL_PORT')
    # P = re.sub(r'\D', '', P)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{U}:{PW}@{H}:{P}/{D}'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['API_URL'] = os.getenv('API_URL')
    db.init_app(app)

    import main.controllers as resources

    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<int:id>')
    api.init_app(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=3600)
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(routes.auth)

    return app

def get_redis():
    from redis import Redis

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    return Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)