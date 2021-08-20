import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from app import create_app, db
from app.config import Database


class TestDatabase(Database):
    @classmethod
    def name(cls):
        return f'test_{cls.NAME}'


@pytest.fixture(scope='session')
def database():
    """
    Creating a testing database for the entire length of the testing session.
    This fixture will only be run once per testing session.
    """
    engine = create_engine(TestDatabase.connection_uri())
    if database_exists(engine.url):
        confirm = input(
            "\n\nThe test database already exists. It may have been left in "
            "an improper state because of previous exception.\n"
            "Type 'yes' if you would like to try deleting the test "
            "database '%s', or 'no' to cancel: " % TestDatabase.name()
        )
        if confirm == 'yes':
            drop_database(engine.url)
        else:
            raise Exception("Tests cancelled.")

    create_database(engine.url)
    yield engine
    drop_database(engine.url)


@pytest.fixture
def application(database):
    """Yields an application with an app context."""
    application = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': database.url
    })

    # An application context is required to handle requests or database queries
    with application.app_context():
        db.create_all()
        yield application
        # Remove any ongoing sessions; this will help prevent locking
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(application):
    """Yields a client that can send mock HTTP requests."""
    yield application.test_client()
