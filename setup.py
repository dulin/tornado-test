#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

from setuptools import setup, find_packages

requires = [
    "tornado",
    "pycryptodomex",
    "psycopg2"
]

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))

setup(
    name="tornado_playground",
    version=__version__,
    description="My playground",
    author="Martin Dulin",
    author_email='martin@dulin.me.uk',
    keywords='web tornado',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    scripts= ['bin/playground'],
    entry_points={
        "console_scripts": [
            "serve = app:main",
        ],
    },
)
