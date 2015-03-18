#!/usr/bin/env python

"""
Setup file for toolaudit.
"""

__author__ = "Jon Stutters"
__copyright__ = "Copyright 2015, Jon Stutters"
__date__ = "$Date: 2015-03-18 00:03:36 +0000 (Wed, 18 Mar 2015) $".split()[1]

from setuptools import setup
import toolaudit

setup(
    name='toolaudit',
    version=toolaudit.__version__,
    packages=['toolaudit'],
    entry_points={
        'console_scripts': [
            'toolaudit = toolaudit:main',
        ],
    },
)
