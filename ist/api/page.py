from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from ist.model.type import Page

from cornice.resource import resource, view

# TODO:
# json legyen elfogadva POSTban, put-ban
# model encoder?
# validate kulon legyen
# base class + page class


@resource(collection_path='/api/page', path='/api/page/{id}')
class PageRest:
    def __init__(self, request):
        self.request = request

    # get all instances
    def collection_get(self):
        pages = [p.json() for p in Page.select()]
        return {'pages': pages}

    @view(accept='text/json', permission='user')
    def collection_post(self):
        for key in Page.rest_required_fields:
            if key not in self.request.POST:
                return {'success': 0, 'error': 'missing field: %s' % key}
    
        name = self.request.POST['name']
        description = self.request.POST['description']
        is_owner_public = self.request.POST.get('is_owner_public', 'true')
        if is_owner_public == 'true':
            is_owner_public = True
        else:
            is_owner_public = False
    
        if len(name) > 30:
            return {'success': 0, 'error': 'Name is too long'}
    
        if len(description) > 250:
            return {'success': 0, 'error': 'Too long description'}
    
        owner = self.request.user
    
        page = Page(owner=owner, name=name, description=description, is_owner_public=is_owner_public)
        page.save()
    
        return {'success': 1, 'page': page.json()}

    def get(self):
        id = self.request.matchdict['id']
        try:
            id = int(id)
        except TypeError:
            raise HTTPNotFound()

        try:
            page = Page.get(id=id)
        except Page.DoesNotExist:
            raise HTTPNotFound()

        return page.json()

    # modify existing instance
    def put(self):
        id = self.request.matchdict['id']
        page = Page.get(id=id)

        modified = False
        for key in Page.rest_editable_fields:
            if key in self.request.POST:
                modified = True
                setattr(page, key, self.request.POST[key])

        if modified:
            page.save()

        return {'success': 1, 'page': page.json()}

    @view(permission='user')
    def delete(self):
        id = self.request.matchdict['id']
        page = Page.get(id=id)

        page.delete_instance()

        return {'success': 1}
