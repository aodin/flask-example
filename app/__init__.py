from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Default, Development


db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


def create_app(test_config=None):
    """Application-factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Development)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Allow tests to override any configuration
    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    return app
