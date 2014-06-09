from .base import TwitterExplorerTestCase

from twitter_explorer.errors import DBFieldNotUniqueError
from twitter_explorer.models import User, TwitterConfig, db


class UserModelTestCase(TwitterExplorerTestCase):

    def test_create(self):
        username = 'Test 1'
        email = 'test_1@test.com'
        password = '123456'

        u1 = User.register(username, email, password)

        self.assertEquals(username, u1.username)
        self.assertEquals(email, u1.email)
        self.assertNotEquals(password, u1.password)

    def test_no_email_duplicates(self):
        username = 'Test 2'
        email = 'test_2@test.com'
        password = '123456'

        User.register(username, email, password)

        with self.assertRaises(DBFieldNotUniqueError) as err:
            User.register(username, email, password)
            self.assertEquals('email', err.field)
            self.assertEquals(email, err.value)

    def test_check_good_password(self):
        username = 'Test 3'
        email = 'test_3@test.com'
        password = '123456'

        user = User.register(username, email, password)

        self.assertTrue(user.check_password(password))

    def test_check_bad_password(self):
        username = 'Test 4'
        email = 'test_4@test.com'
        password = '123456'
        bad_password = 'bad password'

        user = User.register(username, email, password)

        self.assertFalse(user.check_password(bad_password))

    def test_get_user_by_email(self):
        username = 'Test 5'
        email = 'test_5@test.com'
        password = '123456'

        user = User.register(username, email, password)
        fetched_user = User.get_by_email(email)

        self.assertEqual(user, fetched_user)

    def test_get_not_existing_user(self):
        email = 'fake_email@test.com'
        fetched_user = User.get_by_email(email)
        self.assertIsNone(fetched_user)

    def test_get_user_id(self):
        username = 'Test 6'
        email = 'test_6@test.com'
        password = '123456'

        user = User.register(username, email, password)
        self.assertEqual(email, user.get_id())
        self.assertTrue(isinstance(user.get_id(), unicode))


class TwitterConfigModelTestCase(TwitterExplorerTestCase):

    def setUp(self):
        super(TwitterConfigModelTestCase, self).setUp()

        self.u = User.register('Test 7', 'test_7@test.com', '123456')

        self.key = '123'
        self.secret = '456'

    def tearDown(self):
        db.session.delete(self.u)
        db.session.commit()

    def test_create(self):
        conf = TwitterConfig.update(self.u, self.key, self.secret)

        self.assertEqual(self.key, conf.token_key)
        self.assertEqual(self.secret, conf.token_secret)

    def test_update(self):
        conf = TwitterConfig.update(self.u, self.key, self.secret)

        self.key = 'new_key'
        self.secret = 'new_secret'
        conf = TwitterConfig.update(self.u, self.key, self.secret)

        self.assertEqual(self.key, conf.token_key)
        self.assertEqual(self.secret, conf.token_secret)

    def test_get(self):
        conf1 = TwitterConfig.update(self.u, self.key, self.secret)
        conf2 = TwitterConfig.get_by_user(self.u)

        self.assertEquals(conf1, conf2)
        self.assertEqual(self.key, conf2.token_key)
        self.assertEqual(self.secret, conf2.token_secret)
        self.assertEqual(self.u.id, conf2.user_id)

    def test_get_no_existing(self):
        self.assertIsNone(TwitterConfig.get_by_user(self.u))
