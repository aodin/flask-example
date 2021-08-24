from app import db
from app.users import User


class TestUser:
    """Test the User model."""
    def test_db(self, context):
        user = User(email='user@example.com')
        assert user.email == 'user@example.com'
        db.session.add(user)
        db.session.commit()
