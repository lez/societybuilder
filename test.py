from peewee import *
from sb.model.base import Base


class TestImage(Base):
    size = IntegerField()
    class Meta:
        db_table = 'imgs'

class TestComment(Base):
    image = ForeignKeyField(TestImage, on_delete='CASCADE')
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


TestImage.create_table()
TestComment.create_table()

i = TestImage(size=15)
i.save()
c = TestComment(image=i, msg='hello')
c.save()


c.delete_instance(recursive=True, delete_nullable=True)
