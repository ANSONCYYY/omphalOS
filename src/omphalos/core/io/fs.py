from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator


DEFAULT_PRUNE_DIRS: set[str] = {
    ".git",
    ".venv",
    ".uv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    ".tox",
    "artifacts",
}


def list_files(root: Path, *, prune_dirs: Iterable[str] | None = None) -> Iterator[Path]:
    """Yield all files under root.

    prune_dirs is applied to directory names (not paths) and is evaluated at each
    level of the walk. This is used to keep repository-wide scans fast and
    bounded.
    """

    prune = set(prune_dirs) if prune_dirs is not None else set(DEFAULT_PRUNE_DIRS)
    for dirpath, dirnames, filenames in os.walk(root):
        if prune:
            dirnames[:] = [d for d in dirnames if d not in prune]
        for fn in filenames:
            yield Path(dirpath) / fn


def is_binary(path: Path, sample_bytes: int = 2048) -> bool:
    try:
        data = path.read_bytes()[:sample_bytes]
    except OSError:
        return True
    return b"\x00" in data


def safe_relpath(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()
