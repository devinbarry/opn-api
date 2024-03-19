import click
import json

from opn_api.formats.base import Format


class JsonOutputFormat(Format):
    def echo(self):
        click.echo(json.dumps(self._json_data))
