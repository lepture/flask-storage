from flask_storage.qiniu import QiniuStorage
from ._base import BaseCase


class TestQiniuStorage(BaseCase):
    CONFIG = dict(
        access_key='test_access_key',
        secret_key='test_secret_key',
        bucket='qiniu_test'
    )

    storage = QiniuStorage('qiniu', None, CONFIG)

    def setUp(self):
        super(TestQiniuStorage, self).setUp()
        self.io = self.patch('qiniu.io')
        self.upload_token = self.patch('qiniu.rs.PutPolicy.token')

    def test_upload(self):
        ret, err = {'key': 'flask.png'}, None
        self.io.put.return_value = ret, err
        response = self.upload()
        assert self.upload_token.call_count == 1
        assert self.io.put.call_count == 1
