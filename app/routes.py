import datetime

from flask import current_app
from flask import Blueprint, jsonify, render_template, redirect, url_for

from .files import Example


main = Blueprint('main', __name__, cli_group=None)


@main.route('/')
def index():
    """Index route with jinja context and filter examples."""
    context = {
        'now': datetime.datetime.now(),
        'number': 1200.34000,
    }
    return render_template('index.html', **context)


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
