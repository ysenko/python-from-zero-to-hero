import unittest

from flask.ext.sqlalchemy import SQLAlchemy

import twitter_explorer

from twitter_explorer import app
from twitter_explorer import application
from twitter_explorer import models


class TwitterExplorerTestCase(unittest.TestCase):

    def setUp(self):
        application.load_config(app, env='test')
        self.app = app.test_client()
        # Reinitialize SQLAlchemy with new app settings.
        twitter_explorer.db = SQLAlchemy(app)
        models.create()

    def assert_response_200(self, resp):
        """Assert that application returned HTTP 200."""
        code = resp.status_code
        self.assertEqual(200, code,
                         'HTTP code 200 expexted, but %d received' % (code,))

    def tearDown(self):
        models.drop()
