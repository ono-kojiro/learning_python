import libcst as cst

class InstalledAppsExtractor(cst.CSTVisitor):
    def __init__(self):
        self.apps = None

    def visit_Assign(self, node):
        # INSTALLED_APPS = [...] を探す
        if (
            isinstance(node.targets[0].target, cst.Name)
            and node.targets[0].target.value == "INSTALLED_APPS"
        ):
            if isinstance(node.value, cst.List):
                # リストの中身を抽出
                self.apps = [
                    el.value.value.strip("'\"")
                    for el in node.value.elements
                    if isinstance(el.value, cst.SimpleString)
                ]

def extract_installed_apps(settings_path):
    code = settings_path.read_text(encoding="utf-8")
    tree = cst.parse_module(code)

    extractor = InstalledAppsExtractor()
    tree.visit(extractor)

    return extractor.apps or []

