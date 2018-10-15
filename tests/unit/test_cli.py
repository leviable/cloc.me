from unittest.mock import patch

from click.testing import CliRunner

import cli
from clocme import DEFAULT_BRANCH

MOCK_REPO = 'https://github.com/not/real'


@patch('cli.clocme')
def test_repo_required(clocme_mock):
    result = CliRunner().invoke(cli.main, [])

    assert result.exit_code == 2
    assert not clocme_mock.called
    assert 'Missing argument "REPO_URL"' in result.output


@patch('cli.clocme')
def test_cli_defaults(clocme_mock):
    result = CliRunner().invoke(cli.main, [MOCK_REPO, ])

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert len(clocme_mock.call_args[-1]) == 5
    assert "mongo_host='localhost'" in str(clocme_mock.call_args)
    assert "mongo_port=27017" in str(clocme_mock.call_args)
    assert "after_date=None" in str(clocme_mock.call_args)
    assert "before_date=None" in str(clocme_mock.call_args)
    assert f"branch='{DEFAULT_BRANCH}'" in str(clocme_mock.call_args)


@patch('cli.clocme')
def test_cli_date_values(clocme_mock):
    cmds = [MOCK_REPO, '--after-date', '11-11-11', '--before-date', '12-12-12']
    result = CliRunner().invoke(cli.main, cmds)

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert "after_date='11-11-11'" in str(clocme_mock.call_args)
    assert "before_date='12-12-12'" in str(clocme_mock.call_args)


@patch('cli.clocme')
def test_cli_mongo_values(clocme_mock):
    cmds = [MOCK_REPO, '--mongo-host', 'mongo-foo', '--mongo-port', '12345']
    result = CliRunner().invoke(cli.main, cmds)

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert "mongo_host='mongo-foo'" in str(clocme_mock.call_args)
    assert "mongo_port=12345" in str(clocme_mock.call_args)


@patch('cli.clocme')
def test_cli_branch_value(clocme_mock):
    cmds = [MOCK_REPO, '--branch', 'foobranch']
    result = CliRunner().invoke(cli.main, cmds)

    assert result.exit_code == 0
    assert clocme_mock.called
    assert len(clocme_mock.call_args) == 2
    assert "branch='foobranch'" in str(clocme_mock.call_args)
