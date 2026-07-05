# ------------------------------------------------------------
# Comment: comment_id
# ------------------------------------------------------------
def test_comment_id(comment_ref):
    fields = comment_ref["fields"]
    assert "comment_id" in fields
    assert fields["comment_id"]["type"] == "CharField"
    assert fields["comment_id"]["unique"] is True
    assert fields["comment_id"]["max_length"] == 100


# ------------------------------------------------------------
# Comment: text
# ------------------------------------------------------------
def test_comment_text(comment_ref):
    fields = comment_ref["fields"]
    assert "text" in fields
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500


# ------------------------------------------------------------
# Composition Model のため OneToMany は参照モデルに出ない
# ------------------------------------------------------------
def test_comment_no_device(comment_ref):
    fields = comment_ref["fields"]
    assert "device" not in fields
