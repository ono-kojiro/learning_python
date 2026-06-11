import pytest
from opnsense_python import VirtualIPAPI
from utils import extract_vip_list


@pytest.mark.order("last")
def test_cleanup_last_added_virtual_ips(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)

    # -----------------------------
    # 1. 現在の VIP 一覧を取得
    # -----------------------------
    result = vip.list_virtual_ips()
    vip_list = extract_vip_list(result)

    if not vip_list:
        return

    # -----------------------------
    # 2. 最後に追加された VIP を特定
    # -----------------------------
    last_vip = vip_list[-1]
    last_uuid = last_vip["uuid"]

    # -----------------------------
    # 3. 削除実行
    # -----------------------------
    del_result = vip.delete_virtual_ip(last_uuid)
    assert isinstance(del_result, dict)

    # -----------------------------
    # 4. 削除されたことを確認
    # -----------------------------
    result_after = vip.list_virtual_ips()
    vip_list_after = extract_vip_list(result_after)

    assert not any(entry["uuid"] == last_uuid for entry in vip_list_after)

