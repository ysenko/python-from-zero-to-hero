"""Database models."""

import logging
import re

from flask.ext.login import UserMixin
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from twitter_explorer import bcrypt, db, errors, login_manager


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


class User(db.Model, SafeMixin, UserMixin):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(256), nullable=False)

    def __str__(self):
        return (
            '<User id=%(id)s email=%(email)s username=%(username)s>' %
            {key: getattr(self, key) for key in ('id', 'username', 'email')}
        )

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
        logging.info('New user registered: %s', user)
        return user

    @classmethod
    def get_by_email(cls, email_addr):
        """Return a user object that corresponds to the given email or None if
        user was not found.
        """
        query = db.session.query(cls).filter(cls.email == email_addr)
        try:
            user = query.one()
            logging.debug('User found: %s', user)
            return user
        except NoResultFound:
            logging.debug('User was not found. Email address is: %s',
                          email_addr)
            return None

    def get_id(self):
        """We identify user by its email address."""
        return unicode(self.email)
