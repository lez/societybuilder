import time

from cornice.resource import resource
from pyramid.response import Response
from pyramid.view import view_config

from ist.api.page import BaseRest
from ist.model.type import Post, Comment, Image
from ist.model.base import db, ApiEncoder
from pyramid.httpexceptions import HTTPNotFound
from ist.util import *

# @view_config(route_name='post_one', renderer='json', request_method=('DELETE', 'GET', 'PUT'), permission='user')
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


@resource(collection_path='/api/post', path='/api/post/{id}', renderer='api')
class PostRest(BaseRest):
    def __init__(self, request):
        super().__init__(request, Post, 'posts')

    def _pre_create(self, fields):
        fields['author'] = self.request.user
        fields['images'] = self.request.POST['images']
        # TODO check if the images exist
        if 'wall' not in fields:
            fields['wall'] = self.request.user.wall_id
        if 'role' not in fields:
            fields['role'] = self.request.user.role_id
