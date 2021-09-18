from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config['SECRET_KEY'] = '116bd3d8cb283b020a8f080e'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from MARKET import routes


# venv\Scripts\activate.ps1

# $env:FLASK_APP = 'run.py'
# $env:FLASK_DEBUG = 1
# flask run