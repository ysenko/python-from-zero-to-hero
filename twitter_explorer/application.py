from flask import Flask


CUSTOM_CONFIG_VAR = 'TWITTER_EXPLORER_CONF'


def load_config(app_obj, custom_conf_var=None):
    """Load configuration for given Flask application.

    Load base configuration from config folder and then load custom config
    file (if exists).
    """
    app.config.from_pyfile('config/config.py', silent=False)
    if custom_conf_var is not None:
        app.config.from_envvar(custom_conf_var, silent=True)


app = Flask(__name__)
load_config(app, CUSTOM_CONFIG_VAR)
