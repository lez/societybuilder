from pyramid.config import Configurator
from pyramid.tests.pkgs.staticpermapp import RootFactory
import logging

from .api import api_methods
from .page import page_methods
from .view import notfound
from .requestfactory import MyRequest

from .util import l

def main(global_settings, **settings):

    settings['debug.peewee'] = settings.get('debug.peewee', False)

    if settings['debug.peewee']:
        pwlogger = logging.getLogger('peewee')
        pwlogger.setLevel(logging.DEBUG)

    from .auth import IsAuthenticationPolicy, IsAuthorizationPolicy, user

    config = Configurator(settings=settings, authentication_policy=IsAuthenticationPolicy(), root_factory=RootFactory, authorization_policy=IsAuthorizationPolicy(), request_factory=MyRequest)

    config.include('ist.model.base')

    config.add_renderer(name='pyxl', factory='ist.renderer.PyxlRenderer')
    config.add_renderer(name='layout', factory='ist.renderer.LayoutRenderer')
    config.add_request_method(user, reify=True)

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.include(api_methods, '/api')
    config.add_route('upload', '/upload')
    config.add_route('hello', '/hello')
    config.add_route('test', '/test')
    config.add_route('me', '/me')
    config.include(page_methods, '/page')
    config.add_route('media', '/media/{subpath:.*}')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('favicon', '/favicon.ico')
    config.add_route('user_profile', '/{login}/profile')
    config.add_notfound_view(notfound)
    config.include('pyramid_redis_sessions')
    config.include('cornice')
    config.scan(__name__)
    return config.make_wsgi_app()

if __name__ == '__main__':
    app = main({})
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
