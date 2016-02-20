from util import Client

BASE_URL = 'http://localhost:81/'

def before_scenario(c, scenario):
    c.client = Client(BASE_URL)
