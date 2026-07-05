# src/amcli/cli/maintenance_commands.py

import click

@click.command(name="configure")
@click.option("-o", "--output", "output_file", required=True)
@click.option("-a", "--application", required=True)
@click.option("-p", "--project", required=True)
def configure_cmd(output_file, application, project):
    from amcli.commands.configure import run
    run(output_file=output_file, application=application, project=project)


@click.command(name="patch")
@click.option("--target", "-t", required=True, type=click.Choice(["urls"]))
@click.option("--project", "-p", required=True)
@click.option("--application", "-a", required=True)
def patch_cmd(target, project, application):
    from amcli.commands.patch import run
    run(target=target, project=project, application=application)


@click.command(name="createsuperuser")
@click.option("-p", "--project", required=True)
def createsuperuser_cmd(project):
    from amcli.commands.createsuperuser import run
    run(project=project)


@click.command(name="mclean")
def mclean_cmd():
    from amcli.commands.mclean import run
    run()


@click.command(name="maintainer-clean")
def maintainer_clean_cmd():
    from amcli.commands.mclean import run
    run()

