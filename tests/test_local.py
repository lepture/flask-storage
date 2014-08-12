import os
import shutil

from flask_storage.local import LocalStorage
from ._base import BaseCase


class TestLocalStorage(BaseCase):
    CONFIG = dict(
        base_dir='tmp',
        base_url='/url/'
    )
    storage = LocalStorage('local', None, CONFIG)

    def setUp(self):
        super(TestLocalStorage, self).setUp()
        self._clean_up()

    def tearDown(self):
        super(TestLocalStorage, self).tearDown()
        self._clean_up()

    def _clean_up(self):
        if os.path.isdir(self.CONFIG['base_dir']):
            shutil.rmtree(self.CONFIG['base_dir'])

    def test_upload(self):
        response = self.upload()
        assert response.status_code == 200
        assert response.data == b'/url/flask.png'
        assert os.path.exists('tmp/flask.png')
