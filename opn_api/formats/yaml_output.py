import click
import yaml
from opn_api.formats.base import Format


class YamlOutputFormat(Format):
    def echo(self):
        filtered_data = self.get_filtered_data_by_columns()
        yaml_output = yaml.dump(filtered_data, sort_keys=False)
        click.echo(yaml_output)
