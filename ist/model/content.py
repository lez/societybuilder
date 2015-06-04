from peewee import IntegerField, ForeignKeyField, TextField, CharField
from .base import Base
from ist.model.user import User
from time import time

class Content(Base):
    created = IntegerField(default=time)
    user = ForeignKeyField(User, on_delete='CASCADE')
    content = TextField(null=True)
    images = CharField()

    class Meta:
        db_table = 'contents'
