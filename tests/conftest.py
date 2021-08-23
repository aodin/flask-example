import pytest

from app import create_app, db
from app.config import SqliteDatabase, PostgresDatabase


@pytest.fixture(scope='session')
def database():
    """
    Creating a testing database for the entire length of the testing session.
    This fixture will only be run once per testing session.
    """
    # test_db = SqliteDatabase('sqlite:////tmp/test.db')
    test_db = PostgresDatabase('postgresql+psycopg2://postgres:postgres@localhost:5432/test_db')
    test_db.create()
    yield test_db
    test_db.drop()


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
