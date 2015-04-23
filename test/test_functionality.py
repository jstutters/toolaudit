"""
Tests of overall functionality
"""

import pytest
import toolaudit
import yaml


def test_simple_audit(capsys):
    """
    Check simple audit gives the expected output
    """
    app = toolaudit.application.ToolauditApp()
    try:
        app.run(kitlist_file='test/example.yaml')
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    returned_yaml = yaml.load(out)
    print returned_yaml
    assert returned_yaml['tools'][0]['checksum'] == '9c3bb3efa8095f36aafd9bf3a698efe439505021'
