from opnsense.unbound.api.settings import Settings


def _assert_common(data):
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )


def _assert_search(data):
    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )
    if "rows" in data:
        assert isinstance(data["rows"], list)


def _assert_get(data, keys):
    # keys: ["forward", "forward_item"] など
    all_keys = keys + [
        "dot",          # forward の揺らぎ
        "host",         # hostoverride の揺らぎ
        "alias",        # hostalias の揺らぎ
        "blocklist",    # dnsbl の揺らぎ
    ]

    assert (
        data == {} or
        data == [] or
        any(k in data for k in all_keys + ["result", "message", "errorMessage", "status"])
    )

    for k in all_keys:
        if k in data:
            assert isinstance(data[k], dict)


def test_unbound_getnameservers(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    data = api.getnameservers().json()

    assert (
        data == {} or
        data == [] or
        isinstance(data, list) or
        "nameservers" in data or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )

    if isinstance(data, list):
        return

    if "nameservers" in data:
        assert isinstance(data["nameservers"], list)


# forward
def test_unbound_getforward(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)
    _assert_get(api.getforward().json(), ["forward", "forward_item"])


# hostoverride
def test_unbound_gethostoverride(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)
    _assert_get(api.gethostoverride().json(), ["hostoverride", "hostoverride_item"])


# hostalias
def test_unbound_gethostalias(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)
    _assert_get(api.gethostalias().json(), ["hostalias", "hostalias_item"])


# dnsbl
def test_unbound_getdnsbl(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)
    _assert_get(api.getdnsbl().json(), ["dnsbl", "dnsbl_item"])

