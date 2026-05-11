from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.self_readability import build_jarvis_memory_visibility_entry


def test_jarvis_memory_visibility_models_smoke() -> None:
    visibility = build_jarvis_memory_visibility_entry()

    assert visibility.visibility_ready is True
    assert visibility.source_attribution_required is True
    assert visibility.evidence_pack_required is True
    assert visibility.preview_trace_required is True
    assert "project_notes" in visibility.visible_domains
    assert "secrets" in visibility.hidden_domains
