import click

from clocme import clocme, DEFAULT_BRANCH


@click.command('')
@click.argument('repo_url')
@click.option('-v', '--verbose', count=True)
@click.option(
    '--after-date', help='Only evaluate commits before this date'
)
@click.option(
    '--before-date', help='Only evaluate commits before this date'
)
@click.option(
    '--branch', default=DEFAULT_BRANCH, help=f'Git branch to evaluate. Defaults to {DEFAULT_BRANCH}'
)
def main(repo_url, **kwargs):
    """ Clocme """
    click.echo("Cloc Me started")
    clocme(repo_url, **kwargs)
