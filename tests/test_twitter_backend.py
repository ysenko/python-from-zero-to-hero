"""Twitter backend related tests."""

import mock

from twitter_explorer.twitter_backend import auth

from .base import TwitterExplorerTestCase

class TwitterAuthTestCase(TwitterExplorerTestCase):

    def setUp(self):
        super(TwitterAuthTestCase, self).setUp()

        self.token_key = 'my_token_key'
        self.token_secret = 'my_token_secret'

        self.app_token_key = 'app_token_key'
        self.app_token_secret = 'app_token_secret'

    @mock.patch('twitter_explorer.twitter_backend.auth.tweepy.API', autospec=True)
    @mock.patch('twitter_explorer.twitter_backend.auth.tweepy.OAuthHandler', autospec=True)
    def test_get_authorized_api(self, auth_handler_mock, api_mock):
        res = auth.get_authorized_api(self.token_key,
                                       self.token_secret,
                                       self.app_token_key,
                                       self.app_token_secret)

        auth_handler_mock.assert_called_once_with(
            self.app_token_key,
            self.app_token_secret
        )

        auth_object_mock = auth_handler_mock(self.app_token_key,
                                             self.app_token_secret)
        auth_object_mock.set_access_token.assert_called_once_with(
            self.token_key,
            self.token_secret
        )

        api_mock.assert_called_once_with(auth_object_mock)

        api_object_mock = api_mock(auth_object_mock)
        self.assertTrue(api_object_mock.me.called)
        self.assertEqual(api_object_mock, res)
