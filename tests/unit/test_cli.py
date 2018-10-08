from click.testing import CliRunner
from unittest.mock import call, patch

import cli


@patch('cli.clocme')
def test_cli_foo_default(clocme_mock):
    result = CliRunner().invoke(cli.main, [])

    assert result.exit_code == 0
    assert clocme_mock.called
    assert call(True) == clocme_mock.call_args


@patch('cli.clocme')
def test_cli_foo_is_true(clocme_mock):
    result = CliRunner().invoke(cli.main, ['--foo', ])

    assert result.exit_code == 0
    assert clocme_mock.called
    assert call(True) == clocme_mock.call_args


@patch('cli.clocme')
def test_cli_foo_is_false(clocme_mock):
    result = CliRunner().invoke(cli.main, ['--no-foo', ])

    assert result.exit_code == 0
    assert clocme_mock.called
    assert call(False) == clocme_mock.call_args
