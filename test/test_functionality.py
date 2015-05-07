"""
Tests of overall functionality
"""

import pytest
import toolaudit
import yaml


def test_simple_audit(capsys, monkeypatch):
    """
    Check simple audit gives the expected output
    """
    def mockreturn(path):
        return '9c3bb3efa8095f36aafd9bf3a698efe439505021'
    monkeypatch.setattr(toolaudit.readers, 'sha1_file', mockreturn)
    app = toolaudit.application.ToolauditApp()
    try:
        app.run(kitlist_file='test/example.yaml')
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    returned_yaml = yaml.load(out)
    assert returned_yaml['tools'][0]['checksum'] == '9c3bb3efa8095f36aafd9bf3a698efe439505021'
