#!python
import json

import unittest

import time
from behave import when, then, given
from importlib import import_module

t = unittest.TestCase('__init__')


@when('the testuser signs up')
def step_impl(c):
    r = c.client.post('api/signup', data={'login': 'testuser', 'passwd': 'jelszo', 'email': 'test@jovilag.hu'})
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

@when('I create a page with an invalid field')
def step_impl(c):
    c.r = c.client.post('api/page', data={'name': 'lust for life', 'description': 'you know', 'invalid_field': 'one more please'})

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

@when('I modify the page invalid_field to "{value}"')
def step_impl(c, value):
    c.r = c.client.put('api/page/%d' % c.page_id, data={'invalid_field': value})

@when('I modify the page without request body')
def step_impl(c):
    c.r = c.client.put('api/page/%d' % c.page_id, data={})

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

@given('I have a post')
def step_impl(c):
    c.r = c.client.post('api/post', data={'content': 'this is what I have', 'images':''})
    resp = json.loads(c.r.text)
    if 'id' in resp:
        c.post_id = resp['id']
        c.post = resp

@when('I comment "{comment}" on the post')
def step_impl(c, comment):
    c.r = c.client.post('api/comment', data={'item_type': 'post', 'item_id': c.post_id, 'comment': comment})
    c.comment = json.loads(c.r.text)

@then('the post has 1 comment "{comment}"')
def step_impl(c, comment):
    c.r = c.client.get('api/post/%d/comments' % c.post_id)
    resp = json.loads(c.r.text)
    t.assertIn('comments', resp)
    t.assertEqual(1, len(resp['comments']))
    t.assertEqual(comment, resp['comments'][0]['comment'])

@then('the comment author is me')
def step_impl(c):
    t.assertEqual(1, c.comment['user']['id'])

@then('the comment created time is just now')
def step_impl(c):
    current_time = int(time.time())
    t.assertGreater(current_time + 1, c.comment['created'])
    t.assertLess(current_time - 2, c.comment['created'])

@then('the comment modified time is null')
def step_impl(c):
    t.assertEqual(None, c.comment['modified'])

@given('I have a comment on the post')
def step_impl(c):
    c.r = c.client.post('api/comment', data={'comment': 'initial comment', 'item_id': c.post['id'], 'item_type': 'post'})
    resp = json.loads(c.r.text)
    if 'id' in resp:
        c.comment = resp
        c.comment_id = resp['id']
    t.assertEqual(200, c.r.status_code)

@when('I modify the comment to "{comment}"')
def step_impl(c, comment):
    c.r = c.client.put('api/comment/%d' % c.comment_id, data={'comment': comment})
    resp = json.loads(c.r.text)
    if 'id' in resp:
        c.comment = resp
        c.comment_id = resp['id']

@then('the comment modified time is just now')
def step_impl(c):
    current_time = int(time.time())
    t.assertGreater(current_time + 1, c.comment['modified'])
    t.assertLess(current_time - 2, c.comment['modified'])

@when('I query /api/me')
def step_impl(c):
    c.r = c.client.get('api/me')
    c.user = json.loads(c.r.text)

@then('my "{what}" is "{name}"')
def step_impl(c, what, name):
    t.assertEqual(name, c.user[what])

@when('I change my "{field}" to "{value}"')
def step_impl(c, field, value):
    c.r = c.client.put('api/me', data={field: value})
    c.user = json.loads(c.r.text)
