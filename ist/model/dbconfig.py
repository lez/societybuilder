from peewee import PostgresqlDatabase
from ..util import l

db = None

def includeme(config):
    global db
    settings = config.get_settings()

    # default ini database settings
    settings['database.db'] = settings.get('database.db', 'is')
    settings['database.username'] = settings.get('database.username', 'is')
    settings['database.password'] = settings.get('database.password', 'is')
    settings['database.host'] = settings.get('database.host', '127.0.0.1')
    settings['database.port'] = int(settings.get('database.port', 5432))

    l.info('using database "%s"' % settings['database.db'])
    db = PostgresqlDatabase(settings['database.db'], user=settings['database.username'], password=settings['database.password'], host=settings['database.host'], port=settings['database.port'])

