#!python
import json

import requests
import unittest

from behave import when, then, given

from importlib import import_module

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

@then('the testuser is able to log out')
def step_impl(c):
    r = c.client.logout()
    t.assertEqual(302, r.history[0].status_code)
    t.assertEqual(200, r.status_code)
    t.assertFalse(c.client.logged_in())


@given('I am signed in')
def step_impl(c):
    c.client.login('testuser', 'jelszo')


@given('{cls} records are cleaned from the database')
def step_impl(c, cls):
    types = import_module('ist.model.type')
    model = getattr(types, cls)
    model.delete().execute()


@when('I create a page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    create = c.client.post('api/page', data={'name': name, 'description': desc})
    t.assertEqual(200, create.status_code)
    response = json.loads(create.text)
    c.page_id = response['page']['id']


@when('I modify the page description to "{new_desc}"')
def step_impl(c, new_desc):
    r = c.client.put('api/page/%d' % c.page_id, data={'description': new_desc})
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(1, resp['success'])


@then('I can view the page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    r = c.client.get('api/page/%d' % c.page_id)
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(name, resp['name'])
    t.assertEqual(desc, resp['description'])

@then('I see {num} pages in page listing')
def step_impl(c, num):
    r = c.client.get('api/page')
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    c.page_listing = resp['pages']
    t.assertEqual(int(num), len(c.page_listing))

@then('The first page in the list is called "{name}"')
def step_impl(c, name):
    t.assertEqual(name, c.page_listing[0]['name'])

@then('The second page in the list is called "{name}"')
def step_impl(c, name):
    t.assertEqual(name, c.page_listing[1]['name'])
