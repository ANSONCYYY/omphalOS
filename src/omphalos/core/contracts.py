from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import jsonschema
import yaml

from .exceptions import ContractError

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACTS_DIR = REPO_ROOT / "contracts"
SCHEMAS_DIR = CONTRACTS_DIR / "schemas"


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json_schema(schema_filename: str) -> Dict[str, Any]:
    p = SCHEMAS_DIR / schema_filename
    if not p.exists():
        raise ContractError(f"schema not found: {schema_filename}")
    return json.loads(p.read_text(encoding="utf-8"))


def validate_json_against_schema(data: Any, schema: Dict[str, Any]) -> None:
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise ContractError(str(e)) from e


def validate_json_file(json_path: Path, schema_filename: str) -> None:
    schema = load_json_schema(schema_filename)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    validate_json_against_schema(data, schema)
