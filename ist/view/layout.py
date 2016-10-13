#coding: pyxl
from pyramid.httpexceptions import HTTPFound, HTTPMovedPermanently, HTTPForbidden, HTTPNotFound
from pyramid.view import view_config
from pyramid.response import Response, FileResponse
from pyramid.security import forget, authenticated_userid

from ist.auth import remember_user
from ist.model.base import ValidationError
from ist.model.type import Post, User
from ist.view.element import *
from ..auth import remember_user
from ..model.base import ValidationError
from ..model.type import User

from ..util import *
from pyxl.html import *


@view_config(route_name='signup', renderer='layout', request_method='GET')
def signup_page(request):
    return <signupbox />, None

@view_config(route_name='hello', renderer='layout', request_method='GET', permission='user')
def hello_page(request):
    return <div id="hello">
        Welcome, {request.user.login}!
    </div>

@view_config(route_name='home', renderer='layout')
def home(request):
    posts = Post.select().order_by(-Post.created)
    return <frag>\
        <if cond={request.user}>
            <react_poster user="{request.user}" wall="{request.user.wall_id}" role="{request.user.role}" />
        </if>
        <posts posts="{posts}" user="{request.user}" />
    </frag>

@view_config(route_name='test', renderer='layout')
def test(request):
    return <react_post post={Post.select().order_by(-Post.id).get()} user={request.user} />

@view_config(route_name='user_wall', renderer='layout')
def user_wall(request):
    login = request.matchdict['login']
    user = User.get_by_login(login)
    posts = user.posts()
    return <frag>\
        <if cond={request.user}>
            <react_poster user="{request.user}" wall="{user.wall_id}" role="{request.user.role}" />
        </if>
        <posts posts="{posts}" user="{request.user}" />
    </frag>

@view_config(route_name='user_redirect')
def user_redirect(request):
    login_lower = request.matchdict['login'].lower()
    user = User.get_by_login_lower(login_lower)
    return HTTPMovedPermanently(location='/%s' % user.login)

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

@view_config(route_name='user_profile', renderer='layout', permission='user')
def show_profile(request):
    try:
        user = User.select().where(User.login == request.matchdict['login']).get()
    except User.DoesNotExist:
        l.info('race')
        raise HTTPNotFound()

    return <frag>
        # FIXME: read-only if it's not my profile
        <react_restimagefield image="{user.image}" url="/api/me" field="image" reload="{True}" />
        <react_resttextfield text="{user.about}" url="/api/me" field="about" label="About me" />
        <if cond="{user == request.user}">
            <a href="/{user.login}/change_password">Change password</a>
        </if>
    </frag>


@view_config(route_name='user_change_password', renderer='layout', permission='user')
def change_password(request):
    try:
        user = User.select().where(User.login == request.matchdict['login']).get()
        if user != request.user:
            raise HTTPNotFound()
    except User.DoesNotExist:
        raise HTTPNotFound()

    js_string = "IS.submit(event, this, function(user){document.location = '/' + user.login + '/profile';});"
    return <div id="change_password">
        <form data-url="/api/change_password" method="post" class="verticalform" onsubmit={js_string}>
            <field name="passwd" type="password" placeholder="current password">Current password:</field>
            <field name="new_passwd" type="password" placeholder="new password">New password:</field>
            <field name="new_passwd_again" type="password" placeholder="new password again">Repeat new password:</field>
            <p><input name="submit" type="submit" value="Change" /></p>
        </form>
    </div>
