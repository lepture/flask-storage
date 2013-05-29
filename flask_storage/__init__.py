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
