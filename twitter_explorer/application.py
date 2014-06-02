from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config.helpers import PROD_ENV, CUSTOM_CONFIG_VAR, load_config

# Create Flask app object.
app = Flask(__name__)

# Load app config.
load_config(app, env=PROD_ENV, custom_conf_var=CUSTOM_CONFIG_VAR)

# Initialize Flask-SQLAlchemy.
db = SQLAlchemy(app)
