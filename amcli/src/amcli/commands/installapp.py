from pathlib import Path
import yaml
import sys
from amcli.utils.settings_editor import replace_installed_apps

def run(app_name: str, project_dir: str):
    project_path = Path(project_dir).resolve()

    # installed_apps.yml のパス
    apps_yml = project_path / "installed_apps.yml"

    if not apps_yml.exists():
        print(f"[amcli] ERROR: installed_apps.yml not found: {apps_yml}")
        sys.exit(1)

    # YAML を読み込み
    apps = yaml.safe_load(apps_yml.read_text(encoding="utf-8"))
    if not isinstance(apps, list):
        print("[amcli] ERROR: installed_apps.yml must contain a list")
        sys.exit(1)

    # すでに存在する場合は何もしない
    if app_name not in apps:
        apps.append(app_name)
        apps_yml.write_text(
            yaml.dump(apps, allow_unicode=True, sort_keys=False),
            encoding="utf-8"
        )
        print(f"[amcli] App '{app_name}' added to installed_apps.yml")
    else:
        print(f"[amcli] App '{app_name}' already exists in installed_apps.yml")

    # settings.py を YAML 読み込み方式に変換（初回のみ）
    settings_path = project_path / "settings.py"
    code = settings_path.read_text(encoding="utf-8")

    if "yaml.safe_load" not in code:
        print("[amcli] Updating settings.py to use installed_apps.yml")
        replace_installed_apps(settings_path, project_path.name)
    else:
        print("[amcli] settings.py already uses installed_apps.yml")

