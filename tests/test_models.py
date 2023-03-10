from app import db
from app.users import User, Permission

from .conftest import SECURE_PASSWORD


class TestUser:
    """Test the User model."""

    def test_db(self, context):
        user = User(email="user@example.com")
        user.set_unusable_password()
        assert user.email == "user@example.com"
        db.session.add(user)
        db.session.commit()
        assert user.id is not None, "The new user's id was not set"
        assert not user.is_active(), "A user without a password should be inactive"

        saved = db.session.get(User, user.id)
        assert user.created_at is not None, "The user's created timestamp should be set"

        saved.set_password(SECURE_PASSWORD)
        db.session.commit()
        assert (
            saved.updated_at is not None
        ), "The user's updated timestamp should be set"
        assert saved.is_active(), "Users with usuable passwords should be active"

        assert saved.check_password(SECURE_PASSWORD)

        # Add a Permission
        publish = Permission(user=user, action="Publish")
        db.session.add(publish)
        db.session.commit()
        assert publish.id is not None, "The new permission's id was not set"

        # Relationships will be queried when accessed
        assert len(user.permissions) == 1
