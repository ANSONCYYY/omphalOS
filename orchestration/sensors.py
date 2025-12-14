from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Sensor:
    name: str
    path: Path

    def triggered(self) -> bool:
        return self.path.exists()
