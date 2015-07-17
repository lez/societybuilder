from pyramid.view import view_config
from xhpy3.xhpy.pylib import *
from ist.auth import check_login
from ist.view.element import *

@view_config(route_name='test', renderer='xhpy')
@check_login
def test(request):
    return \
    <ui:layout user={request.current_user} >
        <ui:creator />
        <ui:createpage />
    </ui:layout>


@view_config(route_name='home', renderer='xhpy')
@check_login
def home(request):
    return \
    <ui:layout user={request.current_user} >
        Home
    </ui:layout>

