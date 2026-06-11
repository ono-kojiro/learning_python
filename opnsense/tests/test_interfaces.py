from opnsense.python import InterfacesAPI


def test_list_interfaces(opnsense_client):
    api = InterfacesAPI(opnsense_client)

    result = api.list_interfaces()

    # overview/interfaces_info の返却構造に合わせる
    assert "rows" in result
    assert isinstance(result["rows"], list)
    assert len(result["rows"]) > 0

    # インターフェース名一覧を取得
    keys = api.get_interface_keys()
    assert isinstance(keys, list)
    assert len(keys) > 0

