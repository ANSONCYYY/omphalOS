from __future__ import annotations

from importlib import metadata

from .registry import REGISTRY
from .interfaces import Connector, Exporter, Transform


def load_entrypoint_plugins() -> None:
    """Load plugins declared via Python entry points."""
    eps = metadata.entry_points()
    for ep in eps.select(group="omphalos.connectors"):
        obj = ep.load()
        if isinstance(obj, type):
            obj = obj()
        if isinstance(obj, Connector):
            REGISTRY.register_connector(obj)

    for ep in eps.select(group="omphalos.transforms"):
        obj = ep.load()
        if isinstance(obj, type):
            obj = obj()
        if isinstance(obj, Transform):
            REGISTRY.register_transform(obj)

    for ep in eps.select(group="omphalos.exporters"):
        obj = ep.load()
        if isinstance(obj, type):
            obj = obj()
        if isinstance(obj, Exporter):
            REGISTRY.register_exporter(obj)
