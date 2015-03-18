"""
The toolaudit application
"""

import sys
import toolaudit


class ToolauditApp(object):
    """Class for toolaudit functions"""
    def __init__(self, arguments):
        """
        Initialize the toolaudit class

        Parameters
        ----------
        arguments : Namespace
            The output of :class:`argparse.ArgumentParser.parse_args`
        """

        self.arguments = arguments

    def run(self):
        pass
