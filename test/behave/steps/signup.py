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
    c.r = c.client.post('api/page', data={'name': name, 'description': desc})
    response = json.loads(c.r.text)
    if 'id' in response:
        c.page_id = response['id']
    if 'errors' in response:
        c.errors = response['errors']

@given('There is a page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    # FIXME: direct DB create
    create = c.client.post('api/page', data={'name': name, 'description': desc})
    t.assertEqual(200, create.status_code)
    response = json.loads(create.text)
    c.page_id = response['id']

@when('I modify the page description to "{new_desc}"')
def step_impl(c, new_desc):
    r = c.client.put('api/page/%d' % c.page_id, data={'description': new_desc})
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(new_desc, resp['description'])

@when('I delete the page')
def step_impl(c):
    c.r = c.client.delete('api/page/%d' % c.page_id)

@then('I can view the page called "{name}" with description "{desc}"')
def step_impl(c, name, desc):
    r = c.client.get('api/page/%d' % c.page_id)
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(name, resp['name'])
    t.assertEqual(desc, resp['description'])

@then('I cannot view the page')
def step_impl(c):
    r = c.client.get('api/page/%d' % c.page_id)
    t.assertEqual(404, r.status_code)

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

@when('I modify a nonexistent page')
def step_impl(c):
    c.r = c.client.put('api/page/12345', data={'description': 'something'})

@when('I delete a nonexistent page')
def step_impl(c):
    c.r = c.client.delete('api/page/12345')

@then('I get a {code} error')
def step_impl(c, code):
    t.assertEqual(int(code), c.r.status_code)

@then('I get a 200 OK')
def step_impl(c):
    t.assertEqual(200, c.r.status_code)

@then('Value of "{field}" is invalid because "{msg}"')
def step_impl(c, field, msg):
    t.assertEqual(field, c.errors[0]['field'])
    t.assertEqual(msg, c.errors[0]['error'])

@when('I post "{content}" on my wall')
def step_impl(c, content):
    c.r = c.client.post('api/post', data={'content':content, 'images':''})
    resp = json.loads(c.r.text)
    if 'id' in resp:
        c.post_id = resp['id']

@then('I can view the post with content "{content}"')
def step_impl(c, content):
    r = c.client.get('api/post/%d' % c.post_id)
    t.assertEqual(200, r.status_code)
    resp = json.loads(r.text)
    t.assertEqual(content, resp['content'])

@when('I post "{content}" on the wall of the page')
def step_impl(c, content):
    t.assertTrue(c.page_id)
    c.r = c.client.post('api/post', data={'content': content, 'images': '', 'wall': 'page:%d' % c.page_id})
    resp = json.loads(c.r.text)
    if 'id' in resp:
        c.post_id = resp['id']
        c.post = resp

@then('the post is on the wall of the page')
def step_impl(c):
    t.assertEqual(c.page_id, c.post['wall']['page']['id'])