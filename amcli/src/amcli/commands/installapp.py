from pathlib import Path
import yaml
import sys
import argparse
from amcli.utils.settings_editor import (
    replace_installed_apps,
    extract_installed_apps_list,
)

def export_installed_apps(settings_path: Path, out_yaml: Path):
    """settings.py の INSTALLED_APPS を YAML に書き出す"""
    apps = extract_installed_apps_list(settings_path)
    out_yaml.write_text(
        yaml.dump(apps, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )
    print(f"[amcli] INSTALLED_APPS exported to {out_yaml}")


def replace_installed_apps_with_yaml(settings_path: Path, yaml_path: Path):
    """settings.py の INSTALLED_APPS を YAML 参照方式に置き換える"""
    replace_installed_apps(settings_path, yaml_path.name)
    print(f"[amcli] INSTALLED_APPS replaced to use {yaml_path.name}")


def add_app_to_yaml(app_name: str, yaml_path: Path):
    """installed_apps.yml にアプリを追加"""
    apps = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if not isinstance(apps, list):
        print("[amcli] ERROR: installed_apps.yml must contain a list")
        sys.exit(1)

    if app_name in apps:
        print(f"[amcli] App '{app_name}' already exists in installed_apps.yml")
        return

    apps.append(app_name)
    yaml_path.write_text(
        yaml.dump(apps, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )
    print(f"[amcli] App '{app_name}' added to installed_apps.yml")


def run(app_name, project_dir, export_yaml, replace_yaml):
    project_path = Path(project_dir).resolve()
    project_name = project_path.name
    settings_path = project_path / "settings.py"

    # export
    if export_yaml:
        export_installed_apps(settings_path, Path(export_yaml))
        return

    # replace
    if replace_yaml:
        replace_installed_apps(settings_path, project_name)
        return

    # add app
    apps_yml = project_path / "installed_apps.yml"
    add_app_to_yaml(app_name, apps_yml)
