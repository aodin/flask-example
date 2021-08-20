from http import HTTPStatus

from app import db
from app.models import User


def test_user(client):
    """Test the user route."""
    user = User(email='user@example.com')
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
