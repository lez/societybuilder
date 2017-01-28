from util import Client

BASE_URL = 'http://localhost:81'

def before_scenario(c, scenario):
    c.client = Client(BASE_URL)

def before_all(c):
    from sb.model.base import db
    db.init('is_test', user='is', password='is', host='127.0.0.1', port=5432)
    c.db = db