import os

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Development, Production
from .filters import register_filters


db = SQLAlchemy()
mail = Mail()
migrate = Migrate()


def create_app(test_config=None):
    """Application-factory pattern."""
    app = Flask(__name__)

    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object(Development)
    else:
        app.config.from_object(Production)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Allow tests to override any configuration
    if test_config:
        app.config.from_mapping(test_config)

    # Register extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Register custom jinja filters
    register_filters(app)

    return app
