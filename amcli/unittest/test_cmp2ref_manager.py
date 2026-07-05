import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_manager(tmp_path):
    """
    specs/manager.yml が Composition Model として正しく変換され、
    work/specs/manager.json が正しい参照モデルになっていることを確認する。
    """

    specs = [
        "../specs/comment.yml",
        "../specs/device.yml",
        "../specs/ipv4.yml",
        "../specs/manager.yml",
        "../specs/netif.yml",
        "../specs/os.yml",
        "../specs/remark.yml",
    ]

    out = tmp_path / "manager.json"

    run(
        spec="../specs/manager.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "manager.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # manager_id
    # ------------------------------------------------------------
    assert "manager_id" in fields
    assert fields["manager_id"]["type"] == "CharField"
    assert fields["manager_id"]["unique"] is True
    assert fields["manager_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # name
    # ------------------------------------------------------------
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100

    # ------------------------------------------------------------
    # email
    # ------------------------------------------------------------
    assert "email" in fields
    assert fields["email"]["type"] == "CharField"
    assert fields["email"]["max_length"] == 255

    # ------------------------------------------------------------
    # device_ids (ManyToManyField)
    # ------------------------------------------------------------
    assert "device_ids" in fields
    assert fields["device_ids"]["type"] == "ManyToManyField"
    assert fields["device_ids"]["to"] == "Device"


