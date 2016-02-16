import json
from peewee import Model, PostgresqlDatabase
from ist.util import *
import logging

db = PostgresqlDatabase(None)

def includeme(config):
    global db
    settings = config.get_settings()

    if settings['debug.peewee']:
        pwlogger = logging.getLogger('peewee')
        pwlogger.setLevel(logging.DEBUG)

    db.init(settings['db.database'], user=settings['db.username'], password=settings['db.password'], host=settings['db.host'], port=settings['db.port'])


class Base(Model):
    class Meta:
        database = db


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Base) and hasattr(obj, 'json'):
            return obj.json()
        l.debug('cannot encode object %r' % obj)
        return json.JSONEncoder.default(self, obj)


class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(message)

