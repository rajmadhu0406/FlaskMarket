from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete  #db.session.delete(table_object)
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config['SECRET_KEY'] = '116bd3d8cb283b020a8f080e'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from MARKET import routes


# venv\Scripts\activate.ps1

# $env:FLASK_APP = 'run.py'
# $env:FLASK_DEBUG = 1
# flask run