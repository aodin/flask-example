from http import HTTPStatus


def test_user(client):
    """Test the user route."""
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
