# src/amcli/cli/nestedadmin_commands.py

import click
from amcli.commands.gennestedadmin import run

@click.command(name="gennestedadmin")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_json", required=True)
def gennestedadmin_cmd(loader_dir, output_file, schema_json):
    """Generate nested Django admin.py from schema.json"""
    run(loader_dir, output_file, schema_json)

