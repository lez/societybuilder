from peewee import CharField, IntegerField, ForeignKeyField
from .base import Base
from ist.model.user import User

class Image(Base):
    item_id = IntegerField()
    item_type = CharField(max_length=16)
    created = IntegerField()
    user = ForeignKeyField(User, on_delete='CASCADE')
    extension = CharField(max_length=16)
    orig_filename = CharField()
    mime = CharField(max_length=32)
    size = IntegerField()
    width = IntegerField()
    height = IntegerField()
    tmp = IntegerField(default=1)
    path = CharField()  # dir1/dir2/<id>-<random>.<extension>

    class Meta:
        db_table = 'images'
