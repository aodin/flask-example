Flask Example
====

An example [Flask](https://flask.palletsprojects.com/en/2.0.x/) application with the following goals:

- [X] Use standard CLI commands, such as `flask run` and `flask db`
- [X] Separate development and production configurations set by `FLASK_ENV`
- [x] `pytest` can run from the project root
- [x] Uses database migrations
- [ ] Uses database migrations in testing
- [x] Can use PostGres for testing
- [x] Creates a separate PostGres database for testing
- [ ] Runs PostGres tests in transactions
- [ ] Can use sqlite for testing
- [ ] Database configuration can be set without modifying committed files
- [X] Example Blueprint usage
- [X] Custom CLI commands
- [X] Can send email from routes and test them via pytest
- [ ] Example S3 bucket access and testing
- [ ] Example Flask-Login usage and testing
- [ ] Example timestamp model mixin
- [ ] Custom Jinja function examples
- [ ] Middleware and global template context variable examples


## Quickstart

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


#### Database Configuration

The database configuration is set in [config.py](app/config.py).

Some systems may require the installation of `psycopg2-binary` instead of the `psycopg2` package.


## Tutorials

* Example applications
  - [Flask Mega-Tutorial application](https://github.com/miguelgrinberg/microblog)
  - [Test-Driven Development application](https://github.com/mjhea0/flaskr-tdd)
  - [RealPython application using migrations](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/)
* Configuration
  - [Flask API](https://flask.palletsprojects.com/en/2.0.x/config/)
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
from app import db, create_app, User

app = create_app()

db.create_all(app=create_app())

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
