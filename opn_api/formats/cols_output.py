import click
from opn_api.formats.base import Format


class ColsOutputFormat(Format):
    def echo(self):
        click.echo(",".join(self._cols))
