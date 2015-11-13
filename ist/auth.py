from pyramid.compat import native_, bytes_
from pyramid.httpexceptions import HTTPForbidden
from pyramid.interfaces import IAuthenticationPolicy, IAuthorizationPolicy, IRendererInfo, IRendererFactory
from pyramid.security import remember, authenticated_userid
from webob.cookies import CookieProfile
from zope.interface import implementer
from .model.type import User, AuthToken
from .util import *
from xhpy3.xhpy.pylib import *
from ist.view.element import *

def remember_user(user, request):
    request.session['user'] = user.id
    token = AuthToken(token=random_string(100), user=user)
    token.save()
    return remember(request, token.token)

def user(request):
    userid = authenticated_userid(request)
    if not userid:
        return None
    try:
        user = User.get(id=userid)
    except User.DoesNotExist:
        return None
    return user

@implementer(IAuthenticationPolicy)
class IsAuthenticationPolicy:
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
            userid = request.session['user']
            try:
                # make sure the user exists in the database
                User.get(id=userid)
            except User.DoesNotExist:
                return
            return userid
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

    def unauthenticated_userid(self, request):
        l.info('unauthenticated_userid')
        return 'nobody'

    def effective_principals(self, request):
        l.info('effective_principals')
        if self.authenticated_userid(request):
            return ['user']
        return []


class _SimpleSerializer(object):
    def loads(self, bstruct):
        return native_(bstruct)

    def dumps(self, appstruct):
        return bytes_(appstruct)


@implementer(IRendererFactory)
class XHPyRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        return str(value)

@implementer(IRendererFactory)
class LayoutRenderer:
    def __init__(self, info):
        self.info = info

    def __call__(self, value, system):
        user = system['request'].user

        if isinstance(value, tuple) and len(value) == 2:
            content, rightbar = value
        else:
            content = value
            rightbar = <ui:rightbar user={user} />

        layout = <ui:layout user={user}>
            <div id="content">
                {content}
            </div>
            {rightbar}
        </ui:layout>

        return str(layout)

@implementer(IAuthorizationPolicy)
class IsAuthorizationPolicy:

    def permits(self, context, principals, permission):
        """ Return ``True`` if any of the ``principals`` is allowed the
        ``permission`` in the current ``context``, else return ``False``
        """
        l.info('permits(%r,%r,%r)'%(context, principals, permission))
        return permission in principals

    def principals_allowed_by_permission(self, context, permission):
        """ Return a set of principal identifiers allowed by the
        ``permission`` in ``context``.  This behavior is optional; if you
        choose to not implement it you should define this method as
        something which raises a ``NotImplementedError``.  This method
        will only be called when the
        ``pyramid.security.principals_allowed_by_permission`` API is
        used."""
        raise NotImplementedError()
