# -*- coding: utf-8 -*-

from .local import LocalStorage
from .s3 import S3Storage
from .upyun import UpyunStorage


_storages = {
    'local': LocalStorage,
    's3': S3Storage,
    'upyun': UpyunStorage
}


class Uploader(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    @property
    def backend(self):
        pass
