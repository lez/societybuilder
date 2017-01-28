#coding: pyxl
from sb.view.element import *
from pyxl import html

from pyramid.interfaces import IRendererFactory
from zope.interface import implementer


@implementer(IRendererFactory)
class PyxlRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        return str(value)


@implementer(IRendererFactory)
class ApiRenderer:
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        request = system.get('request')
        if request is not None:
            request.response.content_type = 'application/json'

        return ApiEncoder().encode(value)



@implementer(IRendererFactory)
class LayoutRenderer:
    def __init__(self, info):
        self.info = info

    def __call__(self, value, system):
        user = system['request'].user

        if isinstance(value, tuple) and len(value) == 2:
            content, rightbar = value
        else:
            content = value
            rightbar = <rightbar user="{user}" />

        layout = <layout user="{user}">
            <div id="sb_content">
                {content}
            </div>
            {rightbar}
        </layout>

        return str(layout)
