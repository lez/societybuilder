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
    <ui:page user={request.current_user} >
        <ui:createpage />
    </ui:page>

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
    <ui:page user={request.current_user} >
        <ui:showpage page={page} user={request.current_user} />
    </ui:page>
