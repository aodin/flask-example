from app import db
from app.models import User


class TestUser:
    """Test the User model."""
    # NOTE: the application fixture is required for database access

    def test_db(self, application):
        user = User(email='user@example.com')
        assert user.email == 'user@example.com'
        db.session.add(user)
        db.session.commit()
