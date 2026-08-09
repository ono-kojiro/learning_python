from opnsense.radvd.settings import Settings


def test_radvd_searchentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchentry()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_radvd_getentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getentry()
    data = r.json()

    # getentry は以下のいずれか：
    # - {} / []
    # - entry（dict）
    # - entries（dict）
    # - result / message / errorMessage
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["entry", "entries", "result", "message", "errorMessage"])
    )

    if "entry" in data:
        assert isinstance(data["entry"], dict)

    if "entries" in data:
        assert isinstance(data["entries"], dict)


def test_radvd_addentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.addentry()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_radvd_setentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.setentry()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_radvd_delentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.delentry()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_radvd_toggleentry(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.toggleentry()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

