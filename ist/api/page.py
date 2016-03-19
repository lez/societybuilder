from ist.api.base import BaseFullRest
from ist.model.type import Page
from ist.util import permalink

from cornice.resource import resource

@resource(collection_path='/api/page', path='/api/page/{id}', renderer='api')
class PageRest(BaseFullRest):
    def __init__(self, request):
        super().__init__(request, Page)

    def _pre_create(self, fields):
        fields['owner'] = self.request.user
        fields['permalink'] = permalink(fields['name'])
        fields['permalink_lower'] = fields['permalink'].lower()
