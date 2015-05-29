from pyramid.config import Configurator
from pyramid.tests.pkgs.staticpermapp import RootFactory
from .auth import IsAuthPolicy

# from xhpy.init import register_xhpy_module
# register_xhpy_module('pages')
# import pages

def main(global_settings, **settings):
    config = Configurator(settings=settings, authentication_policy=IsAuthPolicy(), root_factory=RootFactory)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.add_route('api', '/api/content')
    config.add_route('upload', '/upload')
    config.add_route('hello', '/hello')
    config.include('pyramid_redis_sessions')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan(__name__)
    return config.make_wsgi_app()

if __name__ == '__main__':
    app = main({})
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
