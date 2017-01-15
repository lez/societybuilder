from ist.api.base import BaseFullRest
from ist.model.type import Flag, User

from cornice.resource import resource

# @resource(collection_path='/api/flag', path='/api/flag/{id}', renderer='api')
# class FlagRest(BaseFullRest):
#     def __init__(self, request):
#         super().__init__(request, Flag)
#
