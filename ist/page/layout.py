#coding: pyxl
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from ist.util import l
from ist.model.type import Page, User, AuthToken
from pyxl.html import *

@view_config(route_name='createpage', renderer='layout', permission='user')
def create_page(request):
    return <createpage />

# hozz létre egy oldalt az együttesednek, témádnak, cégednek, akárcsak más közösségi oldalakon. A leírásból legyen egyértelmű, miről szól az oldal.


@view_config(route_name='page_wall', renderer='layout')
def show_page(request):
    permalink = request.matchdict['permalink']
    try:
        page = Page.get_by_permalink(permalink)
    except Page.DoesNotExist:
        l.info('race condition, wow.')
        raise HTTPNotFound('no such page')

    posts = page.posts()
    if page.owner == request.user:
        poster = <react_poster user="{request.user}" wall="{page.wall_id}" role="{page.role}" />
    elif request.user:
        poster = <react_poster user="{request.user}" wall="{page.wall_id}" role="{request.user.role}" />
    else:
        poster = None

    content = <frag>\
        <div class="page_header">
            <react_pagethumbnail page={page} size="medium" />
            <h1 class="page_name">{page.name}</h1>
        </div>
        {poster}
        <posts posts="{posts}" user="{request.user}" />
    </frag>

    rightbar = <rightbar user="{request.user}">
        <div class="description">
            {page.description}
        </div>
        <a href="/{page.permalink}/edit">edit</a>
    </rightbar>

    return content, rightbar

@view_config(route_name='page_edit', renderer='layout')
def page_edit(request):

    try:
        page = Page.get_by_permalink(request.matchdict['permalink'])
    except Page.DoesNotExist:
        l.info('no page found, strange')
        raise HTTPNotFound('no such page')

    content = <frag>\
        <breadcrumb href="/{page.permalink}">Back to page wall</breadcrumb>
        <content_header>{page.name}</content_header>
        <react_restimagefield url="/api/page/{page.id}" image="{page.image or ''}" field="image" />
        <react_resttextfield url="/api/page/{page.id}" text="{page.description or ''}" field="description" label="What is this page about?"/>
    </frag>

    return content

@view_config(route_name='showallpages', renderer='layout')
def show_all_pages(request):
    pages = Page.select()

    a = <ul/>
    for page in pages:
        a.append_children([<li><a href="/{page.permalink}">{page.name}</a></li>])

    return a

@view_config(route_name='showmypages', renderer='layout', permission='user')
def show_my_pages(request):
    pages = request.user.pages()

    a = <ul/>
    for page in pages:
        a.append_children([<li><a href="/{page.permalink}">{page.name}</a></li>])

    return a
