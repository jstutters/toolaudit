"""
Tests of command line argument handling
"""

import pytest
import toolaudit


@pytest.mark.parametrize('opt', ['-V', '--version'])
def test_version(capsys, opt):
    """
    Test the output of -V and --version
    """
    parser = toolaudit.create_parser()
    try:
        parser.parse_args([opt])
    except SystemExit:
        pass
    _, err = capsys.readouterr()
    correct_version = "{0} {1}\n".format(
        toolaudit.__name__,
        toolaudit.__version__
    )
    assert err == correct_version


@pytest.mark.parametrize('opt', ['-V', '--version'])
def test_version_exits(opt):
    """
    The -V and --version options should raise SystemExit
    """
    parser = toolaudit.create_parser()
    pytest.raises(SystemExit, parser.parse_args, [opt])


def test_no_args_exits():
    """
    Supplying no arguments should exit
    """
    pytest.raises(SystemExit, toolaudit.main)
