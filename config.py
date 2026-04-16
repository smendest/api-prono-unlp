from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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

    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Configure the SQLite database - ABSOLUTE PATH to project root
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "forecasts.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    return app
