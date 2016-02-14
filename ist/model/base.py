import json
from peewee import Model
from ist.util import *

from .dbconfig import db

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
