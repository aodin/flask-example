from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # Project root


class Database:
    ENGINE = 'postgresql'
    NAME = 'flask_postgres'
    USER = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = 5432

    @classmethod
    def name(cls):
        return cls.NAME

    @classmethod
    def connection_uri(cls):
        engine = cls.ENGINE
        user = cls.USER
        password = cls.PASSWORD
        host = cls.HOST
        port = cls.PORT
        if port:
            host = f'{host}:{port}'
        name = cls.name()
        return f'{engine}://{user}:{password}@{host}/{name}'


class Default:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''

    # Connection format: dialect+driver://username:password@host:port/database
    # e.g. for PostGres postgresql://user:password@host/database
    # e.g. for local SQLite 'sqlite:////tmp/test.db'
    SQLALCHEMY_DATABASE_URI = Database.connection_uri()


class Development(Default):
    """Development config."""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True

    # Mail options: https://pythonhosted.org/Flask-Mail/#configuring-flask-mail
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'sender@example.com'


class Production(Default):
    """Production config."""
    pass
