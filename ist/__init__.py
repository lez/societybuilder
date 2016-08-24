import os
ROOT = os.path.abspath(os.path.dirname(__path__[0]))

from pyramid.config import Configurator
from pyramid.settings import asbool

from ist.model.type import User, Page
from ist.util import l
from .view import notfound, notfound_api, forbidden, forbidden_api
from .auth import IsAuthenticationPolicy, IsAuthorizationPolicy, user


default_settings = {
    'peewee.debug': False,
    'peewee.database': 'sb',
    'peewee.username': 'sb',
    'peewee.password': 'sb',
    'peewee.host': '127.0.0.1',
    'peewee.port': 5432,
}

bool_settings = {
    'peewee.debug',
    'react.render'
}

def main(global_settings, **settings):

    for key in default_settings:
        settings[key] = settings.get(key, default_settings[key])

    for key in bool_settings:
        settings[key] = asbool(settings.get(key, False))

    config = Configurator(settings=settings,
                          authentication_policy=IsAuthenticationPolicy(),
                          authorization_policy=IsAuthorizationPolicy())

    config.include('ist.model.base')
    config.include('ist.react')
    config.add_renderer(name='pyxl', factory='ist.renderer.PyxlRenderer')
    config.add_renderer(name='api', factory='ist.renderer.ApiRenderer')
    config.add_renderer(name='layout', factory='ist.renderer.LayoutRenderer')

    config.add_request_method(user, reify=True)

    config.add_route('home', '/')

    # user
    config.add_route('signup', '/signup')
    config.add_route('api_signup', '/api/signup')
    config.add_route('api_login', '/api/login')
    config.add_route('api_change_password', '/api/change_password')
    config.add_route('logout', '/logout')

    # test
    config.add_route('hello', '/hello')
    config.add_route('test', '/test')

    # static
    config.add_route('media', '/media/{subpath:.*}')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('.well-known', '.well-known', cache_max_age=3600)  # for certbot
    config.add_route('favicon', '/favicon.ico')
    config.add_route('upload', '/upload')

    # pages
    config.add_route('createpage', '/page/create')
    config.add_route('showallpages', '/page/all')
    config.add_route('showmypages', '/page/my')

    # predicated stuff
    config.add_route('user_profile', '/{login}/profile', custom_predicates=(user_exists,))
    config.add_route('user_change_password', '/{login}/change_password', custom_predicates=(user_exists,))
    config.add_route('user_wall', '/{login}', custom_predicates=(user_exists,))
    config.add_route('user_redirect', '/{login}', custom_predicates=(user_exists_lower,))

    config.add_route('page_edit', '/{permalink}/edit', custom_predicates=(page_exists,))
    config.add_route('page_wall', '/{permalink}', custom_predicates=(page_exists,))
    config.add_route('page_redirect', '/{permalink}', custom_predicates=(page_exists_lower,))

    config.add_notfound_view(notfound, custom_predicates=(not_api,))
    config.add_notfound_view(notfound_api, custom_predicates=(is_api,))
    config.add_forbidden_view(forbidden, custom_predicates=(not_api,))
    config.add_forbidden_view(forbidden_api, custom_predicates=(is_api,))

    config.include('pyramid_redis_sessions')
    config.include('cornice')
    config.scan(__name__)

    config.add_tween('ist.request_logger')

    return config.make_wsgi_app()


def request_logger(handler, registry):
    def request_handler(request):
        response = handler(request)

        if not request.path or '/' not in request.path:
            l.info('[???] invalid request')
            return response
            # TODO "GET //xxx" returns a valid response with the main page

        # exclude common paths from being logged for clearness
        if request.path.split('/')[1] in ('static', 'favicon.ico', 'media', '_debug_toolbar'):
            return response

        info_log = '[%d] %s %s' % (response.status_int, request.method, request.path_qs)
        if response.status_int in [301, 302]:
            info_log += ' => %s' % response.headers['location']

        l.info(info_log)

        return response

    return request_handler

def user_exists(info, request):
    login = info['match']['login']
    try:
        User.get_by_login(login)
        return True
    except User.DoesNotExist:
        return False

def user_exists_lower(info, request):
    login_lower = info['match']['login'].lower()
    try:
        User.get_by_login_lower(login_lower)
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

def page_exists_lower(info, request):
    permalink_lower = info['match']['permalink'].lower()
    try:
        Page.get_by_permalink_lower(permalink_lower)
        return True
    except Page.DoesNotExist:
        return False

def is_api(info, request):
    if request.path.startswith('/api'):
        return True
    return False

def not_api(info, request):
    return not is_api(info, request)

if __name__ == '__main__':
    app = main({})
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
