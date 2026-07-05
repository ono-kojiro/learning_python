import json
import pytest
from pathlib import Path

# 別名を付けて競合を防ぐ
from amcli.commands.cmp2ref import run as run_cmp2ref
from amcli.commands.generate_schema import run as run_genschema

spec_dir = "../../specs"

# ------------------------------------------------------------
# 共通：cmp2ref の specs 一覧
# ------------------------------------------------------------
@pytest.fixture
def cmp2ref_specs():
    return [
        f"{spec_dir}/comment.yml",
        f"{spec_dir}/device.yml",
        f"{spec_dir}/ipv4.yml",
        f"{spec_dir}/manager.yml",
        f"{spec_dir}/netif.yml",
        f"{spec_dir}/os.yml",
        f"{spec_dir}/remark.yml",
    ]


# ------------------------------------------------------------
# 共通：cmp2ref で参照モデル JSON を生成する fixture
# ------------------------------------------------------------
@pytest.fixture
def device_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "device.json"

    run_cmp2ref(
        spec=f"{spec_dir}/device.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "device.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def netif_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "netif.json"

    run_cmp2ref(
        spec=f"{spec_dir}/netif.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "netif.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def ipv4_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "ipv4.json"

    run_cmp2ref(
        spec=f"{spec_dir}/ipv4.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "ipv4.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def comment_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "comment.json"

    run_cmp2ref(
        spec=f"{spec_dir}/comment.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "comment.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def manager_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "manager.json"

    run_cmp2ref(
        spec=f"{spec_dir}/manager.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "manager.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def os_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "os.json"

    run_cmp2ref(
        spec=f"{spec_dir}/os.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "os.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def remark_ref(tmp_path, cmp2ref_specs):
    out = tmp_path / "remark.json"

    run_cmp2ref(
        spec=f"{spec_dir}/remark.yml",
        output_file=str(out),
        input_files=cmp2ref_specs,
    )

    assert out.exists(), "remark.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------------------------------------------
# 共通：specs の一覧
# ------------------------------------------------------------
@pytest.fixture
def specs():
    return [
        "../../work/specs/comment.json",
        "../../work/specs/device.json",
        "../../work/specs/ipv4.json",
        "../../work/specs/manager.json",
        "../../work/specs/netif.json",
        "../../work/specs/os.json",
        "../../work/specs/remark.json",
    ]


# ------------------------------------------------------------
# 共通：schema.json を生成して読み込む fixture
# ------------------------------------------------------------
@pytest.fixture
def schema(tmp_path, specs):
    out = tmp_path / "schema.json"

    run_genschema(
        output_file=str(out),
        project="myproject",
        application="myapp",
        input_files=specs,
    )

    assert out.exists(), "schema.json が生成されていません"

    with open(out, "r", encoding="utf-8") as f:
        return json.load(f)


