"""
The toolaudit application
"""

from kitlist import KitList
import readers
import os.path


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
        """
        Run the checks
        """

        checked_kitlist = self.check()
        if self.arguments.compare:
            self.compare(checked_kitlist)
        if self.arguments.output_file:
            checked_kitlist.save(self.arguments.output_file[0])
        else:
            checked_kitlist.to_stdout()

    def check(self):
        """
        Read the KitList specified by the user then run the checks.
        """

        kitlist = KitList.from_file(self.arguments.kitlist_file[0])
        for tool in kitlist.tools:
            if not os.path.exists(tool.path):
                err_msg = "The path for '{0}' does not exist: {1}".format(
                    tool.name, tool.path
                )
                raise IOError(err_msg)
            tool.version = tool.reader_func(tool.path, **tool.reader_args)
            tool.checksum = readers.sha1(tool.path)
        return kitlist

    def compare(self, comparison):
        """
        Compare the KitList from the current test session with a reference copy
        """

        reference = KitList.from_file(self.arguments.compare[0])
        mismatches = []
        for ref_tool in reference.tools:
            comp_tool = comparison.get_tool(ref_tool.name)
            for k in ('checksum', 'path', 'version'):
                if getattr(ref_tool, k) != getattr(comp_tool, k):
                    mismatches.append((k, ref_tool, comp_tool))
        if not mismatches:
            print "No mismatches found"
        else:
            for m in mismatches:
                print '{0}\n\t{1}: {2} - {3}'.format(
                    m[1].name,
                    m[0],
                    getattr(m[1], m[0]),
                    getattr(m[2], m[0])
                )
