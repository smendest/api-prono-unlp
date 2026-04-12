from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # Initialize at module level


def create_app():
    """Create and configure the application and database"""

    # app creation
    app = Flask(__name__)

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Session config
    app.config["SESSION_PERMANENT"] = False  # TODO: Not working
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure the SQLite database - ABSOLUTE PATH to project root
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "forecasts.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    return app
