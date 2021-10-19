from http import HTTPStatus

from flask_login import login_user

from app import db, mail
from .conftest import SECURE_PASSWORD


def test_login(client, user):
    """Test login."""
    response = client.get('/login')
    assert response.status_code == HTTPStatus.OK

    # A valid login should redirect
    response = client.post('/login', data=dict(
        email=user.email,
        password=SECURE_PASSWORD,
    ))
    assert response.status_code == HTTPStatus.FOUND
    assert len(response.headers.getlist('Set-Cookie')), \
        "A cookie was not set after a valid login"


def test_profile(client, user):
    """Test a route that requires authentication."""
    response = client.get('/profile')
    assert response.status_code == HTTPStatus.FOUND

    client.post('/login', data=dict(
        email=user.email,
        password=SECURE_PASSWORD,
    ))

    response = client.get('/profile')
    assert response.status_code == HTTPStatus.OK


def test_file(client, s3):
    response = client.get(f'/example.json')
    assert response.status_code == HTTPStatus.OK


def test_user(user, client):
    """Test the user route."""
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK


def test_mail(user, client):
    """Test the send mail route."""
    with mail.record_messages() as outbox:
        response = client.post(f'/users/{user.id}/mail')
        assert response.status_code == HTTPStatus.OK
        assert len(outbox) == 1
        assert outbox[0].subject == "Hello"
