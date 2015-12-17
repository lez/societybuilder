from pyramid.view import view_config
from xhpy3.xhpy.pylib import *
from ist.view.element import *

@view_config(route_name='home', renderer='layout')
def home(request):
    return 'home'

@view_config(route_name='test', renderer='string')
def test(request):
    return 'test'

@view_config(route_name='me', renderer='layout', permission='user')
def me(request):
    posts = request.user.posts()
    return \
    <x:frag>
        <react:poster user={request.user} wall={request.user.wall_id} role={request.user.role} roles={[request.user.role]}/>
        <ui:posts posts={posts} user={request.user} />
    </x:frag>
