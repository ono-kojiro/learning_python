# ------------------------------------------------------------
# Device: device_id
# ------------------------------------------------------------
def test_device_id(device_ref):
    fields = device_ref["fields"]
    assert "device_id" in fields
    assert fields["device_id"]["type"] == "CharField"
    assert fields["device_id"]["unique"] is True
    assert fields["device_id"]["max_length"] == 100


# ------------------------------------------------------------
# Device: name
# ------------------------------------------------------------
def test_device_name(device_ref):
    fields = device_ref["fields"]
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100


# ------------------------------------------------------------
# Device: serial_number
# ------------------------------------------------------------
def test_device_serial_number(device_ref):
    fields = device_ref["fields"]
    assert "serial_number" in fields
    assert fields["serial_number"]["type"] == "CharField"
    assert fields["serial_number"]["max_length"] == 100


# ------------------------------------------------------------
# Device: comment (ForeignKey)
# ------------------------------------------------------------
def test_device_comment_fk(device_ref):
    fields = device_ref["fields"]
    assert "comment" in fields
    comment = fields["comment"]

    assert comment["type"] == "ForeignKey"
    assert comment["to"] == "Comment"
    assert comment["on_delete"] == "SET_NULL"
    assert comment["null"] is True
    assert comment["blank"] is True


# ------------------------------------------------------------
# Device: remark (ForeignKey)
# ------------------------------------------------------------
def test_device_remark_fk(device_ref):
    fields = device_ref["fields"]
    assert "remark" in fields
    remark = fields["remark"]

    assert remark["type"] == "ForeignKey"
    assert remark["to"] == "Remark"
    assert remark["on_delete"] == "SET_NULL"
    assert remark["null"] is True
    assert remark["blank"] is True
