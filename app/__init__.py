from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Comment out routes for now
    # from app.routes import main, auth, teams, games
    # app.register_blueprint(main.bp)
    # app.register_blueprint(auth.bp)
    # app.register_blueprint(teams.bp)
    # app.register_blueprint(games.bp)

    return app

from app import models 