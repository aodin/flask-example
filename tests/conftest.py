import pytest

from app import create_app, get_config, db
from app.config import Database


@pytest.fixture(scope='session')
def configuration():
    """
    Get the current configuration and modify it for testing. This fixture will
    only be run once per testing session.
    """
    config = get_config()
    config.TESTING = True
    config.WTF_CSRF_ENABLED = False

    # Create a test version of the current database URI
    db_instance = Database(config.SQLALCHEMY_DATABASE_URI)
    test_db = db_instance.for_testing()
    config.SQLALCHEMY_DATABASE_URI = str(test_db.url)

    # Create the test database - this does not need an application context
    test_db.create()
    yield config
    test_db.drop()


@pytest.fixture
def application(configuration):
    # Create an application using the test configuration
    application = create_app(configuration)

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
