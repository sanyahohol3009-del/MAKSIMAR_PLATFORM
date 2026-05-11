from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.self_readability import build_jarvis_memory_self_read_boundary


def test_jarvis_memory_boundary_models_smoke() -> None:
    boundary = build_jarvis_memory_self_read_boundary()

    assert boundary.boundary_ready is True
    assert boundary.canonical_write_allowed is False
    assert boundary.runtime_mutation_allowed is False
    assert boundary.auto_promotion_allowed is False
    assert boundary.auto_conflict_resolution_allowed is False
    assert boundary.secrets_access_allowed is False
