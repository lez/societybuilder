from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.response import Response
from pyramid.security import forget, authenticated_userid
from pyramid.view import view_config
from .auth import remember_user
from .model.base import ValidationError

from .model.user import User
from .util import *

logo = """
<img src="/static/img/is_logo.gif" width="40" height="40" />
"""

login_form = """
<form action="/login" method="POST">
<input name="login" type="text" placeholder="login" />
<input name="passwd" type="password" placeholder="password" />
<input name="submit" type="submit" value="Log in" />
</form>
"""

signup_form = """
<form action="/signup" method="POST">
<input name="login" type="text" placeholder="login" />
<input name="passwd" type="password" placeholder="password" />
<input name="email" type="text" placeholder="email address" />
<input name="submit" type="submit" value="Sign up" />
</form>
"""

creator = """
<div id="creator"></div>
<link href="/static/style/bundle.css" media="all" rel="stylesheet" />
<script type="text/javascript" src="/static/js/app.js" />
<script type="text/javascript" src="/static/js/jquery.min.js" />
<script type="text/javascript">
IS.addComposer(document.getElementById('creator'), 'asdf');
</script>
"""

@view_config(route_name='home')
def home_view(request):
    login = authenticated_userid(request)

    return Response(logo + 'hello, %s' % login + login_form +' ' + str(int(request.session.created)) + creator)

@view_config(route_name='login')
def login_view(request):
    if authenticated_userid(request):
        raise HTTPForbidden('You are already logged in')
    next = request.params.get('next') or '/'
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
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='signup')
def signup_view(request):
    if request.method == 'GET':
        return Response(signup_form)
    elif request.method == 'POST':
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