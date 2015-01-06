# coding: utf-8
"""
   flask_storage.qiniu
    ~~~~~~~~~~~~~~~~~~~

    Qiniu storage, save the file to Qiniu.
"""

from __future__ import absolute_import

from werkzeug import cached_property
import qiniu

from ._base import BaseStorage
from ._compat import urljoin
from ._utils import ConfigItem


_missing = object()


class QiniuStorage(BaseStorage):

    access_key = ConfigItem('access_key', required=True)
    secret_key = ConfigItem('secret_key', required=True)

    bucket = ConfigItem('bucket', required=True)
    base_url = ConfigItem('base_url', default=_missing)
    base_dir = ConfigItem('base_dir')

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
        if self.base_url is _missing:
            base_url = 'http://%s.qiniudn.com/' % self.bucket
        else:
            base_url = self.base_url

        if self.base_dir:
            urlbase = urljoin(base_url, self.base_dir)

        return urljoin(urlbase, filename)

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

    def save(self, storage, filename, token=None, extra=None):
        self.check(storage)
        if token is None:
            token = self.generate_upload_token()
        stream = storage.stream
        ret, err = qiniu.put_data(token, filename, stream)
        if err:
            raise QiniuException(err)
        return ret

    def delete(self, filename):
        ret, err = self._client.delete(self.bucket, filename)
        if err:
            raise QiniuException(err)
        return ret


class QiniuException(Exception):
    pass
