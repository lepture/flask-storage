# coding: utf-8
"""
    flask_storage.contrib.sae
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Storage for SAE backend.
"""

from .._base import BaseStorage


class SaeStorage(BaseStorage):
    @property
    def bucket(self):
        return self.config.get('STORAGE_SAE_BUCKET')

    def save(self):
        pass
