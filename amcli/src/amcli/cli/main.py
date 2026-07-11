# src/amcli/cli/main.py

import click

from amcli.cli.start_commands import startproject_cmd, startapp_cmd
from amcli.cli.install_commands import installapp_cmd, edit_cmd
from amcli.cli.schema_commands import cmp2ref_cmd, genschema_cmd, gentestschema_cmd
from amcli.cli.generate_commands import (
    genmodel_cmd, genadmin_cmd, genview_cmd,
    genserializer_cmd, genfixture_cmd, genimporter_cmd,
    gendashboard_cmd,
    genprojecturls_cmd
)
from amcli.cli.test_commands import (
    gentest_cmd, gentestdata_cmd, gentestscript_cmd, test_cmd
)
from amcli.cli.maintenance_commands import (
    configure_cmd, patch_cmd, createsuperuser_cmd,
    mclean_cmd, maintainer_clean_cmd
)
from amcli.cli.run_commands import generate_cmd, runserver_cmd

from amcli.cli.nestedadmin_commands import gennestedadmin_cmd

@click.group()
def main():
    """Asset Manager Command Line Interface"""
    pass


# Register commands
main.add_command(startproject_cmd)
main.add_command(startapp_cmd)
main.add_command(installapp_cmd)
main.add_command(edit_cmd)
main.add_command(cmp2ref_cmd)
main.add_command(genschema_cmd)
main.add_command(gentestschema_cmd)
main.add_command(genmodel_cmd)
main.add_command(genadmin_cmd)
main.add_command(genview_cmd)
main.add_command(genserializer_cmd)
main.add_command(genfixture_cmd)
main.add_command(genimporter_cmd)
main.add_command(gentest_cmd)
main.add_command(gentestdata_cmd)
main.add_command(gentestscript_cmd)
main.add_command(test_cmd)
main.add_command(configure_cmd)
main.add_command(patch_cmd)
main.add_command(createsuperuser_cmd)
main.add_command(mclean_cmd)
main.add_command(maintainer_clean_cmd)
main.add_command(generate_cmd)
main.add_command(runserver_cmd)

main.add_command(gennestedadmin_cmd)
main.add_command(gendashboard_cmd)
main.add_command(genprojecturls_cmd)

