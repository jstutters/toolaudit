"""
Methods to read the version number from various things
"""

import hashlib
import re
import subprocess


class InputError(Exception):
    """
    An exception that may occur when reading files
    """
    pass


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
    version = None
    if regex:
        for line in response.split('\n'):
            m = re.search(regex, line)
            if m:
                version = m.groups(0)[0]
                break
    else:
        version = response
    return version


def _get_line(path, line_no):
    """
    Get the specified line from the file at *path*.

    Parameters
    ----------
    path : str
        Path to read.
    line_no : int
        The line to get.

    Returns
    -------
    line : str
        Requested line.

    Raises
    ------
    InputError
        If the requested line is beyond the end of the file.
    """

    with open(path, 'r') as f:
        for _ in range(line_no - 1):
            l = f.readline()
            if not l:
                raise InputError("Line number beyond end-of-file")
        line = f.readline()
    if not line:
        raise InputError("Line number beyond end-of-file")
    line = line.strip()
    return line


def line_in_file(path, line_no=None, regex=None):
    """
    Read a line from a file optionally apply a regex.

    Parameters
    ----------
    line_no : int
        Line number to read.
    regex : str or None
        Regular expression to apply to the read line.

    Returns
    -------
    version : str
        The contents of group 0 of the regex.

    Raises
    ------
    InputError
        If the regex pattern returns no matches.
    """

    line = _get_line(path, line_no)
    if regex:
        m = re.search(regex, line)
        if m:
            version = m.groups()[0]
        else:
            raise InputError({'message': "Pattern not found",
                              'regex': regex,
                              'line': line})
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


def sha1(path):
    """
    Calculate the SHA-1 checksum of a file.
    """
    sha = hashlib.sha1()  # pylint: disable=E1101
    with open(path, 'rb') as hashfile:
        while True:
            block = hashfile.read(2**10)  # Magic number: one-megabyte blocks.
            if not block:
                break
            sha.update(block)
    return sha.hexdigest()
