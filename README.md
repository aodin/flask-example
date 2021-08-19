Flask + PostGres
====

Install [Poetry](https://python-poetry.org/docs/#installation) and then run:

    poetry install

A virtual environment can then be activated with:

    poetry shell

Requirements are generated with:

    poetry export -f requirements.txt --output requirements.txt --without-hashes


If you don't wast to use Poetry, create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) locally with:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If you later decide to use poetry, it should already be tied to the local virtual environment. This is specified in the `poetry.toml` file, which was created with:

    poetry config virtualenvs.in-project true --local


#### ARM64

Some packages require special handling for ARM64.

For `psycopg`:

```sh
export PATH=/opt/local/lib/postgresql13/bin:$PATH
python -m pip install -U psycopg2 --no-cache
```


## Tutorials

https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

https://github.com/mjhea0/flaskr-tdd

https://flask-sqlalchemy.palletsprojects.com/en/2.x/

  * https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


### Quickstart

```py
from flask_postgres.app import db

db.create_all()  # Only run when schema changes

from flask_postgres.app import User
admin = User(email='admin@example.com')
db.session.add(admin)
db.session.commit()

User.query.first()
User.query.all()
User.query.filter_by(email='admin@example.com').first()
User.query.filter(User.email.ilike('%@EXAMPLE.COM')).all()

query = User.query.filter(User.email.ilike('@EXAMPLE.COM'))
print(query)
print(query.statement)

db.session.add_all([
    User(email='user@example.com'),
    User(email='client@example.com'),
    User(email='guest@example.com'),
])

db.session.query(User).filter_by(email='admin@example.com').first()
db.session.query(User).order_by(User.id)[1:3]
print(db.session.query(User).order_by(User.id))
```

#### Using PostGres

With `psql`:

    CREATE DATABASE flask_postgres;
