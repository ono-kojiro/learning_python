#!/usr/bin/env python3
import sys
import getopt
import yaml
import os
from string import Template

TEMPLATE = Template("""
import requests

class $class_name:
    def __init__(self, base_url, api_key=None, api_secret=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_secret = api_secret

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return requests.request(
            method,
            url,
            auth=(self.api_key, self.api_secret),
            verify=False,
            **kwargs
        )

$methods
""")

METHOD_TEMPLATE = Template("""
    def $func(self, **kwargs):
        \"\"\"$summary\"\"\"
        return self._request("$method", "$path", **kwargs)
""")

def usage():
    print("Usage: yaml2py.py [-o output_file] controller.yml")
    sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    except getopt.GetoptError:
        usage()

    output_file = None
    for opt, val in opts:
        if opt in ("-o", "--output"):
            output_file = val

    if len(args) != 1:
        usage()

    yaml_file = args[0]

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # ★ 空 YAML の場合は空クラスを生成して終了
    if not data or "paths" not in data:
        base = os.path.basename(yaml_file).replace(".yml", "")
        class_name = base.replace("controller", "").capitalize()

        py_code = f"class {class_name}:\n    pass\n"

        out_file = output_file if output_file else base.replace("controller", "").lower() + ".py"
        with open(out_file, "w") as out:
            out.write(py_code)

        print(f"Generated empty API class: {out_file}")
        return

    paths = data["paths"]

    base = os.path.basename(yaml_file).replace(".yml", "")
    class_name = base.replace("controller", "").capitalize()

    methods_code = ""

    for path, methods in paths.items():
        for method, info in methods.items():
            func = info.get("operationId", "unknown")
            summary = info.get("summary", "")
            methods_code += METHOD_TEMPLATE.substitute(
                func=func,
                summary=summary,
                method=method.upper(),
                path=path
            )

    py_code = TEMPLATE.substitute(class_name=class_name, methods=methods_code)

    out_file = output_file if output_file else base.replace("controller", "").lower() + ".py"

    with open(out_file, "w") as out:
        out.write(py_code)

    print(f"Generated {out_file}")

if __name__ == "__main__":
    main()
