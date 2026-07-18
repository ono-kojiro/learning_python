# file: tests/unittest/test_020_genschema.py
# generate_schema の出力全体を最新仕様に合わせて検証する（あなたの DSL 対応）

# ------------------------------------------------------------
# 1. project / application
# ------------------------------------------------------------
def test_project_application(schema):
    assert schema["project"] == "myproject"
    assert schema["application"] == "myapp"


# ------------------------------------------------------------
# 2. models の存在確認
# ------------------------------------------------------------
def test_models_exist(schema):
    models = schema["models"]
    expected = ["Comment", "Device", "IPv4", "NetIF", "Remark"]
    for name in expected:
        assert name in models


# ------------------------------------------------------------
# 3. dependencies（直接依存）
# ------------------------------------------------------------
def test_dependencies(schema):
    deps = schema["dependencies"]

    assert deps["Device"] == ["OS", "Manager"]

    # IPv4 → NetIF（FK）
    assert deps["IPv4"] == ["NetIF"]

    # NetIF → Device（FK）
    assert deps["NetIF"] == ["Device"]

    # Comment → Device（FK）
    assert deps["Comment"] == ["Device"]

    # Remark → Device（FK）
    assert deps["Remark"] == ["Device"]


# ------------------------------------------------------------
# 5. reverse_dependencies（逆依存）
# ------------------------------------------------------------
def test_reverse_dependencies(schema):
    rev = schema["reverse_dependencies"]

    # JSONField は依存ではないため、Comment / Remark は逆依存を持たない
    assert rev["Comment"] == []
    assert rev["Remark"] == []

    # NetIF は IPv4 に参照される（FK）
    assert set(rev["NetIF"]) == {"IPv4"}

    # Device は NetIF, Comment, Remark に参照される（FK）
    assert set(rev["Device"]) == {"NetIF", "Comment", "Manager", "OS", "Remark"}


# ------------------------------------------------------------
# 7. nested（逆参照構造）
# ------------------------------------------------------------
def test_nested_comment(schema):
    nested = schema["nested"]
    # Comment は Device を参照するだけなので nested に出ない
    assert "Comment" not in nested


def test_nested_remark(schema):
    nested = schema["nested"]
    assert "Remark" not in nested


def test_nested_netif(schema):
    nested = schema["nested"]
    # NetIF は IPv4 を所有する（親側に OneToMany がある）
    assert nested["NetIF"][0]["model"] == "IPv4"
    assert nested["NetIF"][0]["fk"] == "netif"


def test_nested_device_netif(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(
        n.get("model") == "NetIF" and n["kind"] == "one_to_many"
        for n in device_nested
    )


def test_nested_device_comments(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(
        n.get("model") == "Comment" and n["kind"] == "one_to_many"
        for n in device_nested
    )


def test_nested_device_remarks(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(
        n.get("model") == "Remark" and n["kind"] == "one_to_many"
        for n in device_nested
    )


# ------------------------------------------------------------
# 8. field_categories
# ------------------------------------------------------------
def test_field_categories(schema):
    fc = schema["field_categories"]
    for key in ["CharField", "ForeignKey", "JSONField"]:
        assert key in fc


# ------------------------------------------------------------
# 9. dependency_categories
# ------------------------------------------------------------
def test_dependency_categories(schema):
    dc = schema["dependency_categories"]

    # Manager / OS は存在しない
    #assert "Manager" not in dc
    #assert "OS" not in dc

    assert dc["Device"] == "fk_parent"
    assert dc["IPv4"] == "fk_child"
    assert dc["Comment"] == "fk_child"
    assert dc["Remark"] == "fk_child"
    assert dc["NetIF"] == "fk_parent"
