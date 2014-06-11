import logging

from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from config.helpers import PROD_ENV, CUSTOM_CONFIG_VAR, load_config
from sentiment import sentiment_dict

# Create Flask app object.
app = Flask(__name__)

# Load app config.
load_config(app, env=PROD_ENV, custom_conf_var=CUSTOM_CONFIG_VAR)

# Initialize Flask-SQLAlchemy.
db = SQLAlchemy(app)

# Initialize BCrypt
bcrypt = Bcrypt(app)

# Flask login manager.
login_manager = LoginManager(app)

# AFINN lexicon file
afinn_file = open(app.config.get('AFINN_FILE_PATH'))
word_scores = sentiment_dict(afinn_file)

# Logging.
logging.basicConfig(level=logging.DEBUG)
