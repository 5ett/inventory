import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()
secret_code = os.getenv("HIDDEN_SECRET_KEY") 
app = Flask(__name__)
app.config['SECRET_KEY'] = secret code
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent1.db'

db = SQLAlchemy(app)
guard = Bcrypt(app)
osyrus = LoginManager(app)

from invent import routes
from invent import other_functions
