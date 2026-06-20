from pathlib import Path
import yaml
from amcli.utils.settings_editor import (
    extract_setting_list,
    replace_setting_with_yaml,
)

def run(setting_name, project_dir, export_yaml, import_yaml):
    project_path = Path(project_dir).resolve()
    settings_path = project_path / "settings.py"

    # export
    if export_yaml:
        values = extract_setting_list(settings_path, setting_name)
        Path(export_yaml).write_text(
            yaml.dump(values, allow_unicode=True, sort_keys=False),
            encoding="utf-8"
        )
        print(f"[amcli] {setting_name} exported to {export_yaml}")
        return

    # import
    if import_yaml:
        replace_setting_with_yaml(settings_path, setting_name, project_path.name)
        print(f"[amcli] {setting_name} replaced to use {import_yaml}")
        return

