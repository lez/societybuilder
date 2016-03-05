from cornice.resource import resource

from ist.api.base import BaseFullRest, BaseCollectionRest
from ist.model.type import Comment, Post


@resource(collection_path='/api/comment', path='/api/comment/{id}', renderer='api')
class CommentRest(BaseFullRest):
    def __init__(self, request):
        super().__init__(request, Comment)

    def _pre_create(self, fields):
        fields['image'] = self.request.POST.get('image_id', None)
        fields['user'] = self.request.user


# TODO this could be a single decorated function
@resource(collection_path='/api/post/{post_id}/comments', path='nonexistent', renderer='api')
class PostCommentRest(BaseCollectionRest):
    def __init__(self, request):
        super().__init__(request, Comment)

    def collection_get(self):
        post = self._item(custom_cls=Post, custom_id_name='post_id')
        comments = Comment.select().where(Comment.item_type=='post' and Comment.item_id==post.id)
        return {Comment.rest_collection_name: comments}