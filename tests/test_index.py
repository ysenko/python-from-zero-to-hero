import mock

from twitter_explorer.models import User, TwitterConfig, db

from .base import TwitterExplorerTestCase


class IndexTestCase(TwitterExplorerTestCase):

    def setUp(self):
        super(IndexTestCase, self).setUp()

        self.username = 'Test 9'
        self.email = 'test_9@test.com'
        self.password = '123456'

        self.u = User.register(self.username,
                               self.email,
                               self.password)
        self.key = 'key'
        self.token = 'token'
        self.conf = TwitterConfig.update(self.u, self.key, self.token)

    def tearDown(self):
        db.session.delete(self.u)
        db.session.commit()

    def _login(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        self.app.post('/login', data=data, follow_redirects=True)

    def test_get_no_login(self):
        resp = self.app.get('/', follow_redirects=True)

        self.assertIn('Please sign in', resp.data)
        self.assertEqual(200, resp.status_code)

    def test_get(self):
        self._login()
        resp = self.app.get('/', follow_redirects=True)

        self.assertIn('search_query', resp.data)
        self.assertIn('Search', resp.data)
        self.assertIn('Search Results', resp.data)
        self.assertIn('No tweets found.', resp.data)

    @mock.patch('twitter_explorer.handlers.index.search.search',
                autospec=True)
    @mock.patch('twitter_explorer.handlers.index.auth.get_authorized_api',
                autospec=True)
    def test_get_search_results(self, api_mock, search_mock):
        search_mock.return_value = [
            {
                'text': 't1',
                'author': 'a1',
                'geo_data': 'c1,c1'
            },
            {
                'text': 't2',
                'author': 'a2',
                'geo_data': None
            },
        ]

        self._login()
        resp = self.app.post('/', data={'search_query': 'q1'},
                             follow_redirects=True)

        self.assertEqual(200, resp.status_code)
        for token in ('t1', 'a1', 'c1,c1', 't2', 'a2', 'No geo'):
            self.assertIn(token, resp.data)

        self.assertTrue(api_mock.called)
        api_obj_mock = api_mock(None, None, None, None)
        search_mock.assert_called_once_with(api_obj_mock, 'q1', count=50)
