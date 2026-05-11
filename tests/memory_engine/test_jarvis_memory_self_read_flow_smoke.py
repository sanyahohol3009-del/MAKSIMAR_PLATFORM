from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.self_readability import (
    build_jarvis_memory_self_read_model,
    build_jarvis_memory_self_read_preview,
    validate_jarvis_memory_self_read_model,
)


def test_jarvis_memory_self_read_flow_smoke() -> None:
    model = build_jarvis_memory_self_read_model()
    preview = build_jarvis_memory_self_read_preview()

    assert validate_jarvis_memory_self_read_model(model) is True
    assert preview["preview_ready"] is True
    assert preview["can_explain_where_searched"] is True
    assert preview["can_explain_constraints_applied"] is True
    assert preview["can_explain_evidence_pack"] is True
    assert preview["can_explain_preview_trace"] is True
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
