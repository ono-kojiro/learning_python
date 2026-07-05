import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_comment(tmp_path):
    """
    specs/comment.yml が Composition Model として正しく変換され、
    work/specs/comment.json が正しい参照モデルになっていることを確認する。
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

    out = tmp_path / "comment.json"

    run(
        spec="../specs/comment.yml",
        output_file=str(out),
        input_files=specs,
    )

    assert out.exists(), "comment.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # comment_id
    assert "comment_id" in fields
    assert fields["comment_id"]["type"] == "CharField"
    assert fields["comment_id"]["unique"] is True
    assert fields["comment_id"]["max_length"] == 100

    # text
    assert "text" in fields
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500

    # Composition Model のため OneToMany は参照モデルに出ない
    assert "device" not in fields

