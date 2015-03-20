"""
Tests for the functions in the readers module
"""

from toolaudit import readers


def test_manual():
    """
    manual() returns it's second argument
    """
    assert readers.manual("", "foo") == "foo"

def test_regex_line():
    """
    line_in_file() gets a line and applies a regex
    """
    assert readers.line_in_file("test/testdoc.yaml", 2) == "tools:"
