import hashlib
import time
import re
import os
import ist
from peewee import CharField, IntegerField, ForeignKeyField, TextField, Proxy, BooleanField, CompositeKey, PrimaryKeyField

from .base import Base, ValidationError
from ..util import *

ImageProxy = Proxy()

class User(Base):
    login = CharField(unique=True, max_length=50)
    fullname = CharField(max_length=100, null=True)
    email = CharField(unique=True, max_length=100)
    password_sha512 = CharField(max_length=132)
    salt = CharField(max_length=132)
    created_ts = IntegerField(null=False, default=time.time)
    image = ForeignKeyField(ImageProxy, on_delete='CASCADE', null=True)
    modified = IntegerField(default=time.time)
    about = TextField(null=True)

    rest_editable_fields = ('email', 'image', 'about')

    def check_password(self, password):
        hasher = hashlib.sha512()
        hasher.update(self.salt.encode())
        hasher.update(password.encode())
        if hasher.hexdigest() != self.password_sha512:
            raise self.AuthFailed('invalid password')

    def set_password(self, password):
        salt = random_string(132)
        hasher = hashlib.sha512()
        hasher.update(salt.encode())
        hasher.update(password.encode())
        self.password_sha512 = hasher.hexdigest()
        self.salt = salt

    def validate(self):
        if len(self.login) < 3:
            raise ValidationError('login', 'login name is too short')
        if len(self.login) > 20:
            raise ValidationError('login', 'login name is too long')
        if re.search(r'[^a-zA-Z0-9_-]', self.login):
            raise ValidationError('login', 'invalid character, use alphanumeric letters, \'_\' and \'-\'')
        if not re.search(r'^[a-zA-Z]', self.login):
            raise ValidationError('login', 'login name must start with an alphabetical letter')
        if not re.search(EMAIL_REGEX, self.email, flags=re.IGNORECASE):
            raise ValidationError('email', 'invalid email address, please use a conventional one')

    class Meta:
        db_table = 'users'

    class AuthFailed(Exception):
        pass

    @property
    def wall_id(self):
        return "user:%d" % self.id

    @property
    def role_id(self):
        return "user:%d" % self.id

    def posts(self):
        return Post.select().where(Post.wall==self.wall_id).order_by(-Post.id)

    def pages(self):
        return Page.select().where(Page.owner==self).order_by(-Page.id)

    @property
    def role(self):
        return get_role(self.role_id)

    @classmethod
    def get_by_token(cls, token):
        try:
            userauth = AuthToken.get(token=token)
        except AuthToken.DoesNotExist:
            l.info('token not found in database')
            raise User.DoesNotExist('token not found')
        if userauth.expire_ts < time.time():
            l.info('token expired')
            raise User.DoesNotExist('token expired')
        l.info('valid token')
        return userauth.user

    @classmethod
    def get_by_login(cls, login):
        try:
            user = User.select().where(User.login==login).get()
        except User.DoesNotExist:
            l.info('login %s does not exist' % login)
            raise
        return user

    @classmethod
    def authenticate(cls, login, password):
        try:
            user = User.get(login=login)
        except User.DoesNotExist:
            raise User.AuthFailed()
        user.check_password(password)
        return user

    def thumbnail(self, thumbnail='100x100'):
        if self.image:
            return self.image.uri(thumbnail=thumbnail)
        return None

    def json(self):
        return {
            'login': self.login,
            'id': self.id,
            'image': self.image.json() if self.image else None,
            'email': self.email,
        }

def _token_expire():
    return int(time.time()) + 2 * 365 * 24 * 3600

class AuthToken(Base):
    token = CharField(unique=True, max_length=100)
    user = ForeignKeyField(User, on_delete='CASCADE')
    expire_ts = IntegerField(null=False, default=_token_expire)

    class Meta:
        db_table = 'auth_tokens'

