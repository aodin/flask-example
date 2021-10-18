from flask import Flask

from .config import get_config
from .extensions import db, mail, migrate
from .filters import register_filters
from .routes import main
from .users.routes import users


def create_app(test_config=None, local_config='local_config.py'):
    """Create the application using an application-factory pattern."""
    app = Flask(__name__)
    app.config.from_object(get_config())
    if app.config.from_pyfile(local_config, silent=True):
        app.logger.info(f'Successfully loaded local config from {local_config}')

    # Test configuration must be set after local configuration changes
    if test_config:
        app.config.from_mapping(test_config)

    # NOTE: all config values should be set by this point
    # If there is a required config value, check it now
    assert app.config['SECRET_KEY'], "Please set a value for SECRET_KEY"
    assert app.config['S3_BUCKET'], "Please set a value for S3_BUCKET"

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
