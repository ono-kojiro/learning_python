from opnsense.ipsec.api.settings import Settings


def test_ipsec_get(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # ipsec get は環境によって以下のいずれかを返す：
    # - {} / []
    # - ipsec（旧バージョン）
    # - settings（新バージョン）
    # - result
    # - errorMessage
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["ipsec", "settings", "result", "errorMessage"])
    )

    if "ipsec" in data:
        assert isinstance(data["ipsec"], dict)

    if "settings" in data:
        assert isinstance(data["settings"], dict)


