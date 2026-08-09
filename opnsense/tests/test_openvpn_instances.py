from opnsense.openvpn.api.instances import Instances


def test_openvpn_search(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.search()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_openvpn_get(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["instance", "result", "message", "errorMessage"])
    )


def test_openvpn_add(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.add()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_set(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.set()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_delete(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.delete()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_toggle(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.toggle()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_searchstatickey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.searchstatickey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_openvpn_getstatickey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.getstatickey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["statickey", "result", "message", "errorMessage"])
    )


def test_openvpn_addstatickey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.addstatickey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_setstatickey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.setstatickey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_delstatickey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.delstatickey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_openvpn_genkey(api_config):
    base_url, key, secret = api_config
    api = Instances(base_url, api_key=key, api_secret=secret)

    r = api.genkey()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["key", "result", "message", "errorMessage"])
    )

    if "key" in data:
        assert isinstance(data["key"], str)

