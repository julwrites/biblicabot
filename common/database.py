# coding=utf-8

# Google App Engine Modules
from google.appengine.ext import db


def retrieve(region, name):
    return db.get(db.Key.from_path(region, name))


class BooleanProperty(db.BooleanProperty):
    def __init__(self, default=None, indexed=False):
        super(BooleanProperty, self).__init__(default=default, indexed=indexed)


class StringProperty(db.StringProperty):
    def __init__(self, default=None, indexed=False, multiline=False):
        super(StringProperty, self).__init__(
            default=default, indexed=indexed, multiline=multiline)


class DateTimeProperty(db.DateTimeProperty):
    def __init__(self, default=None, indexed=False):
        super(DateTimeProperty, self).__init__(
            default=default, indexed=indexed)


class Item(db.Model):
    def update():
        self.put()

    def id():
        return self.key()

    def name():
        return self.key().name