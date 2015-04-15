"""
Contains the KitList class
"""

from collections import namedtuple
import sys
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import readers
import testers


Reader = namedtuple('Reader', ['name', 'func', 'args'])
Tester = namedtuple('Tester', ['name', 'func', 'args'])


class AuditJob(object):  # pylint: disable=R0903
    """
    The audit of a single tool
    """

    def __init__(self, name, path, reader, tester=None, version=None,
                 checksum=None, output_checksum=None):
        self.name = name
        self.path = path
        self.reader = reader
        self.tester = tester
        self.version = version
        self.checksum = checksum
        self.output_checksum = output_checksum

    def __repr__(self):
        r = "{0}({1!r}, {2!r}, {3!r}, {4!r}, {5!r}, {6!r}, {7!r}, {8!r})"
        return r.format(
            'AuditJob',
            self.name,
            self.path,
            self.reader,
            self.tester,
            self.version,
            self.checksum,
            self.output_checksum
        )

    def as_dict(self):
        """
        Convert to a dict

        Returns
        -------
        dict : AuditJob
            This AuditJob as a dictionary
        """
        reader_dict = {'name': self.reader.name}
        for k, v in self.reader.args.iteritems():
            reader_dict[k] = v
        if self.tester:
            tester_dict = {'name': self.tester.name}
            for k, v in self.tester.args.iteritems():
                tester_dict[k] = v
        else:
            tester_dict = None
        return {
            'name': self.name,
            'path': self.path,
            'reader': reader_dict,
            'tester': tester_dict,
            'version': self.version,
            'checksum': self.checksum,
            'output_checksum': self.output_checksum
        }


class KitList(object):
    """
    Represents a list of applications used in a pipeline and the procedure
    used to check each applications version
    """

    reader_functions = {
        'command_line': readers.command_line,
        'line_in_file': readers.line_in_file,
        'manual': readers.manual
    }

    tester_functions = {
        'stdout': testers.stdout,
        'file': testers.fileout
    }

    def __init__(self):
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
            reader = self._parse_reader_element(tool['reader'])
            if 'test' in tool:
                tester = self._parse_tester_element(tool['test'])
            else:
                tester = None
            audit_job = AuditJob(
                tool_name, tool_path,
                reader,
                tester,
                tool.get('version', None),
                tool.get('checksum', None),
                tool.get('output_checksum', None)
            )
            tools.append(audit_job)
        self.tools = tools

    @classmethod
    def _parse_tester_element(cls, element):
        """
        Take a tester element read from a KitList file and convert it to a
        Tester namedtuple
        """
        tester_name = element['name']
        if tester_name not in cls.tester_functions:
            raise(KeyError(
                'Unknown tester function {}'.format(tester_name)
            ))
        args = [
            (k, v) for k, v in element.iteritems() if k != 'name'
        ]
        tester_func = cls.tester_functions[tester_name]
        tester_args = dict(args)
        tester = Tester(tester_name, tester_func, tester_args)
        return tester

    @classmethod
    def _parse_reader_element(cls, element):
        """
        Take a reader element read from a KitList file and convert it to a
        Reader namedtuple
        """
        reader_name = element['name']
        if reader_name not in cls.reader_functions:
            raise(KeyError(
                'Unknown reader function {}'.format(reader_name)
            ))
        args = [
            (k, v) for k, v in element.iteritems() if k != 'name'
        ]
        reader_func = cls.reader_functions[reader_name]
        reader_args = dict(args)
        if 'regex' in reader_args:
            reader_args['regex'] = cls._fixup_regex(reader_args['regex'])
        reader = Reader(reader_name, reader_func, reader_args)
        return reader

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
