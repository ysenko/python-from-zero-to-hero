from .base import TwitterExplorerTestCase

from twitter_explorer.errors import DBFieldNotUniqueError
from twitter_explorer.models import User


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
