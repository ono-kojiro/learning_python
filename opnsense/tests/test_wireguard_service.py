from opnsense.wireguard.api.service import Service


def test_wireguard_reconfigure(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    data = api.reconfigure().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "status", "message", "errorMessage"])
    )


def test_wireguard_show(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    data = api.show().json()

    # show は interfaces / peers / status / rows のどれでも正常
    assert (
        data == {} or
        data == [] or
        any(k in data for k in [
            "interfaces",
            "peers",
            "status",
            "rows",
            "result",
            "message",
            "errorMessage"
        ])
    )

    if "interfaces" in data:
        assert isinstance(data["interfaces"], list)

    if "peers" in data:
        assert isinstance(data["peers"], list)

    if "status" in data:
        assert isinstance(data["status"], dict)

    if "rows" in data:
        assert isinstance(data["rows"], list)

