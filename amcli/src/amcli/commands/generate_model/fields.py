# file: /src/amcli/commands/generate_model/fields.py

from amcli.utils.constants import FieldType


def render_default(k, v):
    if k == "default" and (v in ["list", "dict"]):
        return f"default={v}"
    elif k == "on_delete":
        return f"{k}=models.{v}"
    else:
        return f"{k}={repr(v)}"


def render_simple_field(fname, field_def):
    # ★ アンダースコアで始まるキーを除外
    field_def = {k: v for k, v in field_def.items() if not k.startswith("_")}

    args = []
    for k, v in field_def.items():
        if k == "type":
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))

    arg_str = ", ".join(args)
    return f"{fname} = models.{field_def['type'].value}({arg_str})"


def render_relation_field(fname, field_def, ftype: FieldType):
    # ★ アンダースコアで始まるキーを除外
    field_def = {k: v for k, v in field_def.items() if not k.startswith("_")}

    args = []

    args.append(f"to={repr(field_def['to'])}")

    val = field_def.get("on_delete", "CASCADE")
    if isinstance(val, str) and val.startswith("models."):
        args.append(f"on_delete={val}")
    else:
        args.append(f"on_delete=models.{val}")

    for k, v in field_def.items():
        if k in ["type", "to", "on_delete"]:
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))

    arg_str = ", ".join(args)
    return f"{fname} = models.{ftype.value}({arg_str})"


def render_many_to_many_field(fname, field_def, model_name):
    # ★ アンダースコアで始まるキーを除外
    field_def = {k: v for k, v in field_def.items() if not k.startswith("_")}

    args = []
    args.append(repr(field_def["to"]))

    for k, v in field_def.items():
        if k in ["type", "to"]:
            continue
        args.append(render_default(k, v))

    if not any(a.startswith("related_name=") for a in args):
        args.append(f"related_name='{model_name.lower()}s'")

    arg_str = ", ".join(args)
    return f"{fname} = models.ManyToManyField({arg_str})"
