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
from consulate import Consul
from consulate.models import agent
import socket

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
consul = Consul(host='consul')
kv = consul.kv

def create_app():
    app = Flask(__name__)
    load_dotenv()

    addr = socket.gethostbyname(socket.gethostname())

    checks=agent.Check(
        name="Service 'ms-user' check",
        http="https://ms-user.authme.localhost/auth/healthcheck",
        interval="10s",
        tls_skip_verify=True,
        timeout="1s",
        status="passing"
    )
    consul.agent.service.register(
        name='ms-user',
        service_id=f'ms-user-{addr}',
        address=addr,
        tags=["traefik.enable=true",
                "traefik.http.routers.ms-user.rule=Host(`ms-user.authme.localhost`)",
                "traefik.http.routers.ms-user.tls=true",
                "traefik.http.routers.ms-user.entrypoints=http,https",
                "traefik.http.services.ms-user.loadbalancer.server.port=6000",
                "traefik.http.middlewares.ms-user-cb.circuitbreaker.expression=NetworkErrorRatio() > 0.5",
                "traefik.http.routers.ms-user.middlewares=ms-user-cb"],
        checks=[checks]
    )

    redis = get_redis()
    app.config['REDIS'] = redis


    U = kv['ms-user/MYSQL_USER']
    PW = kv['ms-user/MYSQL_PASSWORD']
    D = kv['ms-user/MYSQL_DATABASE']
    H = kv['ms-user/MYSQL_HOST']
    P = kv['ms-user/MYSQL_PORT']

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{U}:{PW}@{H}:{P}/{D}'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['API_URL'] = kv['ms-user/API_URL']
    db.init_app(app)

    import main.controllers as resources

    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<int:id>')
    api.init_app(app)

    app.config['JWT_SECRET_KEY'] = kv['ms-user/JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=3600)
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(routes.auth)

    return app

def get_redis():
    from redis import Redis

    REDIS_HOST = kv['REDIS_HOST']
    REDIS_PORT = kv['REDIS_PORT']
    REDIS_PASSWORD = kv['REDIS_PASSWORD']

    return Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)