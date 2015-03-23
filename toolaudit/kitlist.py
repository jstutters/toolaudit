"""
Contains the KitList class
"""

import sys
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import readers


class AuditJob(object):  # pylint: disable=R0903
    """
    The audit of a single tool
    """

    def __init__(self, name, path, reader_name,  # pylint: disable=R0913
                 reader_func, reader_args, version=None, checksum=None):
        self.name = name
        self.path = path
        self.reader_name = reader_name
        self.reader_func = reader_func
        self.reader_args = reader_args
        self.version = version
        self.checksum = checksum

    def __repr__(self):
        return "{0}({1!r}, {2!r}, {3!r}, {4!r}, {5!r}, {6!r}, {7!r})".format(
            'AuditJob',
            self.name,
            self.path,
            self.reader_name,
            self.reader_func,
            self.reader_args,
            self.version,
            self.checksum
        )

    def as_dict(self):
        """
        Convert to a dict

        Returns
        -------
        dict : AuditJob
            This AuditJob as a dictionary
        """
        reader = {'name': self.reader_name}
        for k, v in self.reader_args.iteritems():
            reader[k] = v
        return {
            'name': self.name,
            'path': self.path,
            'reader': reader,
            'version': self.version,
            'checksum': self.checksum
        }


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

    @classmethod
    def from_file(cls, path):
        """
        Read the KitList description at *path* using a new instance of
        :class:`KitList` and return the resulting instance.

        Parameters
        ----------
        path : str
            The path to read from

        Returns
        -------
        :class:`KitList` : kitlist
            An instance with data loaded
        """

        instance = cls()
        instance.read(path)
        return instance

    def read(self, path):
        """
        Read a saved KitList in YAML format

        Parameters
        ----------
        path : str
            Path to a saved KitList
        """

        with open(path, 'r') as f:
            yaml_data = yaml.load(f, Loader=Loader)
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
                reader_args['regex'] = self._fixup_regex(reader_args['regex'])
            audit_job = AuditJob(
                tool_name, tool_path,
                reader_name, reader_func, reader_args,
                tool.get('version', None), tool.get('checksum', None)
            )
            tools.append(audit_job)
        self.tools = tools

    def get_tool(self, tool_name):
        """
        Get a single tool identifed by name

        Parameters
        ----------
        tool_name : str
            The name of the tool to retrieve

        Returns
        -------
        tool : class:`AuditJob` or None
            The requested tool or None if not found
        """
        for t in self.tools:
            if t.name == tool_name:
                return t

    def save(self, path):
        """
        Output the kitlist to YAML document.

        Parameters
        ----------
        path : str
            The path to write to
        """

        to_save = {'tools': [t.as_dict() for t in self.tools]}
        with open(path, 'w') as f:
            yaml.dump(to_save, f, explicit_start=True, Dumper=Dumper)

    def to_stdout(self):
        """
        Output the kitlist to stdout.
        """

        to_save = {'tools': [t.as_dict() for t in self.tools]}
        print >> sys.stdout, yaml.dump(
            to_save, explicit_start=True, Dumper=Dumper)

    @classmethod
    def _fixup_regex(cls, regex):
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
