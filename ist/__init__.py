import os
from pyramid.config import Configurator

from ist.model.type import User, Page
from .view import notfound
from .auth import IsAuthenticationPolicy, IsAuthorizationPolicy, user

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
                          authorization_policy=IsAuthorizationPolicy())

    config.include('ist.model.base')
    config.add_renderer(name='pyxl', factory='ist.renderer.PyxlRenderer')
    config.add_renderer(name='api', factory='ist.renderer.ApiRenderer')
    config.add_renderer(name='layout', factory='ist.renderer.LayoutRenderer')

    config.add_request_method(user, reify=True)

    config.add_route('home', '/')

    # user
    config.add_route('signup', '/signup')
    config.add_route('api_signup', '/api/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # test
    config.add_route('hello', '/hello')
    config.add_route('test', '/test')

    # static
    config.add_route('media', '/media/{subpath:.*}')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('favicon', '/favicon.ico')
    config.add_route('upload', '/upload')

    # pages
    config.add_route('createpage', '/page/create')
    config.add_route('showallpages', '/page/all')
    config.add_route('showmypages', '/page/my')

    # predicated stuff
    config.add_route('user_profile', '/{login}/profile')
    config.add_route('user_wall', '/{login}', custom_predicates=(user_exists,))
    config.add_route('page_edit', '/{permalink}/edit')
    config.add_route('page_wall', '/{permalink}', custom_predicates=(page_exists,))

    config.add_notfound_view(notfound)
    config.include('pyramid_redis_sessions')
    config.include('cornice')
    config.scan(__name__)
    return config.make_wsgi_app()

def user_exists(info, request):
    login = info['match']['login']
    try:
        User.get_by_login(login)
        return True
    except User.DoesNotExist:
        return False

def page_exists(info, request):
    permalink = info['match']['permalink']
    try:
        Page.get_by_permalink(permalink)
        return True
    except Page.DoesNotExist:
        return False

if __name__ == '__main__':
    app = main({})
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
