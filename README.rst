Flask-Storage
=============

Flask-Storage is a collection of backends for file storage.

The built-in backends:

- Local backend
- Upyun backend
- Qiniu backend
- S3 backend


Installation
------------

Install flask-storage is simple with pip_::

    $ pip install Flask-Storage

If you don't have pip installed, try with easy_install::

    $ easy_install Flask-Storage

.. _pip: http://www.pip-installer.org/

Quickstart
----------------

A example of Qiniu, put this to your flask config file:

.. code::

    STORAGE_TYPE = "qiniu"
    STORAGE_NAME = "storage_name"
    STORAGE_CONFIG = {
        "access_key": "access_key",
        "secret_key": "secret_key",
        "bucket": "bucket",
        "base_url": "http://xxxcdn.com/",
        "base_dir": "",
    }
    from flask.ext.storage import _base
    STORAGE_EXTENSIONS = _base.IMAGES + _base.ARCHIVES


Your code:

.. code-block:: python
    
    from flask import Flask,request,abort 
    from flask.ext.storage import Storage
    storage = Storage()
    app = Flask(__name__)
    app.config.from_object('default_config')
    storage.init_app(app)

    @app.route("/upload")
    def post(self):
        if len(request.files) == 0:
            abort(400, "didn't get any upload files")
        f = request.files.values()[0]
        ret = storage.save(f, f.filename)
        return ret["key"]
        
    @app.route("/delete/<key>")
    def delete(self, key):
        ret = storage.delete(key)
        return ret or "OK"

Configuration
-------------
