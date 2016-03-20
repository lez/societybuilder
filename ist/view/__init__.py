#coding: pyxl
from pyramid.renderers import render_to_response
from pyxl import html

def notfound(request):
    response = render_to_response('layout', <div class="404">Ajjaj! Nem találjuk az oldalt.</div>, request=request)
    response.status_int = 404
    return response
