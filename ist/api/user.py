from pyramid.view import view_config
from ist.model.type import Image

@view_config(route_name='user', renderer='json', request_method='POST', permission='user')
def content_view(request):
    if 'image_id' in request.POST:
        val = request.POST.getone('image_id')
        val=int(val)
        request.user.image = Image.get(Image.id == val)
        request.user.save()

    return {'success': 1}