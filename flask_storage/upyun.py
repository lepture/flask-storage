# coding: utf-8
"""
    flask_storage.upyun
    ~~~~~~~~~~~~~~~~~~~

    Upyun storage, upload files to upyun.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import log
import base64

from ._base import BaseStorage
from ._compat import http, urljoin
from ._utils import ConfigItem


_missing = object()


def http_request(uri, headers=None, data=None, method=None):
    if headers is None:
        headers = {}

    if data and not method:
        method = 'POST'
    elif not method:
        method = 'GET'

    log.debug('Request %r with %r method' % (uri, method))
    req = http.Request(uri, headers=headers, data=data)
    req.get_method = lambda: method.upper()
    try:
        resp = http.urlopen(req)
    except http.HTTPError as resp:
        pass
    content = resp.read()
    resp.close()
    return resp, content


class UpyunStorage(BaseStorage):

    bucket = ConfigItem('bucket')
    folder = ConfigItem('folder')
    base_url = ConfigItem('base_url', default=_missing)

    username = ConfigItem('username')
    password = ConfigItem('password')

    is_testing = ConfigItem('TESTING')

    @property
    def root(self):
        uri = 'http://v0.api.upyun.com/%s/' % self.bucket
        if self.folder:
            uri = urljoin(uri, self.folder)
        return uri

    def request(self, uri, data=None, method=None, headers=None):
        """Make a request for upyun api.

        You rarely need this API, use save instead.
        """
        auth = base64.b64encode('%s:%s' % (self.username, self.password))

        if not headers:
            headers = {}

        headers['Authorization'] = 'Basic %s' % auth
        if self.is_testing:
            return (0, 0)
        return http_request(uri, headers=headers, data=data, method=method)

    def url(self, filename):
        """Generate the url for a filename.

        :param filename: Name of the file.
        """
        if self.base_url is _missing:
            base_url = 'http://%s.b0.upaiyun.com/' % self.bucket
        else:
            base_url = self.base_url

        if self.folder:
            urlbase = urljoin(base_url, self.folder)

        return urljoin(urlbase, filename)

    def usage(self):
        """Find the usage of your bucket.

        This function returns an integer.
        """
        uri = '%s?usage' % self.root
        resp, content = self.request(uri)
        return content

    def save(self, storage, filename):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The filename you want to save as.
        """
        self.check(storage)
        uri = urljoin(self.root, filename)
        headers = {'Mkdir': 'true'}
        stream = storage.stream
        if isinstance(stream, file):
            length = os.fstat(stream.fileno()).st_size
            headers['Content-Length'] = length
        self.request(uri, stream, 'PUT', headers)
        return self.url(filename)
