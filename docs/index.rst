.. Flask-Storage documentation master file, created by
   sphinx-quickstart on Wed May 29 18:55:59 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-Storage
=============

Flask-Storage is a collection of backends for file storage.

The built-in backends:

- Local backend
- Upyun backend (https://www.upyun.com/)

Installation
------------

Install the extension with pip::

    $ pip install Flask-Storage

or alternatively if have not pip installed::

    $ easy_install Flask-Storage


Configuration
--------------


API Reference
-------------

This part of the documentation covers ench and every public class or
function from Flask-Storage.

.. module:: flask_storage

.. autoclass:: LocalStorage
   :members:

.. autoclass:: UpyunStorage
   :members:
