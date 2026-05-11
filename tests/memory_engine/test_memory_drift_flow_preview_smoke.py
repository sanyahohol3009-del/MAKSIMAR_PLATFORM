from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import (
    build_memory_drift_preview,
    build_memory_drift_report,
    validate_memory_drift_report,
)


def test_memory_drift_flow_preview_smoke() -> None:
    report = build_memory_drift_report()
    preview = build_memory_drift_preview()

    assert validate_memory_drift_report(report) is True
    assert preview["preview_ready"] is True
    assert "memory_contradiction_candidate" in preview["flow"]
