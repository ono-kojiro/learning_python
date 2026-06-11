from opnsense_python import VirtualIPAPI
from utils import extract_vip_list   # 共通関数として import する想定


def test_list_virtual_ips(opnsense_client):
    vip = VirtualIPAPI(opnsense_client)

    result = vip.list_virtual_ips()

    vip_list = extract_vip_list(result)

    # VIP が list として取得できること
    assert isinstance(vip_list, list)

    # 各エントリに uuid が含まれていること
    for entry in vip_list:
        assert "uuid" in entry
        assert "address" in entry

