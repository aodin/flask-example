import os
from pathlib import Path
import tempfile

from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database, drop_database

BASE_DIR = Path(__file__).resolve().parent.parent  # Project root


class Database:
    def __init__(self, url):
        self.url = make_url(url)

    @property
    def name(self):
        return self.url.database

    def exists(self) -> bool:
        return False

    def create(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError


class PostgresDatabase(Database):
    def exists(self) -> bool:
        return database_exists(self.url)

    def create(self):
        if self.exists():
            confirm = input(
                "\n\nThe database already exists. It may have been left in "
                "an improper state because of previous exception.\n"
                "Type 'yes' if you would like to try deleting the "
                "database '%s', or 'no' to cancel: " % self.name
            )
            if confirm == 'yes':
                self.drop()
            else:
                raise Exception("Tests cancelled.")
        create_database(self.url)

    def drop(self):
        drop_database(self.url)


class SqliteDatabase(Database):
    def create(self):
        self.fd, self.path = tempfile.mkstemp()

    def drop(self):
        # Delete the temporary sqlite database after the tests have completed
        os.close(self.fd)
        os.unlink(self.path)


class Default:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''
    S3_BUCKET = ''

    # Connection format: dialect+driver://username:password@host:port/database
    # e.g. for PostGres postgresql://user:password@host/database
    # e.g. for local SQLite 'sqlite:////tmp/test.db'
    SQLALCHEMY_DATABASE_URI = ''


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
