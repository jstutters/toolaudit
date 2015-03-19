"""
The toolaudit application
"""

from kitlist import KitList


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
        self.kitlist = KitList()
        self.load_kitlist()

    def run(self):
        """
        Run the checks
        """
        for tool in self.kitlist.tools:
            print tool.reader_func(tool.path, **tool.reader_args)

    def load_kitlist(self):
        """
        Populate self.kitlist with data from the path provided on the command
        line
        """
        self.kitlist.read(self.arguments.kitlist_file[0])
