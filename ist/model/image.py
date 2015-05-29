from peewee import CharField, IntegerField, ForeignKeyField
from .base import Base
from ist.model.user import User
from time import time

class Image(Base):
    created = IntegerField(default=time)
    user = ForeignKeyField(User, on_delete='CASCADE')
    orig_filename = CharField()
    mime = CharField(max_length=32)
    size = IntegerField()
    width = IntegerField()
    height = IntegerField()
    tmp = IntegerField(default=1)
    path = CharField()  # dir1/dir2/<id>-<random>.<extension>

    @property
    def extension(self):
        EXTS = {
            'image/png': 'png',
            'image/jpeg': 'jpg',
            'image/gif': 'gif',
        }
        return EXTS[self.mime]

    class Meta:
        db_table = 'images'
