from xhpy3.xhpy.pylib import  *
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from ist.util import l
from ist.model.type import Page, User, AuthToken

@view_config(route_name='createpage', renderer='xhpy', permission='user')
def create_page(request):
    return \
    <ui:layout user={request.user} >
        <ui:createpage />
    </ui:layout>

@view_config(route_name='showpage', renderer='xhpy')
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
        role = page.role_id
    else:
        role = request.user.role_id

    return \
    <ui:layout user={request.user}>
        <ui:showpage page={page} user={request.user} />
        <react:poster user={request.user} wall={page.wall_id} role={role} />
        <ui:posts posts={posts} user={request.user} />
    </ui:layout>

@view_config(route_name='showallpages', renderer='xhpy')
def show_all_pages(request):
    pages = Page.select()

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/show/%d"%page.id}>{page.name}</a></li>)
    
    return <ui:layout user={request.user}>{a}</ui:layout>

@view_config(route_name='showmypages', renderer='xhpy', permission='user')
def show_my_pages(request):
    pages = request.user.pages()

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/show/%d" % page.id}>{page.name}</a></li>)

    return <ui:layout user={request.user}>{a}</ui:layout>
