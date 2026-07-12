# src/amcli/commands/cmp2ref/convert.py

from amcli.utils.constants import FieldType

def convert_primitive_field(fdef):
    out = {}
    ftype = fdef["type"]

    if ftype == "String":
        out["type"] = FieldType.CHAR.value
        out["max_length"] = fdef.get("max_length", 255)

    elif ftype == "Text":
        out["type"] = FieldType.TEXT.value

    elif ftype == "Int":
        out["type"] = FieldType.INTEGER.value

    elif ftype == "Float":
        out["type"] = FieldType.FLOAT.value

    elif ftype == "Bool":
        out["type"] = FieldType.BOOLEAN.value

    elif ftype == "ID":
        out["type"] = FieldType.CHAR.value
        out["max_length"] = fdef.get("max_length", 100)
        out["unique"] = True

    elif ftype.startswith("List"):
        out["type"] = FieldType.JSON.value

    elif ftype == "DateTime":
        out["type"] = FieldType.DATETIME.value

    elif ftype == "Date":
        out["type"] = FieldType.DATE.value

    else:
        raise ValueError(f"Unknown primitive type: {ftype}")

    # primary_key は保持するだけ（付けない）
    if "primary_key" in fdef:
        out["primary_key"] = True

    if "unique" in fdef:
        out["unique"] = fdef["unique"]

    if "default" in fdef:
        out["default"] = fdef["default"]

    if "help_text" in fdef:
        out["help_text"] = fdef["help_text"]
    elif "help" in fdef:
        out["help_text"] = fdef["help"]

    return out

