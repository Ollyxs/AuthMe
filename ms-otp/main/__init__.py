import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_mail import Mail
from flask_restful import Api
from consulate import Consul
from consulate.models import agent
import socket


api = Api()
mailsender = Mail()
consul = Consul(host='consul')
kv = consul.kv

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    addr = socket.gethostbyname(socket.gethostname())

    checks=agent.Check(
        name="Service 'ms-otp' check",
        http="https://ms-otp.authme.localhost/otp/healthcheck",
        interval="10s",
        tls_skip_verify=True,
        timeout="1s",
        status="passing"
    )
    consul.agent.service.register(
        name='ms-otp',
        service_id=f'ms-otp-{addr}',
        address=addr,
        tags=["traefik.http.routers.ms-otp.tls=true",
            "traefik.http.routers.ms-otp.entrypoints=http,https,redis",
            "traefik.http.services.ms-otp.loadbalancer.server.port=5000",
            "traefik.http.middlewares.ms-otp-cb.circuitbreaker.expression=NetworkErrorRatio() > 0.5",
            "traefik.http.routers.ms-otp.middlewares=ms-otp-cb"],
        checks=[checks]
    )

    redis = get_redis()
    app.config['REDIS'] = redis
    app.config['TESTING'] = False

    api.init_app(app)

    from main.routes import routes
    app.register_blueprint(routes.otp)

    # app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME']
    app.config['MAIL_SERVER'] = kv['ms-otp/MAIL_SERVER']
    app.config['MAIL_PORT'] = kv['ms-otp/MAIL_PORT']
    app.config['MAIL_USE_TLS'] = kv['ms-otp/MAIL_USE_TLS']
    app.config['MAIL_USERNAME'] = kv['ms-otp/MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = kv['ms-otp/MAIL_PASSWORD']
    app.config['FLASKY_MAIL_SENDER'] = kv['ms-otp/FLASKY_MAIL_SENDER']
    mailsender.init_app(app)

    return app

def get_redis():
    from redis import Redis

    REDIS_HOST = kv['REDIS_HOST']
    REDIS_PORT = kv['REDIS_PORT']
    REDIS_PASSWORD = kv['REDIS_PASSWORD']

    return Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)