"""Database models."""

from twitter_explorer import db, bcrypt


def create():
    """This helper creates all required tables."""
    db.create_all()


def drop():
    """Drop all tables."""
    db.drop_all()


class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = bcrypt.generate_password_hash(raw_password)

    def check_password(self, candidate):
        """Check whether password matches.

        :Return:
            True if matches, otherwise False.
        """
        return bcrypt.check_password_hash(self._password, candidate)
