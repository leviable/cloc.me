import click

from clocme import clocme, DEFAULT_BRANCH


@click.command('')
@click.argument('repo_url')
@click.option(
    '--mongo-host', default='localhost', envvar='MONGO_HOST',
    help='Mongodb host to connect to'
)
@click.option(
    '--mongo-port', default=27017, envvar='MONGO_PORT',
    help='Mongodb port to connect to'
)
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
