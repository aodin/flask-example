import click
from flask import Blueprint, render_template

from . import db
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
