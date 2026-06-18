import libcst as cst
from pathlib import Path

class InstalledAppsTransformer(cst.CSTTransformer):
    def __init__(self, project_name):
        self.project_name = project_name

    def leave_Assign(self, original_node, updated_node):
        # INSTALLED_APPS = [...] を検出
        if (
            isinstance(original_node.targets[0].target, cst.Name)
            and original_node.targets[0].target.value == "INSTALLED_APPS"
        ):
            # 新しい右辺を生成
            new_value = cst.parse_expression(
                f"yaml.safe_load(open(str(BASE_DIR / '{self.project_name}' / 'installed_apps.yml')))"
            )
            return updated_node.with_changes(value=new_value)
        return updated_node


def replace_installed_apps(settings_path: Path, project_name: str):
    code = settings_path.read_text(encoding="utf-8")
    tree = cst.parse_module(code)

    # import yaml がなければ追加
    if "import yaml" not in code:
        code = code.replace(
            "from pathlib import Path",
            "from pathlib import Path\nimport yaml"
        )
        tree = cst.parse_module(code)

    new_tree = tree.visit(InstalledAppsTransformer(project_name))
    settings_path.write_text(new_tree.code, encoding="utf-8")

