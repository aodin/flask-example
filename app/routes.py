import datetime

import click
from flask import current_app
from flask import Blueprint, jsonify, render_template, redirect, url_for
from flask_mail import Message

from . import db, mail
from .files import Example
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


@main.route('/')
def index():
    """Index route with jinja context and filter examples."""
    context = {
        'now': datetime.datetime.now(),
        'number': 1200.34000,
    }
    return render_template('index.html', **context)


@main.route('/users/<int:id>')
def user(id):
    """Example route that queries from the database."""
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)


@main.route('/users/<int:id>/mail', methods=['POST'])
def send_mail(id):
    """Route that ends an email."""
    user = User.query.get_or_404(id)

    msg = Message(
        "Hello",
        sender="sender@example.com",
        recipients=[user.email],
    )
    msg.body = "Testing the email"
    mail.send(msg)
    return "Message Sent"


@main.route('/example.json', methods=['GET'])
def get_file():
    example = Example.load(current_app.config['S3_BUCKET'])
    return jsonify(example.mapping)


@main.route('/example.json', methods=['POST'])
def update_file():
    example = Example.load(current_app.config['S3_BUCKET'])
    example.update()
    example.save(current_app.config['S3_BUCKET'])
    return redirect(url_for('main.get_file'))
