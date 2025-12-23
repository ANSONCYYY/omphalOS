from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from .contracts import CONTRACTS_DIR
from .io.fs import is_binary, list_files, safe_relpath
from .time import deterministic_now_iso

_DEFAULT_RULES_PATH = CONTRACTS_DIR / "quality_rules" / "publishability_gates.yaml"


def _load_rules(rule_paths: List[Path]) -> List[Tuple[str, re.Pattern[str], str]]:
    rules: List[Tuple[str, re.Pattern[str], str]] = []
    for rp in rule_paths:
        spec = yaml.safe_load(rp.read_text(encoding="utf-8")) or {}
        for r in spec.get("rules", []):
            rules.append((r["name"], re.compile(r["pattern"]), r["severity"]))
    return rules


def scan_path(path: Path, *, rule_paths: List[Path] | None = None, max_bytes: int = 2_000_000) -> Dict[str, Any]:
    if rule_paths is None:
        rule_paths = [_DEFAULT_RULES_PATH]
    rules = _load_rules(rule_paths)
    findings: List[Dict[str, Any]] = []
    target = path.name

    if path.is_file():
        candidates = [path]
        base = path.parent
    else:
        candidates = list(list_files(path))
        base = path

    for p in candidates:
        if p.name == ".gitignore":
            continue
        try:
            if p.is_dir():
                continue
            size = p.stat().st_size
        except OSError:
            continue
        if size > max_bytes:
            continue
        if is_binary(p):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for name, pat, sev in rules:
            m = pat.search(text)
            if not m:
                continue
            start = max(0, m.start() - 40)
            end = min(len(text), m.end() + 40)
            excerpt = text[start:end].replace("\n", "\\n")
            findings.append(
                {
                    "path": safe_relpath(p, base) if base.is_dir() else p.name,
                    "rule": name,
                    "severity": sev,
                    "excerpt": excerpt,
                    "offset": m.start(),
                }
            )

    status = "PASS" if not any(f["severity"] == "HIGH" for f in findings) else "FAIL"
    return {
        "schema_version": "1.0",
        "created_at": deterministic_now_iso("publishability", salt=target),
        "target": target,
        "status": status,
        "findings": sorted(findings, key=lambda x: (x["severity"], x["path"], x["offset"])),
    }
