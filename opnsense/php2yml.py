#!/usr/bin/env python3
import sys
import getopt
import re
import os

def usage():
    print("Usage: php2api.py [-o output_file] controller.php")
    sys.exit(1)


def extract_function_body(php, func):
    start = php.find(f"function {func}Action")
    if start == -1:
        return ""

    brace_start = php.find("{", start)
    if brace_start == -1:
        return ""

    depth = 0
    i = brace_start
    length = len(php)

    while i < length:
        if php[i] == "{":
            depth += 1
        elif php[i] == "}":
            depth -= 1
            if depth == 0:
                return php[brace_start+1:i]
        i += 1

    return ""


def split_action_name(action):
    """
    getAlert → ("get", "alert")
    setService → ("set", "service")
    searchTest → ("search", "test")
    toggleGeneral → ("toggle", "general")
    importAlias → ("import", "alias")
    exportAlias → ("export", "alias")
    """
    ops = ["get", "set", "add", "del", "search", "toggle", "check", "reconfigure", "import", "export"]

    action_lower = action.lower()

    for op in ops:
        if action_lower.startswith(op):
            return op, action_lower[len(op):]

    return action_lower, ""


# ★ Python予約語を安全な名前に変換する
RESERVED_MAP = {
    "import": "load",
    "export": "save",
}


def safe_operation_name(op):
    return RESERVED_MAP.get(op, op)


def extract_api_info(filepath):
    with open(filepath, "r") as f:
        php = f.read()

    parts = filepath.split("/")
    module = parts[-2].lower()
    controller = parts[-1].replace("controller.php", "").lower()

    actions = re.findall(r'function\s+(\w+)Action', php)

    api_list = []

    for func in actions:
        action = func.replace("Action", "")
        body = extract_function_body(php, func)

        if "isPost()" in body or "getPost(" in body:
            http_method = "POST"
        elif "$this->request->get(" in body:
            http_method = "GET"
        else:
            http_method = "GET"

        operation, subcategory = split_action_name(action)

        # ★ 予約語変換
        safe_op = safe_operation_name(operation)

        api_path = f"/{module}/{controller}/{safe_op}{subcategory}"

        api_list.append({
            "function": func,
            "method": http_method,
            "path": api_path,
            "operation": safe_op,
            "subcategory": subcategory,
        })

    return module, controller, api_list


def generate_openapi(api_list, title, module, controller):
    out = []
    out.append("openapi: 3.0.3")
    out.append("info:")
    out.append(f"  title: {title}")
    out.append("  version: \"1.0.0\"")
    out.append("paths:")

    tag = f"{module}_{controller}"

    for api in api_list:
        path = api["path"]
        method = api["method"].lower()
        operation = api["operation"]
        subcategory = api["subcategory"]

        summary = subcategory or operation
        operationId = operation  # ★ 予約語変換済み

        out.append(f"  {path}:")
        out.append(f"    {method}:")
        out.append(f"      summary: {summary}")
        out.append(f"      operationId: {operationId}")
        out.append(f"      tags: [\"{tag}\"]")
        out.append(f"      responses:")
        out.append(f"        \"200\":")
        out.append(f"          description: OK")

    return "\n".join(out)


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

    input_file = args[0]

    if not os.path.isfile(input_file):
        print("File not found:", input_file)
        sys.exit(1)

    module, controller, api_list = extract_api_info(input_file)

    if output_file:
        out = open(output_file, "w")
    else:
        out = sys.stdout

    if len(api_list) == 0:
        out.write(f"# No API actions found in {input_file}\n")
        out.write("openapi: 3.0.3\n")
        out.write("info:\n")
        out.write(f"  title: OPNsense {module.capitalize()} {controller.capitalize()} API (Empty)\n")
        out.write("  version: \"1.0.0\"\n")
        out.write("paths: {}\n")
        if output_file:
            out.close()
        return

    for api in api_list:
        out.write(f"# {api['method']:5}  {api['path']:35}  {api['operation']} {api['subcategory']}\n")

    out.write("\n")

    title = f"OPNsense {module.capitalize()} {controller.capitalize()} API"
    out.write(generate_openapi(api_list, title, module, controller) + "\n")

    if output_file:
        out.close()


if __name__ == "__main__":
    main()
