import time
from pyramid.response import Response
from pyramid.view import view_config
from ist.model.type import Post, Comment, Image
from ist.model.base import db, ApiEncoder
from pyramid.httpexceptions import HTTPNotFound
from ist.util import *

@view_config(route_name='post', renderer='json', request_method='POST', permission='user')
def post_view(request):
    keys = ('content', 'images', 'wall', 'role')
    for k in keys:
        if k not in request.POST:
            return {'success': 0, 'error': 'invalid request'}

    content = request.POST['content']
    wall = request.POST['wall']  #TODO validate wall id
    role = request.POST['role']  #TODO validate

    if len(content) > 5000:
        return {'success': 0, 'error': 'Post is too long'}
    image_ids = request.POST.getone('images').split(',')
    if len(image_ids) > 12:
        return {'success': 0, 'error': 'Too many images'}

    # TODO check if the images exist
    post = Post(author=request.user, content=content, images=','.join(map(str, image_ids)), wall=wall, role=role)
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
            return Response(ApiEncoder().encode({'post': post.json()}), content_type='text/json')
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

        for field in Post.rest_editable_fields:
            if field in request.POST:
                setattr(post, field, request.POST.getone(field))

        post.modified = int(time.time())
        post.save()

        return Response(ApiEncoder().encode({'success': 1, 'post': post.json()}), content_type='text/json')
