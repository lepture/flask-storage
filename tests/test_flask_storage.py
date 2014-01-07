import os
import unittest

from flask import Flask, request
from flask_storage.local import LocalStorage


class BaseCase(unittest.TestCase):
    CONFIG = {
        'TESTING': True
    }

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = Flask(__name__)
        app.config.update(self.CONFIG)

        @app.route('/upload', methods=['POST'])
        def upload():
            image = request.files.get('image')
            return self.storage.save(image, 'flask.png')

        return app

    def upload(self):
        image = self.app.open_resource("flask.png")
        response = self.client.post('/upload', data={'image': image})
        return response


class TestLocalStorage(BaseCase):
    CONFIG = dict(
        base_dir='tmp',
        base_url='/url/'
    )
    storage = LocalStorage('local', None, CONFIG)

    def test_upload(self):
        response = self.upload()
        assert response.status_code == 200
        assert response.data == '/url/flask.png'
        assert os.path.exists('tmp/flask.png')
