from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.response import Response, FileResponse
from pyramid.security import forget, authenticated_userid
from pyramid.view import view_config
from .auth import remember_user
from .model.base import ValidationError

from .model.type import User
from .util import *


@view_config(route_name='hello')
def hello_view(request):
    return Response('hello, %s!' % request.user.email)

@view_config(route_name='favicon')
def hello_view(request):
    return FileResponse('ist/static/favicon.ico', request=request, content_type='image/x-icon', cache_max_age=30*24*3600)

@view_config(route_name='logout')
def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    return HTTPFound(location='/', headers=forget(request))

