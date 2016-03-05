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

    rest_editable_fields = set()
    rest_optional_fields = set()
    rest_required_fields = set()

    @classmethod
    def rest_all_fields(cls):
        return list(set(cls.rest_editable_fields).union(set(cls.rest_optional_fields)).union(set(cls.rest_required_fields)))

    class Meta:
        database = db


class ApiEncoder(json.JSONEncoder):
    def default(self, o):
        # our model class should be easy to encode
        if isinstance(o, Base) and hasattr(o, 'json'):
            return o.json()

        # encode iterables for cleaner api code
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        l.debug('cannot encode object %r' % o)
        return json.JSONEncoder.default(self, o)


class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(message)

