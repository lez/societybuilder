from cornice.resource import resource
from ist.api.page import BaseRest
from ist.model.type import Comment

@resource(collection_path='/api/comment', path='/api/comment/{id}', renderer='api')
class CommentRest(BaseRest):
    def __init__(self, request):
        super().__init__(request, Comment)

    def _pre_create(self, fields):
        fields['image'] = self.request.POST.get('image_id', None)
        fields['user'] = self.request.user
