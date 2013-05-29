# coding: utf-8
"""
    flask_storage
    ~~~~~~~~~~~~~

    :copyright: (c) 2013 Hsiaoming Yang.
"""

# flake8: noqa

from ._base import *
from .local import LocalStorage
from .upyun import UpyunStorage
