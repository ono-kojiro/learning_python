import json
from opnsense.core.firmware import Firmware

def test_firmware_cleanup(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.cleanup()
    data = r.json()

    # cleanup は status/result/message のいずれかを返す
    assert any(k in data for k in ["status", "result", "message"])


def test_firmware_connection(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.connection()
    data = r.json()

    # connection は status/connection/message のいずれか
    assert any(k in data for k in ["status", "connection", "message"])


def test_firmware_health(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.health()
    data = r.json()

    # health は health/status のいずれか
    assert any(k in data for k in ["health", "status"])


def test_firmware_running(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.running()
    data = r.json()

    # running は status/product/packages のいずれか
    assert any(k in data for k in ["status", "product", "packages"])


def test_firmware_upgradestatus(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.upgradestatus()
    data = r.json()

    # upgradestatus は status/upgrade/message のいずれか
    assert any(k in data for k in ["status", "upgrade", "message"])


def test_firmware_info(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.info()
    data = r.json()

    # firmware info は製品情報を返す。以下のいずれかが存在すればOK。
    possible_keys = [
        "product",
        "product_version",
        "product_family",
        "product_series",
        "product_type",
        "status",
        "details"
    ]

    assert any(k in data for k in possible_keys)

def test_firmware_getoptions(api_config):
    base_url, key, secret = api_config
    api = Firmware(base_url, api_key=key, api_secret=secret)

    r = api.getoptions()
    data = r.json()

    # getoptions は families/flavours/types のいずれか
    assert any(k in data for k in ["families", "flavours", "types"])
