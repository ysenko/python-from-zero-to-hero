import unittest

from twitter_explorer import app
from twitter_explorer import application


class TwitterExplorerTestCase(unittest.TestCase):

    def setUp(self):
        application.load_config(app, env='test')
        self.app = app.test_client()

    def assert_response_200(self, resp):
        """Assert that application returned HTTP 200."""
        code = resp.status_code
        self.assertEqual(200, code,
                         'HTTP code 200 expexted, but %d received' % (code,))
