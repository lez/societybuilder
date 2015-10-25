import json
from peewee import PostgresqlDatabase, Model
from ist.util import *

db = PostgresqlDatabase('is', user='is', password='is', host='localhost', port=5432)

# uncomment to debug SQL queries:
import logging
pwlogger = logging.getLogger('peewee')
pwlogger.setLevel(logging.DEBUG)

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
