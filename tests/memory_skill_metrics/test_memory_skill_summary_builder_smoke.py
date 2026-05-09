from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_summary,
)


def test_memory_skill_summary_builder_smoke() -> None:
    summary = build_memory_skill_summary()

    assert summary["summary_ready"] is True
    assert summary["conflict_entries"] == 0
    assert summary["promotion_auto_allowed_entries"] == 0
    assert summary["backend_execution_allowed_entries"] == 0
    assert summary["mgrep_blocked"] is True
    assert summary["sqlite_vec_blocked"] is True
    assert summary["read_only_ready"] is True
