# src/amcli/cli/install_commands.py

import click

@click.command(name="installapp")
@click.argument("app_name", required=False)
@click.option("--project", required=True)
@click.option("--export-installed-apps", "export_yaml")
@click.option("--replace-installed-apps", "replace_yaml")
def installapp_cmd(app_name, project, export_yaml, replace_yaml):
    from amcli.commands.installapp import run
    run(app_name=app_name, project_dir=project,
        export_yaml=export_yaml, replace_yaml=replace_yaml)


@click.command(name="edit")
@click.argument("setting_name")
@click.option("--project")
@click.option("--export", "export_yaml")
@click.option("--import", "import_yaml")
@click.option("--file", "-f", "target_file")
def edit_cmd(setting_name, project, export_yaml, import_yaml, target_file):
    from amcli.commands.edit import run
    run(setting_name=setting_name, project_dir=project,
        export_yaml=export_yaml, import_yaml=import_yaml,
        target_file=target_file)

