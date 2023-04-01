from flask import Flask
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
db = mysql.connector.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'),
            host=os.getenv('MYSQL_HOST'), port=os.getenv('MYSQL_PORT'), database=os.getenv('MYSQL_DATABASE'))

def create_app():
    app = Flask(__name__)
    db
    return app