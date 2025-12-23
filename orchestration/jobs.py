from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from omphalos.core.settings import load_run_config
from omphalos.core.pipeline import run_workbench


@dataclass(frozen=True)
class Job:
    name: str
    config_path: Path

    def run(self) -> Path:
        cfg = load_run_config(self.config_path)
        return run_workbench(cfg, config_path=str(self.config_path))


def job_catalog() -> Dict[str, Job]:
    return {
        "example": Job(name="example", config_path=Path("config/runs/example_run.yaml")),
        "hermetic": Job(name="hermetic", config_path=Path("config/runs/hermetic_demo.yaml")),
    }
