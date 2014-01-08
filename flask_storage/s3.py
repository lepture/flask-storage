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

from ._base import BaseStorage, urljoin
from ._utils import ConfigItem


class S3Storage(BaseStorage):

    _params = ConfigItem('connection_params')

    access_key = ConfigItem('access_key', required=True)
    secret_key = ConfigItem('secret_key', required=True)
    bucket_name = ConfigItem('bucket', required=True)

    base_dir = ConfigItem('base_dir')
    base_url = ConfigItem('base_url')

    @cached_property
    def _connection(self):
        return S3Connection(self.access_key, self.secret_key, **self._params)

    @cached_property
    def bucket(self):
        if self.bucket_name not in self._connection:
            return self._connection.create_bucket(self.bucket_name)
        return self._connection.get_bucket(self.bucket_name)

    def url(self, filename):
        """Generate the url for a filename.

        :param filename: filename for generating the url
        """
        if self.base_dir:
            filename = '%s/%s' % (self.base_dir, filename)
        return urljoin(self.base_url, filename)

    def read(self, filename):
        if self.base_dir:
            filename = '%s/%s' % (self.base_dir, filename)
        k = self.bucket.get_key(filename)
        if not k:
            return None
        return k.read()

    def _generate_key(self, filename, headers=None):
        if self.base_dir:
            filename = '%s/%s' % (self.base_dir, filename)

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
