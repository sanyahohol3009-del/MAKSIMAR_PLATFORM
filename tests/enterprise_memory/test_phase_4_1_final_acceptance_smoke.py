from __future__ import annotations

from MAKSIMAR_CORE_LIB.enterprise_memory_domains import (
    build_enterprise_memory_phase_preview,
    build_enterprise_memory_phase_readiness,
    build_enterprise_memory_preview,
    build_enterprise_memory_summary,
)


def test_phase_4_1_final_acceptance_smoke() -> None:
    summary = build_enterprise_memory_summary()
    preview = build_enterprise_memory_preview()
    readiness = build_enterprise_memory_phase_readiness()
    phase_preview = build_enterprise_memory_phase_preview()

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True
