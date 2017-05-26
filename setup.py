#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=['C1t1.py'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
