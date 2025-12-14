from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .contracts import load_json_schema, validate_json_against_schema
from .exceptions import ConfigError
from .fingerprint import sha256_json


@dataclass(frozen=True)
class RunInputs:
    trade_feed_records: int
    registry_entities: int


@dataclass(frozen=True)
class RuleConfig:
    pack: str
    paths: List[str]


@dataclass(frozen=True)
class RunSettings:
    seed: int
    run_name: str
    hermetic: bool
    output_root: str


@dataclass(frozen=True)
class RunConfig:
    schema_version: str
    run: RunSettings
    inputs: RunInputs
    rules: RuleConfig

    def fingerprint(self) -> str:
        """Stable fingerprint (excludes execution paths like output_root)."""
        return sha256_json(fingerprint_payload(self))


def fingerprint_payload(cfg: RunConfig) -> Dict[str, Any]:
    """Canonical payload used for run identity and determinism."""
    return {
        "schema_version": cfg.schema_version,
        "run": {"seed": cfg.run.seed, "run_name": cfg.run.run_name, "hermetic": cfg.run.hermetic},
        "inputs": {
            "trade_feed": {"records": cfg.inputs.trade_feed_records},
            "registry": {"entities": cfg.inputs.registry_entities},
        },
        "rules": {"pack": cfg.rules.pack, "paths": list(cfg.rules.paths)},
    }


def to_primitive(cfg: RunConfig) -> Dict[str, Any]:
    """Full config payload including execution details."""
    payload = fingerprint_payload(cfg)
    payload["run"]["output_root"] = cfg.run.output_root
    return payload


def load_run_config(path: Path) -> RunConfig:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ConfigError(f"failed to read config: {path}") from e

    schema = load_json_schema("config.schema.json")
    try:
        validate_json_against_schema(raw, schema)
    except Exception as e:
        raise ConfigError(f"invalid config: {e}") from e

    try:
        run = raw["run"]
        inputs = raw["inputs"]
        rules = raw["rules"]
        return RunConfig(
            schema_version=str(raw["schema_version"]),
            run=RunSettings(
                seed=int(run["seed"]),
                run_name=str(run.get("run_name", "run")),
                hermetic=bool(run["hermetic"]),
                output_root=str(run["output_root"]),
            ),
            inputs=RunInputs(
                trade_feed_records=int(inputs["trade_feed"]["records"]),
                registry_entities=int(inputs["registry"]["entities"]),
            ),
            rules=RuleConfig(
                pack=str(rules["pack"]),
                paths=[str(p) for p in rules["paths"]],
            ),
        )
    except Exception as e:
        raise ConfigError("failed to construct config") from e
