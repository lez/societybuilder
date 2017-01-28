import json
import logging

from peewee import Model
from playhouse.postgres_ext import PostgresqlExtDatabase

from pyramid.request import Request

from sb.util import *

db = PostgresqlExtDatabase(None)

class MyRequest(Request):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db.connect()
        self.add_finished_callback(self.close_database)

    def close_database(self, request):
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

    rest_required_fields = set()  # these fields are mandatory when creating a new instance
    rest_optional_fields = set()  # not mandatory, but valid fields
    rest_editable_fields = set()  # these fields are editable over rest by default

    def is_editable_by(self, user):
        raise NotImplementedError()

    @classmethod
    def rest_all_fields(cls):
        return list(
            set(cls.rest_required_fields)
                .union(set(cls.rest_optional_fields))
                .union(set(cls.rest_editable_fields))
        )

    class Meta:
        database = db


class ApiEncoder(json.JSONEncoder):
    def default(self, o):
        # our model class should be easy to encode
        if isinstance(o, Base) and hasattr(o, 'json'):
            return o.json()

        if isinstance(o, type(Ellipsis)):
            return None

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

