from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Type

from .interfaces import Connector, Exporter, Transform


@dataclass
class PluginRegistry:
    connectors: Dict[str, Connector]
    transforms: Dict[str, Transform]
    exporters: Dict[str, Exporter]

    def __init__(self) -> None:
        self.connectors = {}
        self.transforms = {}
        self.exporters = {}

    def register_connector(self, connector: Connector) -> None:
        self.connectors[connector.name] = connector

    def register_transform(self, transform: Transform) -> None:
        self.transforms[transform.name] = transform

    def register_exporter(self, exporter: Exporter) -> None:
        self.exporters[exporter.name] = exporter


REGISTRY = PluginRegistry()
