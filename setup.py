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
    install_requires=[
        "alabaster==0.7.2",
        "argparse==1.3.0",
        "Babel==1.3",
        "docutils==0.12",
        "Jinja2==2.7.3",
        "MarkupSafe==0.23",
        "numpydoc==0.5",
        "py==1.4.26",
        "Pygments==2.0.2",
        "pytest==2.6.4",
        "pytz==2014.10",
        "PyYAML==3.11",
        "six==1.9.0",
        "snowballstemmer==1.2.0",
        "Sphinx==1.3.1",
        "sphinx-rtd-theme==0.1.7"
    ],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    entry_points={
        'console_scripts': [
            'toolaudit = toolaudit:main',
        ],
    },
)
