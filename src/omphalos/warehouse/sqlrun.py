from __future__ import annotations

import csv
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping

import yaml


@dataclass(frozen=True)
class QuerySpec:
    name: str
    path: str
    params: Mapping[str, Any]


@dataclass(frozen=True)
class Manifest:
    name: str
    database: str
    queries: List[QuerySpec]


def load_manifest(path: Path) -> Manifest:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    qs: List[QuerySpec] = []
    for q in raw.get("queries", []):
        qs.append(QuerySpec(name=str(q["name"]), path=str(q["path"]), params=dict(q.get("params", {}))))
    return Manifest(name=str(raw["name"]), database=str(raw["database"]), queries=qs)


def _rows_to_csv(path: Path, cols: List[str], rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c) for c in cols})


def run_manifest(run_dir: Path, manifest_path: Path, out_rel: str = "exports/sql") -> List[Dict[str, Any]]:
    m = load_manifest(manifest_path)
    db_path = run_dir / m.database
    out_dir = run_dir / out_rel / m.name
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    results: List[Dict[str, Any]] = []
    try:
        for q in m.queries:
            sql_text = (run_dir / q.path).read_text(encoding="utf-8") if (run_dir / q.path).exists() else (Path(q.path).read_text(encoding="utf-8"))
            cur = conn.execute(sql_text, dict(q.params))
            fetched = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = [dict(r) for r in fetched]
            out_csv = out_dir / f"{q.name}.csv"
            out_json = out_dir / f"{q.name}.json"
            _rows_to_csv(out_csv, cols, rows)
            out_json.write_text(json.dumps({"columns": cols, "rows": rows}, indent=2, sort_keys=False) + "\n", encoding="utf-8")
            results.append({"name": q.name, "rows": len(rows), "csv": str(out_csv.relative_to(run_dir)), "json": str(out_json.relative_to(run_dir))})
    finally:
        conn.close()
    (out_dir / "manifest_results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results
