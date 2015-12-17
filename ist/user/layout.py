from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from ist.view.element import *
from xhpy3.xhpy.pylib import  *
from ist.model.type import User

@view_config(route_name='user_profile', renderer='layout')
def show_profile(request):
    try:
        user = User.select().where(
            User.login == request.matchdict['login']
        ).get()
    except User.DoesNotExist:
        raise HTTPNotFound()

    return <react:editprofileimage image={request.user.image} url="/api/user" />
