import json
from opnsense.core import Core


def test_firmware_cleanup(client):
    api = Core(client)
    data = api.cleanup_firmware()
    assert any(k in data for k in ["status", "result", "message"])


def test_firmware_connection(client):
    api = Core(client)
    data = api.connection_firmware()
    assert any(k in data for k in ["status", "connection", "message"])


def test_firmware_health(client):
    api = Core(client)
    data = api.health_firmware()
    assert any(k in data for k in ["health", "status"])


def test_firmware_running(client):
    api = Core(client)
    data = api.running_firmware()
    assert any(k in data for k in ["status", "product", "packages"])


def test_firmware_upgradestatus(client):
    api = Core(client)
    data = api.upgradestatus_firmware()
    assert any(k in data for k in ["status", "upgrade", "message"])


def test_firmware_info(client):
    api = Core(client)
    data = api.info_firmware()

    possible_keys = [
        "product",
        "product_version",
        "product_family",
        "product_series",
        "product_type",
        "status",
        "details",
    ]
    assert any(k in data for k in possible_keys)
