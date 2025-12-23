from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, List


_COLUMNS = ["entity_id", "entity_name", "country", "shipment_count", "total_value_usd", "chokepoint_score"]


def write_briefing_table_entities(run_dir: Path, entity_scores: List[dict[str, Any]]) -> List[str]:
    out_rel = "exports/briefing_tables/briefing_table_entities.csv"
    out_path = run_dir / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [{k: r.get(k) for k in _COLUMNS} for r in entity_scores]
    rows.sort(key=lambda r: (-float(r["chokepoint_score"]), str(r["entity_id"])))

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=_COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    return [out_rel]
