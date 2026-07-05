# src/amcli/cli/start_commands.py

import click

@click.command(name="startproject")
@click.argument("name")
@click.option("--dir", "directory", default=".", help="Target directory")
def startproject_cmd(name, directory):
    from amcli.commands.startproject import run
    run(name, directory)


@click.command(name="startapp")
@click.argument("app_name")
@click.option("--dir", "directory", required=True, help="Target directory")
def startapp_cmd(app_name, directory):
    from amcli.commands.startapp import run
    run(app_name, directory)

