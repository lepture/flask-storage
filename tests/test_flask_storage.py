from flask.ext.testing import TestCase
from flask import Flask, request
from flask_storage import Storage


class BaseCase(TestCase):
    CONFIG = {}

    def create_app(self):
        app = Flask(__name__)
        app.config.update(self.CONFIG)
        app.testing = True
        s = Storage(app)

        @app.route('/upload', methods=('POST'))
        def upload():
            print request.files
            return s.save(request.files)

        return app

    def upload(self):
        fps = [self.app.open_resource("flask.png") for i in xrange(3)]
        data = [("uploads-%d.png" % i, fp) for i, fp in enumerate(fps)]
        response = self.client.post('/upload', data=dict(data))
        return response


class TestLocalStorage(BaseCase):
    CONFIG = dict(
        STORAGE_LOCAL_ROOT='tmp',
        STORAGE_LOCAL_URL='/url/'
    )

    def test_upload(self):
        self.upload()
