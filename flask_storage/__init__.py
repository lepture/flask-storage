# coding: utf-8
"""
    flask_storage
    ~~~~~~~~~~~~~

    Collection of storage backends.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

# flake8: noqa

from ._info import VERSION as __version__
from ._info import AUTHOR as __author__

from ._base import *
from .local import LocalStorage
from .s3 import S3Storage


class Storage(object):
    """Create a storage instance.

    :param app: Flask app instance
    """

    def __init__(self, app=None):
        self.backends = {}
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['storage'] = self

    def add_backend(self, name, backend):
        self.backends[name] = backend
        return backend

    @classmethod
    def create_backend(cls, type, name=None, extensions=None, config=None):
        if not name:
            name = type

        backends = {
            'local': LocalStorage,
            's3': S3Storage,
        }
        return backends[type](name, extensions, config)

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            backend = self.backends.get(key)
            if backend:
                return backend
            raise AttributeError('No such backend: %s' % key)
