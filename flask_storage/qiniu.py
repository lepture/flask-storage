# coding: utf-8
"""
   flask_storage.qiniu
    ~~~~~~~~~~~~~~~~~~~

    Qiniu storage, save the file to Qiniu.
"""

from __future__ import absolute_import
import os
from werkzeug import cached_property
import qiniu

from ._base import BaseStorage
from ._compat import urljoin
from ._utils import ConfigItem


class QiniuStorage(BaseStorage):

    access_key = ConfigItem('access_key', required=True)
    secret_key = ConfigItem('secret_key', required=True)

    bucket = ConfigItem('bucket', required=True)
    base_url = ConfigItem('base_url', required=True)
    base_dir = ConfigItem('base_dir')
    private = ConfigItem('private', default=False)
    expires = ConfigItem('expires', default=3600)

    def __init__(self, name, extensions, config):
        super(QiniuStorage, self).__init__(name, extensions, config)

    @cached_property
    def auth(self):
        return qiniu.Auth(self.access_key, self.secret_key)

    @cached_property
    def _client(self):
        return qiniu.BucketManager(self.auth)

    def url(self, filename):
        """Generate the url for a filename.

        :param filename: Name of the file.
        """
        base_url = urljoin(self.base_url, self.base_dir) if self.base_dir else self.base_url

        file_url = urljoin(base_url, filename)
        if self.private:
            return self.auth.private_download_url(file_url, expires=self.expires)
        return file_url

    def generate_upload_token(self, filename=None):
        """
        Generate a upload token used by client.
        :param filename: Client can upload file if filename is None.
                    Otherwise, client can modify the file.
        """
        if filename:
            token = self.auth.upload_token(self.bucket, filename)
        else:
            token = self.auth.upload_token(self.bucket)
        return token

    def save(self, storage, filename, token=None):
        self.check(storage)

        _, extname = os.path.splitext(filename)
        ext = extname.lower()[1:]
        if not self.extension_allowed(ext):
            _, extname = os.path.splitext(storage.filename)
            ext = extname.lower()[1:]
            filename = '{}.{}'.format(filename, ext) if ext else filename

        if token is None:
            token = self.generate_upload_token()
        stream = storage.stream
        ret, info = qiniu.put_data(token, filename, stream)
        if ret is None:
            raise QiniuException(info)
        return ret

    def delete(self, filename):
        ret, info = self._client.delete(self.bucket, filename)
        if ret is None:
            raise QiniuException(info)
        return ret


class QiniuException(Exception):
    pass
