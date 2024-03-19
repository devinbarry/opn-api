import click
import json
from opn_api.formats.base import Format


class JsonFilterOutputFormat(Format):
    def echo(self):
        filtered_data = self.get_filtered_data_by_columns()
        click.echo(json.dumps(filtered_data))
