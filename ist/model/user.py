import hashlib
import time
import re
from peewee import CharField, IntegerField, ForeignKeyField, TextField
from .base import Base, ValidationError
from ..util import *

class Content:
    pass

class User(Base):
    login = CharField(unique=True, max_length=50)
    fullname = CharField(max_length=100, null=True)
    email = CharField(unique=True, max_length=100)
    password_sha512 = CharField(max_length=132)
    salt = CharField(max_length=132)
    created_ts = IntegerField(null=False, default=time.time)

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

    def posts(self):
        contents = Content.select().where(Content.user==self)

        return contents

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
    def authenticate(cls, login, password):
        try:
            user = User.get(login=login)
        except User.DoesNotExist:
            raise User.AuthFailed()
        user.check_password(password)
        return user


def _token_expire():
    return int(time.time()) + 2 * 365 * 24 * 3600

class AuthToken(Base):
    token = CharField(unique=True, max_length=100)
    user = ForeignKeyField(User, on_delete='CASCADE')
    expire_ts = IntegerField(null=False, default=_token_expire)

    class Meta:
        db_table = 'auth_tokens'

class Content(Base):
    created = IntegerField(default=time.time)
    user = ForeignKeyField(User, on_delete='CASCADE')
    content = TextField(null=True)
    images = CharField()

    class Meta:
        db_table = 'contents'
