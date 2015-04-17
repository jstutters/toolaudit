#!/usr/bin/env python

"""
A tool for auditing software pipelines
"""

import argparse
from application import ToolauditApp

__author__ = "Jon Stutters"
__copyright__ = "Copyright 2015, Jon Stutters"
__version__ = '0.0.2'
__date__ = '2015-04-17'


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
    parser.add_argument("-c", "--compare",
                        nargs=1,
                        help='reference kitlist for comparison')
    parser.add_argument("-o", "--output_file",
                        nargs=1,
                        help='file to write to')
    parser.add_argument("kitlist_file", nargs=1)
    return parser
