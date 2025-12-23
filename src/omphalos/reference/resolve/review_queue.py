from __future__ import annotations

from typing import Any, Dict, List


def make_review_item(shipment_id: str, exporter_name: str, candidates: List[Dict[str, Any]], reason: str) -> Dict[str, Any]:
    return {
        "shipment_id": shipment_id,
        "exporter_name": exporter_name,
        "reason": reason,
        "candidates": candidates,
    }
