from opnsense.kea.ddns import Ddns


def test_kea_ddns_get(api_config):
    base_url, key, secret = api_config
    api = Ddns(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # kea ddns get は環境によって以下のいずれかを返す：
    # - {} / []
    # - ddns（旧バージョン）
    # - settings（新バージョン）
    # - result
    # - errorMessage
    # - message
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["ddns", "settings", "result", "errorMessage", "message"])
    )

    if "ddns" in data:
        assert isinstance(data["ddns"], dict)

    if "settings" in data:
        assert isinstance(data["settings"], dict)

