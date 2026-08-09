#!/usr/bin/env python3
import sys
import getopt
import yaml
from pathlib import Path


def usage():
    print("Usage: generate_wrappers.py -o output_dir openapi.yml")
    sys.exit(1)


def snake_to_camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def extract_settings_subcategory(path: str):
    """
    /monit/settings/getalert → alert
    /monit/settings/setservice → service
    /monit/settings/gettest → test
    """
    last = path.split("/")[-1]  # getalert
    ops = ["get", "set", "add", "del", "search", "toggle"]
    for op in ops:
        if last.startswith(op):
            return last[len(op):]
    return last


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    except getopt.GetoptError:
        usage()

    output_dir = None
    for opt, val in opts:
        if opt in ("-o", "--output"):
            output_dir = val

    if output_dir is None or len(args) != 1:
        usage()

    input_file = args[0]

    with open(input_file) as f:
        spec = yaml.safe_load(f)

    paths = spec.get("paths", {})

    prefix_map = {}

    for path, item in paths.items():
        for http_method, detail in item.items():
            operationId = detail.get("operationId")
            tags = detail.get("tags", [])

            if not operationId or not tags:
                continue

            tag = tags[0]  # monit_status
            prefix, category = tag.split("_")  # monit, status

            # subcategory の決定
            if category == "settings":
                subcategory = extract_settings_subcategory(path)
            else:
                subcategory = category  # status / service

            method_name = f"{operationId}_{subcategory}".lower()

            # import パス
            filename = operationId
            if operationId in ["set", "del"]:
                filename = operationId + "_"

            import_path = f"opnsense.{prefix}.{category}.{filename}"

            prefix_map.setdefault(prefix, [])
            prefix_map[prefix].append({
                "method_name": method_name,
                "import": import_path,
            })

    # 出力
    for prefix, methods in prefix_map.items():
        class_name = snake_to_camel(prefix)

        target_dir = Path(output_dir) / prefix
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = target_dir / "__init__.py"

        lines = []
        lines.append("import json\n\n")
        lines.append(f"class {class_name}:\n")
        lines.append("    def __init__(self, client):\n")
        lines.append("        self.client = client\n\n")

        for m in methods:
            lines.append(f"    def {m['method_name']}(self):\n")
            lines.append(f"        from {m['import']} import sync_detailed\n")
            lines.append("        r = sync_detailed(client=self.client)\n")
            lines.append("        return json.loads(r.content)\n\n")

        with open(filename, "w") as f:
            f.write("".join(lines))

        print(f"Generated: {filename}")


if __name__ == "__main__":
    main()
