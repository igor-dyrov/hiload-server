from enum import IntEnum


class StatusCode(IntEnum):
    OK = 200
    NOT_FOUND = 404
    FORBIDDEN = 403
    METHOD_NOT_ALLOWED = 405


STATUS_CODES = {
    StatusCode.OK: 'OK',
    StatusCode.NOT_FOUND: 'Not Found',
    StatusCode.FORBIDDEN: 'Forbidden',
    StatusCode.METHOD_NOT_ALLOWED: 'Method Not Allowed'
}

CONTENT_TYPES = {
    'css': 'text/css',
    'gif': 'image/gif',
    'html': 'text/html',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'swf': 'application/x-shockwave-flash',
    'txt': 'text/plain'
}


ALLOWED_METHODS = ('GET', 'HEAD')
SERVER = 'PythonPreforkHttpServer'
HTTP_VERSION = 'HTTP/1.1'
