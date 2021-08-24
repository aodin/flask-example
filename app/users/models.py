from sqlalchemy import Column, Integer, String

from ..extensions import db


def normalize_email(email: str) -> str:
    """Normalize the email address by lowercasing the domain."""
    try:
        name, domain = email.strip().rsplit('@', 1)
        email = name + '@' + domain.lower()
    except ValueError:
        pass
    return email


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
