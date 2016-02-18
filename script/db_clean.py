import sys
import os
import traceback
from subprocess import PIPE

import subprocess
from pyramid.paster import bootstrap

from ist.model.base import Base
from ist.model.type import *

if len(sys.argv) < 2:
    print('usage: %s <config.ini>' % sys.argv[0])
    sys.exit(1)

env = bootstrap(sys.argv[1])
registry = env['registry']
settings = registry.settings

subprocess.Popen(['psql', '-U', settings['peewee.database']], stdin=PIPE).communicate(
                 input=b'drop schema public cascade; create schema public;')

User.create_table()
print('User table created')
AuthToken.create_table()
print('AuthToken table created')
Image.create_table()
print('Image table created')
Post.create_table()
print('Post table created')
Page.create_table()
print('Page table created')
Comment.create_table()
print('Comment table created')


env['closer']()
