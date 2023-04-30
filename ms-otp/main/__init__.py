import os
from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail
from flask_restful import Api
from flask_retry import retry


api = Api()
mailsender = Mail()

def create_app():
    app = Flask(__name__)
    retry = Retry(app)
    load_dotenv()

    redis = get_redis()
    app.config['REDIS'] = redis
    app.config['TESTING'] = False

    api.init_app(app)

    from main.routes import routes
    app.register_blueprint(routes.otp)

    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    mailsender.init_app(app)

    return app

def get_redis():
    from redis import Redis

    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    return Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)