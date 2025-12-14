from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .artifacts import ArtifactStore
from .contracts import load_json_schema, validate_json_against_schema
from .fingerprint import sha256_file
from .lineage import write_lineage
from .logging import make_logger
from .publishability import scan_path
from .quality import enforce, evaluate
from .sbom import generate_sbom_manifest
from .packs import effective_publishability_rules, effective_quality_rules, load_pack
from .settings import RunConfig, fingerprint_payload
from .time import deterministic_now_iso
from ..reference.pipeline import run_reference_pipeline

_MANIFEST_RELPATH = "run_manifest.json"

# Files that carry environment details or depend on the payload root hash. They are recorded
# in the manifest but excluded from the payload root hash.
_LOG_RELPATH = "logs/run.jsonl"
_QUALITY_RELPATH = "reports/quality_report.json"
_DETERMINISM_RELPATH = "reports/determinism_report.json"
_PUBLISHABILITY_RELPATH = "reports/publishability_report.json"
_SBOM_RELPATH = "reports/sbom_manifest.json"

_CONTROL_RELPATHS: List[str] = [_LOG_RELPATH, _QUALITY_RELPATH, _DETERMINISM_RELPATH, _PUBLISHABILITY_RELPATH, _SBOM_RELPATH]


def _make_run_id(cfg_fp: str) -> str:
    return f"run-{cfg_fp[:8]}-{cfg_fp[8:12]}"


def _file_record(run_dir: Path, relpath: str) -> Dict[str, Any]:
    p = run_dir / relpath
    return {"path": relpath, "sha256": sha256_file(p), "bytes": p.stat().st_size}


def run_workbench(cfg: RunConfig, config_path: Optional[str] = None) -> Path:
    cfg_fp = cfg.fingerprint()
    run_id = _make_run_id(cfg_fp)

    run_dir = Path(cfg.run.output_root) / run_id
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"run_dir already exists and is non-empty: {run_dir}")

    store = ArtifactStore(run_dir)
    logger = make_logger(run_dir, cfg_fp)
    logger.log("INFO", "run_start", run_id=run_id)

    results = run_reference_pipeline(cfg=cfg, run_dir=run_dir, clock_seed=cfg_fp, logger=logger, run_id=run_id)

    pack = load_pack(cfg.rules.pack)
    metrics = results["metrics"]
    quality_rule_paths = effective_quality_rules(pack=pack, extra_paths=cfg.rules.paths)
    publishability_rule_paths = effective_publishability_rules(pack=pack, extra_paths=[])

    lineage_path = run_dir / "lineage" / "lineage.jsonl"
    write_lineage(results["lineage_events"], lineage_path)

    # Compute the payload root hash. Control artifacts and the manifest itself are excluded.
    payload_exclude = [_MANIFEST_RELPATH, "logs/"] + list(_CONTROL_RELPATHS)
    payload_idx = store.index(exclude=payload_exclude)
    payload_root_hash = payload_idx.root_hash

    det_rep = {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": deterministic_now_iso(payload_root_hash, salt="determinism"),
        "status": "PASS",
        "fingerprints": {
            "config": cfg_fp,
            "inputs": {i["name"]: i["fingerprint"] for i in results["inputs_index"]},
            "exports": results["exports_fingerprints"],
            "root": payload_root_hash,
        },
    }
    validate_json_against_schema(det_rep, load_json_schema("determinism_report.schema.json"))
    store.write_text(_DETERMINISM_RELPATH, json.dumps(det_rep, indent=2, sort_keys=True) + "\n")

    pub_rep = scan_path(run_dir, rule_paths=publishability_rule_paths)
    validate_json_against_schema(pub_rep, load_json_schema("publishability_report.schema.json"))
    store.write_text(_PUBLISHABILITY_RELPATH, json.dumps(pub_rep, indent=2, sort_keys=True) + "\n")

    sb_rep = generate_sbom_manifest()
    validate_json_against_schema(sb_rep, load_json_schema("sbom_manifest.schema.json"))
    store.write_text(_SBOM_RELPATH, json.dumps(sb_rep, indent=2, sort_keys=True) + "\n")

    qrep = evaluate(quality_rule_paths, run_dir, metrics, cfg_fp, run_id)
    validate_json_against_schema(qrep, load_json_schema("quality_report.schema.json"))
    store.write_text(_QUALITY_RELPATH, json.dumps(qrep, indent=2, sort_keys=True) + "\n")
    enforce(qrep)

    logger.log("INFO", "run_complete", run_id=run_id, payload_root_hash=payload_root_hash)

    control_files = sorted([_file_record(run_dir, p) for p in _CONTROL_RELPATHS], key=lambda x: x["path"])

    cfg_block: Dict[str, Any] = {"fingerprint": cfg_fp, "payload": fingerprint_payload(cfg)}
    if config_path:
        try:
            cp = Path(config_path)
            if cp.exists() and cp.is_file():
                cfg_block["source"] = {"name": cp.name, "sha256": sha256_file(cp)}
        except OSError:
            pass

    manifest: Dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": deterministic_now_iso(payload_root_hash, salt="manifest"),
        "config": cfg_block,
        "inputs": results["inputs_index"],
        "artifacts": {
            "root_hash": payload_root_hash,
            "files": [{"path": f.path, "sha256": f.sha256, "bytes": f.bytes} for f in payload_idx.files],
            "control_files": control_files,
        },
        "reports": {
            "quality": "reports/quality_report.json",
            "determinism": "reports/determinism_report.json",
            "publishability": "reports/publishability_report.json",
            "sbom": "reports/sbom_manifest.json",
        },
        "lineage": store.rel(lineage_path),
        "warehouse": store.rel(results["warehouse_path"]),
        "exports": results["exports_paths"],
    }

    schema = load_json_schema("run_manifest.schema.json")
    validate_json_against_schema(manifest, schema)
    store.write_text(_MANIFEST_RELPATH, json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    return run_dir
