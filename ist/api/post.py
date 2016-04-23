import re
from cornice.resource import resource

from ist.api.page import BaseFullRest
from ist.model.type import Post, Comment, Image


@resource(collection_path='/api/post', path='/api/post/{id}', renderer='api')
class PostRest(BaseFullRest):
    def __init__(self, request):
        super().__init__(request, Post)

    def _pre_create(self, fields):
        fields['author'] = self.request.user
        fields['images'] = self.request.POST['images']
        # TODO check if the images exist and owned by author
        if 'wall' not in fields:
            fields['wall'] = self.request.user.wall_id
        if 'role' not in fields:
            fields['role'] = self.request.user.role_id

        fields['content'] = re.sub('\n{3,}', '\n\n', fields['content'].strip())

    def _pre_delete(self, post):
        for c in Comment.select().where(Comment.item_type=='post').where(Comment.item_id==post.id):
            if c.image:
                Image.delete().where(Image.id==c.image).execute()
            c.delete_instance()
        if post.images:
            Image.delete().where(Image.id << post.get_image_ids()).execute()
