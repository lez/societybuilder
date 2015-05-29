from symbol import decorator
from pyramid.compat import native_, bytes_
from pyramid.httpexceptions import HTTPForbidden
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import remember, authenticated_userid
from webob.cookies import CookieProfile
from zope.interface import implementer
from .model.user import User, AuthToken
from .util import *

def remember_user(user, request):
    request.session['user'] = user.id
    token = AuthToken(token=random_string(100), user=user)
    token.save()
    return remember(request, token.token)


def require_login(func):
    def lookup_user(request, *args, **kwargs):
        userid = authenticated_userid(request)
        if not userid:
            raise HTTPForbidden('You must be logged in')
        request.current_user = User.get(id=userid)
        return func(request, *args, **kwargs)
    return lookup_user


@implementer(IAuthenticationPolicy)
class IsAuthPolicy:
    def __init__(self):
        self.cookie_profile = CookieProfile(
            cookie_name = 'me',
            max_age = 365 * 24 * 3600,
            path = '/',
            serializer=_SimpleSerializer()
        )

    def remember(self, request, token, **kw):
        profile = self.cookie_profile(request)
        return profile.get_headers(token, domains=self._cookie_domains(request))

    def authenticated_userid(self, request):
        if 'user' in request.session:
            l.info('user found in session')
            return request.session['user']
        token = request.cookies.get('me')
        if not token:
            l.info('token not found in cookie')
            return
        try:
            user = User.get_by_token(token)
        except User.DoesNotExist:
            self.forget(request)
            return
        request.session['user'] = user.id
        return user.id

    def forget(self, request):
        return self.cookie_profile(request).get_headers(None, domains=self._cookie_domains(request))

    def _cookie_domains(self, request):
        return [None, request.domain]

    # def unauthenticated_userid(self, request):
    #     l.info('unauthenticated_userid')
    #     return 'what'
    #
    # def effective_principals(self, request):
    #     l.info('effective_principals')
    #     return ['user']


class _SimpleSerializer(object):
    def loads(self, bstruct):
        return native_(bstruct)

    def dumps(self, appstruct):
        return bytes_(appstruct)