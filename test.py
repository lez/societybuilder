from peewee import *
from ist.model.base import Base


class Image(Base):
    size = IntegerField()
    class Meta:
        db_table = 'imgs'

class Comment(Base):
    image = ForeignKeyField(Image, on_delete='CASCADE')
    msg = TextField()
    class Meta:
        db_table = 'comms'


#try:
#    Image.drop_table()
#except:
#    pass
#try:
#    Comment.drop_table()
#except:
#    pass


Image.create_table()
Comment.create_table()

i = Image(size=15)
i.save()
c = Comment(image=i, msg='hello')
c.save()


c.delete_instance(recursive=True, delete_nullable=True)
