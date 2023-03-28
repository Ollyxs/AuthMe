from flask import Flask
import os
from dotenv import load_dotenv
from main.utils import db


def create_app():
    app = Flask(__name__)
    load_dotenv()
    db
    return app