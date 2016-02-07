#coding: pyxl
from pyramid.view import view_config
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
    return <frag>
        <react_poster user="{request.user}" wall="{request.user.wall_id}" role="{request.user.role}" roles="{[request.user.role]}" />
        <posts posts="{posts}" user="{request.user}" />
    </frag>
