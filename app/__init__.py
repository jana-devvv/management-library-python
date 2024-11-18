from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jd_library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '107f3612ecf34aceffa0c045bb1864e105c2ba7ba41036ec'
db = SQLAlchemy(app)

from app import routes, models