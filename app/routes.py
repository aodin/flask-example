import click
from flask import Blueprint, render_template
from flask_mail import Message

from . import db, mail
from .models import User, normalize_email


main = Blueprint('main', __name__, cli_group='users')


@main.cli.command('create')
@click.argument('email')
def create_user(email: str):
    """Create a new user with the given email"""
    email = normalize_email(email)
    user = User.query.filter_by(email=email).first()
    if user:
        raise click.BadParameter(
            f"A user with the email {user.email} already exists",
        )

    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Created a user with the email {user.email}")


@main.route('/users/<int:id>')
def user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)


@main.route('/users/<int:id>/mail', methods=['POST'])
def send_mail(id):
    user = User.query.get_or_404(id)

    msg = Message(
        "Hello",
        sender="sender@example.com",
        recipients=[user.email],
    )
    msg.body = "Testing the email"
    mail.send(msg)
    return "Message Sent"
