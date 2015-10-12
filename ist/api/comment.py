from pyramid.view import view_config
from ist.model.type import Comment

@view_config(route_name='comment', renderer='json', request_method='POST', permission='user')
def content_view(request):
    try:
        comment = request.POST['comment']
        item_id = request.POST['item_id']
        item_type = request.POST['item_type']
    except KeyError:
        return {'success': 0, 'error': 'invalid request'}

    if len(comment) > 1000:
        return {'success': 0, 'error': 'Comment is too long'}

    image_id = request.POST.get('image_id', None)
    new_comment = Comment(user=request.user, item_id=item_id, item_type=item_type, comment=comment, image=image_id)
    new_comment.save()

    return {'success': 1, 'comment': new_comment.json()}