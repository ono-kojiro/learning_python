# test_011_cmp2ref_device.py
# Device の Reference Model の構造を検証する（新仕様対応）

def test_device_id(device_ref):
    fields = device_ref["fields"]
    assert "device_id" in fields
    assert fields["device_id"]["type"] == "CharField"
    assert fields["device_id"]["unique"] is True
    assert fields["device_id"]["max_length"] == 100


def test_device_name(device_ref):
    fields = device_ref["fields"]
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100


def test_device_serial_number(device_ref):
    fields = device_ref["fields"]
    assert "serial_number" in fields
    assert fields["serial_number"]["type"] == "CharField"
    assert fields["serial_number"]["max_length"] == 100


# ------------------------------------------------------------
# Device: comments (JSONField, owned children)
# ------------------------------------------------------------
def test_device_comments_jsonfield(device_ref):
    fields = device_ref["fields"]
    assert "comments" in fields

    comments = fields["comments"]
    assert comments["type"] == "JSONField"
    assert comments["help_text"] == "Owned children of Comment"


# ------------------------------------------------------------
# Device: remarks (JSONField, owned children)
# ------------------------------------------------------------
def test_device_remarks_jsonfield(device_ref):
    fields = device_ref["fields"]
    assert "remarks" in fields

    remarks = fields["remarks"]
    assert remarks["type"] == "JSONField"
    assert remarks["help_text"] == "Owned children of Remark"


# ------------------------------------------------------------
# Device: os (OneToOneField)
# ------------------------------------------------------------
def test_device_os_one_to_one(device_ref):
    fields = device_ref["fields"]
    assert "os" in fields

    osf = fields["os"]
    assert osf["type"] == "OneToOneField"
    assert osf["to"] == "OS"
    assert osf["null"] is False
    assert osf["blank"] is False


# ------------------------------------------------------------
# Device: manager_ids (ManyToManyField)
# ------------------------------------------------------------
def test_device_manager_ids_m2m(device_ref):
    fields = device_ref["fields"]
    assert "manager_ids" in fields

    m2m = fields["manager_ids"]
    assert m2m["type"] == "ManyToManyField"
    assert m2m["to"] == "Manager"
