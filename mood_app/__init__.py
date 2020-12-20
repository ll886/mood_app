from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# init flask app
app = Flask(__name__)
# config
app.config["SECRET_KEY"] = "359281cf99cf9b27b6946c5c60e44fa2"
# using sqlite for testing, name: 'demo.db'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
# init db
db = SQLAlchemy(app)
# init bycrypt and login_manager
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


from mood_app import routes

