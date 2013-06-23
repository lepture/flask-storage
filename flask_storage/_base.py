# coding: utf-8
"""
    flask_storage._base
    ~~~~~~~~~~~~~~~~~~~~

    Common utilities for flask storage.

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import logging
import urllib2
from werkzeug import FileStorage

__all__ = (
    'TEXT', 'DOCUMENTS', 'IMAGES', 'AUDIO', 'DATA', 'SCRIPTS',
    'ARCHIVES', 'EXECUTABLES', 'BaseStorage',
    'UploadNotAllowed', 'UploadFileExists', 'make_request'
)

log = logging.getLogger('flask_storage')

TEXT = ('txt',)

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
    def __init__(self, name='base', extensions=None, config=None):
        self.name = name
        self.config = config
        self.extensions = extensions or IMAGES

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

        _, extname = os.path.splitext(storage.filename)
        ext = extname.lower()[1:]
        if not self.extension_allowed(ext):
            raise UploadNotAllowed()

    def exists(self, filename):
        raise NotImplementedError

    def read(self, filename):
        raise NotImplementedError

    def delete(self, filename):
        raise NotImplementedError

    def save(self, storage, filename):
        raise NotImplementedError


class UploadNotAllowed(Exception):
    """This exception is raised if the upload was not allowed."""


class UploadFileExists(Exception):
    """This exception is raised when the uploaded file exits."""


def make_request(uri, headers=None, data=None, method=None):
    if headers is None:
        headers = {}

    if data and not method:
        method = 'POST'
    elif not method:
        method = 'GET'

    log.debug('Request %r with %r method' % (uri, method))
    req = urllib2.Request(uri, headers=headers, data=data)
    req.get_method = lambda: method.upper()
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as resp:
        pass
    content = resp.read()
    resp.close()
    return resp, content
