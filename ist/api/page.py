from pyramid.view import view_config
from ist.model.page import Page

@view_config(route_name='page', renderer='json', request_method='POST', permission='user')
def content_view(request):
    keys = ('name', 'description', 'owner_public')
    for k in keys:
        if k not in request.POST:
            return {'success': 0, 'error': 'invalid request'}

    name = request.POST['name']
    description = request.POST['description']
    owner_public = request.POST['owner_public']
    if owner_public == 'true':
        owner_public = True
    else:
        owner_public = False

    if len(name) > 30:
        return {'success': 0, 'error': 'Name is too long'}

    if len(description) > 250:
        return {'success': 0, 'error': 'Too long description'}

    user = request.user

    page = Page(user=user, name=name, description=description, owner_public=owner_public)
    page.save()

    return {'success': 1}