class Post(Base):
    created = IntegerField(default=time.time)
    modified = IntegerField(default=time.time)
    author = ForeignKeyField(User, on_delete='CASCADE')  # the user who is logged in when the post is sent
    wall = CharField(max_length=20)  # 'wall' is where posts are created.
    role = CharField(max_length=20)  # posts are created on behalf of a virtual personality, a so called 'role'. Currently it can be a user or a page.
    content = TextField(null=True)
    images = CharField()
    privacy = IntegerField(default=0)

    item_type = 'post'
    rest_required_fields = {'content', 'images'}
    rest_optional_fields = {'role', 'wall'}
    rest_editable_fields = {'content', 'images'}
    rest_collection_name = 'posts'

    def get_comments(self):
        return list(Comment.select().where(Comment.item_id==self.id, Comment.item_type==self.item_type))

    def get_images(self):
        if not self.images:
            return []
        ids = list(map(int, self.images.split(',')))
        images = list(Image.select().where(Image.id << ids))
        return images

    def get_image_ids(self):
        return self.images.split(',')

    def get_wall(self):
        return get_wall(self.wall)

    def get_role(self):
        return get_role(self.role)

    def json(self):
        return {
            'id': self.get_id(),
            'content': self.content,
            'images': self.get_images(),
            'comments': self.get_comments(),
            'created': self.created,
            'modified': self.modified,
            'wall': self.get_wall(),
            'role': self.get_role(),
        }

    def validate(self):
        if len(self.content) > 5000:
            yield {'field': 'content', 'error': 'Post is too long'}
        # FIXME
        # if len(self.image_ids) > 12:
        #     yield {'field': 'image_ids', 'error': 'Too many images'}


    class Meta:
        db_table = 'posts'

class Comment(Base):
    item_id = IntegerField(null=False)
    item_type = CharField(null=False, max_length=8)
    created = IntegerField(default=time.time)
    user = ForeignKeyField(User, on_delete='CASCADE')
    comment = TextField(null=True)
    image = ForeignKeyField(ImageProxy, null=True)
    modified = IntegerField(null=True)

    rest_collection_name = 'comments'

    rest_required_fields = {'comment', 'item_id', 'item_type'}
    rest_editable_fields = {'comment', 'image'}

    def json(self):
        return {
            'id': self.get_id(),
            'comment': self.comment,
            'created': self.created,
            'user': self.user.json(),
            'image': self.image.json() if self.image else None,
            'modified': self.modified,
        }

    def validate(self):
        if self.comment and len(self.comment) > 1000:
            yield {'field': 'comment', 'error': 'Comment is too long'}


    class Meta:
        db_table = 'comments'
        indexes = (
            (('item_type', 'item_id', 'id'), True),
        )


MEDIA_ROOT = ist.__path__[0]
MEDIA_DIR = 'media'

class Image(Base):
    created = IntegerField(default=time.time)
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

    def json(self):
        return {
            'id': self.id,
            'thumbnail': self.uri()
        }

    class Meta:
        db_table = 'images'

class Page(Base):
    created = IntegerField(default=time.time)
    modified = IntegerField(null=True)
    owner = ForeignKeyField(User)
    name = CharField(max_length=30)
    description = CharField(max_length=250)     # null = True?
    is_owner_public = BooleanField(default=False)
    is_public = BooleanField(default=True)
    image = ForeignKeyField(ImageProxy, null=True)
    permalink = CharField(unique=True, max_length=30)

    rest_editable_fields = {'name', 'description', 'is_owner_public', 'is_public', 'image'}
    rest_required_fields = {'name', 'description'}

    rest_collection_name = 'pages'

    @classmethod
    def get_by_permalink(self, permalink):
        return Page.select().where(Page.permalink==permalink).get()

    class Meta:
        db_table = 'pages'

    @property
    def wall_id(self):
        return 'page:%d' % self.id

    @property
    def role_id(self):
        return 'page:%d' % self.id

    @property
    def role(self):
        return get_role(self.role_id)

    def posts(self):
        return Post.select().where(Post.wall==self.wall_id).order_by(-Post.id)

    def json(self):
        return {
            'id': self.id,
            'image': self.image,
            'name': self.name,
            'description': self.description,
            'permalink': self.permalink,
        }

    def validate(self):
        if len(self.name) > 30:
            yield {'field': 'name', 'error': 'Name is too long'}

        if len(self.description) > 250:
            yield {'field': 'description', 'error': 'description is too long'}

    # FIXME: ValidationError


ImageProxy.initialize(Image)


# some model related helpers at the end

def get_wall(wall_id):
    type, id_ = wall_id.split(':')
    if type == 'page':
        wall = {'page': Page.get(id=id_)}
    elif type == 'user':
        wall = {'user': User.get(id=id_)}
    else:
        raise Exception('unknown wall type: %s' % type)
    return wall


def get_role(role_id):
    type, id_ = role_id.split(':')
    if type == 'page':
        page = Page.get(id=id_)
        role = {'id': role_id, 'name': page.name, 'image': page.image, 'page': page}
    elif type == 'user':
        user = User.get(id=id_)
        role = {'id': role_id, 'name': user.login, 'image': user.image, 'user': user}
    else:
        raise Exception('unknown role type: %s' % type)
    return role

