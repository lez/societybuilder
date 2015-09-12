import os
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config
from ist import images
from ist.model.image import MEDIA_DIR

@view_config(route_name='media')
def media_view(request):
    path = os.path.join(os.path.dirname(__file__), MEDIA_DIR, request.matchdict['subpath'])
    if not os.path.exists(path):
        # try to generate thumbnail
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        parts = filename.split('.')

        if len(parts) != 3:
            return HTTPNotFound('File not found: %s' % path)
        resolution = parts[1]
        if resolution not in ['60x60', '100x100', '200x200', '300x300']:
            return HTTPNotFound('File not found: %s' % path)
        width, height = resolution.split('x')
        src = os.path.join(dirname, '{}.{}'.format(parts[0], parts[2]))
        images.generate_thumbnail(src, path, width=int(width), height=int(width))

    return FileResponse(path, request=request)