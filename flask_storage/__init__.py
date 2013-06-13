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


def create(app):
    """Create a storage instance.

    :param app: Flask app instance
    """
    type = app.config.get('STORAGE_TYPE', 'local')
    name = app.config.get('STORAGE_NAME', type)
    extensions = app.config.get('STORAGE_EXTENSIONS', None)

    if type == 'upyun':
        s = UpyunStorage(name, extensions, app.config)
    else:
        s = LocalStorage(name, extensions, app.config)

    app.extensions = getattr(app, 'extensions', {})
    app.extensions['storage'] = s
    return s
