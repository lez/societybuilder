from pyramid.view import view_config
from ist.model.type import Post
from pyramid.httpexceptions import HTTPNotFound
from ist.util import *

@view_config(route_name='post', renderer='json', request_method='POST', permission='user')
def post_view(request):
    try:
        content = request.POST['content']
    except KeyError:
        return {'success': 0, 'error': 'invalid request'}

    if len(content) > 5000:
        return {'success': 0, 'error': 'Post is too long'}
    image_ids = request.POST.getall('image_ids[]')
    if len(image_ids) > 12:
        return {'success': 0, 'error': 'Too many images'}

    post = Post(user=request.user, content=content, images=','.join(map(str, image_ids)))
    post.save()

    return {'success': 1}

@view_config(route_name='post_one', renderer='json', request_method=('DELETE', 'GET', 'PUT'), permission='user')
def post_one_view(request):
    id = request.matchdict['id']

    if request.method == 'DELETE':
        l.info('delete post %s' % id)
        success = Post.delete().where(Post.id == id).execute()
        return {'success': success}
        # TODO: delete comments + images

    if request.method == 'GET':
        try:
            id = int(id)
        except TypeError:
            raise HTTPNotFound()

        try:
            post = Post.select().where(Post.id == id).get()
            return {'post': post.json()}
        except Post.DoesNotExist:
            raise HTTPNotFound()

    if request.method == 'PUT':
        raise NotImplementedError('TO BE IMPLEMENTED')
