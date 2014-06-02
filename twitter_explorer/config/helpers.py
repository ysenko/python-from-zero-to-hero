"""Configuration helpers."""

CUSTOM_CONFIG_VAR = 'TWITER_EXPLORER_CONF'
TEST_ENV = 'test'
PROD_ENV = 'prod'


def load_config(app, env='prod', custom_conf_var=None):
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

    # Set SQLALCHEMY_DATABASE_URI which is required by Flask-SQLAlchemy.
    app.config.setdefault('SQLALCHEMY_DATABASE_URI',
                          _get_sqlalchemy_database_url(app))


def _get_sqlalchemy_database_url(app):
    """Properly set SQLALCHEMY_DATABASE_URI config var."""
    tmpl = 'mysql+pymysql://%(username)s:%(password)s@%(host)s:%(port)s/%(db_name)s'
    args = {
        'username': app.config['DB_USER'],
        'password': app.config['DB_PASSWORD'],
        'host': app.config['DB_HOST'],
        'port': app.config['DB_PORT'],
        'db_name': app.config['DB_NAME']
    }
    return tmpl % args
