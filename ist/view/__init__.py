from pyramid.response import Response

def notfound(request):
    response = Response('404 van!')
    response.status_int = 404
    return response