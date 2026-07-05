# src/amcli/cli/schema_commands.py

import click

@click.command(name="cmp2ref")
@click.option("--spec", required=True)
@click.option("--output", "-o", "output_file", required=True)
@click.argument("input_files", nargs=-1)
def cmp2ref_cmd(spec, output_file, input_files):
    from amcli.commands.cmp2ref import run
    run(spec, output_file, input_files)


@click.command(name="genschema")
@click.option("-o", "--output", "output_file", required=True)
@click.option("-a", "--application", required=True)
@click.option("-p", "--project", required=True)
@click.argument("ref_json_files", nargs=-1)
def genschema_cmd(output_file, application, project, ref_json_files):
    from amcli.commands.generate_schema import run
    run(output_file, ref_json_files, application=application, project=project)

