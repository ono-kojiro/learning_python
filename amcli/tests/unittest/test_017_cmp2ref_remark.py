# ------------------------------------------------------------
# Remark: remark_id
# ------------------------------------------------------------
def test_remark_id(remark_ref):
    fields = remark_ref["fields"]
    assert "remark_id" in fields
    assert fields["remark_id"]["type"] == "CharField"
    assert fields["remark_id"]["unique"] is True
    assert fields["remark_id"]["max_length"] == 100


# ------------------------------------------------------------
# Remark: text
# ------------------------------------------------------------
def test_remark_text(remark_ref):
    fields = remark_ref["fields"]
    assert "text" in fields
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500


# ------------------------------------------------------------
# Composition Model のため OneToMany は参照モデルに出ない
# ------------------------------------------------------------
def test_remark_no_device(remark_ref):
    fields = remark_ref["fields"]
    assert "device" not in fields
