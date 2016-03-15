from pyramid.response import Response
from ..util import l

def notfound(request):
    l.info('404 Not Found; path="%s%s"' % (request.path, '?'+request.query_string if request.query_string else ''))
    response = Response('404 van!')
    response.status_int = 404
    return response
