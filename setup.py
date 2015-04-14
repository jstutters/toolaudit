#!/usr/bin/env python

"""
Setup file for toolaudit.
"""

__author__ = "Jon Stutters"
__copyright__ = "Copyright 2015, Jon Stutters"
__date__ = "$Date: 2015-03-18 00:03:36 +0000 (Wed, 18 Mar 2015) $".split()[1]

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import toolaudit


class Tox(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(
    name='toolaudit',
    version=toolaudit.__version__,
    packages=['toolaudit'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    entry_points={
        'console_scripts': [
            'toolaudit = toolaudit:main',
        ],
    },
)
