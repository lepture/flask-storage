# coding: utf-8
"""
    flask_storage.s3
    ~~~~~~~~~~~~~~~~~~~

    S3 storage, save the file to Amazon S3.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

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

    @property
    def bucket(self):
        return self.config.get('bucket')

    @property
    def folder(self):
        return self.config.get('folder')

    def read(self, filename):
        pass

    def write(self, filename, body, headers=None):
        pass

    def save(self, storage, filename, check=True):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The destination of the storage.
        """

        if check:
            self.check(storage)
