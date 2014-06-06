"""Tests for Login/logout and registration."""

from twitter_explorer import models

from .base import TwitterExplorerTestCase


class LoginTestCase(TwitterExplorerTestCase):

    def test_login(self):
        username = 'new_user_1'
        password = '123'
        email = 'new_user_1@test.com'

        models.User.register(username, email, password)

        resp = self.app.post(
            '/login',
            data={
                'email': email,
                'password': password
            },
            follow_redirects=True
        )

        self.assertNotIn('Please sign in', resp.data)
        self.assertEqual(200, resp.status_code)

    def test_login_invalid_password(self):
        username = 'new_user_2'
        password = '123'
        email = 'new_user_2@test.com'

        models.User.register(username, email, password)

        resp = self.app.post(
            '/login',
            data={
                'email': email,
                'password': 'wrong_password'
            },
            follow_redirects=True
        )

        self.assertIn('Please sign in', resp.data)
        self.assertEqual(200, resp.status_code)

    def test_logout(self):
        username = 'new_user_3'
        password = '123'
        email = 'new_user_3@test.com'

        models.User.register(username, email, password)

        resp = self.app.post(
            '/login',
            data={
                'email': email,
                'password': password
            },
            follow_redirects=True
        )
        self.assertNotIn('Please sign in', resp.data)

        resp = self.app.get('/logout', follow_redirects=True)
        self.assertIn('Please sign in', resp.data)
        self.assertEqual(200, resp.status_code)

        # Make sure we logged out.
        resp = self.app.get('/', follow_redirects=True)
        self.assertIn('Please sign in', resp.data)
        self.assertEqual(200, resp.status_code)
