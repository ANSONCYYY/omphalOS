from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from .contracts import CONTRACTS_DIR
from .exceptions import ConfigError


@dataclass(frozen=True)
class RulePack:
    name: str
    version: str
    quality_rules: List[Path]
    publishability_rules: List[Path]


def _dedupe_paths(paths: List[Path]) -> List[Path]:
    seen = set()
    out: List[Path] = []
    for p in paths:
        key = p.as_posix()
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def load_pack(name: str) -> RulePack:
    pack_path = CONTRACTS_DIR / "packs" / f"{name}.yaml"
    if not pack_path.exists():
        raise ConfigError(f"rule pack not found: {name}")
    spec = yaml.safe_load(pack_path.read_text(encoding="utf-8")) or {}
    try:
        version = str(spec.get("version", "1.0"))
        quality_rules = [Path(p) for p in spec.get("quality_rules", [])]
        publishability_rules = [Path(p) for p in spec.get("publishability_rules", [])]
    except Exception as e:
        raise ConfigError(f"invalid rule pack: {name}") from e

    root = CONTRACTS_DIR.parent
    q = _dedupe_paths([(root / p).resolve() for p in quality_rules])
    pub = _dedupe_paths([(root / p).resolve() for p in publishability_rules])
    return RulePack(name=name, version=version, quality_rules=q, publishability_rules=pub)


def effective_quality_rules(*, pack: RulePack, extra_paths: List[str]) -> List[Path]:
    root = CONTRACTS_DIR.parent
    extras = [(root / Path(p)).resolve() for p in extra_paths]
    return _dedupe_paths(list(pack.quality_rules) + extras)


def effective_publishability_rules(*, pack: RulePack, extra_paths: List[str]) -> List[Path]:
    root = CONTRACTS_DIR.parent
    extras = [(root / Path(p)).resolve() for p in extra_paths]
    return _dedupe_paths(list(pack.publishability_rules) + extras)
