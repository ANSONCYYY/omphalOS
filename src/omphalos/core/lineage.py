from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

from .fingerprint import sha256_json
from .time import deterministic_now_iso


@dataclass(frozen=True)
class LineageEvent:
    schema_version: str
    run_id: str
    event_id: str
    created_at: str
    kind: str
    inputs: Sequence[str]
    outputs: Sequence[str]
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "event_id": self.event_id,
            "created_at": self.created_at,
            "kind": self.kind,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "details": dict(self.details),
        }

    @staticmethod
    def create(run_id: str, kind: str, inputs: Sequence[str], outputs: Sequence[str], details: Dict[str, Any], clock_seed: str) -> "LineageEvent":
        payload = {
            "schema_version": "1.0",
            "run_id": run_id,
            "kind": kind,
            "inputs": list(inputs),
            "outputs": list(outputs),
            "details": details,
        }
        event_id = "ev-" + sha256_json(payload)[:16]
        created_at = deterministic_now_iso(clock_seed, salt=f"lineage:{event_id}")
        return LineageEvent(
            schema_version="1.0",
            run_id=run_id,
            event_id=event_id,
            created_at=created_at,
            kind=kind,
            inputs=list(inputs),
            outputs=list(outputs),
            details=details,
        )


def write_lineage(events: Iterable[LineageEvent], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e.to_dict(), sort_keys=True) + "\n")
