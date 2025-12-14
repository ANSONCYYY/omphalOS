from __future__ import annotations

from pathlib import Path

from omphalos.core.determinism import verify_run_dir
from omphalos.core.pipeline import run_workbench
from omphalos.core.settings import load_run_config

from tests.helpers import with_output_root


def test_end_to_end_baseline(tmp_path: Path, repo_root: Path) -> None:
    cfg_path = repo_root / "config" / "runs" / "example_run.yaml"
    cfg = load_run_config(cfg_path)
    cfg = with_output_root(cfg, tmp_path / "runs")

    run_dir = run_workbench(cfg, config_path=str(cfg_path))
    assert (run_dir / "run_manifest.json").exists()
    rep = verify_run_dir(run_dir)
    assert rep["status"] == "PASS", rep
