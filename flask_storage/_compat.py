import sys
try:
    from urlparse import urljoin
    import urllib2 as http
except ImportError:
    from urllib.parse import urljoin
    from urllib import request as http

if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = unicode


__all__ = ['urljoin', 'http', 'string_type', 'to_bytes']


def to_bytes(text):
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text
