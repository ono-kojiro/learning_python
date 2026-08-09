#!/usr/bin/env python3
import sys
import getopt
import re
import os

def usage():
    print("Usage: php2api.py [-o output_file] controller.php")
    sys.exit(1)


def extract_function_body(php, func):
    """
    function <func>Action (...) { ... } の本体を
    正規表現ではなくブレースカウントで安全に抽出する
    """
    start = php.find(f"function {func}Action")
    if start == -1:
        return ""

    # 関数開始位置から最初の '{' を探す
    brace_start = php.find("{", start)
    if brace_start == -1:
        return ""

    depth = 0
    i = brace_start
    length = len(php)

    # 本体抽出
    while i < length:
        if php[i] == "{":
            depth += 1
        elif php[i] == "}":
            depth -= 1
            if depth == 0:
                # 関数本体終了
                return php[brace_start+1:i]
        i += 1

    return ""


def extract_api_info(filepath):
    with open(filepath, "r") as f:
        php = f.read()

    parts = filepath.split("/")
    module = parts[-2].lower()
    controller = parts[-1].replace("controller.php", "").lower()

    actions = re.findall(r'function\s+(\w+)Action', php)

    api_list = []

    for func in actions:
        action = func.replace("Action", "").lower()

        # 関数本体をブレースカウントで抽出
        body = extract_function_body(php, func)

        # HTTPメソッド判定（誤判定防止）
        if "isPost()" in body or "getPost(" in body:
            http_method = "POST"
        elif "$this->request->get(" in body:
            http_method = "GET"
        else:
            http_method = "GET"

        api_path = f"/api/{module}/{controller}/{action}"

        api_list.append({
            "function": func,
            "method": http_method,
            "path": api_path,
            "summary": action
        })

    return api_list


def generate_openapi(api_list, title):
    out = []
    out.append("openapi: 3.0.3")
    out.append("info:")
    out.append(f"  title: {title}")
    out.append("  version: \"1.0.0\"")
    out.append("paths:")

    for api in api_list:
        path = api["path"]
        method = api["method"].lower()
        summary = api["summary"]
        operationId = api["summary"]

        out.append(f"  {path}:")
        out.append(f"    {method}:")
        out.append(f"      summary: {summary}")
        out.append(f"      operationId: {operationId}")
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

    api_list = extract_api_info(input_file)

    if output_file:
        out = open(output_file, "w")
    else:
        out = sys.stdout

    if len(api_list) == 0:
        out.write(f"# No API actions found in {input_file}\n")
        if output_file:
            out.close()
        return

    # コメントとして API 一覧を出力
    for api in api_list:
        out.write(f"# {api['method']:5}  {api['path']:35}  {api['summary']}\n")

    out.write("\n")

    # OpenAPI YAML 出力
    module = api_list[0]['path'].split('/')[2].capitalize()
    controller = api_list[0]['path'].split('/')[3].capitalize()
    title = f"OPNsense {module} {controller} API"

    out.write(generate_openapi(api_list, title) + "\n")

    if output_file:
        out.close()


if __name__ == "__main__":
    main()

