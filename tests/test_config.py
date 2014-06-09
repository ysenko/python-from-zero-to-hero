"""Tests for /config endpoint."""

from .base import TwitterExplorerTestCase

from twitter_explorer.models import User, TwitterConfig, db


class ConfigTestCase(TwitterExplorerTestCase):

    def setUp(self):
        super(ConfigTestCase, self).setUp()

        self.username = 'Test 8'
        self.email = 'test_8@test.com'
        self.password = '123456'

        self.u = User.register(self.username,
                               self.email,
                               self.password)

    def tearDown(self):
        db.session.delete(self.u)
        db.session.commit()

    def _login(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        self.app.post('/login', data=data, follow_redirects=True)

    def get_config_page_test(self):
        self._login()
        resp = self.app.get('/config')

        self.assertEqual(200, resp.status_code)
        self.assertIn('Twitter Configuration for %s' % (self.u.username,),
                      resp.data)
        self.assertIn('token_key', resp.data)
        self.assertIn('token_secret', resp.data)

    def post_config_page_test(self):
        self._login()
        token_key = 'cool_key'
        token_secret = 'cool_secret'

        resp = self.app.post('/config',
                             data={
                                 'token_key': token_key,
                                 'token_secret': token_secret
                             }, follow_redirects=True)
        self.assertIn('Twitter Configuration for %s' % (self.u.username,),
                      resp.data)
        self.assertIn(token_key, resp.data)
        self.assertIn(token_secret, resp.data)

