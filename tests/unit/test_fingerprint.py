from __future__ import annotations

from omphalos.core.fingerprint import sha256_json


def test_sha256_json_is_order_independent_for_mappings() -> None:
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert sha256_json(a) == sha256_json(b)
