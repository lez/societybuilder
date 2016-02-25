from ist.api.base import BaseRest
from ist.model.type import Page

from cornice.resource import resource

@resource(collection_path='/api/page', path='/api/page/{id}', renderer='api')
class PageRest(BaseRest):
    def __init__(self, request):
        super().__init__(request, Page)

    def _pre_create(self, fields):
        fields['owner'] = self.request.user
