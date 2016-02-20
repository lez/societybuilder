#!python
import json

import requests
import unittest

from behave import when, then, given


t = unittest.TestCase('__init__')


@when('the testuser signs up')
def step_impl(c):
    r = c.client.post('signup', data={'login': 'testuser', 'passwd': 'jelszo', 'email': 'test@jovilag.hu'})
    t.assertEqual(200, r.status_code)


@then('the testuser is able to log in')
def step_impl(c):
    r = c.client.login('testuser', 'jelszo')
    t.assertEqual(302, r.history[0].status_code)
    t.assertEqual(200, r.status_code)
    t.assertTrue(c.client.logged_in())
    assert('logout' in r.text)


@given('I am signed in')
def step_impl(c):
    c.client.login('testuser', 'jelszo')


@when('I create a page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    create = c.client.post('api/page', data={'name': name, 'description': desc})
    t.assertEqual(200, create.status_code)
    response = json.loads(create.text)
    c.page_id = response['page']['id']


@then('I can view the page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    r = c.client.get('api/page/%d' % c.page_id)
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(name, resp['name'])
    t.assertEqual(desc, resp['description'])
