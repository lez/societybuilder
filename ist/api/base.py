import json
import time

from cornice.resource import view
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ist.model.base import db

# TODO:
# authorization
# ----------
# pagination
# json legyen elfogadva POSTban, PUTban, esetleg image.id szintaxisu post fieldek ☃

# Convention what's followed:
# GET  /api/foo -> all foo objects
# POST /api/foo -> new foo object
# GET  /api/foo/1 -> get one foo object with id 1
# PUT  /api/foo/1 -> modify foo object with id 1
# DELETE /api/foo/1 -> delete foo object with id 1

class BaseRest:
    def __init__(self, request, cls):
        self.request = request
        self.cls = cls

    def _item(self, *, custom_cls=None, custom_id_name=None):
        id_name = custom_id_name or 'id'
        id = self.request.matchdict[id_name]
        try:
            id = int(id)
        except TypeError:
            raise HTTPNotFound()

        cls = custom_cls or self.cls
        try:
            item = cls.get(id=id)
        except cls.DoesNotExist:
            raise HTTPNotFound()

        return item

class BaseCollectionRest(BaseRest):

    # create new instance
    @view(permission='user')
    def collection_post(self):

        for key in self.cls.rest_required_fields:
            if key not in self.request.POST:
                raise HTTPBadRequest(body=json.dumps({'error': 'missing field', 'field': key}))

        for key in self.request.POST:
            if key not in self.cls.rest_all_fields():
                raise HTTPBadRequest(body=json.dumps({'error': 'invalid field', 'field': key}))

        fields = {}

        for key in self.cls.rest_all_fields():
            if key in self.request.POST:
                fields[key] = self.request.POST[key]

        self._pre_create(fields)

        item = self.cls(**fields)

        errors = list(item.validate())
        if errors:
            raise HTTPBadRequest(body=json.dumps({'errors': errors}))

        try:
            item.save()
        except Exception as e:
            print('Cannot save item; cls="%s", fields=%r' % (self.cls.__name__, fields))
            raise

        return item

    # get all instances
    def collection_get(self):
        return {self.cls.rest_collection_name: self.cls.select()}

    def _pre_create(self, fields):
        # This is a hook for you to override
        ...


class BaseItemRest(BaseRest):

    # get one instance by id
    def get(self):
        return self._item()

    # modify existing instance
    def put(self):
        item = self._item()

        modified = False
        for key in self.request.POST:
            if key in self.cls.rest_editable_fields:
                modified = True
                setattr(item, key, self.request.POST[key])
            else:
                raise HTTPBadRequest(body=json.dumps({'error': 'invalid field', 'field': key}))

        if modified:
            assert hasattr(item, 'modified')
            item.modified = int(time.time())
            item.save()
        else:
            raise HTTPBadRequest(body=json.dumps({'error': 'missing request body'}))

        return item

    @view(permission='user')
    def delete(self):
        item = self._item()
        with db.transaction():
            self._pre_delete(item)
            item.delete_instance()
        return {}

    def _pre_delete(self, item):
        # Override me to remove child instances as well
        ...

class BaseFullRest(BaseItemRest, BaseCollectionRest):
    pass