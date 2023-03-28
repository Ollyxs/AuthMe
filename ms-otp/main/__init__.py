import os
from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail


def create_app():
    app = Flask(__name__)
    load_dotenv()
    return app