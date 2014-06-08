#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

import twitter_explorer

from twitter_explorer import app, models
from twitter_explorer.config.helpers import PROD_ENV, TEST_ENV, CUSTOM_CONFIG_VAR, load_config
from twitter_explorer.twitter_backend import auth


ENVS_MAP = {
    'test': PROD_ENV,
    'prod': TEST_ENV
}


manager = Manager(app)

db_manager = Manager(help='DB related commands.')
twitter_manager = Manager(help='Twitter related commands.')


@db_manager.option('-e', '--environment', default='prod',
                   choices=ENVS_MAP.keys(),
                   help='Environment type. Either "prod" or "test".')
def create(environment):
    """Create all required tables using prod settings."""
    load_config(app, env=environment)
    twitter_explorer.db = SQLAlchemy(app)
    models.create()


@db_manager.option('-e', '--environment', default='prod',
                   choices=ENVS_MAP.keys(),
                   help='Environment type. Either "prod" or "test".')
def drop(environment):
    """Create all required tables using prod settings."""
    load_config(app, env=environment)
    twitter_explorer.db = SQLAlchemy(app)
    models.drop()


@twitter_manager.command
def access_token():
    """Get Twitter access token."""
    auth.get_access_token(app.config['TWITTER_TOKEN_KEY'],
                          app.config['TWITTER_TOKEN_SECRET'])


manager.add_command('db', db_manager)
manager.add_command('twitter', twitter_manager)


if __name__ == '__main__':
    manager.run()
