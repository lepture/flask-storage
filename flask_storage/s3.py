# coding: utf-8
"""
    flask_storage.s3
    ~~~~~~~~~~~~~~~~~~~

    S3 storage, save the file to Amazon S3.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import mimetypes
from werkzeug import cached_property
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from ._base import BaseStorage, UploadFileExists, urljoin


class S3Storage(BaseStorage):
    @cached_property
    def _connection(self):
        access_key = self.config.get('access_key')
        secret_key = self.config.get('secret_key')

        assert access_key
        assert secret_key

        params = self.config.get('connection_params', {})
        return S3Connection(access_key, secret_key, **params)

    @cached_property
    def bucket(self):
        name = self.config.get('bucket')
        if name not in self._connection:
            return self._connection.create_bucket(name)
        return self._connection.get_bucket(name)

    @cached_property
    def folder(self):
        return self.config.get('folder')

    def url(self, filename):
        """Generate the url for a filename.

        :param filename: filename for generating the url
        """
        if self.folder:
            filename = '%s/%s' % (self.folder, filename)
        urlbase = self.config.get('base_url')
        return urljoin(urlbase, filename)

    def read(self, filename):
        if self.folder:
            filename = '%s/%s' % (self.folder, filename)
        k = self.bucket.get_key(filename)
        if not k:
            return None
        return k.read()

    def _generate_key(self, filename, headers=None):
        if self.folder:
            filename = '%s/%s' % (self.folder, filename)

        k = self.bucket.new_key(filename)
        if not headers or 'Content-Type' not in headers:
            ct = mimetypes.guess_type(filename)[0]
            if ct:
                k.set_metadata('Content-Type', ct)

        return k

    def write(self, filename, body, headers=None):
        k = self._generate_key(filename, headers)
        # since Flask-Storage is designed for public storage
        # we need to set it public-read
        return k.set_contents_from_string(
            body, headers=headers, policy='public-read'
        )

    def save(self, storage, filename, headers=None, check=True):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The destination of the storage.
        """

        if check:
            self.check(storage)

        k = self._generate_key(filename)
        return k.set_contents_from_stream(
            storage.stream, headers=headers, policy='public-read'
        )
