import logging

from flask.ext.sqlalchemy import SQLAlchemy

import twitter_explorer

from twitter_explorer import app
from twitter_explorer import application
from twitter_explorer import models


def setup_package():
    logging.info('package setup')
    application.load_config(app, env='test')
    # Reinitialize SQLAlchemy with new app settings.
    twitter_explorer.db = SQLAlchemy(app)
    models.create()


def teardown_package():
    logging.info('package teardown')
    models.drop()
