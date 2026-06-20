import libcst as cst
from pathlib import Path

class InstalledAppsTransformer(cst.CSTTransformer):
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.already_yaml = False

    def visit_Assign(self, node: cst.Assign):
        # safe_load を検出
        if (
            isinstance(node.value, cst.Call)
            and isinstance(node.value.func, cst.Attribute)
            and node.value.func.attr.value == "safe_load"
        ):
            print("[DEBUG] Detected existing YAML safe_load")
            self.already_yaml = True
        return True

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign):
        # YAML 化済みならスキップ
        if self.already_yaml:
            print("[DEBUG] Skipping because already_yaml=True")
            return original_node

        # INSTALLED_APPS のみ置換
        if (
            isinstance(original_node.targets[0].target, cst.Name)
            and original_node.targets[0].target.value == "INSTALLED_APPS"
        ):
            print("[DEBUG] Replacing INSTALLED_APPS with YAML reference")
            new_value = cst.parse_expression(
                f"yaml.safe_load(open(str(BASE_DIR / '{self.project_name}' / 'installed_apps.yml')))"
            )
            return updated_node.with_changes(value=new_value)

        return updated_node


def replace_installed_apps(settings_path: Path, project_name: str):
    code = settings_path.read_text(encoding="utf-8")

    print("=== replace_installed_apps START ===")
    print("project_name:", project_name)
    print("settings_path:", settings_path)
    print("installed_apps.yml in code?:", "installed_apps.yml" in code)

    # すでに YAML 参照方式なら何もしない
    if "installed_apps.yml" in code:
        print("[DEBUG] Already YAML mode. Skipping replace.")
        print("=== replace_installed_apps END ===")
        return

    # import yaml がなければ追加
    if "import yaml" not in code:
        print("[DEBUG] Adding import yaml")
        code = code.replace(
            "from pathlib import Path",
            "from pathlib import Path\nimport yaml"
        )

    tree = cst.parse_module(code)
    print("[DEBUG] Parsed CST")

    new_tree = tree.visit(InstalledAppsTransformer(project_name))
    print("[DEBUG] Transformer applied")

    settings_path.write_text(new_tree.code, encoding="utf-8")
    print("[DEBUG] settings.py updated")
    print("=== replace_installed_apps END ===")


class AllowedHostsYamlTransformer(cst.CSTTransformer):
    def __init__(self, project_name):
        self.project_name = project_name

    def leave_Assign(self, original_node, updated_node):
        if (
            isinstance(original_node.targets[0].target, cst.Name)
            and original_node.targets[0].target.value == "ALLOWED_HOSTS"
        ):
            new_value = cst.parse_expression(
                f"yaml.safe_load(open(str(BASE_DIR / '{self.project_name}' / 'allowed_hosts.yml')))"
            )
            return updated_node.with_changes(value=new_value)

        return updated_node


def replace_allowed_hosts_with_yaml(settings_path, project_name):
    code = settings_path.read_text(encoding="utf-8")
    tree = cst.parse_module(code)

    transformer = AllowedHostsYamlTransformer(project_name)
    new_tree = tree.visit(transformer)

    settings_path.write_text(new_tree.code, encoding="utf-8")

import ast

def extract_installed_apps_list(settings_path):
    """
    settings.py の INSTALLED_APPS = [...] を抽出して Python の list として返す。
    YAML 参照方式の場合は YAML を読み込んで返す。
    """
    code = settings_path.read_text(encoding="utf-8")

    # YAML 参照方式の場合
    if "installed_apps.yml" in code:
        import yaml
        from pathlib import Path

        # BASE_DIR / 'installed_apps.yml' を探す
        settings_dir = settings_path.parent
        yaml_path = settings_dir / "installed_apps.yml"

        if not yaml_path.exists():
            raise RuntimeError(f"installed_apps.yml not found: {yaml_path}")

        return yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    # Python リスト方式の場合（初回）
    tree = ast.parse(code)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "INSTALLED_APPS":
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        return [ast.literal_eval(elt) for elt in node.value.elts]

    raise RuntimeError("INSTALLED_APPS not found in settings.py")


def replace_allowed_hosts_with_yaml(settings_path: Path, project_name: str):
    code = settings_path.read_text(encoding="utf-8")

    print("=== replace_allowed_hosts_with_yaml START ===")
    print("project_name:", project_name)
    print("allowed_hosts.yml in code?:", "allowed_hosts.yml" in code)

    # すでに YAML 参照方式なら何もしない
    if "allowed_hosts.yml" in code:
        print("[DEBUG] Already YAML mode. Skipping replace.")
        print("=== replace_allowed_hosts_with_yaml END ===")
        return

    # import yaml がなければ追加
    if "import yaml" not in code:
        print("[DEBUG] Adding import yaml")
        code = code.replace(
            "from pathlib import Path",
            "from pathlib import Path\nimport yaml"
        )

    tree = cst.parse_module(code)

    class AllowedHostsTransformer(cst.CSTTransformer):
        def leave_Assign(self, original_node, updated_node):
            if (
                isinstance(original_node.targets[0].target, cst.Name)
                and original_node.targets[0].target.value == "ALLOWED_HOSTS"
            ):
                print("[DEBUG] Replacing ALLOWED_HOSTS with YAML reference")
                new_value = cst.parse_expression(
                    f"yaml.safe_load(open(str(BASE_DIR / '{project_name}' / 'allowed_hosts.yml')))"
                )
                return updated_node.with_changes(value=new_value)
            return updated_node

    new_tree = tree.visit(AllowedHostsTransformer())
    settings_path.write_text(new_tree.code, encoding="utf-8")

    print("[DEBUG] settings.py updated")
    print("=== replace_allowed_hosts_with_yaml END ===")

def extract_setting_list(settings_path: Path, setting_name: str):
    code = settings_path.read_text(encoding="utf-8")
    tree = ast.parse(code)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == setting_name:
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    return [ast.literal_eval(elt) for elt in node.value.elts]

    raise RuntimeError(f"{setting_name} not found in settings.py")

def replace_setting_with_yaml(settings_path: Path, setting_name: str, project_name: str):
    code = settings_path.read_text(encoding="utf-8")

    # すでに YAML 化されているなら何もしない
    if f"{setting_name.lower()}.yml" in code:
        return

    if "import yaml" not in code:
        code = code.replace(
            "from pathlib import Path",
            "from pathlib import Path\nimport yaml"
        )

    tree = cst.parse_module(code)

    class Transformer(cst.CSTTransformer):
        def leave_Assign(self, original_node, updated_node):
            if (
                isinstance(original_node.targets[0].target, cst.Name)
                and original_node.targets[0].target.value == setting_name
            ):
                new_value = cst.parse_expression(
                    f"yaml.safe_load(open(str(BASE_DIR / '{project_name}' / '{setting_name.lower()}.yml')))"
                )
                return updated_node.with_changes(value=new_value)
            return updated_node

    new_tree = tree.visit(Transformer())
    settings_path.write_text(new_tree.code, encoding="utf-8")
