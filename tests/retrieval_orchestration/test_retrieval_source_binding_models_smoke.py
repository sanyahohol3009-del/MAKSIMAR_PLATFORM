from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_default_retrieval_source_bindings,
)


def test_retrieval_source_binding_models_smoke() -> None:
    sources = build_default_retrieval_source_bindings()

    assert sources
    assert all(source.evidence_supported for source in sources)
    assert all(source.trace_supported for source in sources)
    assert all(source.policy_allowed for source in sources)
