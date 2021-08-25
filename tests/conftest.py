import boto3
from moto import mock_s3
import pytest

from app import create_app, db, migrate
from app.config import Database
from app.files import Example


@pytest.fixture(scope='session')
def application():
    """
    Get the current application and modify it for testing. A test database
    will also be created, but the database schema will not be added.
    Most test functions should use the 'context' fixture, which will
    generate a blank database schema per function.
    """
    application = create_app(dict(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    ))

    # Create a test version of the current database URI
    db_instance = Database(application.config['SQLALCHEMY_DATABASE_URI'])
    test_db = db_instance.for_testing()
    application.config['SQLALCHEMY_DATABASE_URI'] = str(test_db.url)

    # Re-register the new URL with the database and migration extensions
    db.init_app(application)
    migrate.init_app(application, db)

    # Create the test database - this does not need an application context
    test_db.create()
    yield application
    test_db.drop()


@pytest.fixture(scope='session')
def s3(application):
    """Mock S3 bucket."""
    with mock_s3():
        conn = boto3.resource('s3', region_name=application.config['S3_REGION'])
        bucket = conn.create_bucket(Bucket=application.config['S3_BUCKET'])
        # Load any files that are required for the application
        Example({'timestamp': 1000}).save(bucket.name)
        yield bucket


@pytest.fixture
def context(application):
    """Create an application context with a valid database schema."""
    # An application context is required to handle requests or database queries
    with application.app_context():
        db.create_all()  # Create schema, such as the users table
        yield application
        # The following code will execute once all tests have finished
        db.session.remove()  # Remove ongoing sessions to help prevent locking
        db.drop_all()  # Drop all schema


@pytest.fixture
def client(context):
    """Yields a client that can send mock HTTP requests."""
    yield context.test_client()
