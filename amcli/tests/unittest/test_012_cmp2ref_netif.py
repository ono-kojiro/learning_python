# test_012_cmp2ref_netif.py
# NetIF の Reference Model の構造を検証する（新仕様対応）

# ------------------------------------------------------------
# NetIF: netif_id
# ------------------------------------------------------------
def test_netif_id(netif_ref):
    fields = netif_ref["fields"]
    assert "netif_id" in fields
    assert fields["netif_id"]["type"] == "CharField"
    assert fields["netif_id"]["unique"] is True
    assert fields["netif_id"]["max_length"] == 100


# ------------------------------------------------------------
# NetIF: name
# ------------------------------------------------------------
def test_netif_name(netif_ref):
    fields = netif_ref["fields"]
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100
    #assert fields["name"]["help_text"] == "Interface name (ex. eth0)"


# ------------------------------------------------------------
# NetIF: device (ForeignKey)
# ------------------------------------------------------------
def test_netif_device_fk(netif_ref):
    fields = netif_ref["fields"]
    assert "device" in fields

    device = fields["device"]
    assert device["type"] == "ForeignKey"
    assert device["to"] == "Device"
    assert device["on_delete"] == "CASCADE"
    assert device["max_length"] == 100

    # nullable / blank は specs/netif.yml に無いので出ないのが正しい
    assert "null" not in device
    assert "blank" not in device


# ------------------------------------------------------------
# NetIF: ipv4s (JSONField, owned children)
# ------------------------------------------------------------
def test_netif_ipv4s_jsonfield(netif_ref):
    fields = netif_ref["fields"]
    assert "ipv4s" in fields

    ipv4s = fields["ipv4s"]
    assert ipv4s["type"] == "JSONField"
    #assert ipv4s["help_text"] == "Owned children of IPv4"
