from __future__ import annotations

from typing import Any, Dict, Set


def explain_match(exporter_name: str, entity_name: str, score: float, exporter_tokens: Set[str], entity_tokens: Set[str]) -> Dict[str, Any]:
    common = sorted(exporter_tokens & entity_tokens)
    return {
        "exporter_name": exporter_name,
        "entity_name": entity_name,
        "score": score,
        "common_tokens": common,
        "exporter_tokens": sorted(exporter_tokens),
        "entity_tokens": sorted(entity_tokens),
    }
