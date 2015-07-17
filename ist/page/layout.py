from xhpy3.xhpy.pylib import  *
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.auth import require_login, check_login
from ist.view.element import *
from ist.util import l
from ist.model.page import Page

@view_config(route_name='createpage', renderer='xhpy')
@require_login
def create_page(request):
    return \
    <ui:layout user={request.current_user} >
        <ui:createpage />
    </ui:layout>

@view_config(route_name='showpage', renderer='xhpy')
@check_login
def show_page(request):
    id_ = request.matchdict['id']
    try:
        id_ = int(id_)
    except TypeError:
        raise HTTPNotFound('invalid_id')
    try:
        page = Page.get(id=id_)
    except Page.DoesNotExist:
        raise HTTPNotFound('nosuchpage')

    return \
    <ui:layout user={request.current_user} >
        <ui:showpage page={page} user={request.current_user} />
    </ui:layout>

@view_config(route_name='showallpages', renderer='xhpy')
@check_login
def show_all_pages(request):
    pages = Page.select()

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/show/%d"%page.id}>{page.name}</a></li>)
    
    return <ui:layout user={request.current_user}>{a}</ui:layout>

@view_config(route_name='showmypages', renderer='xhpy')
@require_login
def show_my_pages(request):
    pages = Page.select().where(Page.user==request.current_user)

    a = <ul/>
    for page in pages:
        a.appendChild(<li><a href={"/page/show/%d"%page.id}>{page.name}</a></li>)
    
    return <ui:layout user={request.current_user}>{a}</ui:layout>
