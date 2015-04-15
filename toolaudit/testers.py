"""
Methods to validate the output of various things
"""

import hashlib
import os.path
import readers
import shlex
import shutil
import subprocess
import tempfile


def test(func):
    """
    Decorator which handles test setup

    Makes a temporary directory, copies all files specified by the inputs
    argument to that directory, sets the temporary directory as working
    directory, passes control to the test, deletes the temporary directory.
    """
    def prepare_and_cleanup(*args, **kwargs):
        orig_dir, temp_dir = _prepare(kwargs['inputs'])
        ret = func(*args, **kwargs)
        _cleanup(orig_dir, temp_dir)
        return ret
    return prepare_and_cleanup


def _prepare(input_files):
    temp_dir = tempfile.mkdtemp()
    cwd = os.getcwd()

    for f in input_files.values():
        shutil.copy(f, temp_dir)

    os.chdir(temp_dir)
    return cwd, temp_dir


def _cleanup(original_directory, temp_dir):
    os.chdir(original_directory)
    shutil.rmtree(temp_dir)


@test
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

    cmd = command.format(exe=executable_path, **inputs)
    response = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
    sha = hashlib.sha1()
    sha.update(response[0])
    return sha.hexdigest()


@test
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

    cmd = command.format(exe=executable_path, **inputs)
    with open(os.devnull, 'w') as f:
        subprocess.check_call(
            shlex.split(cmd),
            stdout=f,
            stderr=f
        )
    if not os.path.exists(output_path):
        err_msg = "Output file from '{1}' not found ({2})".format(
            executable_path, output_path
        )
        raise(readers.InputError(err_msg))
    return readers.sha1(output_path)
