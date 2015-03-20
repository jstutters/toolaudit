"""
Tests for the functions in the readers module
"""

import pytest
from toolaudit import readers


@pytest.fixture()
def example_input_file(tmpdir):
    tmpdir.chdir()
    p = tmpdir.join("kitlist.yaml")
    p.write("foo\nbar v2.0\nbob")
    return "kitlist.yaml"


def test_manual():
    """
    manual() returns it's second argument
    """
    assert readers.manual("", "foo") == "foo"


def test_regex_line(example_input_file):
    """
    line_in_file() gets a line and applies a regex
    """
    assert readers.line_in_file(example_input_file, 3) == "bob"
    assert readers.line_in_file(
        example_input_file, 2, "^bar\sv([0-9\.]*)$") == "2.0"
    pytest.raises(
        readers.InputError,
        readers.line_in_file,
        example_input_file,
        3,
        "^boo([0-9])$"
    )
    pytest.raises(
        readers.InputError,
        readers.line_in_file,
        example_input_file,
        5
    )
