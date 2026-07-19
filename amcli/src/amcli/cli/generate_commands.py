# src/amcli/cli/generate_commands.py

import click

@click.command(name="genmodel")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_json", required=True)
@click.argument("input_files", nargs=-1)
def genmodel_cmd(loader_dir, output_file, input_files, schema_json):
    from amcli.commands.generate_model import run
    run(loader_dir, output_file, input_files, schema_json)


@click.command(name="genadmin")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
@click.argument("ref_yaml")
def genadmin_cmd(loader_dir, output_file, schema_yaml, ref_yaml):
    from amcli.commands.generate_admin import run
    run(loader_dir, output_file, schema_yaml, ref_yaml)


@click.command(name="genview")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.argument("ref_yaml")
def genview_cmd(loader_dir, output_file, ref_yaml):
    from amcli.commands.generate_view import run
    run(loader_dir, output_file, ref_yaml)


@click.command(name="genserializer")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
@click.argument("ref_yaml")
def genserializer_cmd(loader_dir, output_file, schema_yaml, ref_yaml):
    from amcli.commands.generate_serializer import run
    run(loader_dir, output_file, schema_yaml, ref_yaml)


@click.command(name="gendashboard")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
def gendashboard_cmd(loader_dir, output_file, schema_yaml):
    from amcli.commands.generate_dashboard import run
    run(loader_dir, output_file, schema_yaml)

@click.command(name="genprojecturls")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
def genprojecturls_cmd(loader_dir, output_file, schema_yaml):
    from amcli.commands.generate_project_urls import run
    run(loader_dir, output_file, schema_yaml)

@click.command(name="genfixture")
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
@click.option("-t", "--testschema", "testschema_yaml", required=True)
@click.option("-n", "--names", "names_yaml", required=True)
@click.option("-c", "--count", default=10)
@click.option("--with-deps", "include_deps", flag_value=True, default=False)
@click.argument("ref_yaml_list", nargs=-1)
def genfixture_cmd(loader_dir, output_file, schema_yaml, testschema_yaml, names_yaml, count, include_deps, ref_yaml_list):
    from amcli.commands.generate_fixture import run
    run(loader_dir, output_file, schema_yaml, testschema_yaml, names_yaml, ref_yaml_list, count, include_deps)


@click.command(name="genimporter")
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_path")
@click.argument("template_files", nargs=-1)
def genimporter_cmd(output_file, schema_path, template_files):
    from amcli.commands.generate_importer import run
    run(output_file, schema_path, template_files)

