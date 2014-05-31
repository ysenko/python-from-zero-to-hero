from flask import Flask


CUSTOM_CONFIG_VAR = 'TWITER_EXPLORER_CONF'
TEST_ENV = 'test'
PROD_ENV = 'prod'


def load_config(app_obj, env='prod', custom_conf_var=None):
    """Load configuration for given Flask application.

    Load base configuration from config folder and then load custom config
    file (if exists).
    """
    assert env in (TEST_ENV, PROD_ENV), \
        'You must be in either test or prod environment.'
    if env == 'prod':
        app.config.from_pyfile('config/config.py', silent=False)
    else:
        app.config.from_pyfile('config/test_config.py', silent=False)

    if custom_conf_var is not None:
        app.config.from_envvar(custom_conf_var, silent=True)


app = Flask(__name__)
load_config(app, env=PROD_ENV, custom_conf_var=CUSTOM_CONFIG_VAR)
