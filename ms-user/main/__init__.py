import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_restful import Api

api = Api()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    U = os.getenv('MYSQL_USER')
    PW = os.getenv('MYSQL_PASSWORD')
    D = os.getenv('MYSQL_DATABASE')
    H = os.getenv('MYSQL_HOST')
    P = os.getenv('MYSQL_PORT')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{U}:{PW}@{H}:{P}/{D}'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)

    import main.controllers as resources

    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<int:id>')
    api.init_app(app)

    return app