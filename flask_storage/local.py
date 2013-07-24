# coding: utf-8
"""
    flask_storage.local
    ~~~~~~~~~~~~~~~~~~~

    Local storage, save the file in local directory.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import sys
from ._base import BaseStorage, UploadFileExists, urljoin

if sys.version_info[0] == 3:
    string_type = str
else:
    string_type = unicode


class LocalStorage(BaseStorage):
    """Storage for local filesystem.

    Configuration:

        - base_dir: save file in base dir
        - base_url: base url root
    """
    @property
    def root(self):
        return self.config.get('base_dir')

    def exists(self, filename):
        """Detect if the file exists.

        :param filename: name of the file.
        """
        dest = os.path.join(self.root, filename)
        return os.path.exists(dest)

    def read(self, filename):
        """Read content of a file."""
        dest = os.path.join(self.root, filename)
        with open(dest) as f:
            return f.read()

    def write(self, filename, body, headers=None):
        """Write content to a file."""
        dest = os.path.join(self.root, filename)
        dirname = os.path.dirname(dest)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(dest, 'wb') as f:
            return f.write(to_bytes(body))

    def delete(self, filename):
        """Delete the specified file.

        :param filename: name of the file.
        """
        dest = os.path.join(self.root, filename)
        return os.remove(dest)

    def save(self, storage, filename, check=True):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The destination of the storage.
        """

        if check:
            self.check(storage)

        dest = os.path.join(self.root, filename)

        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(dest):
            raise UploadFileExists()

        storage.save(dest)
        return self.url(filename)


def to_bytes(text):
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text
