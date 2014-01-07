# coding: utf-8
"""
    flask_storage.contrib.sae
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Storage for SAE backend.
"""

from ._base import BaseStorage
from ._utils import ConfigItem


class SaeStorage(BaseStorage):

    bucket = ConfigItem('STORAGE_SAE_BUCKET')

    def save(self):
        pass  # TODO
