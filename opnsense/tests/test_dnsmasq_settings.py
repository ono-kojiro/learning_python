import json
from opnsense.dnsmasq.settings import Settings

def test_dnsmasq_get(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # dnsmasq get は設定全体を返す（空でもOK）
    assert isinstance(data, dict)


def test_dnsmasq_searchhost(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchhost()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_gethost(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.gethost()
    data = r.json()

    # gethost は host または hosts または destination の可能性がある
    assert any(k in data for k in ["host", "hosts", "destination", "result", "server"])

    if "host" in data:
        assert isinstance(data["host"], dict)
    if "hosts" in data:
        assert isinstance(data["hosts"], list)


def test_dnsmasq_searchdomain(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchdomain()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_getdomain(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getdomain()
    data = r.json()

    # getdomain は環境によって以下のいずれかを返す：
    # - {}（設定なし）
    # - "domain"
    # - "domains"
    # - "domainoverride"（あなたの環境）
    # - "result"
    assert (
        data == {} or
        any(k in data for k in ["domain", "domains", "domainoverride", "result"])
    )

    if "domain" in data:
        assert isinstance(data["domain"], dict)
    if "domains" in data:
        assert isinstance(data["domains"], list)
    if "domainoverride" in data:
        assert isinstance(data["domainoverride"], dict)

def test_dnsmasq_searchtag(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchtag()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_gettag(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.gettag()
    data = r.json()

    assert any(k in data for k in ["tag", "tags", "result"])

    if "tag" in data:
        assert isinstance(data["tag"], dict)
    if "tags" in data:
        assert isinstance(data["tags"], list)


def test_dnsmasq_searchrange(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchrange()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_getrange(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getrange()
    data = r.json()

    assert any(k in data for k in ["range", "ranges", "result"])

    if "range" in data:
        assert isinstance(data["range"], dict)
    if "ranges" in data:
        assert isinstance(data["ranges"], list)


def test_dnsmasq_searchoption(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchoption()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_getoption(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getoption()
    data = r.json()

    assert any(k in data for k in ["option", "options", "result"])

    if "option" in data:
        assert isinstance(data["option"], dict)
    if "options" in data:
        assert isinstance(data["options"], list)


def test_dnsmasq_searchboot(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchboot()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_dnsmasq_getboot(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getboot()
    data = r.json()

    assert any(k in data for k in ["boot", "boots", "result"])

    if "boot" in data:
        assert isinstance(data["boot"], dict)
    if "boots" in data:
        assert isinstance(data["boots"], list)


def test_dnsmasq_gettaglist(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.gettaglist()
    data = r.json()

    # gettaglist は tags の一覧を返す
    assert any(k in data for k in ["tags", "result"])

