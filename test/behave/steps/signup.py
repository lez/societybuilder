#!python
import requests
import unittest

t = unittest.TestCase('__init__')

@when('the testuser signs up')
def step_impl(context):
    r = requests.post('http://localhost/signup', data={'login': 'testuser', 'passwd': 'jelszo', 'email': 'test@jovilag.hu'}, allow_redirects=False)
    t.assertEqual(302, r.status_code)

@then('the testuser is able to log in')
def step_impl(context):
    r = requests.post('http://localhost/login', data={'login': 'testuser', 'passwd': 'jelszo'})
    assert(r.history[0].status_code == 302)
    t.assertEqual(200, r.status_code)
    assert('Hello,' in r.text)
