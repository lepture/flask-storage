# coding: utf-8
"""
    flask_storage
    ~~~~~~~~~~~~~

    Collection of storage backends.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

# flake8: noqa

from . import _info
__version__ = _info.VERSION
__author__ = _info.AUTHOR

from ._base import *
from .local import LocalStorage
from .upyun import UpyunStorage


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

        # TODO: more types
        if type == 'upyun':
            s = UpyunStorage(name, extensions, config)
        else:
            s = LocalStorage(name, extensions, config)

        return s

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            backend = self.backends.get(key)
            if backend:
                return backend
            raise AttributeError('No such backend: %s' % key)
