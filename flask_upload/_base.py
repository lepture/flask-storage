# coding: utf-8


class BaseStorage(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def normalize_filename(self, filename):
        # TODO
        pass

    def is_allowed(self, storage):
        # TODO
        pass

    def save(self, storage, destination):
        """
        This saves a `werkzeug.FileStorage into the destination.

        :param storage: The uploaded file to save
        :param destination: The destination for the storage
        """
        raise NotImplementedError
