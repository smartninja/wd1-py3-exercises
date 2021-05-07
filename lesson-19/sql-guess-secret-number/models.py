import os
from sqla_wrapper import SQLAlchemy

# the replace method is needed due to this issue: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)  # a username must be unique! Two users cannot have the same username
    email = db.Column(db.String, unique=True)  # email must be unique! Two users cannot have the same email address
    secret_number = db.Column(db.Integer, unique=False)  # must NOT be unique across user objects
