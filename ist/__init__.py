import os
from pyramid.config import Configurator
from pyramid.tests.pkgs.staticpermapp import RootFactory

from .api import api_methods
from .page import page_methods
from .view import notfound
from .auth import IsAuthenticationPolicy, IsAuthorizationPolicy, user

from .util import l

ROOT = os.path.dirname(__path__[0])

default_settings = {
    'peewee.debug': False,
    'peewee.database': 'is',
    'peewee.username': 'is',
    'peewee.password': 'is',
    'peewee.host': '127.0.0.1',
    'peewee.port': 5432,
}

def main(global_settings, **settings):

    for key in default_settings:
        settings[key] = settings.get(key, default_settings[key])

    config = Configurator(settings=settings,
                          authentication_policy=IsAuthenticationPolicy(),
                          root_factory=RootFactory,
                          authorization_policy=IsAuthorizationPolicy())

    config.include('ist.model.base')
    config.add_renderer(name='pyxl', factory='ist.renderer.PyxlRenderer')
    config.add_renderer(name='api', factory='ist.renderer.ApiRenderer')
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
