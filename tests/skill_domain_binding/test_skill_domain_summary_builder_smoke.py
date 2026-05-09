from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import build_skill_domain_summary


def test_skill_domain_summary_builder_smoke() -> None:
    summary = build_skill_domain_summary()

    assert summary["summary_ready"] is True
    assert summary["skill_ready_bindings"] == summary["skill_bindings"]
    assert summary["domain_cubes_ready"] == summary["domain_cubes"]
    assert summary["domain_layers_ready"] == summary["domain_layers"]
    assert 0 <= summary["skill_memory_reference_bound_bindings"] <= summary["skill_bindings"]
