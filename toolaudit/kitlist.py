"""
Contains the KitList class
"""

from collections import namedtuple
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import readers

AuditJob = namedtuple(
    'AuditJob',
    ['name', 'path', 'reader_func', 'reader_args']
)


class KitList(object):
    """
    Represents a list of applications used in a pipeline and the procedure
    used to check each applications version
    """

    def __init__(self):
        self.reader_functions = {
            'command_line': readers.command_line,
            'line_in_file': readers.line_in_file,
            'manual': readers.manual
        }
        self.tools = []

    def read(self, path):
        """
        Read a saved KitList in YAML format

        Parameters
        ----------
        path : str
            Path to a saved KitList
        """

        with open(path, 'r') as f:
            yaml_data = load(f, Loader=Loader)
        if 'tools' not in yaml_data:
            raise(KeyError(
                'The kitlist provided does not contain a tools element'
            ))
        tools = []
        for tool in yaml_data['tools']:
            tool_name = tool['name']
            tool_path = tool['path']
            reader_name = tool['reader']['name']
            if reader_name not in self.reader_functions:
                raise(KeyError(
                    'Unknown reader function {}'.format(reader_name)
                ))
            args = [
                (k, v) for k, v in tool['reader'].iteritems() if k != 'name'
            ]
            reader_func = self.reader_functions[reader_name]
            reader_args = dict(args)
            if 'regex' in reader_args:
                reader_args['regex'] = self.fixup_regex(reader_args['regex'])
            audit_job = AuditJob(
                tool_name, tool_path, reader_func, reader_args
            )
            tools.append(audit_job)
        self.tools = tools

    @classmethod
    def fixup_regex(cls, regex):
        """
        Replace double backslashes in a string with single backslashes.

        PyYAML needs backslashes in strings to be escaped but they need
        to be unescaped when used with :module:`re`.

        Parameters
        ----------
        regex : str
            A regular expression string in which backslashes are escaped

        Returns
        -------
        fixed_regex : str
            The input string with backslashes unescaped
        """

        return regex.replace('\\\\', '\\')
