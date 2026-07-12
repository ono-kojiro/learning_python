# amcli/utils/nested.py (NEW LOGIC VERSION)

from amcli.utils.constants import FieldType, normalize_field_type

def collect_nested(models):
    """
    新ロジック:
    Device を root として正方向の参照から nested を構築する。

    Device
      ├─ OS (OneToOneField)
      ├─ NetIF (ForeignKey)
      │    └─ IPv4 (ForeignKey)
      ├─ Comment (ForeignKey)
      ├─ Remark (ForeignKey)
      └─ Manager (ManyToMany)

    Manager
      └─ Device (ManyToMany)
    """

    print("[DEBUG] NEW LOGIC EXECUTED: collect_nested() started")

    nested = {}

    # ------------------------------------------------------------
    # Device の子モデルを収集（正方向の参照）
    # ------------------------------------------------------------
    device_children = []

    device_fields = models["Device"]["fields"]
    for fname, fdef in device_fields.items():
        ftype = normalize_field_type(fdef.get("type"))
        to = fdef.get("to")

        if ftype == FieldType.ONE_TO_ONE and to == "OS":
            device_children.append({
                "name": "os",
                "kind": "one_to_one",
                "model": "OS",
                "fk": "device"
            })

        elif ftype == FieldType.MANY_TO_MANY and to == "Manager":
            device_children.append({
                "name": "managers",
                "kind": "many_to_many"
            })

    # ------------------------------------------------------------
    # Device を参照するモデル（ForeignKey）
    # ------------------------------------------------------------
    for model_name, model_def in models.items():
        if model_name == "Device":
            continue

        for fname, fdef in model_def["fields"].items():
            ftype = normalize_field_type(fdef.get("type"))
            to = fdef.get("to")

            if ftype == FieldType.FOREIGN_KEY and to == "Device":
                device_children.append({
                    "name": model_name.lower() + "s",
                    "kind": "one_to_many",
                    "model": model_name,
                    "fk": "device"
                })

    nested["Device"] = device_children

    # ------------------------------------------------------------
    # NetIF の子モデル（IPv4）
    # ------------------------------------------------------------
    netif_children = []
    for fname, fdef in models["IPv4"]["fields"].items():
        ftype = normalize_field_type(fdef.get("type"))
        to = fdef.get("to")

        if ftype == FieldType.FOREIGN_KEY and to == "NetIF":
            netif_children.append({
                "name": "ipv4s",
                "kind": "one_to_many",
                "model": "IPv4",
                "fk": "netif"
            })

    if netif_children:
        nested["NetIF"] = netif_children

    # ------------------------------------------------------------
    # Manager の逆参照（ManyToMany）
    # ------------------------------------------------------------
    manager_children = []
    for fname, fdef in models["Manager"]["fields"].items():
        ftype = normalize_field_type(fdef.get("type"))
        to = fdef.get("to")

        if ftype == FieldType.MANY_TO_MANY and to == "Device":
            manager_children.append({
                "name": "devices",
                "kind": "many_to_many"
            })

    if manager_children:
        nested["Manager"] = manager_children

    print("[DEBUG] NEW LOGIC EXECUTED: collect_nested() finished")

    return nested
