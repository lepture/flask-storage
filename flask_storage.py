# coding: utf-8
"""
    flask_storage
    ~~~~~~~~~~~~~

    :copyright: (c) 2013 Hsiaoming Yang.
"""

import os
import logging
import base64
import urllib2
from urlparse import urljoin
from werkzeug import secure_filename, FileStorage

log = logging.getLogger('flask_storage')

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


class Storage(object):
    def __init__(self, app):
        self.backends = {}
        self.backend = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['storage'] = self

    def add_backend(self, name, extensions, config):
        if config.get('STORAGE_LOCAL_ROOT'):
            backend = LocalStorage(name, extensions, config)
        elif config.get('STORAGE_UPYUN_URL'):
            backend = UpyunStorage(name, extensions, config)
        elif config.get('STORAGE_S3_URL'):
            backend = LocalStorage(name, extensions, config)
        else:
            raise ValueError('Configuration Error')

        if not self.backend:
            self.backend = backend

        self.backends[name] = backend
        return backend

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            app = self.backends.get(key)
            if app:
                return app
            raise AttributeError('No such backend: %s' % key)


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
        dest = os.path.join(self.root, filename)

        folder = os.path.dirname(dest)
        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(dest):
            raise UploadFileExists()

        storage.save(dest)
        return self.url(filename)


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
    @property
    def bucket(self):
        return self.config.get('STORAGE_UPYUN_BUCKET')

    @property
    def folder(self):
        return self.config.get('STORAGE_UPYUN_FOLDER')

    @property
    def root(self):
        uri = 'http://v0.api.upyun.com/%s/' % self.bucket
        if self.folder:
            uri = urljoin(uri, self.folder)
        return uri

    def request(self, uri, data=None, method=None):
        username = self.config.get('STORAGE_UPYUN_USERNAME')
        password = self.config.get('STORAGE_UPYUN_PASSWORD')
        auth = base64.b64encode('%s:%s' % (username, password))
        headers = {'Authorization': 'Basic %s' % auth}
        return make_request(uri, headers=headers, data=data, method=method)

    def url(self, filename):
        urlbase = self.config.get('STORAGE_UPYUN_URL')
        if not urlbase:
            urlbase = 'http://%s.b0.upaiyun.com/' % self.bucket

        if self.folder:
            urlbase = urljoin(urlbase, self.folder)
        return urljoin(urlbase, filename)

    def usage(self):
        uri = '%s?usage' % self.root
        resp, content = self.request(uri)
        return content

    def save(self, storage, filename):
        self.check(storage)
        uri = urljoin(self.root, filename)
        self.request(uri, storage.stream, 'PUT')
        return self.url(filename)


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
