import shutil
from pyramid.view import view_config
import os
import tempfile
from ist.auth import require_login
from ist.model.image import Image
from ..util import *
from .. import images

@view_config(route_name='upload', renderer='json', request_method='POST')
@require_login
def store_file(request):
    filename = request.POST['file'].filename.split('/')[-1]
    input_file = request.POST['file'].file

    input_file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tmpname = f.name
        shutil.copyfileobj(input_file, f)

    width, height, mime = images.identify(tmpname)
    size = os.path.getsize(tmpname)

    image = Image(
        width=width,
        height=height,
        mime=mime,
        size=size,
        user=request.current_user,
        orig_filename=filename,
    )
    image.path = 'tmp/%s.%s' % (random_string(), image.extension)
    os.makedirs(os.path.dirname(image.real_path), exist_ok=True)
    image.save()
    os.rename(tmpname, image.real_path)
    return {'success': 1, 'image_id': image.id, 'thumbnail': image.uri(thumbnail='100x100')}