#coding: pyxl
from pyramid.view import view_config

from ist.model.type import Post
from ist.view.element import *
from pyxl.html import *

@view_config(route_name='home', renderer='layout')
def home(request):
    posts = Post.select().order_by(-Post.created)
    return <frag>\
        <if cond={request.user}>
            <react_poster user="{request.user}" wall="{request.user.wall_id}" role="{request.user.role}" roles="{[request.user.role]}" />
        </if>
        <posts posts="{posts}" user="{request.user}" />
    </frag>

@view_config(route_name='test', renderer='string')
def test(request):
    return 'test'

@view_config(route_name='wall', renderer='layout', permission='user')
def me(request):
    login = request.matchdict['login']
    user = User.get_by_login(login)
    posts = user.posts()
    return <frag>
        <react_poster user="{request.user}" wall="{user.wall_id}" role="{request.user.role}" roles="{[request.user.role]}" />
        <posts posts="{posts}" user="{request.user}" />
    </frag>
