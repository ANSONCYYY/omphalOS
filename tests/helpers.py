from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from omphalos.core.settings import RunConfig


def with_output_root(cfg: RunConfig, output_root: Path) -> RunConfig:
    """Return a config with a different output_root while preserving stable identity."""
    return replace(cfg, run=replace(cfg.run, output_root=str(output_root)))
