import sys
from subprocess import PIPE, Popen
import time
import atexit
from pyramid.paster import bootstrap as pyramid_bootstrap

from ist import ROOT
from ist.model.type import *

def bootstrap(ini_filename=None):

    if not ini_filename:
        # get ini file from command line
        if len(sys.argv) < 2:
            print('usage: %s <config.ini>' % sys.argv[0])
            sys.exit(1)

        ini_filename = sys.argv[1]

    if ini_filename not in ('development.ini', 'testing.ini', 'production.ini'):
        print('invalid ini file:', sys.argv[1])
        sys.exit(2)

    env = pyramid_bootstrap(ini_filename)
    registry = env['registry']
    settings = registry.settings

    atexit.register(env['closer'])

    return env, registry, settings

def reset_schema(settings):
    if len(sys.argv) > 1 and sys.argv[1] == 'production.ini':
        raise Exception("I don't work in production environment")
   
    Popen(['psql', '-U', settings['peewee.username']], stdin=PIPE).communicate(
                     input=b'drop schema public cascade; create schema public;')

def create_tables():
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

def reset_db(settings):
    reset_schema(settings)
    create_tables()

def start_test_server():

    print("Starting test server in the background")
    status = Popen(['pserve', 'testing.ini', '--daemon', '--pid-file=testing.pid']).wait()

    if status == 2:
        print('*** pserve deamon is already running, using it for testing ***')
    else:
        print('************************')
        print('**  STARTING SERVER   **')
        print('************************')
        time.sleep(1)  # FIXME


def stop_test_server():
    print("Stopping test server")
    Popen(['pserve', 'testing.ini', '--stop-daemon', '--pid-file=%s' % os.path.join(ROOT, 'testing.pid')]).wait()

def run_behave():
    print("Starting behave tests")
    os.chdir(os.path.join(ROOT, 'test/behave'))
    sys.argv[0] = 'behave'
    Popen(sys.argv, env=os.environ.update({'PYTHONPATH': ROOT})).wait()

def run_cucumber():
    print("Starting cucumber tests")
    os.chdir(os.path.join(ROOT, 'frontend'))
    sys.argv[0] = './node_modules/.bin/cucumber.js'
    Popen(sys.argv, env=os.environ.update({'PYTHONPATH': ROOT})).wait()

def run_test(settings, cucumber=False, behave=False):
    start_test_server()
    if behave:
        reset_db(settings)
        run_behave()
    if cucumber:
        reset_db(settings)
        run_cucumber()
    stop_test_server()

