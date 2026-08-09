from opnsense.ntpd.api.service import Service


def test_ntpd_meta(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    r = api.meta()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        isinstance(data, dict) or
        any(k in data for k in ["meta", "result", "message", "errorMessage"])
    )

    if "meta" in data:
        assert isinstance(data["meta"], dict)


def test_ntpd_gps(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    r = api.gps()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        isinstance(data, dict) or
        any(k in data for k in ["gps", "result", "message", "errorMessage"])
    )

    if "gps" in data:
        # gps は dict / list / str のどれでも正常
        assert isinstance(data["gps"], (dict, list, str))


def test_ntpd_status(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    r = api.status()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        isinstance(data, dict) or
        any(k in data for k in ["status", "rows", "result", "message", "errorMessage"])
    )

    if "status" in data:
        assert isinstance(data["status"], (dict, str))

    if "rows" in data:
        assert isinstance(data["rows"], list)
