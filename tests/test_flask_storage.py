import os
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

        @app.route('/upload', methods=['POST'])
        def upload():
            image = request.files.get('image')
            return s.save(image, 'flask.png')

        return app

    def upload(self):
        image = self.app.open_resource("flask.png")
        response = self.client.post('/upload', data={'image': image})
        return response


class TestLocalStorage(BaseCase):
    CONFIG = dict(
        STORAGE_LOCAL_ROOT='tmp',
        STORAGE_LOCAL_URL='/url/'
    )

    def test_upload(self):
        response = self.upload()
        assert response.status_code == 200
        assert response.data == '/url/flask.png'
        assert os.path.exists('tmp/flask.png')
