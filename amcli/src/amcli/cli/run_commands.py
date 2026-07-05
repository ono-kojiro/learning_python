# src/amcli/cli/run_commands.py

import click

@click.command(name="generate")
def generate_cmd():
    from amcli.commands.generate import run
    run()


@click.command(name="runserver")
def runserver_cmd():
    from amcli.commands.runserver import run
    run()

