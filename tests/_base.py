from mock import patch
import unittest

from flask import Flask, request


class BaseCase(unittest.TestCase):
    CONFIG = {
        'TESTING': True,
        'DEBUG': True,
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
            return str(self.storage.save(image, 'flask.png'))

        return app

    def upload(self):
        image = self.app.open_resource("flask.png")
        response = self.client.post('/upload', data={'image': image})
        return response

    def patch(self, target, *args, **kwargs):
        patcher = patch(target, *args, **kwargs)
        patched_object = patcher.start()
        self.addCleanup(patcher.stop)
        return patched_object
