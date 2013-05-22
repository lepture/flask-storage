#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Flask-Upload",
    version="0.1.0",
    author="Hsiaoming Yang",
    author_email="me@lepture.com",
    url="https://github.com/lepture/flask-uploadr",
    packages=["flask_upload"],
    description="Flask uploader extensions.",
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    install_requires=[],
    classifiers=[
    ]
)
