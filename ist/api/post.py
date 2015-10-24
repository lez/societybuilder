from pyramid.response import Response
from pyramid.view import view_config
from ist.model.type import Post, Comment, Image
from ist.model.base import db, ModelEncoder
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
        with db.transaction():
            post = Post.get(id=id)
            for c in Comment.select().where(Comment.item_type=='post').where(Comment.item_id==id):
                if c.image:
                    Image.delete().where(Image.id==c.image).execute()
                c.delete_instance()
            if post.images:
                Image.delete().where(Image.id << post.get_image_ids()).execute()
            post.delete_instance()
            l.info('deleted post '+id)

        return {'success': 1}

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
        try:
            id = int(id)
        except TypeError:
            raise HTTPNotFound()

        try:
            post = Post.get(id=id)
        except Post.DoesNotExist:
            raise HTTPNotFound()

        for field in Post.rest_fields:
            if field in request.POST:
                l.info('setting post '+field)
                setattr(post, field, request.POST.getone(field))

        post.save()

        # TODO renderer = model-json
        return Response(ModelEncoder().encode({'success': 1, 'post': post.json()}), content_type='text/json')
