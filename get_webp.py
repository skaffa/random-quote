from webptools import cwebp

def get_webp(_path):
    path = path.replace('.png', '.webp')
    cwebp(_path, path, "-q 95")
    return path