import mimetypes
import http.client as httplib
import magic

VALID_IMAGE_MIMETYPES = [
    "image"
]

def get_mimetype(fobject):
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobject.read(1024))
    fobject.seek(0)
    return mimetype

def valid_image_mimetype(fobject):
    # http://stackoverflow.com/q/20272579/396300
    mimetype = get_mimetype(fobject)
    if mimetype:
        return mimetype.startswith('image')
    else:
        return False

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]


def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list])





def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    # http://stackoverflow.com/a/10543969/396300
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def image_exists(domain, path, check_size=False, size_limit=1024):
    try:
        conn = httplib.HTTPConnection(domain)
        conn.request('HEAD', path)
        response = conn.getresponse()
        headers = response.getheaders()
        conn.close()
    except:
        return False

    try:
        length = int([x[1] for x in headers if x[0] == 'content-length'][0])
    except:
        length = 0
    if length > size_limit:
        return False

    return response.status == 200