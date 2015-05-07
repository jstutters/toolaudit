#!/usr/bin/env python

"""
A tool for auditing software pipelines
"""

import argparse
from . import application

__author__ = "Jon Stutters"
__copyright__ = "Copyright 2015, Jon Stutters"
__version__ = '0.0.3'
__date__ = '2015-04-23'


def main():
    """The main function"""
    parser = create_parser()
    args = parser.parse_args()
    if 'compare' in args:
        compare_file = args.compare
    else:
        compare_file = None
    if 'outputfile' in args:
        output_file = args.outputfile
    else:
        output_file = None
    if 'onlytest' in args:
        only_test = args.onlytest
    app = application.ToolauditApp()
    app.run(
        args.kitlist_file,
        compare_file=compare_file,
        output_file=output_file,
        skip_tests=args.skiptests,
        only_test=only_test
    )


def create_parser():
    """
    Create a configured instance of :class:`argparse.ArgumentParser`

    Returns
    -------
    parser : :class:`argparse.ArgumentParser`
    """

    parser = argparse.ArgumentParser(prog=__name__)
    parser.add_argument('-V', '--version',
                        action='version',
                        version='{0:} {1:}'.format(__name__, __version__))
    parser.add_argument('-S', '--skiptests',
                        help='just get version numbers and binary hashes',
                        action='store_true')
    parser.add_argument('-O', '--onlytest',
                        help='only run the specified test')
    parser.add_argument('-c', '--compare',
                        help='reference kitlist for comparison')
    parser.add_argument('-o', '--outputfile',
                        help='file to write to')
    parser.add_argument('kitlist_file')
    return parser
