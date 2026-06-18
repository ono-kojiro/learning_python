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

