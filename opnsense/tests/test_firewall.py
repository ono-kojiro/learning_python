import json
from opnsense.firewall import Firewall


def test_firewall_category_searchitem(client):
    api = Firewall(client)
    data = api.search_category()

    assert "rows" in data
    assert "rowCount" in data
    assert "total" in data
    assert isinstance(data["rows"], list)
