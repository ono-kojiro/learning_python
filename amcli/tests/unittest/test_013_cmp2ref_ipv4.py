# ------------------------------------------------------------
# IPv4: ipv4_id
# ------------------------------------------------------------
def test_ipv4_id(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "ipv4_id" in fields
    assert fields["ipv4_id"]["type"] == "CharField"
    assert fields["ipv4_id"]["unique"] is True
    assert fields["ipv4_id"]["max_length"] == 100


# ------------------------------------------------------------
# IPv4: method
# ------------------------------------------------------------
def test_ipv4_method(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "method" in fields
    assert fields["method"]["type"] == "CharField"
    assert fields["method"]["max_length"] == 16
    assert fields["method"]["default"] == "manual"


# ------------------------------------------------------------
# IPv4: addresses (JSONField)
# ------------------------------------------------------------
def test_ipv4_addresses(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "addresses" in fields
    addresses = fields["addresses"]

    assert addresses["type"] == "JSONField"
    assert "help_text" in addresses


# ------------------------------------------------------------
# IPv4: gateway
# ------------------------------------------------------------
def test_ipv4_gateway(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "gateway" in fields
    assert fields["gateway"]["type"] == "CharField"
    assert fields["gateway"]["max_length"] == 64


# ------------------------------------------------------------
# IPv4: dns (JSONField)
# ------------------------------------------------------------
def test_ipv4_dns(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "dns" in fields
    dns = fields["dns"]

    assert dns["type"] == "JSONField"
    assert "help_text" in dns


# ------------------------------------------------------------
# IPv4: netif (ForeignKey)
# ------------------------------------------------------------
def test_ipv4_netif_fk(ipv4_ref):
    fields = ipv4_ref["fields"]
    assert "netif" in fields

    netif = fields["netif"]
    assert netif["type"] == "ForeignKey"
    assert netif["to"] == "NetIF"
    assert netif["on_delete"] == "SET_NULL"
    assert netif["null"] is True
    assert netif["blank"] is True
