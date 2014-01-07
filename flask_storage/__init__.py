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
from werkzeug.utils import import_string


backends = {
    'local': 'flask_storage.local.LocalStorage',
    's3': 'flask_storage.s3.S3Storage',
    'upyun': 'flask_storage.upyun.UpyunStorage',
}


class Storage(object):
    """Create a storage instance.

    :param app: Flask app instance
    """

    def __init__(self, app=None):
        self._backend = None
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.config.setdefault('STORAGE_TYPE', 'local')
        t = app.config.get('STORAGE_TYPE')
        assert t in backends, "Storage type not supported."

        Backend = import_string(backends[t])
        name = app.config.get('STORAGE_NAME', t)
        extensions = app.config.get('STORAGE_EXTENSIONS', None)
        config = app.config.get('STORAGE_CONFIG', {})

        self._backend = Backend(name, extensions, config)

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            if self._backend is None:
                raise RuntimeError("Backend not configured.")
            return getattr(self._backend, key)
