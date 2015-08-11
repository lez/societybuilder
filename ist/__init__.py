from pyramid.config import Configurator
from pyramid.tests.pkgs.staticpermapp import RootFactory
from .auth import IsAuthenticationPolicy, IsAuthorizationPolicy, user
from .api import api_methods
from .page import page_methods
from .view import notfound
from pyramid.security import remember, authenticated_userid
from .model.user import User, AuthToken

from xhpy3.xhpy.init import register_xhpy_module
register_xhpy_module('ist.view')
register_xhpy_module('ist.page.layout')

def main(global_settings, **settings):
    config = Configurator(settings=settings, authentication_policy=IsAuthenticationPolicy(), root_factory=RootFactory, authorization_policy=IsAuthorizationPolicy())
    config.add_renderer(name='xhpy', factory='ist.auth.XHPyRenderer')
    config.add_request_method(user, reify=True)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.include(api_methods, '/api')
    config.add_route('upload', '/upload')
    config.add_route('hello', '/hello')
    config.add_route('test', '/test')
    config.include(page_methods, '/page')
    config.add_route('media', '/media/*subpath')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_notfound_view(notfound)
    config.include('pyramid_redis_sessions')
    config.scan(__name__)
    return config.make_wsgi_app()

if __name__ == '__main__':
    app = main({})
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
