import json
import time

from cornice.resource import view
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ist.model.base import db
from ist.model.type import Page

# TODO:
# authorization
# ----------
# pagination
# json legyen elfogadva POSTban, PUTban

class BaseRest:
    def __init__(self, request, cls, plural):
        self.request = request
        self.cls = cls
        self.plural = plural

    def _item(self):
        id = self.request.matchdict['id']
        try:
            id = int(id)
        except TypeError:
            raise HTTPNotFound()

        try:
            item = self.cls.get(id=id)
        except Page.DoesNotExist:
            raise HTTPNotFound()

        return item

    # new instance
    @view(permission='user')
    def collection_post(self):

        for key in self.cls.rest_required_fields:
            if key not in self.request.POST:
                raise HTTPBadRequest(body=json.dumps({'error': 'missing field', 'field': key}))

        fields = {}
        for key in self.cls.rest_editable_fields.union(self.cls.rest_optional_fields):
            if key in self.request.POST:
                fields[key] = self.request.POST[key]

        self._pre_create(fields)

        item = self.cls(**fields)

        errors = list(item.validate())
        if errors:
            raise HTTPBadRequest(body=json.dumps({'errors': errors}))

        item.save()

        return item

    # get all instances
    def collection_get(self):
        return {self.plural: self.cls.select()}

    # get one instance by id
    def get(self):
        return self._item()

    # modify existing instance
    def put(self):
        item = self._item()

        modified = False
        for key in self.cls.rest_editable_fields:
            if key in self.request.POST:
                modified = True
                setattr(item, key, self.request.POST[key])

        if modified:
            assert getattr(item, 'modified')
            item.modified = int(time.time())
            item.save()

        return item

    @view(permission='user')
    def delete(self):
        item = self._item()
        with db.transaction():
            self._pre_delete(item)
            item.delete_instance()
        return {}

    def _pre_create(self, fields):
        pass

    def _pre_delete(self, item):
        pass
