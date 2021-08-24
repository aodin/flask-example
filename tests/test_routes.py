from http import HTTPStatus

import pytest

from app import db, mail
from app.users import User


@pytest.fixture
def user(context):
    user = User(email='user@example.com')
    db.session.add(user)
    db.session.commit()
    yield user


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
