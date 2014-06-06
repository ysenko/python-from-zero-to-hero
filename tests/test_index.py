import unittest

from .base import TwitterExplorerTestCase


@unittest.skip
class IndexTestCase(TwitterExplorerTestCase):

    PATH = '/'

    def test_get(self):
        """Assert that HTTP GET works correctly."""
        resp = self.app.get(self.PATH)
        self.assert_response_200(resp)
        self.assertIn('Hello World', resp.data)
        self.assertEqual('text/html; charset=utf-8', resp.content_type)
