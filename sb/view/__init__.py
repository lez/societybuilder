#coding: pyxl
import json

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid.renderers import render_to_response
from pyxl import html

def notfound(request):
    response = render_to_response('layout', <div class="404">Ajjaj! Nem találjuk az oldalt.</div>, request=request)
    response.status_int = 404
    return response

def notfound_api(request):
    response = HTTPNotFound(body=json.dumps({'error': 'api endpoint not found'}))
    return response

def forbidden(request):
    response = render_to_response('layout', <div class="403">Nincs hozzáférésed ehhez az oldalhoz.</div>, request=request)
    response.status_int = 403
    return response

def forbidden_api(request):
    response = HTTPForbidden(body=json.dumps({'error': 'access denied to this resource'}))
    return response