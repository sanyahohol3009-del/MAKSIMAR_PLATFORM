from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_preview,
    build_memory_skill_summary,
)


def test_phase_2_2_roadmap_v5_reconciliation_smoke() -> None:
    legacy_core_root = Path(
        "MAKSIMAR_CORE_LIB/memory_engine/memory_skill_observability"
    )
    corrected_server_root = Path(
        "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics"
    )

    summary = build_memory_skill_summary()
    preview = build_memory_skill_preview()

    assert corrected_server_root.exists()
    assert not legacy_core_root.exists()

    assert summary["summary_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert summary["total_metric_entries"] == 16
    assert summary["ready_metric_entries"] == 16
    assert summary["backend_execution_allowed_entries"] == 0
    assert summary["mgrep_blocked"] is True
    assert summary["sqlite_vec_blocked"] is True
