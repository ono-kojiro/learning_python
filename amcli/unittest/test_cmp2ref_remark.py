import json
from pathlib import Path
from amcli.commands.cmp2ref import run

def test_cmp2ref_remark(tmp_path):
    """
    specs/remark.yml がコンポジションモデルとして正しく変換され、
    work/specs/remark.json が正しい参照モデルになっていることを確認する。
    """

    # 入力となる specs/*.yml
    specs = [
        "../specs/comment.yml",
        "../specs/device.yml",
        "../specs/ipv4.yml",
        "../specs/manager.yml",
        "../specs/netif.yml",
        "../specs/os.yml",
        "../specs/remark.yml",
    ]

    # 出力先
    out = tmp_path / "remark.json"

    # cmp2ref 実行
    run(
        spec="../specs/remark.yml",
        output_file=str(out),
        input_files=specs,
    )

    # JSON が生成されていること
    assert out.exists(), "remark.json が生成されていません"

    # JSON 内容を読み込み
    with open(out, "r", encoding="utf-8") as f:
        data = json.load(f)

    fields = data["fields"]

    # ------------------------------------------------------------
    # 1. remark_id が正しく CharField(unique=True) になっている
    # ------------------------------------------------------------
    assert "remark_id" in fields, "remark_id フィールドが存在しません"
    assert fields["remark_id"]["type"] == "CharField"
    assert fields["remark_id"]["unique"] is True
    assert fields["remark_id"]["max_length"] == 100

    # ------------------------------------------------------------
    # 2. text が正しく CharField(max_length=500) になっている
    # ------------------------------------------------------------
    assert "text" in fields, "text フィールドが存在しません"
    assert fields["text"]["type"] == "CharField"
    assert fields["text"]["max_length"] == 500

    # ------------------------------------------------------------
    # 3. device(OneToMany) は参照モデルには出ない（Composition Model の仕様）
    # ------------------------------------------------------------
    assert "device" not in fields, "OneToMany の device が参照モデルに出ています（誤り）"

