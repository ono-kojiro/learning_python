import uuid
import pytest
from opnsense_python import VirtualIPAPI


def extract_vip_list(data):
    """
    あなたの環境の構造:
    {
      "vip": {
        "vip": {
          "UUID1": {...},
          "UUID2": {...}
        }
      }
    }

    → 各エントリに uuid フィールドを埋め込んで list にする
    """
    if "vip" not in data:
        raise AssertionError(f"Invalid VIP response: {data}")

    vip_section = data["vip"]

    if isinstance(vip_section, dict) and "vip" in vip_section:
        inner = vip_section["vip"]

        if isinstance(inner, dict):
            result = []
            for uuid_key, item in inner.items():
                # 値の dict に uuid を埋め込む
                entry = dict(item)
                entry["uuid"] = uuid_key
                result.append(entry)
            return result

        if isinstance(inner, list):
            return inner

    raise AssertionError(f"Unexpected VIP structure: {vip_section}")


def test_add_and_delete_virtual_ip(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)

    # -----------------------------
    # 1. VIP を追加
    # -----------------------------
    host = 30 + (uuid.uuid4().int % 50)
    ip = f"192.168.30.{host}"

    vip_data = {
        "vip": {
            "interface": "opt1",
            "mode": "ipalias",
            "address": f"{ip}/24",
            "subnet": ip,
            "subnet_bits": "24",
            "descr": "pytest-added-vip",
            "noexpand": "0",
            "nobind": "0",
            "gateway": "",
            "password": "",
            "vhid": "",
            "advbase": "1",
            "advskew": "0",
            "peer": "",
            "peer6": "",
            "nosync": "0"
        }
    }

    add_result = vip.add_virtual_ip(vip_data)

    assert isinstance(add_result, dict)
    assert "uuid" in add_result, f"UUID missing: {add_result}"

    new_uuid = add_result["uuid"]

    # -----------------------------
    # 2. VIP が追加されたことを確認
    # -----------------------------
    vip_list = extract_vip_list(vip.list_virtual_ips())
    assert any(entry.get("uuid") == new_uuid for entry in vip_list)

    # -----------------------------
    # 3. VIP を削除
    # -----------------------------
    del_result = vip.delete_virtual_ip(new_uuid)
    assert isinstance(del_result, dict)

    # -----------------------------
    # 4. 削除されたことを確認
    # -----------------------------
    vip_list_after = extract_vip_list(vip.list_virtual_ips())
    assert not any(entry.get("uuid") == new_uuid for entry in vip_list_after)


