from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .redaction import redact_fields
from .time import deterministic_now_iso


@dataclass
class Logger:
    path: Path
    clock_seed: str

    def log(self, level: str, msg: str, **fields: Any) -> None:
        rec: Dict[str, Any] = {
            "ts": deterministic_now_iso(self.clock_seed, salt=f"log:{level}:{msg}"),
            "level": level,
            "msg": msg,
        }
        rec.update(redact_fields(fields, keys=["token", "secret", "api_key", "password"]))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")


def make_logger(run_dir: Path, clock_seed: str) -> Logger:
    return Logger(path=run_dir / "logs" / "run.jsonl", clock_seed=clock_seed)
