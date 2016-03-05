from cornice.resource import resource
from pyramid.httpexceptions import HTTPMethodNotAllowed

from ist.api.base import BaseItemRest
from ist.model.type import Image, User


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
