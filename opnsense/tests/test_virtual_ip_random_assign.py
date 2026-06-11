import random
import pytest
import yaml

from opnsense.python import VirtualIPAPI, InterfacesAPI
from utils import extract_vip_list


def load_yaml_vips(path="tests/data/virtual_ips.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def test_random_assign_virtual_ips(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)
    interfaces = InterfacesAPI(opnsense_client)

    # -----------------------------
    # 1. インターフェース一覧を取得（WAN除外）
    # -----------------------------
    keys = interfaces.get_interface_keys()
    candidates = [k for k in keys if k.lower() != "wan"]
    assert len(candidates) > 0

    # -----------------------------
    # 2. YAML の VIP を読み込む
    # -----------------------------
    vip_entries = load_yaml_vips()
    yaml_addresses = {entry["address"] for entry in vip_entries}

    # -----------------------------
    # 3. 既存の VIP のうち、YAML と同じ address を削除
    # -----------------------------
    existing = extract_vip_list(vip.list_virtual_ips())

    for entry in existing:
        if entry.get("address") in yaml_addresses:
            vip.delete_virtual_ip(entry["uuid"])

    # -----------------------------
    # 4. ランダムにインターフェースを割り当てて VIP を追加
    # -----------------------------
    created_uuids = []

    for entry in vip_entries:
        iface = random.choice(candidates)

        entry = entry.copy()
        entry["interface"] = iface

        payload = {"vip": entry}
        result = vip.add_virtual_ip(payload)

        assert "uuid" in result, f"Add failed: {result}"
        created_uuids.append(result["uuid"])

    # -----------------------------
    # 5. 追加された VIP が存在することを確認
    # -----------------------------
    vip_list = extract_vip_list(vip.list_virtual_ips())

    for uuid in created_uuids:
        assert any(v["uuid"] == uuid for v in vip_list)

