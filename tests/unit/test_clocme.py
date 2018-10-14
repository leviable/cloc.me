from datetime import datetime as dt, timedelta
from pathlib import Path
import tempfile
from unittest.mock import call, patch

import pytest

import clocme


class MockCommit(object):
    def __init__(self, num):
        self.hexsha = num
        self.committed_datetime = dt.now() - timedelta(days=num)


@pytest.fixture()
def commit_factory():
    def factory(num):
        return [MockCommit(index) for index in range(num)]

    return factory


@patch('clocme.shutil')
def test_prep_repo_source_does_not_exist_exc(shutil_mock):
    bad_source = '/this-doesnt-exist'
    with pytest.raises(clocme.ClocMeError) as exc:
        clocme.prep_repo(source=bad_source)

    assert "You must mount" in str(exc)
    assert bad_source in str(exc)
    assert not shutil_mock.copytree.called


@patch('clocme.shutil')
def test_prep_repo_source_is_empty_exc(shutil_mock):
    with tempfile.TemporaryDirectory() as empty_dir:
        with pytest.raises(clocme.ClocMeError) as exc:
            clocme.prep_repo(source=empty_dir)

    assert "You must mount" in str(exc)
    assert empty_dir in str(exc)
    assert not shutil_mock.copytree.called


@patch('clocme.shutil')
def test_prep_repo_source_copy_success(shutil_mock):
    copy_to = '/copy-to-this-dir'
    with tempfile.TemporaryDirectory() as temp_dir:
        Path(f'{temp_dir}/file.txt').touch()
        clocme.prep_repo(source=temp_dir, copy_to=copy_to)

    assert shutil_mock.copytree.called
    assert temp_dir in str(shutil_mock.copytree.call_args)
    assert copy_to in str(shutil_mock.copytree.call_args)


@patch('clocme.Repo')
def test_walk_commits_with_no_kwargs(repo_mock, commit_factory):
    repo_mock.return_value = repo_mock
    repo_mock.iter_commits.return_value = commits = commit_factory(3)

    results = list(clocme.walk_commits(**dict()))

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

    results = list(clocme.walk_commits(**kwargs))

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


@patch('clocme.prep_repo')
@patch('clocme.subprocess')
def test_clocme_with_no_args(_, sp_mock):
    pass
