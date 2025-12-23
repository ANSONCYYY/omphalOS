from __future__ import annotations

import json
from pathlib import Path

import yaml

from omphalos.core.quality import evaluate


def test_quality_engine_schema_and_csv_checks(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    (run_dir / "exports" / "packets").mkdir(parents=True)
    (run_dir / "exports" / "briefing_tables").mkdir(parents=True)
    (run_dir / "reports").mkdir(parents=True)

    packet = {"schema_version": "1.0", "run_id": "run-x", "packet_id": "p", "created_at": "2000-01-01T00:00:00Z",
              "claim": "c", "entity": {"entity_id": "e", "entity_name": "n", "country": "X", "chokepoint_score": 0.1,
              "shipment_count": 1, "total_value_usd": 1.0}, "evidence": [], "lineage": [], "review": {"status": "CLEAR", "reason": "r"},
              "hashes": {"packet": "0" * 64}}
    (run_dir / "exports" / "packets" / "packet.json").write_text(json.dumps(packet), encoding="utf-8")

    (run_dir / "exports" / "briefing_tables" / "table.csv").write_text("a,b\n1,2\n", encoding="utf-8")

    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        json.dumps({"type": "object", "required": ["schema_version", "run_id"], "properties": {"schema_version": {"type": "string"}, "run_id": {"type": "string"}}}),
        encoding="utf-8",
    )

    rules = {
        "version": "1.0",
        "checks": [
            {
                "name": "pkt_schema",
                "kind": "schema_validate_glob",
                "params": {"glob": "exports/packets/*.json", "schema": str(schema_path)},
                "severity": "HIGH",
                "message": "ok",
            },
            {
                "name": "csv_min",
                "kind": "csv_row_count_min",
                "params": {"glob": "exports/briefing_tables/*.csv", "min_rows": 2},
                "severity": "MEDIUM",
                "message": "ok",
            },
        ],
    }
    rules_path = tmp_path / "rules.yaml"
    rules_path.write_text(yaml.safe_dump(rules, sort_keys=False), encoding="utf-8")

    rep = evaluate([rules_path], run_dir, metrics={}, clock_seed="seed", run_id="run-x")
    assert rep["status"] == "PASS"
