from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connection URI format: dialect+driver://username:password@host:port/database
# e.g. for PostGres postgresql://scott:tiger@localhost/mydatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
