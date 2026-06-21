# amcli/commands/createsuperuser.py

import os
import subprocess
from pathlib import Path

def run(project: str):
    """
    Create Django superuser using environment variables from .env.
    Equivalent to the old createsuperuser.sh.
    """

    workdir = Path("work")
    env_file = Path(".env")

    # .env を読み込む
    env = os.environ.copy()
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)
                env[key] = value

    # manage.py のある work/ に移動して実行
    subprocess.run(
        ["python3", "manage.py", "createsuperuser", "--noinput"],
        cwd=workdir,
        env=env,
        check=False,   # 既存ユーザーがいてもエラーにしない
    )

    return workdir / "manage.py"

