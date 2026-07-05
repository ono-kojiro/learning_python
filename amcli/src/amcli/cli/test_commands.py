# src/amcli/cli/test_commands.py

import click

@click.command(name="gentest")
@click.argument("template_file", type=click.Path(exists=True))
@click.option("--schema", "-s", required=True)
@click.option("--ref", "-r", required=True)
@click.option("--output", "-o", required=True)
def gentest_cmd(template_file, schema, ref, output):
    from amcli.commands.generate_test import run
    run(schema_yaml=schema, ref_yaml=ref,
        template_file=template_file, output_file=output)


@click.command(name="gentestdata")
@click.option("-s", "--schema", required=True)
@click.option("-o", "--outdir", required=True)
@click.argument("ref_json", nargs=-1)
def gentestdata_cmd(schema, outdir, ref_json):
    from amcli.commands.generate_testdata.main import run
    run(schema_path=schema, outdir=outdir, ref_json_paths=ref_json)


@click.command(name="gentestscript")
@click.option("--action", required=True,
              type=click.Choice(["add", "get", "update", "delete"]))
@click.option("-o", "--out", required=True)
@click.option("-s", "--schema", "schema_path")
@click.argument("json_files", nargs=-1)
def gentestscript_cmd(action, out, schema_path, json_files):
    from amcli.commands.generate_testscript.main import run
    run(action=action, outpath=out, json_files=json_files, schema_path=schema_path)


@click.command(name="test")
def test_cmd():
    from amcli.commands.test import run
    run()

