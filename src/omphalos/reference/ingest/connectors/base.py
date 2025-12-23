from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class ConnectorResult:
    name: str
    rows: List[dict[str, Any]]
