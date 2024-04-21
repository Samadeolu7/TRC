import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()
load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db = SQLAlchemy()
db.init_app(app)