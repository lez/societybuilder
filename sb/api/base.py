import json
import time

from cornice.resource import view
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPClientError

from sb.model.base import db
from sb.util import *

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
        except ValueError:
            raise HTTPNotFound(body=json.dumps({'error': 'resource not found'}), content_type='application/json')

        cls = custom_cls or self.cls
        try:
            item = cls.get(id=id)
        except cls.DoesNotExist:
            raise HTTPNotFound(body=json.dumps({'error': 'resource not found'}), content_type='application/json')

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
                value = self.request.POST[key]
                if value == '' and getattr(self.cls, key).null:
                    value = None
                fields[key] = value

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
        try:
            return self._item()
        except HTTPClientError as e:
            return e

    # modify existing instance
    @view(permission='user')
    def put(self):
        try:
            item = self._item()
            if not item.is_editable_by(self.request.user):
                raise HTTPForbidden(body=json.dumps({'error': 'permission denied'}))

            modified = False
            for key in self.request.POST:
                if key in self.cls.rest_editable_fields:
                    modified = True
                    value = self.request.POST[key]
                    if value == '' and getattr(self.cls, key).null:
                        value = None
                    setattr(item, key, value)
                else:
                    raise HTTPBadRequest(body=json.dumps({'error': 'invalid field', 'field': key}))

            if modified:
                assert hasattr(item, 'modified')
                item.modified = int(time.time())
                item.save()
            else:
                raise HTTPBadRequest(body=json.dumps({'error': 'missing request body'}))

            return item
        except HTTPClientError as e:
            return e

    @view(permission='user')
    def delete(self):
        try:
            item = self._item()

            if not item.is_editable_by(self.request.user):
                raise HTTPForbidden(body=json.dumps({'error': 'permission denied'}))

            with db.transaction():
                self._pre_delete(item)
                item.delete_instance()

            return dict()

        except HTTPClientError as e:
            return e

    def _pre_delete(self, item):
        # Override me to do extra stuff like removing child instances as well
        ...





class BaseSubCollectionRest(BaseRest):

    # create new instance
    @view(permission='user')
    def collection_post(self):

        try:
            item = self._item()
        except self.cls.DoesNotExist:
            l.debug("no such item")
            raise

        for key in self.sub_cls.rest_required_fields:
            if key not in self.request.POST:
                raise HTTPBadRequest(body=json.dumps({'error': 'missing field', 'field': key}))

        for key in self.request.POST:
            if key not in self.sub_cls.rest_all_fields():
                raise HTTPBadRequest(body=json.dumps({'error': 'invalid field', 'field': key}))

        fields = {}

        for key in self.sub_cls.rest_all_fields():
            if key in self.request.POST:
                value = self.request.POST[key]
                if value == '' and getattr(self.sub_cls, key).null:
                    value = None
                fields[key] = value

        self._pre_create(fields)

        sub_item = self.sub_cls(**fields)

        errors = list(sub_item.validate())
        if errors:
            raise HTTPBadRequest(body=json.dumps({'errors': errors}))

        sub_items = getattr(item, self.sub_cls.rest_collection_name)
        sub_item.id = 1 if sub_items == [] else sub_items[-1]['id'] + 1

        sub_items.append(sub_item.json())

        try:
            item.save()
            print('item flags: %s' % json.dumps(item.flags))
        except Exception as e:
            print('Cannot save item; %s; cls="%s", sub_cls="%s" fields=%r' % (str(e), self.cls.__name__, self.sub_cls.__name__, fields))
            raise

        return item

    # get all instances
    def collection_get(self):
        item = self._item()
        l.info('got item: %s' % item.content)
        return {self.sub_cls.rest_collection_name: getattr(item, self.sub_cls.rest_collection_name)}

    def _pre_create(self, fields):
        # This is a hook for you to override
        ...

class BaseSubItemRest(BaseRest):

    # get one instance by id
    def get(self):
        try:
            item = self._item()
            try:
                return next(x for x in getattr(item, self.sub_cls.rest_collection_name) if x['id'] == int(self.request.matchdict['sub_id']))
            except StopIteration:
                raise HTTPNotFound(body=json.dumps({'error': 'resource not found'}), content_type='application/json')
        except HTTPClientError as e:
            return e

    # modify existing instance
    @view(permission='user')
    def put(self):
        raise NotImplementedError()
        ...

    @view(permission='user')
    def delete(self):
        raise NotImplementedError()
        ...


class BaseFullRest(BaseItemRest, BaseCollectionRest):
    pass

class BaseSubFullRest(BaseSubCollectionRest, BaseSubItemRest):
    def __init__(self, request, cls, sub_cls, **kwargs):
        self.sub_cls = sub_cls
        super().__init__(request, cls, **kwargs)
