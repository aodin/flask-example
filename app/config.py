import os
from pathlib import Path
import tempfile

from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database, drop_database


BASE_DIR = Path(__file__).resolve().parent.parent  # Project root


def get_config():
    if os.getenv('FLASK_ENV') == 'development':
        return Development()
    return Production()


class Database:
    def __init__(self, url):
        try:
            self.url = make_url(url)
        except Exception as e:
            raise Exception('Unable to parse SQLALCHEMY_DATABASE_URI') from e

    @property
    def name(self):
        return self.url.database

    def exists(self) -> bool:
        return False

    def create(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def for_testing(self, prefix='test_'):
        backend = self.url.get_backend_name()
        if backend == 'postgresql':
            test_url = self.url.set(database=f'{prefix}{self.url.database}')
            return PostgresDatabase(test_url)
        elif backend == 'sqlite':
            database = self.url.database
            # An empty database property is a special case for the sqlite
            # driver, representing an in-memory database.
            if not database:
                return InMemorySqliteDatabase(self.url)

            path = Path(database)
            test_path = str(path.with_name(f'{prefix}{path.name}'))
            return SqliteDatabase(self.url.set(database=test_path))
        raise Exception(f'A {backend} backend cannot be used for testing')


class PostgresDatabase(Database):
    def exists(self) -> bool:
        return database_exists(self.url)

    def create(self):
        if self.exists():
            confirm = input(
                "\n\nThe database '%s' already exists. It may have been left "
                "in an improper state because of a previous exception.\n"
                "Type 'yes' if you would like to try deleting the "
                "database, or 'no' to cancel: " % self.name
            )
            if confirm == 'yes':
                self.drop()
            else:
                raise Exception("Tests cancelled.")
        create_database(self.url)

    def drop(self):
        drop_database(self.url)


class InMemorySqliteDatabase(Database):
    def create(self):
        pass

    def drop(self):
        pass


class SqliteDatabase(Database):
    # TODO test if file already exists?

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
    WTF_CSRF_ENABLED = True

    # Connection format: dialect+driver://username:password@host:port/database
    # e.g. for PostGres postgresql://user:password@host/database
    # e.g. for local SQLite 'sqlite:////tmp/filename.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
