import click
from flask import Blueprint, render_template
from flask_mail import Message

from ..extensions import db, mail
from .models import User, normalize_email

users = Blueprint("users", __name__, cli_group="users")


@users.cli.command("create")
@click.argument("email")
@click.argument("password")
def create_user(email: str, password: str):
    """Create a new user with the given email and password."""
    email = normalize_email(email)
    user = User.query.filter_by(email=email).first()
    if user:
        raise click.BadParameter(
            f"A user with the email {user.email} already exists",
        )

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    click.echo(f"Created a user with the email {user.email}")


@users.route("/")
def list_users():
    """List all users."""
    results = db.session.scalars(db.select(User).order_by(User.id))
    return render_template("users/list.html", users=results)


@users.route("/<int:id>")
def user(id):
    """Example route that queries from the database."""
    user = db.get_or_404(User, id)
    return render_template("users/user.html", user=user)


@users.route("/<int:id>/mail", methods=["POST"])
def send_mail(id):
    """Route that ends an email."""
    user = db.get_or_404(User, id)

    msg = Message(
        "Hello",
        sender="sender@example.com",
        recipients=[user.email],
    )
    msg.body = "Testing the email"
    mail.send(msg)
    return "Message Sent"
