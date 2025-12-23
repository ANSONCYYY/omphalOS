from __future__ import annotations

import json
from pathlib import Path

from omphalos.core.pipeline import run_workbench
from omphalos.core.settings import load_run_config

from tests.helpers import with_output_root


def _root_hash(run_dir: Path) -> str:
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    return str(manifest["artifacts"]["root_hash"])


def test_golden_payload_root_hashes(tmp_path: Path, repo_root: Path) -> None:
    expected = json.loads((repo_root / "tests" / "golden" / "expected_roots.json").read_text(encoding="utf-8"))

    base_cfg_path = repo_root / "config" / "runs" / "example_run.yaml"
    base_cfg = with_output_root(load_run_config(base_cfg_path), tmp_path / "base")
    base_run = run_workbench(base_cfg, config_path=str(base_cfg_path))
    assert _root_hash(base_run) == expected["baseline_example_run"]

    strict_cfg_path = repo_root / "config" / "runs" / "strict_demo.yaml"
    strict_cfg = with_output_root(load_run_config(strict_cfg_path), tmp_path / "strict")
    strict_run = run_workbench(strict_cfg, config_path=str(strict_cfg_path))
    assert _root_hash(strict_run) == expected["strict_demo"]
