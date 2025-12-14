from __future__ import annotations

import platform
from importlib import metadata
from typing import Any, Dict, List

from .time import deterministic_now_iso


def generate_sbom_manifest() -> Dict[str, Any]:
    packages: List[Dict[str, str]] = []
    for dist in sorted(metadata.distributions(), key=lambda d: (d.metadata.get("Name", ""), d.version)):
        name = dist.metadata.get("Name")
        if not name:
            continue
        packages.append({"name": name, "version": dist.version})

    return {
        "schema_version": "1.0",
        "created_at": deterministic_now_iso("sbom"),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "packages": packages,
    }
