from pyramid.view import view_config
from xhpy3.xhpy.pylib import *
from ist.view.element import *

@view_config(route_name='home', renderer='xhpy')
def home(request):
    a = \
    <ui:layout user={request.user} >
        Home
    </ui:layout>

    if request.user:
        a.appendChild(<ui:poster />)

    return a

@view_config(route_name='test', renderer='xhpy')
def test(request):
    return \
    <ui:layout user={request.user}>
        x
    </ui:layout>


@view_config(route_name='me', renderer='xhpy', permission='user')
def me(request):

    posts = request.user.posts()

    a = \
    <ui:layout user={request.user}>
        <react:poster user={request.user} wall={request.user.wall_id} role={request.user.role_id} />
        <ui:posts posts={posts} user={request.user} />
    </ui:layout>

    return a
