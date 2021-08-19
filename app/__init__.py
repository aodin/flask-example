from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Default, Development


db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application-factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Development)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Allow tests to override any configuration
    if test_config:
        app.config.from_mapping(test_config)

    # Register extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
