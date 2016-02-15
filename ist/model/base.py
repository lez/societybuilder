import json
from peewee import Model, PostgresqlDatabase
from ist.util import *

db = PostgresqlDatabase(None)

def includeme(config):
    global db
    settings = config.get_settings()
    db.init(settings['database.db'], user=settings['database.username'], password=settings['database.password'], host=settings['database.host'], port=settings['database.port'])


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

