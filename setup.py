#!/usr/bin/env python

"""
Setup file for toolaudit.
"""

import codecs
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    """
    Read the contents of the files listed in filenames and return it as a
    string.
    """
    return codecs.open(os.path.join(here, filename), 'r').read()

setup(
    name='toolaudit',
    version='0.0.5',
    packages=['toolaudit'],
    zip_safe=False,
    install_requires=[
        "argparse>=1.3.0",
        "PyYAML>=3.11",
        "six>=1.9.0"
    ],
    entry_points={
        'console_scripts': [
            'toolaudit = toolaudit:main',
        ],
    },
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    description='Report on the tools used in your software pipeline.',
    long_description=read('README.rst'),
    url='https://github.com/jstutters/toolaudit',
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Topic :: System :: Systems Administration'
    ]
)
