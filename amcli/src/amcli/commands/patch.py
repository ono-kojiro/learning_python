# amcli/commands/patch.py

import re
from pathlib import Path

def run(target: str, project: str, application: str):
    """
    Apply patches to Django project files.
    target: "urls" など
    """

    if target == "urls":
        return _patch_urls(project, application)

    raise ValueError(f"Unknown patch target: {target}")


def _patch_urls(project: str, application: str):
    """Patch urls.py to include API routing."""
    urls_path = Path(f"work/{project}/urls.py")
    text = urls_path.read_text()

    # 1. import 行の修正
    target_import = "from django.urls import path, include"
    if target_import not in text:
        text = re.sub(
            r"from django\.urls import path",
            target_import,
            text
        )

    # 2. urlpatterns に api/ を追加
    api_line = f"    path('api/', include('{application}.urls_api')),"
    if api_line not in text:
        text = re.sub(
            r"^\]",
            api_line + "\n]",
            text,
            flags=re.MULTILINE
        )

    urls_path.write_text(text)
    return urls_path

