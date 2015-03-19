"""
Tests for the functions in the readers module
"""

from toolaudit import readers


def test_manual():
    """
    manual() returns it's second argument
    """
    assert readers.manual("", "foo") == "foo"
