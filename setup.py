#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Flask-Storage",
    version="0.1.0",
    author="Hsiaoming Yang",
    author_email="me@lepture.com",
    url="https://github.com/lepture/flask-uploadr",
    packages=["flask_storage"],
    description="Flask upload and storage extensions.",
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    install_requires=['Flask'],
    classifiers=[
    ]
)
