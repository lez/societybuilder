import os
from peewee import CharField, IntegerField, ForeignKeyField
from .base import Base
from ist.model.user import User
from time import time
import ist

MEDIA_ROOT = ist.__path__[0]
MEDIA_DIR = 'media'

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

    @property
    def real_path(self):
        return os.path.join(MEDIA_ROOT, MEDIA_DIR, self.path)

    def uri(self, *, thumbnail=None):
        if not thumbnail:
            return os.path.join('/', MEDIA_DIR, self.path)
        else:
            dirname = os.path.dirname(self.path)
            filename = os.path.basename(self.path)
            base, ext = os.path.splitext(filename)
            thumbnail_filename = base + '.' + thumbnail + ext
            return os.path.join('/', MEDIA_DIR, dirname, thumbnail_filename)

    class Meta:
        db_table = 'images'
