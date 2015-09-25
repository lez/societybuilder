from pyramid.view import view_config
from ist.model.user import Post

@view_config(route_name='content', renderer='json', request_method='POST', permission='user')
def content_view(request):
    try:
        content = request.POST['content']
    except KeyError:
        return {'success': 0, 'error': 'invalid request'}

    if len(content) > 5000:
        return {'success': 0, 'error': 'Post is too long'}
    image_ids = request.POST.getall('image_ids[]')
    if len(image_ids) > 12:
        return {'success': 0, 'error': 'Too many images'}

    content = Post(user=request.user, content=content, images=','.join(map(str, image_ids)))
    content.save()

    return {'success': 1}