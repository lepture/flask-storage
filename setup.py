#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re


def fread(filepath):
    with open(filepath) as f:
        return f.read()


def version():
    content = fread('flask_storage/__init__.py')
    m = re.findall(r'__version__\s*=\s*\'(.*)\'', content)
    return m[0]


extras_require = dict(
    qiniu=['qiniu'],
    s3=['boto'],
    full=['qiniu', 'boto'],
)


setup(
    name='Flask-Storage',
    version=version(),
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    url='https://github.com/lepture/flask-storage',
    packages=["flask_storage"],
    description="Flask upload and storage extensions.",
    long_description=fread('README.rst'),
    license='BSD',
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    tests_require=[
        'nose',
    ],
    extras_require=extras_require,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
