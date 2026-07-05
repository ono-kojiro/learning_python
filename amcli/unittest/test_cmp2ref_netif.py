import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_netif(tmp_path):
    """
    specs/netif.yml が Composition Model として正しく変換され、
    work/specs/netif.json が正しい参照モデルになっていることを確認する。
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

    out = tmp_path / "netif.json"

    run(
        spec="../specs/netif.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "netif.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # netif_id
    # ------------------------------------------------------------
    assert "netif_id" in fields
    assert fields["netif_id"]["type"] == "CharField"
    assert fields["netif_id"]["unique"] is True
    assert fields["netif_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # name
    # ------------------------------------------------------------
    assert "name" in fields
    assert fields["name"]["type"] == "CharField"
    assert fields["name"]["max_length"] == 64
    assert fields["name"]["help_text"] == "Interface name (ex. eth0)"

    # ------------------------------------------------------------
    # device (ForeignKey)
    # ------------------------------------------------------------
    assert "device" in fields
    assert fields["device"]["type"] == "ForeignKey"
    assert fields["device"]["to"] == "Device"
    assert fields["device"]["on_delete"] == "CASCADE"
    assert fields["device"]["max_length"] == 100

    # nullable / blank は specs/netif.yml に無いので出ないのが正しい
    assert "null" not in fields["device"]
    assert "blank" not in fields["device"]


