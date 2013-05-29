# coding: utf-8
"""
    flask_storage.local
    ~~~~~~~~~~~~~~~~~~~

    Local storage, save the file in local directory.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
from urlparse import urljoin
from ._base import BaseStorage, UploadFileExists


class LocalStorage(BaseStorage):
    @property
    def root(self):
        return self.config.get('STORAGE_LOCAL_ROOT')

    def url(self, filename):
        urlbase = self.config.get('STORAGE_LOCAL_URL')
        return urljoin(urlbase, filename)

    def exists(self, filename):
        dest = os.path.join(self.root, filename)
        return os.path.exists(dest)

    def delete(self, filename):
        dest = os.path.join(self.root, filename)
        return os.remove(dest)

    def save(self, storage, filename):
        self.check(storage)
        dest = os.path.join(self.root, filename)

        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(dest):
            raise UploadFileExists()

        storage.save(dest)
        return self.url(filename)
