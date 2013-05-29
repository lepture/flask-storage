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
        """Generate the url for a filename.

        :param filename: filename for generating the url....
        """
        urlbase = self.config.get('STORAGE_LOCAL_URL')
        return urljoin(urlbase, filename)

    def exists(self, filename):
        """Detect if the file exists.

        :param filename: name of the file.
        """
        dest = os.path.join(self.root, filename)
        return os.path.exists(dest)

    def delete(self, filename):
        """Delete the specified file.

        :param filename: name of the file.
        """
        dest = os.path.join(self.root, filename)
        return os.remove(dest)

    def save(self, storage, filename):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The destination of the storage.
        """
        self.check(storage)
        dest = os.path.join(self.root, filename)

        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(dest):
            raise UploadFileExists()

        storage.save(dest)
        return self.url(filename)
