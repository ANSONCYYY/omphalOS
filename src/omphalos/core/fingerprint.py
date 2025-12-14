from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def canonical_json_dumps(obj: Any) -> bytes:
    """Canonical JSON encoding: stable ordering, stable separators, UTF-8."""
    txt = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return txt.encode("utf-8")


def sha256_json(obj: Any) -> str:
    return sha256_bytes(canonical_json_dumps(obj))


@dataclass(frozen=True)
class FingerprintedFile:
    path: str
    sha256: str
    bytes: int


def merkle_root(files: Iterable[FingerprintedFile]) -> str:
    """Stable root hash over (path, sha256, bytes) tuples."""
    items = sorted((f.path, f.sha256, f.bytes) for f in files)
    h = hashlib.sha256()
    for p, dig, size in items:
        h.update(p.encode("utf-8"))
        h.update(b"\0")
        h.update(dig.encode("ascii"))
        h.update(b"\0")
        h.update(str(size).encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()
