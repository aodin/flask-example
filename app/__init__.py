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


def get_config():
    if os.getenv('FLASK_ENV') == 'development':
        return Development()
    return Production()


def create_app(config=None):
    """Application-factory pattern."""
    if config is None:
        config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)

    # Register extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    from .users.routes import users
    app.register_blueprint(users, url_prefix='/users')

    # Register custom jinja filters
    register_filters(app)

    return app
