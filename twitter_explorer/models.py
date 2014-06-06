"""Database models."""

import logging
import re

from sqlalchemy.exc import DBAPIError, IntegrityError

from twitter_explorer import bcrypt, db, errors


DUPLICATE_ERROR_PATTERN = re.compile(
    r"Duplicate entry '(?P<value>.*)' for key '(?P<field>.*)'")


def create():
    """This helper creates all required tables."""
    db.create_all()


def drop():
    """Drop all tables."""
    db.drop_all()


class SafeMixin(object):

    @classmethod
    def _general_error_handler(cls, error, re_raise=True):
        """Error handler."""
        logging.error('Error occured while saving changes to the DB. '
                      'Rollback process started.', exc_info=error)
        db.session.rollback()

    _dbapi_error_handler = _general_error_handler

    @classmethod
    def _intergity_error_handler(cls, error):
        db.session.rollback()

        duplicate = DUPLICATE_ERROR_PATTERN.search(error.message)
        if duplicate is not None:
            raise errors.DBFieldNotUniqueError(**duplicate.groupdict())

    @classmethod
    def _on_complete(cls):
        """You can redefine this method in your calss to execute something
        after `safe_save()` regardless of its status.
        """
        pass

    @classmethod
    def safe_save(cls, commit=True):
        """Write all changes to the db in a safe way.

        Commit all changes to the DB if `commit`==True, otherwise makes a flush.
        """
        try:
            if commit:
                db.session.commit()
            else:
                db.session.flush()
        except IntegrityError as error:
            cls._intergity_error_handler(error)
        except DBAPIError as error:
            cls._dbapi_error_handler(error)
        except Exception, error:
            cls._general_error_handler(error)
        finally:
            cls._on_complete()


class User(db.Model, SafeMixin):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
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

    @classmethod
    def register(cls, username, email, raw_password):
        """Register a new user.

        :Parameters:
            - `username`: str
                Full name of the user.
            - `email`: str
                user's email address
            - `raw_password`: str
                User password.

        :Return:
            Instance of User model.
        """
        user = cls(username, email, raw_password)
        db.session.add(user)
        user.safe_save()
        return user
