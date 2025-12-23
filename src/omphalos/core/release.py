from __future__ import annotations

import io
import json
import tarfile
from pathlib import Path
from typing import Any, Dict, List

from .exceptions import ReleaseError
from .fingerprint import FingerprintedFile, merkle_root, sha256_bytes, sha256_file
from .io.fs import list_files, safe_relpath
from .time import deterministic_now_iso


def build_release_bundle(run_dir: Path, out_bundle: Path) -> Path:
    if not run_dir.is_dir():
        raise ReleaseError("run_dir must be a directory")
    out_bundle.parent.mkdir(parents=True, exist_ok=True)

    files: List[FingerprintedFile] = []
    for p in list_files(run_dir):
        if p.is_dir():
            continue
        rel = safe_relpath(p, run_dir)
        files.append(FingerprintedFile(rel, sha256_file(p), p.stat().st_size))
    files.sort(key=lambda f: f.path)
    root_hash = merkle_root(files)

    with tarfile.open(out_bundle, "w:gz") as tf:
        for f in files:
            abs_p = run_dir / f.path
            ti = tf.gettarinfo(str(abs_p), arcname=f.path)
            ti.mtime = 0
            with abs_p.open("rb") as fd:
                tf.addfile(ti, fileobj=fd)

        manifest = {
            "schema_version": "1.0",
            "created_at": deterministic_now_iso(root_hash, salt="release"),
            "run_id": run_dir.name,
            "bundle_sha256": "",
            "root_hash": root_hash,
            "files": [{"path": x.path, "sha256": x.sha256, "bytes": x.bytes} for x in files],
        }
        payload = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        ti = tarfile.TarInfo("release_manifest.json")
        ti.size = len(payload)
        ti.mtime = 0
        tf.addfile(ti, fileobj=io.BytesIO(payload))

    bundle_hash = sha256_file(out_bundle)
    manifest["bundle_sha256"] = bundle_hash

    manifest_path = out_bundle.with_suffix(out_bundle.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def verify_release_bundle(bundle: Path) -> Dict[str, Any]:
    if not bundle.is_file():
        raise ReleaseError("bundle must be a file")

    bundle_hash = sha256_file(bundle)
    manifest: Dict[str, Any] | None = None
    extracted: List[FingerprintedFile] = []

    with tarfile.open(bundle, "r:gz") as tf:
        for m in tf.getmembers():
            if m.name == "release_manifest.json":
                f = tf.extractfile(m)
                if f is None:
                    raise ReleaseError("missing release_manifest.json payload")
                manifest = json.loads(f.read().decode("utf-8"))
                continue
            if not m.isfile():
                continue
            f = tf.extractfile(m)
            if f is None:
                continue
            data = f.read()
            extracted.append(FingerprintedFile(m.name, sha256_bytes(data), len(data)))

    if manifest is None:
        return {"status": "FAIL", "error": "missing release_manifest.json"}

    root_hash = merkle_root(sorted(extracted, key=lambda x: x.path))
    status = "PASS"
    reasons: List[str] = []

    if manifest.get("bundle_sha256") != bundle_hash:
        status = "FAIL"
        reasons.append("bundle_sha256 mismatch")

    if manifest.get("root_hash") != root_hash:
        status = "FAIL"
        reasons.append("root_hash mismatch")

    expected = {f["path"]: f["sha256"] for f in manifest.get("files", [])}
    for f in extracted:
        if expected.get(f.path) != f.sha256:
            status = "FAIL"
            reasons.append(f"file hash mismatch: {f.path}")

    return {"status": status, "bundle_sha256": bundle_hash, "root_hash": root_hash, "reasons": reasons}
