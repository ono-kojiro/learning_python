import yaml
import pytest
from opnsense.python import VirtualIPAPI
from utils import extract_vip_list


def load_yaml_vips(path="tests/data/virtual_ips.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def test_add_virtual_ips_from_yaml(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)

    # -----------------------------
    # 1. YAML を読み込む
    # -----------------------------
    vip_entries = load_yaml_vips()
    assert isinstance(vip_entries, list)

    created_uuids = []

    # -----------------------------
    # 2. YAML の VIP をすべて追加
    # -----------------------------
    for entry in vip_entries:
        payload = {"vip": entry}
        result = vip.add_virtual_ip(payload)

        assert "uuid" in result
        created_uuids.append(result["uuid"])

    # -----------------------------
    # 3. 追加された VIP が存在することを確認
    # -----------------------------
    vip_list = extract_vip_list(vip.list_virtual_ips())

    for uuid in created_uuids:
        assert any(v["uuid"] == uuid for v in vip_list)


