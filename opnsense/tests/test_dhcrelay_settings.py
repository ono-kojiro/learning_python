from opnsense.dhcrelay import Dhcrelay


def test_dhcrelay_searchrelay(client):
    api = Dhcrelay(client)
    data = api.search_relay()

    # searchrelay は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dhcrelay_getrelay(client):
    api = Dhcrelay(client)
    data = api.get_relay()

    # getrelay は環境によって以下のいずれかを返す：
    # - {}（設定なし）
    # - "relay"
    # - "relays"
    # - "destination"（あなたの環境）
    # - "result"
    assert (
        data == {} or
        any(k in data for k in ["relay", "relays", "destination", "result"])
    )

    if "relay" in data:
        assert isinstance(data["relay"], dict)

    if "relays" in data:
        assert isinstance(data["relays"], list)

    if "destination" in data:
        assert isinstance(data["destination"], dict)


def test_dhcrelay_searchdest(client):
    api = Dhcrelay(client)
    data = api.search_dest()

    # searchdest は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dhcrelay_getdest(client):
    api = Dhcrelay(client)
    data = api.get_dest()

    # getdest は環境によって以下のいずれかを返す：
    # - {}（設定なし）
    # - "dest"
    # - "dests"
    # - "destination"（環境依存）
    # - "result"
    assert (
        data == {} or
        any(k in data for k in ["dest", "dests", "destination", "result"])
    )

    if "dest" in data:
        assert isinstance(data["dest"], dict)

    if "dests" in data:
        assert isinstance(data["dests"], list)

    if "destination" in data:
        assert isinstance(data["destination"], dict)
