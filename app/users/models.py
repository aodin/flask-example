from __future__ import annotations
import secrets

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, login_manager
from ..models import TimestampMixin


UNUSABLE_PASSWORD_PREFIX = "!UNUSABLE/"


def normalize_email(email: str) -> str:
    """Normalize the email address by lowercasing the domain."""
    try:
        name, domain = email.strip().rsplit("@", 1)
        email = name + "@" + domain.lower()
    except ValueError:
        pass
    return email


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False, default="")

    permissions: Mapped[list["Permission"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.email}>"

    @property
    def has_usable_password(self) -> bool:
        return bool(self.password) and not self.password.startswith(
            UNUSABLE_PASSWORD_PREFIX
        )

    @property
    def has_unusable_password(self) -> bool:
        return bool(self.password) and self.password.startswith(
            UNUSABLE_PASSWORD_PREFIX
        )

    def set_password(self, password: str):
        """
        Explicitly set the arguments to generate the password hash, in case
        the defaults change in the future.
        """
        self.password = generate_password_hash(
            password,
            method="pbkdf2:sha256",
            salt_length=16,
        )

    def set_unusable_password(self):
        self.password = UNUSABLE_PASSWORD_PREFIX + secrets.token_urlsafe(16)

    def check_password(self, password: str) -> bool:
        if self.has_unusable_password:
            return False
        return check_password_hash(self.password, password)

    def is_active(self) -> bool:
        """Overwrites the default is_active method of UserMixin."""
        return self.has_usable_password


@login_manager.user_loader
def load_user(id: str) -> User | None:
    return User.query.filter_by(id=id).first()


class Permission(db.Model):
    """A permission for a User."""

    __tablename__ = "permissions"
    __table_args__ = {"schema": "private"}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="permissions")

    def __repr__(self):
        return f"Permission(id={self.id!r}, user_id={self.user_id!r}), action={self.action!r})"
