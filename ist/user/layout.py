from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from xhpy3.xhpy.pylib import  *
from ist.model.user import User

@view_config(route_name='user_profile', renderer='xhpy')
def show_profile(request):
    try:
        user = User.select().where(
            User.login == request.matchdict['login']
        ).get()
    except User.DoesNotExist:
        raise HTTPNotFound()

    return \
    <ui:layout user={request.user}>
        <react:profileimage user={user} />
    </ui:layout>
