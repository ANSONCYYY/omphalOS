from __future__ import annotations

from omphalos.core.packs import load_pack


def test_load_pack_baseline_paths_exist() -> None:
    pack = load_pack("baseline")
    assert pack.name == "baseline"
    assert pack.quality_rules, "baseline pack must define at least one quality rules file"
    assert pack.publishability_rules, "baseline pack must define at least one publishability rules file"
    for p in pack.quality_rules + pack.publishability_rules:
        assert p.exists(), f"missing pack path: {p}"


def test_load_pack_strict_is_stricter() -> None:
    base = load_pack("baseline")
    strict = load_pack("strict")
    assert len(strict.quality_rules) >= len(base.quality_rules)
    assert len(strict.publishability_rules) >= len(base.publishability_rules)
    q_names = {p.name for p in strict.quality_rules}
    pub_names = {p.name for p in strict.publishability_rules}
    assert "strict_quality_rules.yaml" in q_names
    assert "strict_publishability_gates.yaml" in pub_names
