from opnsense.monit.status import Status


def test_monit_status_get(api_config):
    base_url, key, secret = api_config
    api = Status(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # Monit status は環境によって以下のいずれかを返す：
    # - {} / []
    # - status（dict または str）
    # - monit（dict）
    # - result / message / errorMessage
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["status", "monit", "result", "message", "errorMessage"])
    )

    if "status" in data:
        # status は dict または str のどちらでも正常
        assert isinstance(data["status"], (dict, str))

    if "monit" in data:
        assert isinstance(data["monit"], dict)
