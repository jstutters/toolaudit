"""
The toolaudit application
"""

from kitlist import KitList
import logging
import readers
import os
import os.path
import sys


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
        log = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        log.addHandler(handler)

    def run(self):
        """
        Run the checks
        """

        kitlist_path = os.path.abspath(self.arguments.kitlist_file[0])
        kitlist_dir = os.path.dirname(kitlist_path)
        os.chdir(kitlist_dir)
        checked_kitlist = self.check(kitlist_path)
        if self.arguments.compare:
            if self.compare(checked_kitlist):
                sys.exit(1)
            else:
                sys.exit(0)
        if self.arguments.output_file:
            checked_kitlist.save(self.arguments.output_file[0])
        else:
            checked_kitlist.to_stdout()
        sys.exit(0)

    def check(self, kitlist_path):
        """
        Read the KitList specified by the user then run the checks.
        """

        kitlist = KitList.from_file(kitlist_path)
        for tool in kitlist.tools:
            logging.getLogger().info("Testing {0}".format(tool.name))
            if not os.path.exists(tool.path):
                err_msg = "The path for '{0}' does not exist: {1}".format(
                    tool.name, tool.path
                )
                raise IOError(err_msg)
            tool.version = tool.reader.func(tool.path, **tool.reader.args)
            if tool.tester:
                tool.output_checksum = tool.tester.func(
                    tool.path, **tool.tester.args
                )
            else:
                tool.output_checksum = None
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
            for k in ('checksum', 'path', 'version', 'output_checksum'):
                if getattr(ref_tool, k) != getattr(comp_tool, k):
                    mismatches.append((k, ref_tool, comp_tool))
        if not mismatches:
            print >> sys.stderr, "No mismatches found"
            return False
        else:
            for m in mismatches:
                print >> sys.stderr, '{0}\n\t{1}: {2} - {3}'.format(
                    m[1].name,
                    m[0],
                    getattr(m[1], m[0]),
                    getattr(m[2], m[0])
                )
            return True
