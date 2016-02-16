import json
import logging
from peewee import Model, PostgresqlDatabase
from pyramid.request import Request
from ist.util import *

db = PostgresqlDatabase(None)

class MyRequest(Request):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db.connect()
        self.add_finished_callback(self.finish)

    def finish(self, request):
        if not db.is_closed():
            db.close()

def includeme(config):

    settings = config.get_settings()

    if settings['peewee.debug']:
        pwlogger = logging.getLogger('peewee')
        pwlogger.setLevel(logging.DEBUG)

    db.init(settings['peewee.database'], user=settings['peewee.username'], password=settings['peewee.password'], host=settings['peewee.host'], port=settings['peewee.port'])

    config.add_request_method(lambda x: db, 'db', property=True)
    config.set_request_factory(MyRequest)


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

