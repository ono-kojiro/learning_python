from opnsense.syslog.api.service import Service


def test_syslog_reset(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    r = api.reset()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["status", "result", "message", "errorMessage"])
    )


def test_syslog_stats(api_config):
    base_url, key, secret = api_config
    api = Service(base_url, api_key=key, api_secret=secret)

    r = api.stats()
    data = r.json()

    # stats は以下のいずれか：
    # - {} / []
    # - stats（dict）
    # - rows（Diagnostics 系）
    # - status / result / message / errorMessage
    assert (
        data == {} or
        data == [] or
        "stats" in data or
        "rows" in data or
        any(k in data for k in ["status", "result", "message", "errorMessage"])
    )

    if "stats" in data:
        assert isinstance(data["stats"], dict)

    if "rows" in data:
        assert isinstance(data["rows"], list)

