from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9bayb5142b7767f6937161311e7ca3d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent1.db'

db = SQLAlchemy(app)
guard = Bcrypt(app)
osyrus = LoginManager(app)

from invent import routes
from invent import other_functions
