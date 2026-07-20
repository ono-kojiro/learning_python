#!/usr/bin/env python3
# file: tools/generate_testscript.py

import sys
import json
import getopt
import os
import datetime


def usage():
    print("Usage: generate_testscript.py schema.json -o OUTPUT_FILE")
    sys.exit(1)


def singularize(name: str) -> str:
    return name[:-1] if name.endswith("s") else name


def gen_dummy_value_str(fname, fdef):
    ftype = fdef.get("type")

    if ftype == "AutoField":
        return "null"

    if ftype == "CharField":
        return f"\"{fname.upper()}-{os.urandom(4).hex()}\""

    if ftype == "IntegerField":
        return "1"

    if ftype == "DateTimeField":
        return f"\"{datetime.datetime.now().isoformat()}\""

    if ftype == "JSONField":
        return "[]"

    return "null"


def build_order(schema):
    compositions = schema.get("compositions", {})
    root = schema.get("composition_root")
    models = list(schema["models"].keys())

    visited = set()
    order = []

    def dfs(model):
        if model in visited:
            return
        visited.add(model)
        order.append(model)
        for child in compositions.get(model, []):
            dfs(child)

    dfs(root)

    if "Manager" in models and "Manager" not in order:
        order.insert(order.index(root) + 1, "Manager")

    for m in models:
        if m not in order:
            order.append(m)

    return order


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

    schema_path = args[0]
    if not output_file:
        usage()

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    through_lower = {tm["name"].lower() for tm in schema.get("through_models", [])}
    primary_keys = schema.get("primary_keys", {})

    ordered_caps = build_order(schema)
    ordered_models = []
    for cap in ordered_caps:
        lower = cap.lower()
        if lower in through_lower:
            continue
        if cap in schema["models"]:
            ordered_models.append((lower, cap))

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("#!/bin/sh\n")
        out.write("# Auto-generated ADD test script (debug_add.sh style)\n\n")
        out.write(". ./.env\n")
        out.write('if [ -z "$BASE_URL" ]; then echo "ERROR: BASE_URL is not set"; exit 1; fi\n\n')
        out.write('echo "Using BASE_URL=$BASE_URL"\n\n')
        out.write(f'echo "1..{len(ordered_models)}"\n\n')

        for model_lower, model_cap in ordered_models:
            fields_def = schema["models"][model_cap]["fields"]
            pk_field = primary_keys[model_cap]
            var_name = f"id_{model_lower}"

            out.write("############################################\n")
            out.write(f"# Registering {model_cap}\n")
            out.write("############################################\n")
            out.write(f'echo "=== Registering {model_lower} ==="\n\n')

            out.write("json_data=$(cat <<EOF\n")
            out.write("{\n")

            field_items = list(fields_def.items())
            lines = []
            for fname, fdef in field_items:
                if fname == "id":
                    continue

                ftype = fdef["type"]

                if ftype == "ForeignKey":
                    parent = fdef["to"]
                    parent_lower = parent.lower()
                    parent_var = f"${{id_{parent_lower}}}"
                    value = f"\"{parent_var}\""
                    key = f"{fname}_id"
                elif ftype == "ManyToManyField":
                    singular = singularize(fname)
                    key = f"{singular}_ids"
                    value = "[]"
                else:
                    key = fname
                    value = gen_dummy_value_str(fname, fdef)

                lines.append(f'  "{key}": {value}')

            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    out.write(line + ",\n")
                else:
                    out.write(line + "\n")

            out.write("}\n")
            out.write("EOF\n)\n\n")

            api_path = f"/api/{model_lower}s/"

            out.write(f'res=$(curl -s -k -X POST "${{BASE_URL}}{api_path}" \\\n')
            out.write('    -H "Content-Type: application/json" \\\n')
            out.write('    -d "$json_data")\n\n')

            out.write(f'echo "[DEBUG] POST {api_path} response:"\n')
            out.write('echo "$res"\n\n')

            out.write(f'{var_name}=$(echo "$res" | jq -r ".{pk_field}")\n')
            out.write(f'if [ "${{{var_name}}}" = "null" ] || [ -z "${{{var_name}}}" ]; then\n')
            out.write(f'    echo "not ok - add {model_lower} failed"\n')
            out.write("    exit 1\n")
            out.write("else\n")
            out.write(f'    echo "ok - add {model_lower} succeeded"\n')
            out.write("fi\n\n")

    print(f"[OK] Generated test script: {output_file}")


if __name__ == "__main__":
    main()
