from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable


@runtime_checkable
class Connector(Protocol):
    name: str
    def read(self, *, seed: int) -> list[dict[str, Any]]: ...


@runtime_checkable
class Transform(Protocol):
    name: str
    def apply(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]: ...


@runtime_checkable
class Exporter(Protocol):
    name: str
    def export(self, *, run_dir: str, data: Mapping[str, Any]) -> list[str]: ...
