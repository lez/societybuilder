import json

from pyramid.httpexceptions import HTTPBadRequest

from sb.api.base import BaseFullRest
from sb.model.type import Page, User
from sb.util import permalink

from cornice.resource import resource

@resource(collection_path='/api/page', path='/api/page/{id}', renderer='api')
class PageRest(BaseFullRest):
    def __init__(self, request):
        super().__init__(request, Page)

    def _pre_create(self, fields):
        fields['owner'] = self.request.user
        fields['permalink'] = permalink(fields['name'])
        fields['permalink_lower'] = fields['permalink'].lower()

        if 'image' in fields and not fields['image']:
            # remove optional image field if nothing was given
            del fields['image']

        try:
            User.get_by_login_lower(fields['permalink_lower'])
            raise HTTPBadRequest(body=json.dumps({'error': 'this name is already taken'}))
        except User.DoesNotExist:
            pass

