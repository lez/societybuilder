from pyramid.view import view_config
from xhpy3.xhpy.pylib import *
from ist.view.element import *

@view_config(route_name='test', renderer='xhpy')
def test(request):
    return \
    <ui:layout user={request.user} >
        <ui:creator />
        <ui:createpage />
    </ui:layout>


@view_config(route_name='home', renderer='xhpy')
def home(request):
    return \
    <ui:layout user={request.user} >
        Home
    </ui:layout>
