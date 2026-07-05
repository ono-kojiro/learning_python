import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_device(tmp_path):
    """
    specs/device.yml が Composition Model として正しく変換され、
    work/specs/device.json が正しい参照モデルになっていることを確認する。
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

    out = tmp_path / "device.json"

    run(
        spec="../specs/device.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "device.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # device_id
    # ------------------------------------------------------------
    assert "device_id" in fields
    assert fields["device_id"]["type"] == "CharField"
    assert fields["device_id"]["unique"] is True
    assert fields["device_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # name
    # ------------------------------------------------------------
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 100

    # ------------------------------------------------------------
    # serial_number
    # ------------------------------------------------------------
    assert "serial_number" in fields
    assert fields["serial_number"]["type"] == "CharField"
    assert fields["serial_number"]["max_length"] == 100

    # ------------------------------------------------------------
    # comment（ForeignKey）
    # ------------------------------------------------------------
    assert "comment" in fields
    assert fields["comment"]["type"] == "ForeignKey"
    assert fields["comment"]["to"] == "Comment"
    assert fields["comment"]["on_delete"] == "SET_NULL"
    assert fields["comment"]["null"] is True
    assert fields["comment"]["blank"] is True

    # ------------------------------------------------------------
    # remark（ForeignKey）
    # ------------------------------------------------------------
    assert "remark" in fields
    assert fields["remark"]["type"] == "ForeignKey"
    assert fields["remark"]["to"] == "Remark"
    assert fields["remark"]["on_delete"] == "SET_NULL"
    assert fields["remark"]["null"] is True
    assert fields["remark"]["blank"] is True

