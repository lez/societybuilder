#!python
import requests
import unittest

from behave import when, then

t = unittest.TestCase('__init__')

@when('the testuser signs up')
def step_impl(context):
    r = requests.post('http://localhost/signup', data={'login': 'testuser', 'passwd': 'jelszo', 'email': 'test@jovilag.hu'}, allow_redirects=False)
    t.assertEqual(302, r.status_code)

@then('the testuser is able to log in')
def step_impl(context):
    r = requests.post('http://localhost/login', data={'login': 'testuser', 'passwd': 'jelszo'})
    t.assertEqual(302, r.history[0].status_code)
    t.assertEqual(200, r.status_code)
    assert('logout' in r.text)
