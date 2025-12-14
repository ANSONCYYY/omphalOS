from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Schedule:
    name: str
    cron: str
    job: str


def schedules() -> Dict[str, Schedule]:
    return {"nightly_example": Schedule(name="nightly_example", cron="0 3 * * *", job="example")}
