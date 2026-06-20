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

# ---------------------------------------------------------
# cmp2ref（最小限修正：--name → --spec）
# ---------------------------------------------------------
@main.command()
@click.option("--spec", required=True, help="Path to spec YAML file")
@click.option("--output", "-o", "output_file", required=True, help="Output file path for *_ref.json")
@click.argument("input_files", nargs=-1)
def cmp2ref(spec, output_file, input_files):
    from amcli.commands.cmp2ref import run
    run(spec, output_file, input_files)

@main.command()
@click.option("-o", "--output", "output_file", required=True, help="Output schema file (JSON)")
@click.argument("input_files", nargs=-1)
def genschema(output_file, input_files):
    """
    Generate schema.json from reference model JSON files.
    """
    from amcli.commands.generate_schema import run
    run(output_file, input_files)

@main.command()
@click.option("-l", "--loader", "loader_dir", required=True, help="Template loader directory")
@click.option("-o", "--output", "output_file", required=True, help="Output model file")
@click.argument("input_files", nargs=-1)
def genmodel(loader_dir, output_file, input_files):
    from amcli.commands.generate_model import run
    run(loader_dir, output_file, input_files)

@main.command()
@click.option("-l", "--loader", "loader_dir", required=True, help="Template loader directory")
@click.option("-o", "--output", "output_file", required=True, help="Output admin file")
@click.option("-s", "--schema", "schema_yaml", required=True, help="schema.yaml path")
@click.argument("ref_yaml")
def genadmin(loader_dir, output_file, schema_yaml, ref_yaml):
    from amcli.commands.generate_admin import run
    run(loader_dir, output_file, schema_yaml, ref_yaml)

@main.command()
@click.option("-l", "--loader", "loader_dir", required=True, help="Template loader directory")
@click.option("-o", "--output", "output_file", required=True, help="Output view file")
@click.argument("ref_yaml")
def genview(loader_dir, output_file, ref_yaml):
    from amcli.commands.generate_view import run
    run(loader_dir, output_file, ref_yaml)

@main.command()
@click.option("-l", "--loader", "loader_dir", required=True, help="Template loader directory")
@click.option("-o", "--output", "output_file", required=True, help="Output serializer file")
@click.option("-s", "--schema", "schema_yaml", required=True, help="schema.yaml path")
@click.argument("ref_yaml")
def genserializer(loader_dir, output_file, schema_yaml, ref_yaml):
    from amcli.commands.generate_serializer import run
    run(loader_dir, output_file, schema_yaml, ref_yaml)

@main.command()
@click.option("-l", "--loader", "loader_dir", required=True)
@click.option("-o", "--output", "output_file", required=True)
@click.option("-s", "--schema", "schema_yaml", required=True)
@click.option("-n", "--names", "names_yaml", required=True)
@click.option("-c", "--count", "count", default=10)
@click.option("--with-deps", "include_deps", flag_value=True, default=False)
@click.argument("ref_yaml_list", nargs=-1)
def genfixture(loader_dir, output_file, schema_yaml, names_yaml, count, include_deps, ref_yaml_list):
    from amcli.commands.generate_fixture import run
    run(loader_dir, output_file, schema_yaml, names_yaml, ref_yaml_list, count, include_deps)

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
