import json
import logging
import os
import shutil
import subprocess

from git import Repo

log = logging.getLogger(__name__)

SOURCE_PATH = '/source'
COPY_PATH = '/source-copy'
DEFAULT_BRANCH = 'master'


class ClocMeError(Exception):
    pass


def prep_repo(source=SOURCE_PATH, copy_to=COPY_PATH):
    if not os.path.exists(source) or not os.listdir(source):
        raise ClocMeError(f'You must mount a git repo into {source}')

    log.info(f'Copying source from {source} to {copy_to}')
    shutil.copytree(source, copy_to)


def walk_commits(**kwargs):
    repo = Repo(COPY_PATH)

    iter_args = dict()
    if kwargs.get('after_date'):
        iter_args['after'] = kwargs['after_date']
    if kwargs.get('before_date'):
        iter_args['before'] = kwargs['before_date']

    branch = kwargs.get('branch', DEFAULT_BRANCH)

    for commit in repo.iter_commits(branch, **iter_args):
        repo.git.checkout(commit.hexsha)
        yield commit.hexsha, commit.committed_datetime


def clocme(**kwargs):
    log.info("In clocme")
    prep_repo()
    for commit_hash, commit_date in walk_commits(**kwargs):
        log.info(f'Working with commit {commit_hash} for date {commit_date}')
        cloc_cmd = f'cloc --git --json {COPY_PATH}'
        cloc_out = subprocess.check_output(cloc_cmd, shell=True)
        result = json.loads(cloc_out) if cloc_out != b'' else dict()
        log.info(f'Result was {result}')
