from pyramid.view import view_config
from xhpy3.xhpy.pylib import *
from ist.view.element import *
from ist.model.user import Content

@view_config(route_name='home', renderer='xhpy')
def home(request):
    a = \
    <ui:layout user={request.user} >
        Home
    </ui:layout>

    if request.user:
        a.appendChild(<ui:creator />)

    return a

@view_config(route_name='test', renderer='xhpy')
def home(request):
    return \
    <ui:layout user={request.user} >
        <react:test initialCount=3 />
    </ui:layout>


@view_config(route_name='me', renderer='xhpy', permission='user')
def me(request):

    posts = request.user.posts()

    a = \
    <ui:layout user={request.user}>
        <ui:posts posts={posts}/>
    </ui:layout>

    return a
