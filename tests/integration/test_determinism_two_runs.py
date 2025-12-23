from __future__ import annotations

from pathlib import Path

from omphalos.core.determinism import certify_equivalence, verify_run_dir
from omphalos.core.pipeline import run_workbench
from omphalos.core.settings import load_run_config

from tests.helpers import with_output_root


def test_two_runs_equivalent_across_output_roots(tmp_path: Path, repo_root: Path) -> None:
    cfg_path = repo_root / "config" / "runs" / "example_run.yaml"
    cfg = load_run_config(cfg_path)

    run_dir_a = run_workbench(with_output_root(cfg, tmp_path / "runa"), config_path=str(cfg_path))
    run_dir_b = run_workbench(with_output_root(cfg, tmp_path / "runb"), config_path=str(cfg_path))

    assert verify_run_dir(run_dir_a)["status"] == "PASS"
    assert verify_run_dir(run_dir_b)["status"] == "PASS"

    cert = certify_equivalence(run_dir_a, run_dir_b)
    assert cert["status"] == "PASS", cert
