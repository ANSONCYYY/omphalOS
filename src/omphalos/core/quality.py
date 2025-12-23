from __future__ import annotations

import csv
import glob
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .contracts import load_json_schema, validate_json_against_schema
from .exceptions import GateError
from .time import deterministic_now_iso


def _load_schema_ref(schema_ref: str) -> Dict[str, Any]:
    """Load a schema by filename (from contracts/schemas) or by repo-relative path."""
    if "/" not in schema_ref and "\\" not in schema_ref:
        return load_json_schema(schema_ref)
    p = Path(schema_ref)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[3] / p
    return json.loads(p.read_text(encoding="utf-8"))


def _cmp(lhs: float, op: str, rhs: float) -> bool:
    if op == ">=":
        return lhs >= rhs
    if op == "<=":
        return lhs <= rhs
    if op == ">":
        return lhs > rhs
    if op == "<":
        return lhs < rhs
    if op == "==":
        return lhs == rhs
    raise ValueError(f"unsupported op: {op}")


def evaluate(rule_paths: List[Path], run_dir: Path, metrics: Dict[str, float], clock_seed: str, run_id: str) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    for rp in rule_paths:
        spec = yaml.safe_load(rp.read_text(encoding="utf-8")) or {}
        for chk in spec.get("checks", []):
            kind = chk["kind"]
            name = chk["name"]
            sev = chk["severity"]
            msg = chk["message"]
            params = chk.get("params", {})
            status = "PASS"
            details: Dict[str, Any] = {}

            if kind == "file_count_min":
                total = 0
                counts: Dict[str, int] = {}
                for g in params["globs"]:
                    matches = glob.glob(str(run_dir / g))
                    counts[g] = len(matches)
                    total += len(matches)
                if total < int(params["min"]):
                    status = "FAIL"
                details = {"counts": counts, "min": int(params["min"])}
            elif kind == "metric_threshold":
                metric = params["metric"]
                op = params["op"]
                threshold = float(params["value"])
                actual = float(metrics.get(metric, 0.0))
                if not _cmp(actual, op, threshold):
                    status = "FAIL"
                details = {"metric": metric, "op": op, "value": threshold, "actual": actual}
            elif kind == "schema_validate_glob":
                g = str(run_dir / str(params["glob"]))
                matches = sorted(glob.glob(g))
                schema = _load_schema_ref(str(params["schema"]))
                failures: List[Dict[str, Any]] = []
                for mp in matches:
                    p = Path(mp)
                    try:
                        data = json.loads(p.read_text(encoding="utf-8"))
                        validate_json_against_schema(data, schema)
                    except Exception as e:
                        failures.append({"path": p.relative_to(run_dir).as_posix(), "error": str(e)})
                if not matches:
                    status = "FAIL"
                if failures:
                    status = "FAIL"
                details = {"glob": params["glob"], "count": len(matches), "failures": failures}
            elif kind == "json_field_equals":
                rel = str(params["path"])
                field = str(params["field"])
                expected = params["value"]
                p = run_dir / rel
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    actual = data.get(field)
                    if actual != expected:
                        status = "FAIL"
                    details = {"path": rel, "field": field, "expected": expected, "actual": actual}
                except Exception as e:
                    status = "FAIL"
                    details = {"path": rel, "error": str(e)}
            elif kind == "csv_row_count_min":
                g = str(run_dir / str(params["glob"]))
                matches = sorted(glob.glob(g))
                min_rows = int(params["min_rows"])
                counts: Dict[str, int] = {}
                for mp in matches:
                    p = Path(mp)
                    try:
                        with p.open("r", encoding="utf-8", newline="") as f:
                            reader = csv.reader(f)
                            _ = next(reader, None)  # header
                            rows = sum(1 for _ in reader)
                        counts[p.relative_to(run_dir).as_posix()] = rows
                    except Exception:
                        counts[p.relative_to(run_dir).as_posix()] = -1
                if not matches:
                    status = "FAIL"
                if any(v < (min_rows - 1) for v in counts.values()):
                    status = "FAIL"
                details = {"glob": params["glob"], "min_rows": min_rows, "row_counts": counts}
            else:
                status = "WARN"
                details = {"unknown_kind": kind}

            checks.append({"name": name, "status": status, "severity": sev, "message": msg, "details": details})

    overall = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": deterministic_now_iso(clock_seed, salt="quality"),
        "status": overall,
        "checks": checks,
    }


def enforce(report: Dict[str, Any]) -> None:
    if report["status"] != "PASS":
        raise GateError("quality gate failed")
