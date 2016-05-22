#coding: pyxl
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from ist.auth import remember_user
from ist.model.base import ValidationError
from ist.model.type import Post
from ist.view.element import *
from pyxl.html import *


@view_config(route_name='signup', renderer='layout', request_method='GET')
def signup_page(request):
    return <signupbox />

@view_config(route_name='hello', renderer='layout', request_method='GET', permission='user')
def hello_page(request):
    return <div id="hello">
        Welcome, {request.user.login}!
    </div>
