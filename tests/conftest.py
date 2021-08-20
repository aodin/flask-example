import pytest

from app import create_app, db


@pytest.fixture
def application():
    """Yields an application with an app context."""
    application = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost/flask_postgres_test'
    })

    # An application context is required to handle requests or database queries
    with application.app_context():
        db.create_all()
        yield application
        # Remove any ongoing sessions, this will help prevent locking
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(application):
    """Yields a client that can send mock HTTP requests."""
    with application.test_client() as client:
        yield client
