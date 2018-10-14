from click.testing import CliRunner
from unittest.mock import patch

import cli


@patch('cli.clocme')
def test_cli_defaults(clocme_mock):
    result = CliRunner().invoke(cli.main, [])

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert "after_date=None" in str(clocme_mock.call_args)
    assert "before_date=None" in str(clocme_mock.call_args)


@patch('cli.clocme')
def test_cli_date_values(clocme_mock):
    cmds = ['--after-date', '11-11-11', '--before-date', '12-12-12']
    result = CliRunner().invoke(cli.main, cmds)

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert "after_date='11-11-11'" in str(clocme_mock.call_args)
    assert "before_date='12-12-12'" in str(clocme_mock.call_args)
