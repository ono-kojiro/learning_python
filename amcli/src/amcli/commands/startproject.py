import subprocess
import sys
from pathlib import Path

from amcli.utils.settings_editor import replace_installed_apps

def run(project_name: str, directory: str):
    target_dir = Path(directory).resolve()

    print(f"[amcli] Creating Django project: {project_name}")
    print(f"[amcli] Target directory: {target_dir}")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "django",
            "startproject",
            project_name,
            str(target_dir)
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("[amcli] ERROR: Failed to create project")
        print(result.stderr)
        sys.exit(result.returncode)

    print("[amcli] Django project created successfully")

    # Django プロジェクト生成後
    project_dir = Path(target_dir) / project_name
    settings_path = project_dir / "settings.py"

    print("[amcli] Updating INSTALLED_APPS in settings.py")
    replace_installed_apps(settings_path, project_name)

    print("[amcli] settings.py updated successfully")


