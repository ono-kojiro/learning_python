import json
from opnsense.firewall.api.category import Category

def test_firewall_category_searchitem(api_config):
    base_url, key, secret = api_config
    api = Category(base_url, api_key=key, api_secret=secret)

    r = api.searchitem()
    data = r.json()

    assert "rows" in data
    assert "rowCount" in data
    assert "total" in data
    assert isinstance(data["rows"], list)
