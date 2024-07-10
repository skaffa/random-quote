from webptools import cwebp

def get_webp(_path):
    path = _path.replace('.png', '.webp')
    cwebp(_path, path, "-q 85")
    return path