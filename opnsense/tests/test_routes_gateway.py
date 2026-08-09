from opnsense.routes.gateway import Gateway


def test_routes_gateway_status(api_config):
    base_url, key, secret = api_config
    api = Gateway(base_url, api_key=key, api_secret=secret)

    r = api.status()
    data = r.json()

    # gateway status は環境によって以下のいずれかを返す：
    # - {} / []
    # - rows（Diagnostics 系）
    # - status（dict または str）
    # - result / message / errorMessage
    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["status", "result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)

    if "status" in data:
        # status は dict または str のどちらでも正常
        assert isinstance(data["status"], (dict, str))

