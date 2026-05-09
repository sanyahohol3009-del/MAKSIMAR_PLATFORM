from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_summary


def test_evidence_memory_summary_builder_smoke() -> None:
    summary = build_evidence_memory_summary()

    assert summary["summary_ready"] is True
    assert summary["total_records"] == 6
    assert summary["source_event_records"] == 6
    assert summary["source_version_records"] == 6
    assert summary["conflict_marker_records"] == 6
