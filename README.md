Flask Example
====

An example [Flask](https://flask.palletsprojects.com/en/2.0.x/) application with the following goals:

- [X] Dependency management using [poetry](https://python-poetry.org)
- [X] Use standard CLI commands, such as `flask run` and `flask db`
- [X] Separate development and production configurations set by `FLASK_ENV`
- [x] `pytest` can run from the project root
- [x] Uses database migrations
- [ ] Uses database migrations in testing
- [x] Can use PostGres for testing
- [x] Creates a separate PostGres database for testing
- [ ] Runs PostGres tests in transactions
- [X] Can use sqlite for testing
- [X] Database configuration can be set without modifying committed files
- [X] Example Blueprint usage
- [X] Custom CLI commands
- [X] Can send email from routes and test them via pytest
- [X] Example S3 bucket access and testing
- [ ] Example Flask-Login usage and testing
- [ ] Example timestamp model mixin
- [X] Custom Jinja function examples
- [ ] Middleware and global template context variable examples


## Quickstart

Requires Python 3.9+.

Create a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the development server:

    FLASK_ENV=development flask run


Run the test suite:

    pytest


### Poetry

To use Poetry for dependency management, first install [Poetry](https://python-poetry.org/docs/master/#installation) 1.1.8+.

A shell can be activated with:

    poetry shell

And dependencies installed with:

    poetry install

A `requirements.txt` file can be generated with:

    poetry export -f requirements.txt --output requirements.txt --without-hashes


#### Database Configuration

The database URL can be set in a local configuration file located at `app/local_config.py`. This file will be ignored by git. It should be a valid python module, with uppercase keys for any values that should be added to the Flask configuration. Such as:

```py
SECRET_KEY = 'insecure-do-not-use-me'
S3_BUCKET = 'example-bucket'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/sqlite.db'
```

Some systems may require the installation of `psycopg2-binary` instead of the `psycopg2` package.


## Tutorials

* Example applications
  - [Flask Mega-Tutorial application](https://github.com/miguelgrinberg/microblog)
  - [Test-Driven Development application](https://github.com/mjhea0/flaskr-tdd)
  - [RealPython application using migrations](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/)
* Flask Configuration
  - [API/docs](https://flask.palletsprojects.com/en/2.0.x/config/)
  - [Default values](https://github.com/pallets/flask/blob/main/src/flask/app.py#L323)
* [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - [Contexts](https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/)
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* Testing with PostGres
  - [Testing with pytest and postgres](http://alexmic.net/flask-sqlalchemy-pytest/)
  - [Testing with pytest and sqlalchemy](https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/)
  - [Creating a PostGres database with SQLAlchemy](https://stackoverflow.com/a/8977109/868330)
  - [Creating a PostGres database with SQLAlchemy Utils](https://github.com/kvesteri/sqlalchemy-utils)
  - [How Django creates a test database](https://github.com/django/django/blob/ca9872905559026af82000e46cde6f7dedc897b6/django/db/backends/base/creation.py)
* [Example timestamp mixin](https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/#model-mixins)
* Pytest fixtures
  - [Scopes](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-scopes)
  - [Request](https://medium.com/opsops/deepdive-into-pytest-parametrization-cb21665c05b9)
* [Sending Email](https://pythonhosted.org/Flask-Mail/)
* Custom CLI
  - [Use closures to pass app to cli commands decorators](https://github.com/miguelgrinberg/microblog/blob/main/app/cli.py)
* Testing S3
  - [moto](https://github.com/spulec/moto)
  - [With mocks](https://www.sanjaysiddhanti.com/2020/04/08/s3testing/)


#### Example Database Operations

Using an application-factory context:

```py
from app import db, create_app
from app.users import User

app = create_app()

db.create_all(app=app)

# Either use the following with statements, or push an app context with:
# app.app_context().push()

with app.app_context():
    admin = User(email='admin@example.com')
    db.session.add(admin)
    db.session.commit()

with app.app_context():
    User.query.all()
```


#### Using Migrations

Get a list of flask commands:

    flask db --help

Add migrations to an app (only need to run once):

    flask db init

Create a new migration:

    flask db migrate -m "Initial migration."

Perform migrations:

    flask db upgrade


#### Testing Email

Run a local SMTP server:

    python -m smtpd -n -c DebuggingServer localhost:1025
