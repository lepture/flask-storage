# coding: utf-8

import os
from urlparse import urljoin
from werkzeug import secure_filename, FileStorage

TEXT = ('txt')

DOCUMENTS = (
    'rtf', 'odf', 'ods', 'gnumeric', 'abw',
    'doc', 'docx', 'xls', 'xlsx'
)

# This contains basic image types that are viewable by most browsers
IMAGES = ('jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp')

# This contains audio file types
AUDIO = ('wav', 'mp3', 'aac', 'ogg', 'oga', 'flac')

# This is for structured data files
DATA = ('csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml')

# This contains various types of scripts
SCRIPTS = ('py', 'js', 'rb', 'sh', 'pl', 'php')

# This contains archive and compression formats
ARCHIVES = ('gz', 'bz2', 'zip', 'tar', 'tgz', 'txz', '7z')

# This contains shared libraries and executable files
EXECUTABLES = ('so', 'ext', 'dll')


class BaseStorage(object):
    def __init__(self, name='base', extensions=IMAGES, config=None):
        self.name = name
        self.config = config
        self.extensions = extensions

    def url(self, filename):
        """This function gets the URL a filename."""
        raise NotImplementedError

    def extension_allowed(self, extname):
        if not self.extensions:
            return True
        return extname in self.extensions

    def check(self, storage):
        """
        Check if the storage can be saved.

        :param storage: The storage to be saved.

        This function should be called everytime when you want to
        save a storage::

            class DemoStorage(BaseStorage):
                def save(self, storage, filename):
                    # check storage before saving it
                    self.check(storage)
        """
        if not isinstance(storage, FileStorage):
            raise TypeError('storage must be a werkzeug.FileStorage')

        _, extname = os.path.splitext(secure_filename(storage.filename))
        ext = extname.lower()[1:]
        if not self.extension_allowed(ext):
            raise UploadNotAllowed()

    def save(self, storage, filename):
        raise NotImplementedError


class LocalStorage(BaseStorage):
    @property
    def root(self):
        return self.config.get('STORAGE_LOCAL_ROOT')

    def url(self, filename):
        urlbase = self.config.get('STORAGE_LOCAL_URL')
        return urljoin(urlbase, filename)

    def save(self, storage, filename):
        self.check(storage)


class S3Storage(BaseStorage):
    def request(self):
        pass

    def url(self, filename):
        urlbase = self.config.get('STORAGE_S3_URL')
        return urljoin(urlbase, filename)

    def save(self, storage, filename):
        self.check(storage)
        pass


class UpyunStorage(BaseStorage):
    def request(self):
        pass

    def url(self, filename):
        urlbase = self.config.get('STORAGE_UPYUN_URL')
        return urljoin(urlbase, filename)

    def save(self, storage, filename):
        self.check(storage)
        pass


class UploadNotAllowed(Exception):
    """This exception is raised if the upload was not allowed."""
