from pathlib import Path
import yaml
import sys
from amcli.utils.settings_editor import (
    replace_installed_apps,
    replace_allowed_hosts_with_yaml,
)

def run(app_name: str, project_dir: str):
    project_path = Path(project_dir).resolve()

    # -----------------------------
    # 1. installed_apps.yml の更新
    # -----------------------------
    apps_yml = project_path / "installed_apps.yml"

    if not apps_yml.exists():
        print(f"[amcli] ERROR: installed_apps.yml not found: {apps_yml}")
        sys.exit(1)

    apps = yaml.safe_load(apps_yml.read_text(encoding="utf-8"))
    if not isinstance(apps, list):
        print("[amcli] ERROR: installed_apps.yml must contain a list")
        sys.exit(1)

    if app_name not in apps:
        apps.append(app_name)
        apps_yml.write_text(
            yaml.dump(apps, allow_unicode=True, sort_keys=False),
            encoding="utf-8"
        )
        print(f"[amcli] App '{app_name}' added to installed_apps.yml")
    else:
        print(f"[amcli] App '{app_name}' already exists in installed_apps.yml")

    # -----------------------------
    # 2. allowed_hosts.yml の生成（初回のみ）
    # -----------------------------
    allowed_hosts_yml = project_path / "allowed_hosts.yml"
    if not allowed_hosts_yml.exists():
        allowed_hosts_yml.write_text(
            yaml.dump(["0.0.0.0"], allow_unicode=True, sort_keys=False),
            encoding="utf-8"
        )
        print("[amcli] allowed_hosts.yml created")

    # -----------------------------
    # 3. settings.py の YAML 化
    # -----------------------------
    settings_path = project_path / "settings.py"
    code = settings_path.read_text(encoding="utf-8")

    # INSTALLED_APPS の YAML 化
    if "installed_apps.yml" not in code:
        print("[amcli] Updating settings.py to use installed_apps.yml")
        replace_installed_apps(settings_path, project_path.name)
    else:
        print("[amcli] settings.py already uses installed_apps.yml")

    # ALLOWED_HOSTS の YAML 化
    if "allowed_hosts.yml" not in code:
        print("[amcli] Updating settings.py to use allowed_hosts.yml")
        replace_allowed_hosts_with_yaml(settings_path, project_path.name)
    else:
        print("[amcli] settings.py already uses allowed_hosts.yml")
