# coding: utf-8
"""
    flask_storage.local
    ~~~~~~~~~~~~~~~~~~~

    Local storage, save the file in local directory.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import hashlib
import time
from ._compat import to_bytes, urljoin
from ._base import BaseStorage, UploadFileExists
from ._utils import ConfigItem


class LocalStorage(BaseStorage):
    """Storage for local filesystem.

    Configuration:

        - base_dir: save file in base dir
        - base_url: base url root
    """
    base_path = ConfigItem('base_path', required=True)
    base_dir = ConfigItem('base_dir', default='')
    base_url = ConfigItem('base_url', default='')
    secret_key = ConfigItem('secret_key')
    expires = ConfigItem('expires', default=3600)
    private = ConfigItem('private', default=False)

    def url(self, filename, base_dir=None):
        """Generate the url for a filename.

        :param filename: Name of the file.
        """
        filename = os.path.join(base_dir or self.base_dir, filename)

        file_url = urljoin(self.base_url, filename)

        if self.private:
            expires, token = self.generate_download_token(filename)
            file_url = '{}?e={}&t={}'.format(file_url, expires, token)
        return file_url

    def generate_download_token(self, filename=None, expires=None):
        """Generate the token and expires for download.

        :param filename: Name of the file.
        """
        expires = int(time.time()) + (expires or self.expires)
        token = hashlib.md5(self.secret_key+filename+str(expires)).hexdigest()[8:16]
        return expires, token

    def check_private_url(self, filename, expires, token):
        new_token = hashlib.md5(self.secret_key+filename+expires).hexdigest()[8:16]
        return new_token == token

    def exists(self, filename, base_dir=None):
        """Detect if the file exists.

        :param filename: name of the file.
        """
        dest = os.path.join(self.base_path, base_dir or self.base_dir, filename)
        return os.path.exists(dest)

    def read(self, filename, base_dir=None):
        """Read content of a file."""
        dest = os.path.join(self.base_path, base_dir or self.base_dir, filename)
        with open(dest) as f:
            return f.read()

    def write(self, filename, body, headers=None, base_dir=None):
        """Write content to a file."""
        dest = os.path.join(self.base_path, base_dir or self.base_dir, filename)
        dirname = os.path.dirname(dest)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(dest, 'wb') as f:
            return f.write(to_bytes(body))

    def delete(self, filename, base_dir=None):
        """Delete the specified file.

        :param filename: name of the file.
        """
        dest = os.path.join(self.base_path, base_dir or self.base_dir, filename)
        return os.remove(dest)

    def save(self, storage, filename=None, base_dir=None):
        """Save a storage (`werkzeug.FileStorage`) with the specified
        filename.

        :param storage: The storage to be saved.
        :param filename: The destination of the storage.
        """

        self.check(storage)

        filename = filename if filename else storage.filename

        _, extname = os.path.splitext(filename)
        ext = extname.lower()[1:]
        if not self.extension_allowed(ext):
            _, extname = os.path.splitext(storage.filename)
            ext = extname.lower()[1:]
            filename = '{}.{}'.format(filename, ext) if ext else filename

        dest = os.path.join(self.base_path, base_dir or self.base_dir, filename)

        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(dest):
            raise UploadFileExists()

        storage.save(dest)
        return filename
