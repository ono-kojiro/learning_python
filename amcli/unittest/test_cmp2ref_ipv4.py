import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_ipv4(tmp_path):
    """
    specs/ipv4.yml が Composition Model として正しく変換され、
    work/specs/ipv4.json が正しい参照モデルになっていることを確認する。
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

    out = tmp_path / "ipv4.json"

    run(
        spec="../specs/ipv4.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "ipv4.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # ipv4_id
    # ------------------------------------------------------------
    assert "ipv4_id" in fields
    assert fields["ipv4_id"]["type"] == "CharField"
    assert fields["ipv4_id"]["unique"] is True
    assert fields["ipv4_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # method
    # ------------------------------------------------------------
    assert "method" in fields
    assert fields["method"]["type"] == "CharField"
    assert fields["method"]["max_length"] == 16
    assert fields["method"]["default"] == "manual"

    # ------------------------------------------------------------
    # addresses (JSONField)
    # ------------------------------------------------------------
    assert "addresses" in fields
    assert fields["addresses"]["type"] == "JSONField"
    assert "help_text" in fields["addresses"]

    # ------------------------------------------------------------
    # gateway
    # ------------------------------------------------------------
    assert "gateway" in fields
    assert fields["gateway"]["type"] == "CharField"
    assert fields["gateway"]["max_length"] == 64

    # ------------------------------------------------------------
    # dns (JSONField)
    # ------------------------------------------------------------
    assert "dns" in fields
    assert fields["dns"]["type"] == "JSONField"
    assert "help_text" in fields["dns"]

    # ------------------------------------------------------------
    # netif (ForeignKey)
    # ------------------------------------------------------------
    assert "netif" in fields
    assert fields["netif"]["type"] == "ForeignKey"
    assert fields["netif"]["to"] == "NetIF"
    assert fields["netif"]["on_delete"] == "SET_NULL"
    assert fields["netif"]["null"] is True
    assert fields["netif"]["blank"] is True


