import json
from opnsense.dhcrelay.api.settings import Settings

def test_dhcrelay_searchrelay(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchrelay()
    data = r.json()

    # searchrelay は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dhcrelay_getrelay(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getrelay()
    data = r.json()

    # getrelay は relay 情報を返す（空でもOK）
    # OPNsense 26.7 では "relay" または "relays" が返る
    assert any(k in data for k in ["relay", "relays"])

    if "relay" in data:
        assert isinstance(data["relay"], dict)

    if "relays" in data:
        assert isinstance(data["relays"], list)


def test_dhcrelay_getdest(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getdest()
    data = r.json()

    # getdest は設定がない場合は {} を返すことがある
    # 設定がある場合は dest/dests が返る
    assert (
        data == {} or
        any(k in data for k in ["dest", "dests", "result"])
    )

    if "dest" in data:
        assert isinstance(data["dest"], dict)

    if "dests" in data:
        assert isinstance(data["dests"], list)

def test_dhcrelay_searchdest(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchdest()
    data = r.json()

    # searchdest は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dhcrelay_getdest(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getdest()
    data = r.json()

    # getdest は環境によって以下のいずれかを返す：
    # - {}（設定なし）
    # - "dest"
    # - "dests"
    # - "destination"（あなたの環境）
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
