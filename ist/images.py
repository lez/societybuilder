import os
import subprocess

MIME_TYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'GIF': 'image/gif',
}

def identify(path):
    if not os.path.exists(path):
        raise FileNotFoundError('File not found: %s' % path)
    stdout, stderr = subprocess.Popen(['identify', path])
    props = stdout.split(' ')
    width, height = props[2].split('x')
    return int(width), int(height), MIME_TYPES[props[1]]

def generate_thumbnail(src, dst, *, width, height):
    subprocess.Popen(['convert', src, '-strip', '-resize', '{}x{}^'.format(width, height), '-gravity', 'center', '-extent', '{}x{}'.format(width, height), dst]).communicate()
