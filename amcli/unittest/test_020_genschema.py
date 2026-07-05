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
    expected = ["Comment", "Device", "IPv4", "Manager", "NetIF", "OS", "Remark"]
    for name in expected:
        assert name in models


# ------------------------------------------------------------
# 3. dependencies（直接依存）
# ------------------------------------------------------------
def test_dependencies(schema):
    deps = schema["dependencies"]
    assert deps["Device"] == ["Comment", "Remark"]
    assert deps["IPv4"] == ["NetIF"]
    assert deps["Manager"] == ["Device"]
    assert deps["NetIF"] == ["Device"]
    assert deps["OS"] == ["Device"]
    assert deps["Comment"] == []
    assert deps["Remark"] == []


# ------------------------------------------------------------
# 4. all_dependencies（全依存）
# ------------------------------------------------------------
def test_all_dependencies(schema):
    all_deps = schema["all_dependencies"]

    assert set(all_deps["Device"]) == {"Remark", "Comment"}
    assert set(all_deps["Manager"]) == {"Device", "Remark", "Comment"}
    assert set(all_deps["NetIF"]) == {"Device", "Remark", "Comment"}
    assert set(all_deps["OS"]) == {"Device", "Remark", "Comment"}
    assert set(all_deps["IPv4"]) == {"Device", "Remark", "Comment", "NetIF"}


# ------------------------------------------------------------
# 5. reverse_dependencies（逆依存）
# ------------------------------------------------------------
def test_reverse_dependencies(schema):
    rev = schema["reverse_dependencies"]
    assert rev["Comment"] == ["Device"]
    assert rev["Remark"] == ["Device"]
    assert rev["NetIF"] == ["IPv4"]
    assert rev["Device"] == ["Manager", "NetIF", "OS"]


# ------------------------------------------------------------
# 6. load_order（依存順序）
# ------------------------------------------------------------
def test_load_order(schema):
    assert schema["load_order"] == [
        "Device",
        "Comment",
        "Remark",
        "Manager",
        "NetIF",
        "OS",
        "IPv4",
    ]


# ------------------------------------------------------------
# 7. nested（逆参照構造）
# ------------------------------------------------------------
def test_nested_comment(schema):
    nested = schema["nested"]
    assert nested["Comment"][0]["model"] == "Device"
    assert nested["Comment"][0]["fk"] == "comment"


def test_nested_remark(schema):
    nested = schema["nested"]
    assert nested["Remark"][0]["model"] == "Device"
    assert nested["Remark"][0]["fk"] == "remark"


def test_nested_netif(schema):
    nested = schema["nested"]
    assert nested["NetIF"][0]["model"] == "IPv4"
    assert nested["NetIF"][0]["fk"] == "netif"


def test_nested_device_many_to_many(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(n["kind"] == "many_to_many" for n in device_nested)


def test_nested_device_netif(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(
        n.get("model") == "NetIF" and n["kind"] == "one_to_many"
        for n in device_nested
    )


def test_nested_device_os(schema):
    nested = schema["nested"]
    device_nested = nested["Device"]
    assert any(
        n.get("model") == "OS" and n["kind"] == "one_to_one"
        for n in device_nested
    )


# ------------------------------------------------------------
# 8. field_categories
# ------------------------------------------------------------
def test_field_categories(schema):
    fc = schema["field_categories"]
    for key in ["CharField", "ForeignKey", "JSONField", "ManyToManyField", "OneToOneField"]:
        assert key in fc


# ------------------------------------------------------------
# 9. dependency_categories
# ------------------------------------------------------------
def test_dependency_categories(schema):
    dc = schema["dependency_categories"]
    assert dc["Manager"] == "m2m_owner"
    assert dc["Device"] == "fk_child"
    assert dc["IPv4"] == "fk_child"
    assert dc["Comment"] == "fk_parent"
    assert dc["Remark"] == "fk_parent"
    assert dc["NetIF"] == "fk_child"
    assert dc["OS"] == "fk_child"
