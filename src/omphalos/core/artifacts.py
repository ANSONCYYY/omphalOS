from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .exceptions import ArtifactError
from .fingerprint import FingerprintedFile, merkle_root, sha256_file
from .io.fs import list_files, safe_relpath


@dataclass
class ArtifactIndex:
    files: List[FingerprintedFile]
    root_hash: str


class ArtifactStore:
    """Write-once store rooted at a run directory."""

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def write_bytes(self, relpath: str, data: bytes) -> Path:
        p = self.run_dir / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_write(p, data)
        return p

    def write_text(self, relpath: str, text: str) -> Path:
        return self.write_bytes(relpath, text.encode("utf-8"))

    def _atomic_write(self, path: Path, data: bytes) -> None:
        try:
            fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
            os.close(fd)
            tmp_path = Path(tmp)
            tmp_path.write_bytes(data)
            tmp_path.replace(path)
        except Exception as e:
            raise ArtifactError(f"failed to write artifact: {path}") from e

    def index(self, root_subdir: Optional[Path] = None, exclude: Optional[List[str]] = None) -> ArtifactIndex:
        root = (self.run_dir / root_subdir) if root_subdir else self.run_dir
        files: List[FingerprintedFile] = []
        exclude = exclude or []
        for p in list_files(root):
            if p.name == ".gitignore":
                continue
            rel = safe_relpath(p, self.run_dir)
            if _is_excluded(rel, exclude):
                continue
            files.append(FingerprintedFile(rel, sha256_file(p), p.stat().st_size))
        files = sorted(files, key=lambda f: f.path)
        return ArtifactIndex(files=files, root_hash=merkle_root(files))

    def rel(self, path: Path) -> str:
        return safe_relpath(path, self.run_dir)


def _is_excluded(relpath: str, exclude: List[str]) -> bool:
    """Exclude by exact path or prefix.

    If an exclude entry ends with '/', it matches a prefix.
    Otherwise it matches the exact relative path.
    """
    for e in exclude:
        if not e:
            continue
        if e.endswith("/"):
            if relpath.startswith(e):
                return True
        else:
            if relpath == e:
                return True
    return False
