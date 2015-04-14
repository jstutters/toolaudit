"""
Methods to validate the output of various things
"""

import hashlib
import os.path
import readers
import shlex
import subprocess


def stdout(executable_path, command, inputs):
    """
    Execute a program with some inputs and hash what it prints to stdout.

    Parameters
    ----------
    command : str
        A string which will be formatted with the given executable path and
        inputs
    executable_path : str
        The full path to the executable being tested
    inputs : list of str
        A list of input files used by the program under test

    Returns
    -------
    hexdigest : str
        The SHA-1 hash of the program's output
    """

    cmd = command.format(executable_path, *inputs)
    response = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
    sha = hashlib.sha1()
    sha.update(response[0])
    return sha.hexdigest()


def fileout(executable_path, command, inputs, output_path):
    """
    Execute a program with some inputs and hash the file created at
    output_path.

    Parameters
    ----------
    command : str
        A string which will be formatted with the given executable path and
        inputs
    executable_path : str
        The full path to the executable being tested
    inputs : list of str
        A list of input files used by the program under test
    output_path : str
        The full path of the output file to be hashed

    Returns
    -------
    hexdigest : str
        The SHA-1 hash of the program's output
    """

    cmd = command.format(executable_path, *inputs)
    subprocess.check_call(
        shlex.split(cmd)
    )
    if not os.path.exists(output_path):
        err_msg = "Output file from '{1}' not found ({2})".format(
            executable_path, output_path
        )
        raise(readers.InputError(err_msg))
    return readers.sha1(output_path)
