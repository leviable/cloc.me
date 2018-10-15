from datetime import datetime as dt, timedelta
from unittest.mock import call, patch

import pytest
from git.exc import GitCommandError

import clocme

MOCK_REPO = 'https://github.com/not/real'


class MockCommit(object):
    def __init__(self, num):
        self.hexsha = num
        self.committed_datetime = dt.now() - timedelta(days=num)


@pytest.fixture()
def commit_factory():
    def factory(num):
        return [MockCommit(index) for index in range(num)]

    return factory


@patch('clocme.Repo')
def test_pull_repo_from_github(repo_mock):
    clocme.pull_repo(MOCK_REPO)

    assert repo_mock.clone_from.called
    assert MOCK_REPO in str(repo_mock.clone_from.call_args)
    assert clocme.COPY_PATH in str(repo_mock.clone_from.call_args)
    assert not repo_mock.called


@patch('clocme.Repo')
def test_pull_repo_existing_repo_found(repo_mock):
    exc_msg = 'already exists and is not an empty directory'
    repo_mock.clone_from.side_effect = GitCommandError('clone_from', exc_msg)
    clocme.pull_repo(MOCK_REPO)

    assert repo_mock.clone_from.called
    assert MOCK_REPO in str(repo_mock.clone_from.call_args)
    assert clocme.COPY_PATH in str(repo_mock.clone_from.call_args)
    assert repo_mock.called
    assert repo_mock.call_args[0][0].startswith(clocme.COPY_PATH)
    assert repo_mock.call_args[0][0].endswith(MOCK_REPO)


@patch('clocme.Repo')
def test_pull_repo_exc_reraise(repo_mock):
    exc_msg = 'something else'
    repo_mock.clone_from.side_effect = GitCommandError('foobar', exc_msg)
    with pytest.raises(GitCommandError) as exc:
        clocme.pull_repo(MOCK_REPO)

    assert repo_mock.clone_from.called
    assert not repo_mock.called
    assert 'foobar' in exc.value.command
    assert 'something else' in exc.value.status


@patch('clocme.Repo')
def test_walk_commits_with_no_kwargs(repo_mock, commit_factory):
    repo_mock.return_value = repo_mock
    repo_mock.iter_commits.return_value = commits = commit_factory(3)

    results = list(clocme.walk_commits(repo_mock, clocme.DEFAULT_BRANCH, **dict()))

    assert repo_mock.iter_commits.call_args == call(clocme.DEFAULT_BRANCH)

    assert repo_mock.git.checkout.call_args_list[0] == call(commits[0].hexsha)
    assert repo_mock.git.checkout.call_args_list[1] == call(commits[1].hexsha)
    assert repo_mock.git.checkout.call_args_list[2] == call(commits[2].hexsha)

    assert results[0] == (commits[0].hexsha, commits[0].committed_datetime)
    assert results[1] == (commits[1].hexsha, commits[1].committed_datetime)
    assert results[2] == (commits[2].hexsha, commits[2].committed_datetime)


@patch('clocme.Repo')
def test_walk_commits_w_kwargs(repo_mock, commit_factory):
    repo_mock.return_value = repo_mock
    repo_mock.iter_commits.return_value = commits = commit_factory(3)

    kwargs = {'branch': 'develop',
              'after_date': '2018-01-01',
              'before_date': '2018-02-02'}

    results = list(clocme.walk_commits(repo_mock, **kwargs))

    assert '2018-01-01' in str(repo_mock.iter_commits.call_args)
    assert '2018-02-02' in str(repo_mock.iter_commits.call_args)
    assert 'develop' in str(repo_mock.iter_commits.call_args)
    assert clocme.DEFAULT_BRANCH not in str(repo_mock.iter_commits.call_args)

    assert repo_mock.git.checkout.call_args_list[0] == call(commits[0].hexsha)
    assert repo_mock.git.checkout.call_args_list[1] == call(commits[1].hexsha)
    assert repo_mock.git.checkout.call_args_list[2] == call(commits[2].hexsha)

    assert results[0] == (commits[0].hexsha, commits[0].committed_datetime)
    assert results[1] == (commits[1].hexsha, commits[1].committed_datetime)
    assert results[2] == (commits[2].hexsha, commits[2].committed_datetime)
