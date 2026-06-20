import subprocess
import sys
from pathlib import Path

def run(app_name: str, directory: str):
    target_dir = Path(directory).resolve()

    if not target_dir.exists():
        print(f"[amcli] ERROR: Directory does not exist: {target_dir}")
        sys.exit(1)

    print(f"[amcli] Creating Django app: {app_name}")
    print(f"[amcli] Target directory: {target_dir}")

    # ★ Django の startapp は manage.py のあるディレクトリで実行する
    result = subprocess.run(
        [
            sys.executable,
            "manage.py",
            "startapp",
            app_name
        ],
        cwd=target_dir,   # ← ここが manage.py のある work/
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("[amcli] ERROR: Failed to create app")
        print(result.stderr)
        sys.exit(result.returncode)

    print("[amcli] Django app created successfully")
