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

@view_config(route_name='login')
def login_view(request):
    if authenticated_userid(request):
        raise HTTPForbidden('You are already logged in')
    next = request.params.get('next') or request.referer or '/'
    if 'login' not in request.POST:
        return Response('invalid login')
    login = request.POST.get('login')
    passwd = request.POST.get('passwd')
    try:
        user = User.authenticate(login, passwd)
    except User.AuthFailed:
        l.info('auth failed')
        return Response('invalid login')
    l.info('login successful')
    return HTTPFound(location=next, headers=remember_user(user, request))

@view_config(route_name='logout')
def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    headers = forget(request)
    return_to = request.referer or '/'
    return HTTPFound(location=return_to, headers=headers)

@view_config(route_name='signup')
def signup_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        passwd = request.POST.get('passwd')
        email = request.POST.get('email')
        try:
            User.get(login=login)
            raise Exception('this name is already taken')
        except User.DoesNotExist:
            pass
        if len(passwd) < 6:
            raise Exception('too short password')
        try:
            User.get(email=email)
            raise Exception('this email is already taken')
        except User.DoesNotExist:
            pass

        user = User(login=login, email=email)
        user.set_password(passwd)
        try:
            user.validate()
        except ValidationError as e:
            return Response('field=%s, error=%s' % (e.field, str(e)))
        user.save()
        return HTTPFound(location=request.route_url('home'), headers=remember_user(user, request))
