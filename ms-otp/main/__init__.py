import os
from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail
from flask_restful import Api
from redis import Redis

api = Api()
mailsender = Mail()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    redis = Redis(host = REDIS_HOST, port = REDIS_PORT, password = REDIS_PASSWORD)

    app.config['TESTING'] = True

    api.init_app(app)

    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    mailsender.init_app(app)
    
    return app