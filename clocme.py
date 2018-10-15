from functools import partial
import json
import os
from pprint import pformat
import subprocess
import urllib

import click
from git import Repo
from git.exc import GitCommandError
from pymongo import MongoClient

GREEN = partial(click.style, fg='green')
RED = partial(click.style, fg='red')
YELLOW = partial(click.style, fg='yellow')

COPY_PATH = '/source'
DEFAULT_BRANCH = 'master'


class ClocMeError(Exception):
    pass


def pull_repo(repo_url, copy_to=COPY_PATH):
    repo_path = os.path.join(copy_to, urllib.parse.quote(repo_url, safe=''))
    click.echo(f'Repo path is {RED(repo_path)}')
    try:
        repo = Repo.clone_from(repo_url, repo_path)
        click.echo(f'Pulled repo {GREEN(repo_url)}')
    except GitCommandError as e:
        if 'already exists and is not an empty directory' not in str(e):
            raise
        repo = Repo(repo_path)
        click.echo(f'Using previously pulled repo {GREEN(repo_url)}')

    return repo, repo_path


def walk_commits(repo, branch, **kwargs):
    iter_args = dict()
    if kwargs.get('after_date'):
        iter_args['after'] = kwargs['after_date']
    if kwargs.get('before_date'):
        iter_args['before'] = kwargs['before_date']

    for commit in repo.iter_commits(branch, **iter_args):
        repo.git.checkout(commit.hexsha)
        yield commit.hexsha, commit.committed_datetime


def clocme(repo_url, **kwargs):
    click.echo("In clocme")

    m_host, m_port = kwargs['mongo_host'], kwargs['mongo_port']
    click.echo(f"Connecting to mongodb at {m_host}:{m_port}")
    db = MongoClient(m_host, m_port).clocme

    click.echo("Fetching Repo")
    repo, repo_path = pull_repo(repo_url)
    branch = kwargs.pop('branch', DEFAULT_BRANCH)

    repo_col = db[repo_url]

    cloc_cmd = f'cloc --git --json {repo_path}'
    for commit_hash, commit_date in walk_commits(repo, branch, **kwargs):
        click.echo(f'Working with commit {commit_hash} for date {commit_date}')

        if repo_col.find_one({'commit': commit_hash}):
            click.echo(f'Commit alread cloc\'d, moving to next commit')
            continue

        cloc_out = subprocess.check_output(cloc_cmd, shell=True)
        result = json.loads(cloc_out) if cloc_out else dict()
        click.echo(f'Result was {pformat(result)}')
        repo_col.insert_one({'commit': commit_hash,
                             'datetime': commit_date,
                             'result': result})
