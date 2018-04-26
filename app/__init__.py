# This file initializes the app directory into a python module

# Third-party Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow

# Local Imports
from config import app_config

# app variable initialization
app = Flask(__name__, instance_relative_config=True)

# db variable initialization
db = SQLAlchemy()
ma = Marshmallow(app)

login_manager = LoginManager()


# initialize the app
def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    upload_path = 'app/uploads/'
    app.config['UPLOADED_PHOTOS_DEST'] = upload_path
    db.init_app(app)
    migrate = Migrate(app, db)
    Bootstrap(app)
    from app import models
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app


