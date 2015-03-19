"""
Methods to read the version number from various things
"""

import re
import subprocess


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


def regex_line(path, line_no=None, regex=None):
    """
    Read a line from a file and get the version number with a regex

    Parameters
    ----------
    line_no : int
        Line number to read
    regex : str
        Regular expression to apply to the read line

    Returns
    -------
    version : str
        The contents of group 0 of the regex
    """

    with open(path, 'r') as f:
        for _ in range(line_no - 1):
            f.readline()
        line = f.readline().strip()
    m = re.search(regex, line).groups()
    version = m[0]
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
