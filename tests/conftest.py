import pytest

from app import create_app


@pytest.fixture
def application():
    """Yields an application with an app context."""
    application = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })

    # An application context is required to handle requests or database queries
    with application.app_context():
        yield application


@pytest.fixture
def client(application):
    """Yields a client that can send mock HTTP requests."""
    with application.test_client() as client:
        yield client
