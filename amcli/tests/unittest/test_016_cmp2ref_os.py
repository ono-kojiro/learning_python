# ------------------------------------------------------------
# OS: os_id
# ------------------------------------------------------------
def test_os_id(os_ref):
    fields = os_ref["fields"]
    assert "os_id" in fields
    assert fields["os_id"]["type"] == "CharField"
    assert fields["os_id"]["unique"] is True
    assert fields["os_id"]["max_length"] == 100


# ------------------------------------------------------------
# OS: text
# ------------------------------------------------------------
def test_os_text(os_ref):
    fields = os_ref["fields"]
    assert "text" in fields
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500


# ------------------------------------------------------------
# OS: device (OneToOneField)
# ------------------------------------------------------------
def test_os_device_one_to_one(os_ref):
    fields = os_ref["fields"]
    assert "device" in fields

    device = fields["device"]
    assert device["type"] == "ForeignKey"
    assert device["to"] == "Device"
    #assert device["null"] is False
    #assert device["blank"] is False
