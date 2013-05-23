# coding: utf-8


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
    def __init__(self, name='base', extensions=None, config=None):
        self.name = name
        self.config = config
        if extensions is None:
            # default is images
            self.extensions = IMAGES
        else:
            self.extensions = extensions

    def url(self, filename):
        """This function gets the URL a filename."""
        raise NotImplementedError

    def extension_allowed(self, extname):
        return extname in self.extensions

    def save(self, storage, destination):
        raise NotImplementedError
