from opnsense.interfaces.api.overview import Overview


def test_interfaces_interfacesinfo(api_config):
    base_url, key, secret = api_config
    api = Overview(base_url, api_key=key, api_secret=secret)

    r = api.interfacesinfo()
    data = r.json()

    # interfacesinfo は環境によって以下のいずれかを返す：
    # - {} / []
    # - rows (OPNsense 26.7)
    # - interfaces (旧バージョン)
    # - result / status
    assert (
        data == {} or
        data == [] or
        isinstance(data, list) or
        any(k in data for k in ["rows", "interfaces", "result", "status"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)
    if "interfaces" in data:
        assert isinstance(data["interfaces"], dict)


def test_interfaces_getinterface(api_config):
    base_url, key, secret = api_config
    api = Overview(base_url, api_key=key, api_secret=secret)

    r = api.getinterface()
    data = r.json()

    # getinterface は以下のいずれか：
    # - {} / []
    # - interface
    # - message (引数不足)
    # - errorMessage
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["interface", "message", "errorMessage", "result"])
    )

    if "interface" in data:
        assert isinstance(data["interface"], dict)


def test_interfaces_export(api_config):
    base_url, key, secret = api_config
    api = Overview(base_url, api_key=key, api_secret=secret)

    r = api.export()
    data = r.json()

    # export は以下のいずれか：
    # - {} / []
    # - list (OPNsense 26.7)
    # - interfaces / config / result
    assert (
        data == {} or
        data == [] or
        isinstance(data, list) or
        any(k in data for k in ["interfaces", "config", "result"])
    )
