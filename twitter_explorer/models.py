"""Database models."""

import logging
import re

from flask.ext.login import UserMixin
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from twitter_explorer import bcrypt, db, errors, login_manager


log = logging.getLogger(__name__)

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
        log.error('Error occured while saving changes to the DB. '
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
        log.info('New user registered: %s', user)
        return user

    @classmethod
    def get_by_email(cls, email_addr):
        """Return a user object that corresponds to the given email or None if
        user was not found.
        """
        query = db.session.query(cls).filter(cls.email == email_addr)
        try:
            user = query.one()
            log.debug('User found: %s', user)
            return user
        except NoResultFound:
            log.debug('User was not found. Email address is: %s',
                          email_addr)
            return None

    def get_id(self):
        """We identify user by its email address."""
        return unicode(self.email)


class TwitterConfig(db.Model, SafeMixin):
    """Stores per-user Twitter configuration."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    token_key = db.Column(db.TEXT, nullable=False)
    token_secret = db.Column(db.TEXT, nullable=False)

    def __init__(self, user, token_key, token_secret):
        self.user_id = user.id
        self.token_key = token_key
        self.token_secret = token_secret

    @classmethod
    def get_by_user(cls, user):
        """Return Twitter configuration for the given user or if it does not
        exist None.
        """
        query = db.session.query(cls).filter(cls.user_id == user.id)
        try:
            config = query.one()
        except NoResultFound as err:
            log.debug('No configuration was found for %s', user)
            config = None

        return config

    @classmethod
    def update(cls, user, token_key, token_secret):
        """Update (or create) twitter configuration for passed user.

        :Parameters:
            - `user`: Instance of User model
            - `token_key`: str, Twitter access token key
            - `token_secret`: str, Twitter access token secret
        """
        query = (
            db.session.query(cls).filter(
                cls.user_id == user.id).with_for_update()
        )
        try:
            config = query.one()
            log.debug('Updating Twitter configuration for %s', user)
            config.token_key = token_key
            config.token_secret = token_secret

        except NoResultFound as err:
            log.info('Creaing a new Twitter configuration for %s', user)
            config = cls(user, token_key, token_secret)

        db.session.add(config)
        cls.safe_save()

        return config
