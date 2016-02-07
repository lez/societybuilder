#coding: pyxl
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from ist.util import l
from ist.model.type import Page, User, AuthToken

@view_config(route_name='createpage', renderer='layout', permission='user')
def create_page(request):
    return <createpage />

@view_config(route_name='showpage', renderer='layout')
def show_page(request):
    id_ = request.matchdict['id']
    try:
        id_ = int(id_)
    except TypeError:
        raise HTTPNotFound('invalid_id')
    try:
        page = Page.get(id=id_)
    except Page.DoesNotExist:
        raise HTTPNotFound('no such page')

    posts = page.posts()
    if page.owner == request.user:
        poster = <react_poster user="{request.user}" wall="{page.wall_id}" role="{page.role}" roles="{request.user.roles}" />
    elif request.user:
        poster = <react_poster user="{request.user}" wall="{page.wall_id}" role="{request.user.role}" />
    else:
        poster = None

    content = <frag>
        <showpage page="{page}" user="{request.user}" />
        {poster}
        <posts posts="{posts}" user="{request.user}" />
    </frag>

    rightbar = <rightbar user="{request.user}">
        {page.description}
        <br/><a href="/page/{page.id}/edit">edit</a>
    </rightbar>

    return content, rightbar

@view_config(route_name='editpage', renderer='layout')
def edit_page(request):
    id_ = request.matchdict['id']
    try:
        id_ = int(id_)
    except TypeError:
        raise HTTPNotFound('invalid_id')
    try:
        page = Page.get(id=id_)
    except Page.DoesNotExist:
        raise HTTPNotFound('no such page')

    content = "wip"

    return content

@view_config(route_name='showallpages', renderer='layout')
def show_all_pages(request):
    pages = Page.select()

    a = <ul/>
    for page in pages:
        a.append_children([<li><a href="/page/{page.id}/show">{page.name}</a></li>])
    
    return a

@view_config(route_name='showmypages', renderer='layout', permission='user')
def show_my_pages(request):
    pages = request.user.pages()

    a = <ul/>
    for page in pages:
        a.append_children([<li><a href="/page/{page.id}/show">{page.name}</a></li>])

    return a
