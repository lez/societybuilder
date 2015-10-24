from pyramid.view import view_config
from ist.model.type import Page

@view_config(route_name='page', renderer='json', request_method='POST', permission='user')
def content_view(request):
    keys = ('name', 'description', 'is_owner_public')
    for k in keys:
        if k not in request.POST:
            return {'success': 0, 'error': 'invalid request'}

    name = request.POST['name']
    description = request.POST['description']
    is_owner_public = request.POST['is_owner_public']
    if is_owner_public == 'true':
        is_owner_public = True
    else:
        is_owner_public = False

    if len(name) > 30:
        return {'success': 0, 'error': 'Name is too long'}

    if len(description) > 250:
        return {'success': 0, 'error': 'Too long description'}

    owner = request.user

    page = Page(owner=owner, name=name, description=description, is_owner_public=is_owner_public)
    page.save()

    return {'success': 1}
