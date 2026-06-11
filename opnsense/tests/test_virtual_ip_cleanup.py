import pytest
from opnsense.python import VirtualIPAPI
from utils import extract_vip_list


@pytest.mark.order("last")
def test_cleanup_all_virtual_ips(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)

    # 現在の VIP 一覧を取得
    vip_list = extract_vip_list(vip.list_virtual_ips())

    # VIP が無ければ何もしない
    if not vip_list:
        return

    # すべて削除
    for entry in vip_list:
        vip.delete_virtual_ip(entry["uuid"])

    # 削除確認
    vip_list_after = extract_vip_list(vip.list_virtual_ips())
    assert len(vip_list_after) == 0

