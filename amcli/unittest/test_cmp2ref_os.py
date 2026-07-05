import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_os(tmp_path):
    """
    specs/os.yml が Composition Model として正しく変換され、
    work/specs/os.json が正しい参照モデルになっていることを確認する。
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

    out = tmp_path / "os.json"

    run(
        spec="../specs/os.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "os.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # os_id
    # ------------------------------------------------------------
    assert "os_id" in fields
    assert fields["os_id"]["type"] == "CharField"
    assert fields["os_id"]["unique"] is True
    assert fields["os_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # text
    # ------------------------------------------------------------
    assert "text" in fields
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500

    # ------------------------------------------------------------
    # device (OneToOneField)
    # ------------------------------------------------------------
    assert "device" in fields
    assert fields["device"]["type"] == "OneToOneField"
    assert fields["device"]["to"] == "Device"
    assert fields["device"]["null"] is False
    assert fields["device"]["blank"] is False

