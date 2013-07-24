# coding: utf-8
"""
    flask_storage.upyun
    ~~~~~~~~~~~~~~~~~~~

    Upyun storage, upload files to upyun.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import base64
from ._base import BaseStorage, make_request, urljoin


class UpyunStorage(BaseStorage):
    @property
    def bucket(self):
        return self.config.get('bucket')

    @property
    def folder(self):
        return self.config.get('folder')

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
        username = self.config.get('username')
        password = self.config.get('password')
        auth = base64.b64encode('%s:%s' % (username, password))

        if not headers:
            headers = {}

        headers['Authorization'] = 'Basic %s' % auth
        if self.config.get('TESTING'):
            # for testing
            return (0, 0)
        return make_request(uri, headers=headers, data=data, method=method)

    def url(self, filename):
        """Generate the url for a filename.

        :param filename: Name of the file.
        """
        urlbase = self.config.get('base_url')
        if not urlbase:
            urlbase = 'http://%s.b0.upaiyun.com/' % self.bucket

        if self.folder:
            urlbase = urljoin(urlbase, self.folder)
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
