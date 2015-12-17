from xhpy3.xhpy.pylib import  *
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from ist.util import l
from ist.model.type import Page, User, AuthToken

@view_config(route_name='createpage', renderer='layout', permission='user')
def create_page(request):
    return <ui:createpage />

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
        poster = <react:poster user={request.user} wall={page.wall_id} role={page.role} roles={request.user.roles}/>
    elif request.user:
        poster = <react:poster user={request.user} wall={page.wall_id} role={request.user.role} />
    else:
        poster = None

    content = <x:frag>
        <ui:showpage page={page} user={request.user} />
        {poster}
        <ui:posts posts={posts} user={request.user} />
    </x:frag>

    rightbar = <ui:rightbar user={request.user}>
        {page.description}
        <br/><a href={'/page/%d/edit' % page.id}>edit</a>
    </ui:rightbar>

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

    content = <x:frag>

    </x:frag>

    return content

@view_config(route_name='showallpages', renderer='layout')
def show_all_pages(request):
    pages = Page.select()

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/%d/show"%page.id}>{page.name}</a></li>)
    
    return a

@view_config(route_name='showmypages', renderer='layout', permission='user')
def show_my_pages(request):
    pages = request.user.pages()

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/%d/show" % page.id}>{page.name}</a></li>)

    return a
