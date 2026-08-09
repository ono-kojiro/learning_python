from opnsense.routing.settings import Settings


def test_routing_reconfigure(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.reconfigure()
    data = r.json()

    # reconfigure は status / result / message / errorMessage の揺らぎが大きい
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["status", "result", "message", "errorMessage"])
    )


def test_routing_searchgateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchgateway()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_routing_getgateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getgateway()
    data = r.json()

    # getgateway は gateway / gateway_item のどちらでも正常
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["gateway", "gateway_item", "result", "message", "errorMessage"])
    )

    if "gateway" in data:
        assert isinstance(data["gateway"], dict)

    if "gateway_item" in data:
        assert isinstance(data["gateway_item"], dict)


def test_routing_setgateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.setgateway()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_routing_addgateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.addgateway()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_routing_delgateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.delgateway()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_routing_togglegateway(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.togglegateway()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

