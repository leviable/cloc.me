import json
import logging
import os
import shutil
import subprocess

from git import Repo

log = logging.getLogger(__name__)

SOURCE_PATH = '/source'
COPY_PATH = '/source-copy'


class ClocMeError(Exception):
    pass


def prep_repo(**kwargs):
    if not os.path.exists(SOURCE_PATH) or not os.listdir(SOURCE_PATH):
        raise ClocMeError(f'You must mount a git repo into {SOURCE_PATH}')

    log.info(f'Copying source from {SOURCE_PATH} to {COPY_PATH}')
    shutil.copytree(SOURCE_PATH, COPY_PATH)


def walk_commits(**kwargs):
    repo = Repo(COPY_PATH)

    iter_args = dict()
    if kwargs['after_date']:
        iter_args['after'] = kwargs['after_date']
    if kwargs['before_date']:
        iter_args['before'] = kwargs['before_date']

    for commit in repo.iter_commits('master', **iter_args):
        repo.git.checkout(commit.hexsha)
        yield commit.hexsha, commit.committed_datetime


def clocme(**kwargs):
    log.info("In clocme")
    prep_repo(**kwargs)
    for commit_hash, commit_date in walk_commits(**kwargs):
        log.info(f'Working with commit {commit_hash} for date {commit_date}')
        cloc_cmd = f'cloc --git {COPY_PATH} --json'
        cloc_out = subprocess.check_output(cloc_cmd, shell=True)
        cloc_out_json = json.loads(cloc_out) if cloc_out != b'' else dict()
    from pprint import pprint as pp
    import pdb
    pdb.set_trace()
    pp('')
