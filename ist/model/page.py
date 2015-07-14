from peewee import IntegerField, ForeignKeyField, CharField, BooleanField
from .base import Base
from ist.model.user import User
from time import time

class Page(Base):
    created = IntegerField(default=time)
    user = ForeignKeyField(User, on_delete='CASCADE')  # TODO: owner
    name = CharField(max_length=30)
    description = CharField(max_length=250)
    owner_public = BooleanField(default=False)

    class Meta:
        db_table = 'pages'
