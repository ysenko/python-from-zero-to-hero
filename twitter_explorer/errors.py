"""Errors."""


class BaseTwitterExplorerError(Exception):
    pass


class TwitterExplorerDBError(BaseTwitterExplorerError):
    pass


class DBFieldNotUniqueError(TwitterExplorerDBError):

    field = None
    value = None

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return '%(field)s: %(value)s already exists in the DB' % dict(self)
