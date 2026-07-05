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
    assert fields["name"]["max_length"] == 64
    assert fields["name"]["help_text"] == "Interface name (ex. eth0)"


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
