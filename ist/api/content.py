from pyramid.view import view_config
from ist.auth import require_login
from ist.model.content import Content

@view_config(route_name='api', renderer='json', request_method='POST')
@require_login
def content_view(request):
    try:
        content = request.POST['content']
    except KeyError:
        return {'success': 0, 'error': 'invalid request'}

    if len(content) > 5000:
        return {'success': 0, 'error': 'Content is too long'}
    image_ids = request.POST.getall('image_ids[]')
    if len(image_ids) > 12:
        return {'success': 0, 'error': 'Too many images'}
    user = request.current_user

    content = Content(user=user, content=content, images=','.join(map(str, image_ids)))
    content.save()

    return {'success': 1}