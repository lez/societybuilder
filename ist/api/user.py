import json

from cornice.resource import resource
from pyramid.httpexceptions import HTTPMethodNotAllowed, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config

from ist.api.base import BaseItemRest
from ist.auth import remember_user
from ist.model.base import ValidationError, ApiEncoder
from ist.model.type import User


@resource(path='/api/me', renderer='api')
class MeRest(BaseItemRest):
    def __init__(self, request):
        super().__init__(request, User)

    def get(self):
        self.request.matchdict['id'] = self.request.user.id
        return super().get()

    def put(self):
        self.request.matchdict['id'] = self.request.user.id
        return super().put()

    def delete(self):
        raise HTTPMethodNotAllowed()


@view_config(route_name='api_signup', renderer='api', request_method='POST')
def signup_user(request):
    try:
        login = request.POST['login']
    except KeyError:
        return HTTPBadRequest(body=json.dumps({'error': 'required field missing', 'field': 'login'}), content_type='application/json')

    try:
        passwd = request.POST['passwd']
    except KeyError:
        return HTTPBadRequest(body=json.dumps({'error': 'required field missing', 'field': 'passwd'}), content_type='application/json')

    try:
        email = request.POST['email']
    except KeyError:
        return HTTPBadRequest(body=json.dumps({'error': 'required field missing', 'field': 'email'}), content_type='application/json')

    login_lower = login.lower()
    try:
        User.get(login_lower=login_lower)
        return HTTPBadRequest(body=json.dumps({'error': 'this name is already taken', 'field': 'login'}), content_type='application/json')
    except User.DoesNotExist:
        pass

    email_lower = email.lower()
    try:
        User.get(email=email_lower)
        return HTTPBadRequest(body=json.dumps({'error': 'this address is already taken', 'field': 'email'}), content_type='application/json')
    except User.DoesNotExist:
        pass

    if len(passwd) < 6:
        return HTTPBadRequest(body=json.dumps({'error': 'password too short', 'field': 'passwd'}), content_type='application/json')

    user = User(login=login, login_lower=login_lower, email=email_lower)
    user.set_password(passwd)

    try:
        user.validate()
    except ValidationError as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e), 'field': e.field}), content_type='application/json')

    user.save()

    return Response(body=ApiEncoder().encode({'user': user}), headers=remember_user(user, request))
