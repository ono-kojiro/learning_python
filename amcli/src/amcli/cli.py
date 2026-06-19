import click

@click.group()
def main():
    """Asset Manager Command Line Interface"""
    pass

@main.command()
@click.argument("name")
@click.option("--dir", "directory", default=".", help="Target directory to create the project")
def startproject(name, directory):
    """Create a new Django project"""
    from amcli.commands.startproject import run
    run(name, directory)

@main.command()
@click.argument("app_name")
@click.option("--dir", "directory", required=True, help="Target directory to create the app")
def startapp(app_name, directory):
    """Create a new Django app inside the specified directory."""
    from amcli.commands.startapp import run
    run(app_name, directory)

@main.command(name="installapp")
@click.argument("app_name")
@click.option("--project", required=True, help="Path to Django project directory")
def installapp(app_name, project):
    """Install an app into the project (installed_apps.yml + allowed_hosts.yml + settings.py update)"""
    from amcli.commands.installapp import run
    run(app_name, project)

@main.command()
def genschema():
    from amcli.commands.genschema import run
    run()

@main.command()
def generate():
    from amcli.commands.generate import run
    run()

@main.command()
def runserver():
    from amcli.commands.runserver import run
    run()

@main.command()
def test():
    from amcli.commands.test import run
    run()

