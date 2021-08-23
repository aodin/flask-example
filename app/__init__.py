from flask import Flask

from .config import get_config
from .extensions import db, mail, migrate
from .filters import register_filters
from .routes import main
from .users.routes import users


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
    app.register_blueprint(main)
    app.register_blueprint(users, url_prefix='/users')

    # Register custom jinja filters
    register_filters(app)

    return app
