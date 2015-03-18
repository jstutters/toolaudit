#!/usr/bin/env python

"""
Main file for toolaudit - a tool for auditing software pipelines
"""

import argparse
from application import ToolauditApp

__author__ = "Jon Stutters"
__copyright__ = "Copyright 2015, Jon Stutters"
__date__ = "$Date: 2015-03-18 00:08:20 +0000 (Wed, 18 Mar 2015) $".split()[1]
__version__ = '0.0.1'


def main():
    """The main function"""
    parser = create_parser()
    args = parser.parse_args()
    app = ToolauditApp(args)
    app.run()


def create_parser():
    """
    Create a configured instance of :class:`argparse.ArgumentParser`

    Returns
    -------
    parser : :class:`argparse.ArgumentParser`
    """

    parser = argparse.ArgumentParser(prog=__name__)
    parser.add_argument("-V", "--version",
                        action='version',
                        version='{0:} {1:}'.format(__name__, __version__))
    return parser
