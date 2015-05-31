import os
import sh

MIME_TYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'GIF': 'image/gif',
}

def identify(path):
    if not os.path.exists(path):
        raise FileNotFoundError('File not found: %s' % path)
    props = sh.identify(path).split(' ')
    mime = MIME_TYPES[props[1]]
    width, height = props[2].split('x')
    return width, height, mime

def generate_thumbnail(src, dst, *, width, height):
    sh.convert(src, '-strip', '-resize', '{}x{}^'.format(width, height), '-gravity', 'center', '-extent', '{}x{}'.format(width, height), dst)
