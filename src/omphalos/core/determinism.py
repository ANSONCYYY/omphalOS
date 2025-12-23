from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .contracts import validate_json_file
from .fingerprint import FingerprintedFile, merkle_root, sha256_file
from .io.fs import list_files, safe_relpath
from .time import deterministic_now_iso


def _load_manifest(run_dir: Path) -> Dict[str, Any]:
    p = run_dir / "run_manifest.json"
    validate_json_file(p, "run_manifest.schema.json")
    return json.loads(p.read_text(encoding="utf-8"))


def _expected_maps(manifest: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    payload = {f["path"]: f for f in manifest["artifacts"]["files"]}
    control = {f["path"]: f for f in manifest["artifacts"]["control_files"]}
    return payload, control


def _payload_fingerprints_from_disk(run_dir: Path, payload_spec: Dict[str, Dict[str, Any]]) -> List[FingerprintedFile]:
    fps: List[FingerprintedFile] = []
    for rel in sorted(payload_spec.keys()):
        p = run_dir / rel
        fps.append(FingerprintedFile(rel, sha256_file(p), p.stat().st_size))
    return fps


def verify_run_dir(run_dir: Path) -> Dict[str, Any]:
    try:
        manifest = _load_manifest(run_dir)
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

    payload_spec, control_spec = _expected_maps(manifest)
    mismatches: List[str] = []

    def _check_set(spec: Dict[str, Dict[str, Any]], label: str) -> None:
        for rel, meta in spec.items():
            p = run_dir / rel
            if not p.exists():
                mismatches.append(f"missing {label}: {rel}")
                continue
            actual_sha = sha256_file(p)
            if actual_sha != meta["sha256"]:
                mismatches.append(f"hash mismatch {label}: {rel}")
            actual_bytes = p.stat().st_size
            if int(actual_bytes) != int(meta["bytes"]):
                mismatches.append(f"size mismatch {label}: {rel}")

    _check_set(payload_spec, "payload")
    _check_set(control_spec, "control")

    try:
        fps = _payload_fingerprints_from_disk(run_dir, payload_spec)
        computed_payload_root = merkle_root(fps)
    except Exception as e:
        computed_payload_root = ""
        mismatches.append(f"payload root hash compute error: {e}")

    if computed_payload_root != manifest["artifacts"]["root_hash"]:
        mismatches.append("payload root_hash mismatch")

    expected_all = set(payload_spec.keys()) | set(control_spec.keys()) | {"run_manifest.json"}
    actual_all = set()
    for p in list_files(run_dir):
        if p.name == ".gitignore":
            continue
        rel = safe_relpath(p, run_dir)
        actual_all.add(rel)

    extras = sorted(actual_all - expected_all)
    if extras:
        mismatches.append("unexpected files: " + ", ".join(extras))

    return {
        "status": "PASS" if not mismatches else "FAIL",
        "mismatches": mismatches,
        "computed_payload_root_hash": computed_payload_root,
        "expected_payload_root_hash": manifest["artifacts"]["root_hash"],
    }


def certify_equivalence(run_a: Path, run_b: Path) -> Dict[str, Any]:
    a = _load_manifest(run_a)
    b = _load_manifest(run_b)

    a_root = a["artifacts"]["root_hash"]
    b_root = b["artifacts"]["root_hash"]
    status = "PASS" if a_root == b_root else "FAIL"

    a_payload, a_control = _expected_maps(a)
    b_payload, b_control = _expected_maps(b)

    control_diffs: List[Dict[str, Any]] = []
    all_control_paths = sorted(set(a_control.keys()) | set(b_control.keys()))
    for rel in all_control_paths:
        a_sha = a_control.get(rel, {}).get("sha256")
        b_sha = b_control.get(rel, {}).get("sha256")
        if a_sha != b_sha:
            control_diffs.append({"path": rel, "run_a": a_sha, "run_b": b_sha})

    payload_diffs: List[str] = []
    if status == "FAIL":
        all_payload_paths = sorted(set(a_payload.keys()) | set(b_payload.keys()))
        for rel in all_payload_paths:
            a_sha = a_payload.get(rel, {}).get("sha256")
            b_sha = b_payload.get(rel, {}).get("sha256")
            if a_sha != b_sha:
                payload_diffs.append(rel)

    return {
        "schema_version": "1.0",
        "created_at": deterministic_now_iso(a_root, salt=f"certify|{b_root}"),
        "status": status,
        "run_a": {"run_id": a["run_id"], "root_hash": a_root},
        "run_b": {"run_id": b["run_id"], "root_hash": b_root},
        "control_differences": control_diffs,
        "payload_paths_with_differences": payload_diffs,
    }
