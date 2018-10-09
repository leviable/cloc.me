import click
import logging

from clocme import clocme

log_fmt = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
formatter = logging.Formatter(log_fmt)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO,
                    format=log_fmt,
                    datefmt='%m-%d %H:%M:%S',
                    handlers=[console_handler])
log = logging.getLogger("clocme")


@click.command('')
@click.option(
    '--after-date', help='Only evaluate commits before this date'
)
@click.option(
    '--before-date', help='Only evaluate commits before this date'
)
def main(**kwargs):
    log.info("Cloc Me started")
    clocme(**kwargs)
