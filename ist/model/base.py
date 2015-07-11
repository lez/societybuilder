from peewee import PostgresqlDatabase, Model

db = PostgresqlDatabase('is', user='is', password='is', host='localhost', port=5432)

# uncomment to debug SQL queries:
# import logging
# pwlogger = logging.getLogger('peewee')
# pwlogger.setLevel(logging.DEBUG)

class Base(Model):
    class Meta:
        database = db

class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(message)
