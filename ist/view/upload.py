import shutil
from pyramid.view import view_config
import os
import tempfile
from ..util import *

@view_config(route_name='upload', renderer='json', request_method='POST')
def store_file(request):
    filename = request.POST['image'].filename.split('/')[-1]
    input_file = request.POST['image'].file
    input_file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tmpname = f.name
        shutil.copyfileobj(input_file, f)




    os.rename(tmpname, '/tmp/yes')
    return {'success': 1}