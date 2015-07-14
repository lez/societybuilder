from pyramid.response import Response

def notfound(request):
    response = Response(body='404!')
    response.status_int = 404
    return response