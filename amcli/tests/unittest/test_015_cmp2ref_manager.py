# ------------------------------------------------------------
# Manager: manager_id
# ------------------------------------------------------------
def test_manager_id(manager_ref):
    fields = manager_ref["fields"]
    assert "manager_id" in fields
    assert fields["manager_id"]["type"] == "CharField"
    assert fields["manager_id"]["unique"] is True
    assert fields["manager_id"]["max_length"] == 100


# ------------------------------------------------------------
# Manager: name
# ------------------------------------------------------------
def test_manager_name(manager_ref):
    fields = manager_ref["fields"]
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100


# ------------------------------------------------------------
# Manager: email
# ------------------------------------------------------------
def test_manager_email(manager_ref):
    fields = manager_ref["fields"]
    assert "email" in fields
    assert fields["email"]["type"] == "CharField"
    assert fields["email"]["max_length"] == 255


# ------------------------------------------------------------
# Manager: device_ids (ManyToManyField)
# ------------------------------------------------------------
def test_manager_device_ids(manager_ref):
    fields = manager_ref["fields"]
    #assert "device_ids" in fields

    #device_ids = fields["device_ids"]
    #assert device_ids["type"] == "ManyToManyField"
    #assert device_ids["to"] == "Device"
