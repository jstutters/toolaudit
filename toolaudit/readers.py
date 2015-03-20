"""
Methods to read the version number from various things
"""

import re
import subprocess


class InputError(Exception):
    def __init__(self, msg, regex=None, line=None):
        self.regex = regex
        self.line = line
        self.msg = msg


def command_line(path, option=None, regex=None):
    """
    Get the output of a command line tool

    Calls the executable at *path* with *option*.  If a regex is supplied that
    will be applied to executable output and group 0 will be returned,
    otherwise the executable output is returned.

    Parameters
    ----------
    path : str
        The path to executable to be run
    option : str
        The argument to pass
    regex : str or None
        An optional regex to apply to the output of the executable

    Returns
    -------
    version : str
        The value read from the command line after applying a regex if provided
    """

    response = subprocess.Popen(
        [path, option],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).communicate()
    response = response[0].strip()
    if regex:
        m = re.search(regex, response)
        version = m.groups(0)[0]
    else:
        version = response
    return version


def _get_line(path, line_no):
    """
    Get the specified line from the file at *path*

    Parameters
    ----------
    path : str
        Path to read
    line_no : int
        The line to get

    Returns
    -------
    line : str
        Requested line

    Raises
    ------
    InputError

    with open(path, 'r') as f:
        for _ in range(line_no - 1):
            l = f.readline()
            print l
            if not l:
                raise InputError(msg="Line number beyond end-of-file")
        line = f.readline()
    if not line:
        raise InputError(msg="Line number beyond end-of-file")
    line = line.strip()
    return line


def line_in_file(path, line_no=None, regex=None):
    """
    Read a line from a file optionally apply a regex

    Parameters
    ----------
    line_no : int
        Line number to read
    regex : str or None
        Regular expression to apply to the read line

    Returns
    -------
    version : str
        The contents of group 0 of the regex
    """

    line = _get_line(path, line_no)
    if regex:
        m = re.search(regex, line)
        if m:
            version = m.groups()[0]
        else:
            raise InputError(regex, line, "Pattern not found")
    else:
        version = line
    return version


def manual(path, value):  # pylint: disable=W0613
    """
    Dummy function that returns it's input

    For tools that cannot be read automatically use a value from the toolkit
    file

    Parameters
    ----------
    path : str
        Ignored
    value : str
        The value to return

    Returns
    -------
    version : str
        Whatever was passed in as *value*
    """

    return value
