from opnsense_python import OPNsenseClient, FirewallAPI


def test_list_rules(firewall):
    data = firewall.list_rules()
    assert "filter" in data

