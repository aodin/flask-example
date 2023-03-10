from app.users.routes import create_user
from .conftest import SECURE_PASSWORD


def test_create_user(context):
    runner = context.test_cli_runner()
    result = runner.invoke(create_user, ["user@example.com", SECURE_PASSWORD])
    assert "Created a user" in result.output
